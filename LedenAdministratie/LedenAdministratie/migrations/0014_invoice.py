# Generated by Django 2.1.5 on 2019-02-22 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LedenAdministratie', '0013_note_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('username', models.CharField(default='', max_length=255)),
                ('payed', models.BooleanField(default=False, verbose_name='Betaald')),
                ('sent', models.DateTimeField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=6, verbose_name='Bedrag')),
                ('pdf', models.BinaryField(blank=True, editable=True, null=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='LedenAdministratie.Member')),
            ],
        ),
    ]
