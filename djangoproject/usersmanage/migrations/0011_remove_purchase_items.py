# Generated by Django 3.1.7 on 2021-04-24 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0010_auto_20210424_2342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='items',
        ),
    ]