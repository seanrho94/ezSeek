# Generated by Django 2.1 on 2021-05-13 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RS', '0023_post_applied'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(default='In Progress', max_length=200),
        ),
    ]
