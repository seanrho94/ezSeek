# Generated by Django 2.1 on 2019-12-03 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RS', '0017_auto_20191203_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='company_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RS.Company'),
        ),
    ]
