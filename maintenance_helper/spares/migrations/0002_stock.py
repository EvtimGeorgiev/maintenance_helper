# Generated by Django 4.1.4 on 2022-12-11 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('spares', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('part_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='spares.sparepart')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('min_stock_qty', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
