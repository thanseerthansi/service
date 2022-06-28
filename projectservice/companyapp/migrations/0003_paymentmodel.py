# Generated by Django 4.0.5 on 2022-06-28 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companyapp', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentid', models.CharField(max_length=100)),
                ('is_paid', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='companyapp.acceptedquotemodel')),
            ],
        ),
    ]
