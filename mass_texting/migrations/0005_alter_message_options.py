# Generated by Django 3.2.16 on 2022-12-22 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mass_texting', '0004_alter_customer_tag'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-id']},
        ),
    ]
