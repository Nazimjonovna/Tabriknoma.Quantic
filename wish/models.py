from contextlib import nullcontext
from email.policy import default
from django.db import models
import os
from uuid import uuid4
from otp.models import User

# Create your models here.
def get_audio_upload(filename, instance):
    ext = str(filename).split('.')[-1]
    filename = f'{uuid4()}.{ext}'
    return os.path.join("uploads/audio/", filename)




class Wishmodel(models.Model):
    TARIF_CHOICES = (
        ('standart', 'Standart'),
        ('premium', 'Premium'),
    )

    STATUS_CHOICES = (
        ('incompleted', 'Incompleted'),
        ('completed', 'Completed'),
    )

    AUDIO_CHOICES = (
        ('person_name1', 'Person_name1'),
        ('person_name2', 'Person_name2'),
        ('person_name3', 'Person_name3'),
    )

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='wishes')
    text = models.TextField()
    audio = models.FileField(upload_to=get_audio_upload, null=True, blank=True)
    to_number = models.IntegerField(null=True, blank=True)
    voise=models.CharField( max_length=40,
                            choices=AUDIO_CHOICES,
                            null=True, blank=True)

    tarif = models.CharField(max_length=10, choices=TARIF_CHOICES, default='standart')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='incompleted')
                              
    date_of_send = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.text

