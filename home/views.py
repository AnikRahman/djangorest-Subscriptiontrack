from rest_framework import viewsets
from home.models import Customer
from home.serializers import CustomerSerializer


#Customer Viweset
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()