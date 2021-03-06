# Generated by Django 2.0.3 on 2018-03-11 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('style', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gameconfig',
            name='correct_bonus',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='gameconfig',
            name='wrong_penalty',
            field=models.IntegerField(default=30),
        ),
        migrations.AddField(
            model_name='event',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game'),
        ),
    ]
