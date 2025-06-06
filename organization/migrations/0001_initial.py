# Generated by Django 3.2.19 on 2025-04-10 05:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='部门名称')),
            ],
            options={
                'verbose_name': '部门',
                'verbose_name_plural': '部门',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='楼层名称')),
            ],
            options={
                'verbose_name': '楼层',
                'verbose_name_plural': '楼层',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='IncidentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='故障类型')),
            ],
            options={
                'verbose_name': '故障类别',
                'verbose_name_plural': '故障类别',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='服务类型')),
            ],
            options={
                'verbose_name': '服务类别',
                'verbose_name_plural': '服务类别',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.department', verbose_name='所属部门')),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.floor', verbose_name='所在楼层')),
            ],
            options={
                'verbose_name': '地理位置',
                'verbose_name_plural': '地理位置',
                'ordering': ['department', 'floor'],
                'unique_together': {('department', 'floor')},
            },
        ),
    ]
