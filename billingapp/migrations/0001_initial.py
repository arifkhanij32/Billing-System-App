# Generated by Django 5.1.3 on 2025-01-03 06:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Denomination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField()),
                ('count', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('product_id', models.CharField(max_length=50, unique=True)),
                ('available_stocks', models.PositiveIntegerField()),
                ('price', models.FloatField()),
                ('tax_percentage', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_id', models.CharField(blank=True, max_length=255, unique=True)),
                ('customer_email', models.EmailField(max_length=254)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('total_price_without_tax', models.FloatField()),
                ('total_tax', models.FloatField()),
                ('net_price', models.FloatField()),
                ('paid_amount', models.FloatField()),
                ('balance_due', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('purchase_price', models.FloatField()),
                ('tax_payable', models.FloatField()),
                ('total_price', models.FloatField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billingapp.product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='billingapp.purchase')),
            ],
        ),
    ]
