from django.urls import path,include
from rest_framework import routers
from home.views import CustomerViewSet, CompanyViewSet, CustomerViewSet, PaymentViewset, PlanViewSet, PlanchangeViewSet, SubscriptionCancellationViewSet,SubscriptionViewSet,PhoneNumberViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'plan', PlanViewSet)
router.register(r'phone', PhoneNumberViewSet)
router.register(r'company', CompanyViewSet)
router.register(r'subscription', SubscriptionViewSet)
router.register(r'subscriptionCancel', SubscriptionCancellationViewSet)
router.register(r'Payment',PaymentViewset )
router.register(r'PlanChange',PlanchangeViewSet )

urlpatterns = [
    path('', include(router.urls)),
    
   
]