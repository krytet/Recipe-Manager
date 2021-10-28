# Generated by Django 3.2.8 on 2021-10-28 10:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_rename_person_subscription_respondent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='subscriptions',
        ),
        migrations.AddField(
            model_name='subscription',
            name='subscriptions',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to='auth.user'),
            preserve_default=False,
        ),
    ]