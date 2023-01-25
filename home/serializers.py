from rest_framework import serializers
from .models import  Customer



#Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('name','email' ,'address')