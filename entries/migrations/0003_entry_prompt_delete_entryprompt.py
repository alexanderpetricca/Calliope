# Generated by Django 5.0.3 on 2024-07-26 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0002_alter_entry_options_entryprompt'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='prompt',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.DeleteModel(
            name='EntryPrompt',
        ),
    ]