from django.core.cache import cache
from .models import Property


def getallproperties():
    """
    Utility function to get all properties from the cache.
    """
    queryset = cache.get('all_properties')
    if not queryset:
        try:
            queryset = list(Property.objects.all().order_by('-created_at'))
            # set cache
            cache.set('all_properties', queryset, timeout=3600)
        except Exception as e:
            return None
        
    # return the data either cached or freshly fetched
    return queryset
