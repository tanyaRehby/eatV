from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from myapp.models import Journey 
from .serializers import JourneySerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET / api/journeys',
        # 'GET / api/journeys/:journey_code'
    ]
    return Response(routes)

@api_view(['GET'])
def getJourneys(request):
    journeys = Journey.objects.all()
    serializer = JourneySerializer(journeys, many= True)
    return Response(serializer.data)

@api_view(['POST'])
def createJourney(request):
    serializer = JourneySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# @api_view(['GET'])
# def getJourney(request, pk):
#     journey = Journey.objects.get(journey_code = pk)
#     serializer = JourneySerializer(journey, many= False)
#     return Response(serializer.data)