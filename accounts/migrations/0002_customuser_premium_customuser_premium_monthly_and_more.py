# Generated by Django 5.0.3 on 2024-04-15 08:44

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='premium',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='premium_monthly',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='premium_paid_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='tokens',
            field=models.IntegerField(default=4),
        ),
        migrations.CreateModel(
            name='SignUpcode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('code', models.CharField(blank=True, editable=False, max_length=12, null=True, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('used', models.DateTimeField(blank=True, null=True)),
                ('used_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
