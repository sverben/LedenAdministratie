# Generated by Django 2.2.1 on 2019-06-02 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LedenAdministratie", "0026_apitoken"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="telnr",
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
