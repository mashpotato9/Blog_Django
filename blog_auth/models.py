from django.db import models

# Create your models here.
class Capture(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now=True)