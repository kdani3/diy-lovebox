from django.db import models

class Release(models.Model):
    file = models.FileField(upload_to='releases/')
    upload_time = models.DateTimeField(auto_now_add=True)