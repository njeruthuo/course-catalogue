# Generated by Django 5.1.8 on 2025-04-05 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='preview',
            field=models.BooleanField(default=False, help_text="If the user doesn't have access to this course see this?"),
        ),
        migrations.AddField(
            model_name='lesson',
            name='status',
            field=models.CharField(choices=[('pub', 'Published'), ('draft', 'Draft'), ('soon', 'Coming soon')], default='pub', max_length=20),
        ),
    ]
