from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import placeSerializer
from myapp.models import Place, User, FoodSupplier
import json

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET / api/places',
        'POST /api/places/create',

    ]
    return Response(routes)

@api_view(['GET'])
def getPlaces(request):
    places = Place.objects.all()
    serializer = placeSerializer(places, many= True)
    return Response(serializer.data)

@api_view(['POST'])
def createPlace(request):
    serializer = placeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)