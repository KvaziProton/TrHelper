from celery import shared_task
from .logic.models import FlowListener

start = open('tr_helper/last_article_log.txt').readlines()[-1]
listen = FlowListener(start=start)

@shared_task
def check_if_new():
    listen.start()

@shared_task
def clear_log():
    #at 5 a.m every day delete all except today or last 3
    pass
