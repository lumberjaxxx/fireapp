# Generated by Django 5.1.3 on 2024-12-08 12:28

import fire.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fire', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='date_time',
            field=models.DateTimeField(blank=True, null=True, validators=[fire.models.validate_not_future]),
        ),
        migrations.AlterField(
            model_name='weatherconditions',
            name='humidity',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[fire.models.validate_non_negative]),
        ),
        migrations.AlterField(
            model_name='weatherconditions',
            name='temperature',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[fire.models.validate_non_negative]),
        ),
        migrations.AlterField(
            model_name='weatherconditions',
            name='wind_speed',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[fire.models.validate_non_negative]),
        ),
    ]