# Generated by Django 4.0.6 on 2022-07-05 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='subscribe',
            field=models.ManyToManyField(through='news.Subscribers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subscribers',
            name='categoryID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category'),
        ),
        migrations.AddField(
            model_name='subscribers',
            name='userID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
