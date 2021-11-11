import inject
import logging
from celery import Celery
from block.celery import APITask
logger = logging.getLogger(__name__)
current_app = inject.instance(Celery)

DEFAULT_OPTS = {
    "bind": True,
    "exchange": "block",
    "base": APITask,
}


@current_app.task(name="test.notify_test", **DEFAULT_OPTS)
def notify_test(self, name):
    del self
    logger.info(name)
    return "ok"
