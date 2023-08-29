import base64
import os
import time

import requests
from intelliw.utils.iuap_request import sign_authsdk
from intelliw.utils.logger import _get_framework_logger

logger = _get_framework_logger()


class YmsSysEnv:
    ACCESS_KEY = os.getenv('ACCESS_KEY')
    ACCESS_SECRET = os.getenv('ACCESS_SECRET')
    YMS_CONSOLE_ADDRESS = os.getenv('YMS_CONSOLE_ADDRESS')
    YMS_CONSOLE_ACTIVE = os.getenv('YMS_CONSOLE_ACTIVE')
    YMS_CONSOLE_APP_CODE = os.getenv('YMS_CONSOLE_APP_CODE')
    YMS_CONFIG_FIlE_ADDRESS = f"{YMS_CONSOLE_ADDRESS}/api/v2/config/file"
    YMS_PW_DECODE_ADDRESS = f"{YMS_CONSOLE_ADDRESS}/api/v1/ymsConfig/enc/decValue"

    YMS_ENV_CONFIG_PATH = './yms_env_config.yaml'

    def __init__(self):
        self.init_config()
        self.special_env_map = {}
        self.mid_info_map = {}
        self.local_cache = None

    def init_config(self):
        self.ACCESS_KEY = os.getenv('ACCESS_KEY')
        self.ACCESS_SECRET = os.getenv('ACCESS_SECRET')
        self.YMS_CONSOLE_ADDRESS = os.getenv('YMS_CONSOLE_ADDRESS')
        self.YMS_CONSOLE_ACTIVE = os.getenv('YMS_CONSOLE_ACTIVE')
        self.YMS_CONSOLE_APP_CODE = os.getenv('YMS_CONSOLE_APP_CODE')
        self.YMS_CONFIG_FIlE_ADDRESS = f"{self.YMS_CONSOLE_ADDRESS}/api/v2/config/file"
        self.YMS_PW_DECODE_ADDRESS = f"{self.YMS_CONSOLE_ADDRESS}/api/v1/ymsConfig/enc/decValue"

    def _env_precess(self, env):
        for config_group in env['ymsConfigGroupVos']:
            for config in config_group['configItems']:
                code = config['code']
                value: str = config['value']
                if value.find('#{') >= 0:
                    self.special_env_map[code] = value
                    continue
                if value.startswith('YMS(') and value.endswith(')'):
                    value = decode_yms_pw(value)
                os.environ[code] = value
                self.mid_info_map[code] = value
                if self.local_cache is not None:
                    self.local_cache.write(f"{code}={value}\n")

    def _generate_value(self, result: str):
        if result.find('#{') >= 0:
            for k, v in self.mid_info_map.items():
                variable = '#{' + k + '#}'
                if result.find(variable) >= 0:
                    result = result.replace(variable, v)
        return result

    def init_children_info(self, children):
        for c in children:
            if c.get('ymsConfigGroupVos'):
                self._env_precess(c)

            if c.get('children'):
                self.init_children_info(c['children'])

    def init_envs(self, env):
        self.local_cache = open(self.YMS_ENV_CONFIG_PATH, "w")

        if not env:
            logger.warning('YMS配置为空')
            return

        self._env_precess(env['data'])

        if env['data'].get('children'):
            self.init_children_info(env['data']['children'])

        for k, v in self.special_env_map.items():
            v = self._generate_value(v)
            os.environ[k] = v
            self.mid_info_map[k] = v

            if self.local_cache is not None:
                self.local_cache.write(f"{k}={v}\n")

        self._close_file()

    def _close_file(self):
        if self.local_cache is not None and not self.local_cache.closed:
            self.local_cache.close()

    def __del__(self):
        self._close_file()


yms_sys_env = YmsSysEnv()


def request_yms(url, method="GET", params=None, data=None):
    for i in range(1, 5):
        try:
            token = sign_authsdk(url, params, yms_sys_env.ACCESS_KEY, yms_sys_env.ACCESS_SECRET)
            headers = {
                'Content-Type': 'application/json',
                'YYCtoken': token,
                'dcAddr': base64.b64encode(bytes(url, 'utf-8')).decode()
            }
            resp = requests.request(
                method=method, url=url, params=params,
                json=data, verify=False, headers=headers, timeout=5.0
            )
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            if i == 4:
                raise e
            time.sleep(i * 2)
            try:
                body = e.response.text if hasattr(e.response, "text") else e.response
            except:
                body = ""
            logger.error(
                "request retry time: %s, url: %s, body: %s, error: %s",
                i, url, body, e)


def decode_yms_pw(pw):
    resp = request_yms(yms_sys_env.YMS_PW_DECODE_ADDRESS,
                       method='POST',
                       data=[pw, ])

    if resp['success'] != 'true':
        logger.error(f"{resp['error_code']}:{resp['error_message']}")
        return ""

    data = resp.get('data', {})
    return data.get(pw, "")


def run():
    yms_sys_env.init_config()
    if not yms_sys_env.YMS_CONSOLE_ADDRESS:
        return

    resp = request_yms(yms_sys_env.YMS_CONFIG_FIlE_ADDRESS,
                       params={
                           'app': yms_sys_env.YMS_CONSOLE_APP_CODE,
                           'env': yms_sys_env.YMS_CONSOLE_ACTIVE}
                       )
    if resp.get('success') == 'false':
        logger.error(f"{resp['error_code']}:{resp['error_message']}")
        return

    yms_sys_env.init_envs(resp.get('environment'))
    logger.info("执行YMS配置拉取成功")
