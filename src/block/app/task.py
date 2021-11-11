import inject
import logging
from block.config import configure_fromfile
inject.configure(configure_fromfile)
logging.basicConfig(level=logging.INFO, format='[%(name)s]:%(asctime)s:%(filename)s:%(lineno)d %(message)s')
logging.getLogger('sqlalchemy.engine.base.Engine').disabled = True
from celery import Celery
celery = inject.instance(Celery)
