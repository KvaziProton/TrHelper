from celery import shared_task
from .toolbox import FlowListener, Manager, parse


@shared_task
def check_if_new():
    listener = FlowListener()
    listener.start()

@shared_task
def clear_log():
    #at 5 a.m every day delete all except today or last 3
    pass

@shared_task
def check_user_add(url):
    '''Directly pass url to Manager class'''

    manager = Manager(url=url)
    manager.is_new(user_req=True)
    try:
        similar_url = manager.similar_url
        print(similar_url)
    except AttributeError:
        similar_url = None
        manager.write_bd()
    return similar_url

@shared_task
def form_downloard_response(url):
    response = parse(url)
    return response
