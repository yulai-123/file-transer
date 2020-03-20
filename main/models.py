from django.db import models

# Create your models here.

class File(models.Model):
    name = models.CharField(max_length=200, verbose_name="name")
    size = models.DecimalField(max_digits=15, decimal_places=3, verbose_name="size")
    path = models.CharField(max_length=200, verbose_name="path")
    timestamp = models.CharField(max_length=50, verbose_name="timestamp")

    def __str__(self):
        return self.name