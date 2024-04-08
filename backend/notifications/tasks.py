from celery import shared_task

from users.models import User


@shared_task
def send_email(sender: User, receiver: User = None):
    if receiver:
        print(sender.full_name, receiver.full_name)
    else:
        print(sender.full_name)
