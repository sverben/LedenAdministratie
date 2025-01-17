# Generated by Django 4.0.8 on 2023-01-22 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LedenAdministratie', '0039_member_revbank_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stripcard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField(auto_created=True, verbose_name='Datum van uitgifte')),
                ('issued_by', models.CharField(default='', max_length=255, verbose_name='Uitgegeven door')),
                ('count', models.IntegerField(default=10, verbose_name='Aantal')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LedenAdministratie.member')),
            ],
        ),
    ]
