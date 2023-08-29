import logging
import math
import gunicorn.app.base
from importlib.util import find_spec


def number_of_workers(core: str = ''):
    num_core = 1
    try:
        if core:
            if 'm' in core.lower():
                num_core = 1
            elif core.isdigit():
                num_core = int(core)
            else:
                num_core = math.ceil(float(core))
    except:
        pass
    # docker容器里取的是宿主机的
    # return (multiprocessing.cpu_count() * 2) + 1
    # 最优是 2*core+1
    # 但是服务器和算法程序都太脆弱了， 所以减少点
    # return (2 * num_core) + 1
    return num_core + 1


def number_of_threads(core: str = ''):
    num_core = 1
    try:
        if core:
            if 'm' in core.lower():
                num_core = 1
            elif core.isdigit():
                num_core = int(core)
            else:
                num_core = math.ceil(float(core))
    except:
        pass
    return (2 * num_core) + 1


def handler_app(environ, start_response):
    response_body = b'Works fine'
    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/plain'),
    ]

    start_response(status, response_headers)

    return [response_body]


def default_config(bind, workers=None, threads=None, worker_class=None):
    # worker_class greenlet gthread 都不行 各种和算法冲突 蛋疼
    config = {
        'bind': bind,
        'accesslog': '-', 'errorlog': '-',
        'loglevel': 'info',
        'worker_class': worker_class or 'sync',
        'timeout': 300,
        'workers': workers or 1,
        'threads': threads or 1  # 只有在gthread模式下才会生效
    }
    return config


class GunServer(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None, logger=None):
        self.options = options or {}
        self.application = app
        self.logger = logger
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

    def run(self):
        super().run()


if __name__ == '__main__':
    # options = {
    #     'bind': '%s:%s' % ('127.0.0.1', '8080'),
    #     'workers': number_of_workers(),
    # }
    # StandaloneApplication(handler_app, options).run()
    print(number_of_workers("1.7"))
