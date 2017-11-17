from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from .models import Name
logger = get_task_logger(__name__)

@task(name="manual_update_names")
def manual_update_names():
    """sends an email when feedback form is filled successfully"""
    logger.info("Updated names manually")
    all_names = Name.objects.all()
    Name.update(all_names)

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@periodic_task(
    run_every=(crontab(hour='*/12')),
    name="update_names"
)

def update_names():
    all_names = Name.objects.all()
    Name.update(all_names)
    logger.info("Updated names")
