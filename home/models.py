from django.db import models
import random
import datetime
from dateutil.relativedelta import relativedelta
import stripe
from django.conf import settings

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


#Plan Model
class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    contract_duration =models.PositiveSmallIntegerField(help_text='duration in months')
    can_cancel = models.BooleanField()

    def __str__(self):
        return self.name         

#Company Model
class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

#PhoneNumber Model
class PhoneNumber(models.Model):
    number = models.CharField(primary_key=True, max_length=20, default=generate_bd_phone_number)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_primary:
            PhoneNumber.objects.filter(customer=self.customer, is_primary=True).update(is_primary=False)
        super(PhoneNumber, self).save(*args, **kwargs)



#Subscription Model
class Subscription(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    is_cancelled = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
       if self.plan and not self.end_date:
        months = self.plan.contract_duration
        self.end_date = datetime.date.today() + relativedelta(months=+months)
       super().save(*args, **kwargs)      


#Subscription Cancel Model

class SubscriptionCancellation(models.Model):
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE)
    cancel_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    

#Plan change track  
class PlanChange(models.Model):
   subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
   old_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='old_plan')
   new_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='new_plan')
   change_date = models.DateTimeField(auto_now_add=True)    

#Payment Model
class Payment(models.Model):
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    stripe_charge_id = models.CharField(max_length=255) 
    
    def save(self, *args, **kwargs):
      self.amount = self.subscription.plan.price
      super().save(*args, **kwargs)

    def charge_with_stripe(self, stripe_token):
        stripe.api_key = settings.STRIPE_SECRET_KEY
       
        try:
         charge = stripe.Charge.create(
            amount=int(self.amount * 100),
            currency='usd',
            source=stripe_token,
            description='Payment for subscription'
        )
         self.stripe_charge_id = charge.id
         self.save()
        except stripe.error.CardError as e:
         raise ValueError(e)
