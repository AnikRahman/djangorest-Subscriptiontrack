from django.db.models.signals import post_save
from django.dispatch import receiver
from home.models import Subscription, PlanChange

@receiver(post_save, sender=Subscription)
def create_plan_change(sender, instance, **kwargs):
    if kwargs['created']:
        return
    try:
        old_plan = Subscription.objects.get(pk=instance.pk).plan
    except Subscription.DoesNotExist:
        return
    if old_plan != instance.plan:
        PlanChange.objects.create(subscription=instance, old_plan=old_plan, new_plan=instance.plan)