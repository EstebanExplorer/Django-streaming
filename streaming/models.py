from django.db import models
from django.contrib.auth.models import User



class StreamingSetting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='streaming_settings',
        related_name='streaming_settings'
    )

    STATUS_CHOICES = [(i, str(i)) for i in range(1, 5)]
    num_cam = models.IntegerField('Number of cameras', choices=STATUS_CHOICES, default=1)
    start = models.CharField('Start/Stop', max_length=20, default="Start")
    cam1 = models.CharField('Camera 1', max_length=150, blank=True, null=True)
    cam2 = models.CharField('Camera 2', max_length=150, blank=True, null=True)
    cam3 = models.CharField('Camera 3', max_length=150, blank=True, null=True)
    cam4 = models.CharField('Camera 4', max_length=150, blank=True, null=True)
    channel_name = models.CharField('channel id', max_length=150, blank=True)
    date_joined = models.DateTimeField('Entry date', auto_now_add=True)

    def __str__(self):
        return f" ID: {self.id}, State: {self.start}"

