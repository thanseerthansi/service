# Generated by Django 4.0.5 on 2022-07-02 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0007_quotemodel_unique_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotemodel',
            name='unique_code',
            field=models.CharField(default='2022070214a3d2a41d-773e-4415-9a0f-fc97ed175376', editable=False, max_length=100),
        ),
    ]
