# Generated by Django 2.1 on 2019-12-04 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RS', '0020_auto_20191203_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='status',
            field=models.CharField(default='In Progress', max_length=40),
        ),
    ]
