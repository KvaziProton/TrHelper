from celery import shared_task

articles = []

@shared_task
def start_article_flow():
    while True:
        pass
        # check()
        # if new:
        #     articles.append(new)
