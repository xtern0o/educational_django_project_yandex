# Generated by Django 4.2 on 2023-11-08 15:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("feedback", "0006_alter_statuslog_feedback"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="FeedbackModel",
            new_name="Feedback",
        ),
    ]
