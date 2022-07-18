import logging
import time
from datetime import datetime, date, timedelta

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from ...models import User, Category, Post, PostCategory, Subscribers

logger = logging.getLogger(__name__)


def my_job():
    #  Your job processing logic here...
    category_list = Category.objects.all()
    week_ago = date.today() - timedelta(days=7)
    for item in category_list:
        post_list = PostCategory.objects.filter(category_id=item.id).all()
        recipient_list = []
        sub_list = Subscribers.objects.filter(category_id=item.id).all()
        for subscriber in sub_list:
            recipient_list.append(User.objects.get(pk=subscriber.user_id).email)
        posts = []

        subject, from_email, to = 'рассылка', 'softb0x@yandex.ru', recipient_list
        for post in post_list:
            if Post.objects.get(title=post).date >= week_ago:
                posts.append(Post.objects.get(title=post))

        if post and recipient_list:
            print(post, recipient_list)
            html_content = render_to_string(
                'news/mailing_list.html',
                {
                    'posts': posts,
                }
            )
            msg = EmailMultiAlternatives(
                subject=subject,
                body=' ',  # это то же, что и message
                from_email=from_email,
                to=recipient_list,  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()  # отсылаем


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # trigger = CronTrigger(week="*/1"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
