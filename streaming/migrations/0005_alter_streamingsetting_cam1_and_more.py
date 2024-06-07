# Generated by Django 5.0.6 on 2024-06-06 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0004_alter_streamingsetting_num_cam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='streamingsetting',
            name='cam1',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Cámara 1'),
        ),
        migrations.AlterField(
            model_name='streamingsetting',
            name='cam2',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Cámara 2'),
        ),
        migrations.AlterField(
            model_name='streamingsetting',
            name='cam3',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Cámara 3'),
        ),
        migrations.AlterField(
            model_name='streamingsetting',
            name='cam4',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Cámara 4'),
        ),
    ]