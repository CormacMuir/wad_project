# Generated by Django 2.2.3 on 2020-04-03 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workitout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='usage',
            field=models.IntegerField(default=0),
        ),
    ]
