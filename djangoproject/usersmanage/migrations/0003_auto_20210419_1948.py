# Generated by Django 3.1.7 on 2021-04-19 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usersmanage', '0002_bascet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Наименование категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.AlterModelOptions(
            name='bascet',
            options={'verbose_name': 'Корзина', 'verbose_name_plural': 'Корзинки'},
        ),
        migrations.RemoveField(
            model_name='item',
            name='category_code',
        ),
        migrations.RemoveField(
            model_name='item',
            name='category_name',
        ),
        migrations.RemoveField(
            model_name='item',
            name='subcategory_code',
        ),
        migrations.RemoveField(
            model_name='item',
            name='subcategory_name',
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='Наименование подкатегории')),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usersmanage.category', verbose_name='Id категории')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='category_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='usersmanage.category', verbose_name='ID категории'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='subcategory_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usersmanage.subcategory', verbose_name='ID подкатегории'),
        ),
    ]
