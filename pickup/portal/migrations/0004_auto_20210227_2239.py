# Generated by Django 3.1.1 on 2021-02-27 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_event_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='occured',
            field=models.IntegerField(default=False),
        ),
    ]
