# Generated by Django 3.0.6 on 2020-05-31 16:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maketing', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='marketingmessage',
            options={'ordering': ['-start_date', '-end_date']},
        ),
    ]
