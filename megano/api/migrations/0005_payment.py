# Generated by Django 4.2 on 2023-07-16 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=100, verbose_name='number')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='name')),
                ('month', models.CharField(blank=True, max_length=100, verbose_name='month')),
                ('year', models.CharField(blank=True, max_length=100, verbose_name='year')),
                ('code', models.CharField(blank=True, max_length=100, verbose_name='code')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
