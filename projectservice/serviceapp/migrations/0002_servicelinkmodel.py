# Generated by Django 4.0.5 on 2022-07-02 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicelinkModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceapp.servicetypemodel')),
                ('services', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='serviceapp.servicemodel')),
            ],
        ),
    ]
