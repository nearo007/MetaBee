from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Printer(models.Model):
    name = models.CharField(max_length=100, default="Default Printer")
    status = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)], default=0)
    device_id = models.CharField(max_length=100, default="xxxxxxxxxxxxxxxxxxxxxx")