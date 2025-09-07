from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Groups


@receiver(post_save, sender=CustomUser)
def create_user_groups(sender, instance, created, **kwargs):
    if created:
        Groups.objects.create(user=instance, chats=[])


@receiver(post_save, sender=CustomUser)
def save_user_groups(sender, instance, **kwargs):
    if hasattr(instance, 'user_groups'):
        instance.user_groups.save()