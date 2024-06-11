from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import placeSerializer, LocationSerializer, ReverseGeocodeSerializer
from myapp.models import Place
import requests
from rest_framework.views import APIView

class GeocodeView(APIView):
    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            address = serializer.validated_data['address']
            api_key = 'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'  # Replace with your actual API key
            url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'}'
            response = requests.get(url)
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReverseGeocodeView(APIView):
    def post(self, request):
        serializer = ReverseGeocodeSerializer(data=request.data)
        if serializer.is_valid():
            lat = serializer.validated_data['lat']
            lng = serializer.validated_data['lng']
            api_key = 'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'  # Replace with your actual API key
            url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={'AIzaSyCXA-2ogmX_O4eFcyXUqto6LFOHwzMwLco'}'
            response = requests.get(url)
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/places',
        'POST /api/places/create',
        'POST /api/geocode/',
        'POST /api/reverse-geocode/',
    ]
    return Response(routes)

@api_view(['GET'])
def getPlaces(request):
    places = Place.objects.all()
    serializer = placeSerializer(places, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def createPlace(request):
    serializer = placeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
