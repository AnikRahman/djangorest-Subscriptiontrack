from rest_framework import viewsets
from home.models import Customer, Payment, PlanChange
from home.serializers import CustomerSerializer, PaymentSerializer, PlanChangeSerializer
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from home.models import Company, Customer, PhoneNumber, Plan, Subscription, SubscriptionCancellation
from home.serializers import CompanySerializer, CustomerSerializer,  PhoneNumberSerializer,  PlanSerializer, SubscriptionCancellationSerializer, SubscriptionSerializer

from dateutil.relativedelta import relativedelta

from rest_framework import serializers

#Customer Viweset
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


#Customer Viweset

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    
      
#Plan Viweset

class PlanViewSet(viewsets.ModelViewSet):
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    actions = ['list','retrieve']      

#Company Viweset

class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

#PhoneNumber Viweset    
 
class PhoneNumberViewSet(viewsets.ModelViewSet):
    serializer_class = PhoneNumberSerializer
    queryset = PhoneNumber.objects.all()
    

#Subscription Viweset
class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        plan = serializer.validated_data.get('plan', instance.plan)
        start_date = instance.start_date
        months = plan.contract_duration
        end_date = start_date + relativedelta(months=+months)
        serializer.validated_data['end_date'] = end_date
        self.perform_update(serializer)
        return Response(serializer.data)
  

    

#Subscription Cancel Viewset


class SubscriptionCancellationViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionCancellationSerializer
    queryset = SubscriptionCancellation.objects.all()
    
    def perform_create(self, serializer):
        subscription = serializer.validated_data.get('subscription')
        if subscription.plan.can_cancel:
            subscription.is_cancelled = True
            subscription.save()
            serializer.save()
            
        else:
            raise serializers.ValidationError('This subscription cannot be cancelled')
  


  

#Payment Viweset                                                                                                                    



class PaymentViewset(viewsets.ModelViewSet):
  serializer_class = PaymentSerializer
  queryset = Payment.objects.all()  
  def post(self, request, *args, **kwargs):
   serializer = PaymentSerializer(data=request.data)
   serializer.is_valid(raise_exception=True)
   payment = serializer.save()
   payment.charge_with_stripe(request.data['stripe_token'])
   return Response({'message': 'Payment successful'}, status=status.HTTP_201_CREATED)




  
#PlanChange 
 
class PlanchangeViewSet(viewsets.ModelViewSet):
    serializer_class = PlanChangeSerializer
    queryset = PlanChange.objects.all()