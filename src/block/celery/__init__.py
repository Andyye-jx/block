import inject
import logging
from datetime import timedelta
from celery import Celery, Task, schedules
from kombu import Queue, Exchange
from block.config import Config, DbSession
logger = logging.getLogger(__name__)


class APITask(Task):

    def run(self, *args, **kwargs):
        return super().run(*args, **kwargs)

    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        inject.instance(DbSession).remove()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error('exc: %s, task_id: %s, args: %s, einfo: %s', exc, task_id, args, einfo, exc_info=True)


@inject.autoparams()
def init_celery(config: Config):
    broker, backend = config.celery_broker_url, config.celery_backend_url
    celery = Celery("block", set_as_current=False, include=["block.celery.address", "block.celery.beat_task"])
    beat_schedule = {
        "listen_eth_address": {
            "task": "beat_task.assign",
            "schedule": timedelta(seconds=30),
            "args": ("eth", )
        },
        "listen_bsc_address": {
            "task": "beat_task.assign",
            "schedule": timedelta(seconds=30),
            "args": ("bsc", )
        }
    }
    celery.conf.update(
        CELERY_QUEUES=(
            Queue('celery', Exchange('celery'), routing_key='default'),
            Queue('block', Exchange('block'), routing_key='default'),
            Queue('block_beat', Exchange('block_beat'), routing_key='default')
        ),
        CELERY_DEFAULT_QUEUE='celery',
        CELERY_DEFAULT_ROUTING_KEY='default',
        CELERY_DEFAULT_EXCHANGE_TYPE='direct',
        BROKER_URL=broker,
        CELERY_RESULT_BACKEND=backend,
        CELERY_RESULT_PERSISTENT=False,
        CELERY_TASK_RESULT_EXPIRES=300,
        CELERY_TASK_SERIALIZER='json',
        CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
        CELERY_RESULT_SERIALIZER='json',
        CELERY_TIMEZONE='Asia/Shanghai',
        CELERY_ENABLE_UTC=True,
        CELERYBEAT_SCHEDULE=beat_schedule,
        TOTORO_AMQP_CONNECTION_POOL={
            'max_idle_connections': 1,
            'max_open_connections': 500,
            'max_recycle_sec': 3600
        }, )
    return celery
