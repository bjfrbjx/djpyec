# Generated by Django 2.2.3 on 2020-04-18 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='running_list',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('user', models.CharField(max_length=128)),
                ('fun', models.CharField(max_length=128)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('sum_time', models.TimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('执行成功', '执行成功'), ('执行失败', '执行失败'), ('执行中', '执行中')], default='执行中', max_length=32)),
            ],
        ),
    ]
