from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.cache import cache_page
from .utils import get_all_properties, get_redis_cache_metrics

@cache_page(60 * 15)  # Cache the view for 15 minutes
@api_view(['GET'])
def property_list(request):
    properties = get_all_properties()

    data = []
    for p in properties:
        data.append({
            "id": p.id,
            "title": p.title,
            "price": float(p.price),
            "location": p.location,
            "created_at": p.created_at.isoformat(),
        })

    return JsonResponse({
        "properties": data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_metrics():
    metrics = get_redis_cache_metrics()
    return JsonResponse({
        'metrics': metrics
    }, status=status.HTTP_200_OK)
