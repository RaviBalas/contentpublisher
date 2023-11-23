# Generated by Django 4.2.6 on 2023-11-22 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiLogsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('time_taken', models.FloatField(default=0)),
                ('task_name', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('request_type', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('data', models.TextField(blank=True, null=True)),
                ('files', models.TextField(blank=True, null=True)),
                ('json', models.TextField(blank=True, null=True)),
                ('response', models.TextField(blank=True, null=True)),
                ('status_code', models.CharField(blank=True, db_index=True, max_length=5, null=True)),
                ('error', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'apilogsmodel',
            },
        ),
        migrations.CreateModel(
            name='CustomLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('level', models.PositiveSmallIntegerField(choices=[(0, 'NotSet'), (20, 'Info'), (30, 'Warning'), (10, 'Debug'), (40, 'Error'), (50, 'Fatal')], db_index=True, default=40)),
                ('msg', models.TextField()),
                ('trace', models.TextField(blank=True, null=True)),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('error', models.IntegerField(null=True)),
                ('method', models.CharField(max_length=20, null=True)),
            ],
            options={
                'verbose_name': 'Logging',
                'verbose_name_plural': 'Logging',
                'db_table': 'logging',
                'ordering': ('-create_datetime',),
            },
        ),
    ]
