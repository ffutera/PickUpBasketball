# Generated by Django 3.1.1 on 2021-03-10 21:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0006_auto_20210310_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='going',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]