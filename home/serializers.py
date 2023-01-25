from rest_framework import serializers
from .models import  Customer, Payment, PlanChange
import datetime
from rest_framework import serializers
from .models import  Company, Customer, PhoneNumber, Plan, Subscription, SubscriptionCancellation
from datetime import timedelta

from dateutil.relativedelta import relativedelta


#Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('name','email' ,'address')
        

#Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    phone_numbers = serializers.SerializerMethodField()
    primary_phone_number = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()
    subscriptioncancel = serializers.SerializerMethodField()
    payments = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = ('name','email' ,'address','phone_numbers', 'primary_phone_number', 'subscription','subscriptioncancel', 'payments')
    
    def get_phone_numbers(self, obj):
        try:
           phone_numbers = PhoneNumber.objects.filter(customer=obj)
           return PhoneNumberSerializer(phone_numbers, many=True).data
        except PhoneNumber.DoesNotExist:
            return None    
    def get_primary_phone_number(self, obj):
        try:
           primary_phone_number = PhoneNumber.objects.get(customer=obj, is_primary=True)
           return PhoneNumberSerializer(primary_phone_number).data
        except PhoneNumber.DoesNotExist:
            return None
    def get_subscription(self, obj):
      subscription = Subscription.objects.filter(customer=obj).last()
      if subscription:
        return SubscriptionSerializer(subscription).data
      return None
    
    
    def get_subscriptioncancel(self, obj):
      try:
          subscription = Subscription.objects.filter(customer=obj,is_cancelled=True).last()
          return SubscriptionCancellationSerializer(subscription.subscriptioncancellation).data
      except (AttributeError, SubscriptionCancellation.DoesNotExist):
         return None

    def get_payments(self, obj):
        try:
          payments = Payment.objects.filter(subscription__customer=obj)
          return PaymentSerializer(payments, many=True).data
        except Subscription.DoesNotExist:
            return None   
            
    
            

#Plan Serializer
class PlanSerializer(serializers.ModelSerializer):
    contract_duration = serializers.IntegerField(help_text='duration in months')
    class Meta:
        model = Plan
        fields = '__all__'   

#Company Serializer
class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = '__all__'
          
#Phone Number Serializer
class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = '__all__'

    def validate(self, data):
        if data.get('is_primary'):
            if PhoneNumber.objects.filter(customer=data.get('customer'), is_primary=True).exists():
                raise serializers.ValidationError("Customer already has a primary phone number")
        return data     

#Subscription Serializer  

class SubscriptionSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(read_only=True)
    end_date = serializers.DateField(read_only=True)
    is_cancelled = serializers.BooleanField(read_only=True)
    class Meta:
        model = Subscription
        fields = ('id','customer','plan', 'start_date', 'end_date', 'is_cancelled')
    
    def validate(self, data):
        customer = data.get('customer')
        qs = Subscription.objects.filter(customer=customer, end_date__gte=datetime.date.today(), is_cancelled=False)
        if qs.exists():
            raise serializers.ValidationError('Customer already has an active subscription')
        return data
    
    def update(self, instance, validated_data):
        
        if 'customer'not in validated_data:
            raise serializers.ValidationError("Customer don't Match")
        validated_data.pop('customer', None)
        instance.plan = validated_data.get('plan', instance.plan)
        months = instance.plan.contract_duration
        instance.end_date = instance.start_date + relativedelta(months=+months)
        instance.save()
        return instance


#Subscription Cancel Serializer 
class SubscriptionCancellationSerializer(serializers.ModelSerializer):
    cancel_date = serializers.DateTimeField(read_only=True)
    class Meta:
        model = SubscriptionCancellation
        fields = ('subscription', 'cancel_date','reason')
 

#Payment Serializer           

class PaymentSerializer(serializers.ModelSerializer):
  class Meta:
   model = Payment
   fields = ('subscription', 'amount', 'stripe_charge_id')
   read_only_fields = ('amount', 'stripe_charge_id')




#Plan change

class PlanChangeSerializer(serializers.ModelSerializer):
  class Meta:
   model = PlanChange
   fields = '__all__'
    
            