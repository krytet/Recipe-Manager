# Generated by Django 3.2.8 on 2021-10-29 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20211029_1251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartshopping',
            old_name='recipes',
            new_name='recipe',
        ),
        migrations.RenameField(
            model_name='favoriterecipe',
            old_name='recipes',
            new_name='recipe',
        ),
    ]
