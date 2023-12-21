# Generated by Django 4.2.7 on 2023-12-04 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branch', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory_id', models.CharField(max_length=100, unique=True)),
                ('quantity', models.IntegerField()),
                ('expiry_date', models.DateField()),
                ('batch_no', models.CharField(max_length=100)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch.branch')),
                ('medicine_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.medicine')),
            ],
        ),
    ]
