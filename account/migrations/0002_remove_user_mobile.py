# Generated by Django 3.2.7 on 2021-10-13 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='mobile',
        ),
    ]
