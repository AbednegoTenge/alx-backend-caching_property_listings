from .models import Property
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from .serializers import PropertySerializer
from rest_framework import status

# Create your views here.

@cache_page(60 * 15)  # Cache the view for 15 minutes
@api_view(['GET'])
def property_list(request):
    properties = Property.objects.all().order_by('-created_at')
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    