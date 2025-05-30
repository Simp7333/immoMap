# Generated by Django 5.1.4 on 2025-02-18 22:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Biens', '0002_alter_biens_options_rename_quartier_biens_adresse_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biens',
            name='lagitude',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='biens',
            name='longitude',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='biens',
            name='type',
            field=models.ForeignKey(default='Terrain', on_delete=django.db.models.deletion.CASCADE, to='Biens.categories'),
        ),
    ]
