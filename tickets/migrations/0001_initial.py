# Generated by Django 3.2.19 on 2025-04-10 05:57

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='日期')),
                ('issue', models.TextField(verbose_name='问题描述')),
                ('solution', models.TextField(blank=True, verbose_name='解决方法')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.department', verbose_name='部门')),
            ],
            options={
                'verbose_name': '工单记录',
                'verbose_name_plural': '工单记录',
            },
        ),
    ]
