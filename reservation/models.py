from django.db import models
import datetime 

# Create your models here.

class Available(models.Model):
    Table_name = models.CharField(max_length=255)
    Available_count = models.IntegerField(max_length=255)
    Price = models.DecimalField(max_digits = 5,
                         decimal_places = 2)
    
    def __str__(self):
        return self.Table_name





class Reserve(models.Model):
    Table_name = models.ForeignKey(Available, on_delete=models.CASCADE)
    NumSeats_reserved = models.IntegerField(max_length=255)
    ResetTime = models.DateTimeField(default=datetime.datetime.now)

   

  


class Confirm(models.Model):
    Table_name = models.fieldName = models.ForeignKey(Available, on_delete=models.CASCADE)
    NumSeats_reserved = models.TextField(max_length=255)
    person = models.TextField(max_length=255)
    Email_address = models.EmailField(max_length=255)
    