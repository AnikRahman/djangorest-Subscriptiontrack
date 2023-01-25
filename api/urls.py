from django.urls import path,include
from rest_framework import routers
from home.views import CustomerViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)


urlpatterns = [
    path('', include(router.urls)),
    
   
]