import inject
import logging
from flask import Flask
from block.config import Config, configure_fromfile, DbSession
from block.api import monitor, notify
# 设置日志输出
logging.basicConfig(level=logging.INFO, format='[%(name)s]:%(asctime)s:%(filename)s:%(lineno)d %(message)s')
logging.getLogger('sqlalchemy.engine.base.Engine').disabled = True
logger = logging.getLogger(__name__)

# 初始化配置
inject.configure(configure_fromfile)

app = Flask(__name__)
app.url_map.strict_slashes = False

resource_list = [
    monitor.get_monitor_resource(),
    notify.get_notify_resource(),
]

for resource in resource_list:
    app.register_blueprint(resource.blueprint)


@app.teardown_request
def clear_session(exception):
    del exception
    inject.instance(DbSession).remove()


@app.before_request
def before_request():
    pass


def main():
    logger.info('server will serve at 127.0.0.1:%s', Config.api_port)
    app.run(debug=True, host='127.0.0.1', port=Config.api_port)


if __name__ == '__main__':
    main()
