# Generated by Django 4.0.5 on 2022-06-25 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_quotemodel_unique_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotemodel',
            name='unique_code',
            field=models.CharField(default='20220625140d9ff5c5-28a9-4f85-86f4-c752a1d8b068', editable=False, max_length=100),
        ),
    ]
