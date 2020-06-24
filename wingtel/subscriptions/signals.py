from django.db.models.signals import post_save
from django.dispatch import receiver

from wingtel.purchases.models import Purchase
from wingtel.subscriptions.models import SprintSubscription, ATTSubscription


@receiver(post_save, sender=ATTSubscription)
@receiver(post_save, sender=SprintSubscription)
def create_purchase_after_subscribe(sender, instance, created: bool, **kwargs):
    if not created:
        if kwargs.get('update_fields') and 'status' in kwargs.get('update_fields'):
            if instance.status in (SprintSubscription.STATUS.active, ATTSubscription.STATUS.active):
                Purchase.objects.create(
                    user_id=instance.user_id,
                    status=Purchase.STATUS.overdue,
                    amount=instance.plan.price
                )
