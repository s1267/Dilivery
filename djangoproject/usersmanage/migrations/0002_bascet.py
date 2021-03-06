# Generated by Django 3.1.7 on 2021-04-19 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bascet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(verbose_name='Количество')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersmanage.item', verbose_name='Id Товара')),
                ('user_id', models.ForeignKey(on_delete=models.SET(0), to='usersmanage.user', verbose_name='Id Пользователя')),
            ],
            options={
                'verbose_name': 'Корзина',
            },
        ),
    ]
