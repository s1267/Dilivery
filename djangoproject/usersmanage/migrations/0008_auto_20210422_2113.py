# Generated by Django 3.1.7 on 2021-04-22 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0007_auto_20210422_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='photo',
            field=models.ImageField(upload_to='static/'),
        ),
    ]
