# Generated by Django 5.0.6 on 2024-06-06 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('streaming', '0002_alter_camera_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streamingsetting',
            name='cameras',
        ),
        migrations.AddField(
            model_name='streamingsetting',
            name='cam1',
            field=models.CharField(blank=True, max_length=150, verbose_name='Cámara 1'),
        ),
        migrations.AddField(
            model_name='streamingsetting',
            name='cam2',
            field=models.CharField(blank=True, max_length=150, verbose_name='Cámara 2'),
        ),
        migrations.AddField(
            model_name='streamingsetting',
            name='cam3',
            field=models.CharField(blank=True, max_length=150, verbose_name='Cámara 3'),
        ),
        migrations.AddField(
            model_name='streamingsetting',
            name='cam4',
            field=models.CharField(blank=True, max_length=150, verbose_name='Cámara 4'),
        ),
        migrations.DeleteModel(
            name='Camera',
        ),
    ]
