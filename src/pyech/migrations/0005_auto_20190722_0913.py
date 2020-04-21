# Generated by Django 2.2.3 on 2019-07-22 01:13

from django.db import migrations, models
import django.db.models.deletion
import pyech.models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
        ('pyech', '0004_auto_20190710_2212'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uploadfile',
            options={'verbose_name': '文件', 'verbose_name_plural': '文件'},
        ),
        migrations.CreateModel(
            name='CustomChartFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ChartPath', models.FileField(blank=True, upload_to=pyech.models.user_chartfile_path)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.User')),
            ],
            options={
                'verbose_name': '文件',
                'verbose_name_plural': '文件',
            },
        ),
    ]
