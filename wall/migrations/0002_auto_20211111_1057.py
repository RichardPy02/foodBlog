# Generated by Django 3.2.9 on 2021-11-11 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hash',
            field=models.CharField(default=None, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='tx_id',
            field=models.CharField(default=None, max_length=66, null=True),
        ),
    ]
