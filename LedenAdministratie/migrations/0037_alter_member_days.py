# Generated by Django 3.2.12 on 2022-04-10 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LedenAdministratie', '0036_auto_20220410_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='days',
            field=models.IntegerField(choices=[(1, '1 dagdeel'), (2, '2 dagdelen')], default=1, verbose_name='Aantal dagdelen aanwezig'),
        ),
    ]
