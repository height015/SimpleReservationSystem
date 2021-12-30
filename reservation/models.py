from django.db import models
import datetime 

# Create your models here.

class Available(models.Model):
    Table_name = models.TextField(max_length=255)
    Available_count = models.TextField(max_length=255)
    Price = models.DecimalField(max_length=255)


class Reserve(models.Model):
    Table_name = models.ForeignKey(Available, on_delete=models.CASCADE)
    NumSeats_reserved = models.TextField(max_length=255)
    ResetTime = models.datetime(max_length=255, auto_now_add=True)

class Confirm(models.Model):
    Table_name = models.fieldName = models.ForeignKey(Reserve, on_delete=models.CASCADE)
    NumSeats_reserved = models.TextField(max_length=255)
    person = models.TextField(max_length=255)
    Email_address = models.EmailField(max_length=255)
    