# Generated by Django 4.0.5 on 2022-06-21 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0004_servicecitiesmodel_created_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicemodel',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='Image'),
        ),
    ]
