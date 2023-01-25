from django.db import models
import random



# Bangladesh phone number format: +880 xxxx-xxx-xxx


def generate_bd_phone_number():
    
   
    bd_phone_number = "+8801"
    for i in range(1):
        bd_phone_number += str(random.randint(4, 9))
    bd_phone_number += "-"
    for i in range(5):
        bd_phone_number += str(random.randint(0, 9))
    bd_phone_number += "-"
    for i in range(3):
        bd_phone_number += str(random.randint(0, 9))
    return bd_phone_number

#Customer Model
class Customer(models.Model):
    phone_number = models.CharField(primary_key=True, max_length=20, default=generate_bd_phone_number)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True, default=None)
    address = models.CharField(max_length=200,null=True, blank=True, default=None)
    def __str__(self):
        return self.phone_number
