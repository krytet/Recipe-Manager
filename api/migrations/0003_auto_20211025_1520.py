# Generated by Django 3.2.8 on 2021-10-25 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_tag_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='masurement_value',
            new_name='measurement_unit',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='time_cooking',
            new_name='cooking_time',
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='api.Tag'),
        ),
    ]
