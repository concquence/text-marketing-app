# Generated by Django 3.2.16 on 2022-12-22 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mass_texting', '0002_auto_20221221_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='code',
            field=models.CharField(blank=True, max_length=3, verbose_name='Код оператора'),
        ),
    ]
