# Generated by Django 4.0.5 on 2022-06-21 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companyapp', '0003_companymodel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='companymodel',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
