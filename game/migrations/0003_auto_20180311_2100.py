# Generated by Django 2.0.3 on 2018-03-11 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20180311_2050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'permissions': (('start', 'Start game'),)},
        ),
    ]
