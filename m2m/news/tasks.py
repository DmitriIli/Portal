from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Subscribers, Category, PostCategory
from django.contrib.auth.models import User
from django.db.models import signals
from m2m.celery import app
from datetime import datetime, date, timedelta


@app.task
def weekly_notify():
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

        if posts and recipient_list:
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
