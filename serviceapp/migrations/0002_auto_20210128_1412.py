# Generated by Django 3.1.5 on 2021-01-28 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviceapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='serviceapp.employee'),
        ),
    ]
