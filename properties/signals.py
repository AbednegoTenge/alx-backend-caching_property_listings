from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Property
from django.core.cache import cache

@receiver(post_save, sender=Property)
def clear_cache_on_save_or_update(sender, instance, created, **kwargs):
    if created:
        print(f"New property created: {instance.title}")
    else:
        print(f"Property updated: {instance.title}")

    cache.delete('all_properties')
    print("cache invalidated successfully")


@receiver(post_delete, sender=Property)
def clear_cache_on_delete(sender, instance, **kwargs):
    cache.delete('all_properties')
    print("cache invalidated successfully")