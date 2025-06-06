# Generated by Django 3.2.19 on 2025-04-10 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tickets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketlist',
            name='engineer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='工程师'),
        ),
        migrations.AddField(
            model_name='ticketlist',
            name='floor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.floor', verbose_name='楼层'),
        ),
        migrations.AddField(
            model_name='ticketlist',
            name='incident_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='organization.incidenttype', verbose_name='故障类别'),
        ),
        migrations.AddField(
            model_name='ticketlist',
            name='service_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.servicetype', verbose_name='服务类别'),
        ),
    ]
