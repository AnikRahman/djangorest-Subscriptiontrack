from django.contrib import admin
from home.models import Customer,Plan,Company,Subscription,SubscriptionCancellation,PlanChange


# Register your models here for admin
admin.site.register(Customer)
admin.site.register(Plan)
admin.site.register(Company)
admin.site.register(Subscription)
admin.site.register(SubscriptionCancellation)
admin.site.register(PlanChange)
