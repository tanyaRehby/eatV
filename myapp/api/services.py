import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from geopy.distance import geodesic
from myapp.models import Place
import googlemaps
import random
from datetime import datetime
import googlemaps.client
import os 

gmaps = googlemaps.Client(key='AIzaSyB6dFwZLE-e9h_aoAWVXj-zOsbYe4KZaEg')

def geocode_address(address):
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    print(f"Using API Key: {api_key}")  
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    print(f"Geocode URL: {url}")  
    response = requests.get(url)
    response_data = response.json()
    print(f"Geocode response: {response_data}")  

    if response.status_code == 200:
        if response_data['status'] == 'OK':
            location = response_data['results'][0]['geometry']['location']
            return (location['lat'], location['lng'])
        else:
            raise Exception(f"Geocoding error: {response_data['status']} - {response_data.get('error_message', 'Unknown error')}")
    else:
        raise Exception(f"HTTP error: {response.status_code}")


def filter_places(user_lat, user_lng, kosher, vegan, max_distance_km):
    places = Place.objects.all()
    filtered_places = []
    for place in places:
        if kosher and not place.is_kosher:
            continue
        if vegan and not place.has_vegan_option:
            continue

        distance = geodesic((user_lat, user_lng), (place.latitude, place.longitude)).km
        if distance <= max_distance_km:
            filtered_places.append(place)
    
    return filtered_places


def plan_tour(user_address, kosher=False, vegan=False, num_stops=5):
    user_lat, user_lng = geocode_address(user_address)
    filtered_places = filter_places(user_lat, user_lng, kosher, vegan, 3)
    random.shuffle(filtered_places)

    if len(filtered_places) < num_stops:
        num_stops = len(filtered_places)
    
    waypoints = [f"{place.latitude},{place.longitude}" for place in filtered_places[:num_stops]]
    
    print(f"user_lat: {user_lat}, user_lng: {user_lng}")
    src = f"{user_lat},{user_lng}"
    now = datetime.now()
    result = gmaps.directions(src, src, mode="walking", waypoints=waypoints, optimize_waypoints=True, departure_time=now)
    waypoint_order = result[0]['waypoint_order']
    print(f"waypoint_order: {waypoint_order}")
    optimal_route_places = [filtered_places[i] for i in waypoint_order]
    return optimal_route_places


class TourView(APIView):
    def post(self, request):
        try:
            address = request.data.get('address')
            kosher = request.data.get('kosher', False)
            vegan = request.data.get('vegan', False)
            num_stops = request.data.get('num_stops', 5)
            try:
                num_stops = int(num_stops)
            except ValueError:
                return Response({"error": "num_stops must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

            tour = plan_tour(address, kosher, vegan, num_stops)

            if tour is not None:
                serialized_tour = [{
                    'place_name': place.place_name,
                    'city': place.city,
                    'address': place.address,
                    'food_category': place.food_category,
                    'latitude': place.latitude,
                    'longitude': place.longitude,
                } for place in tour]
                return Response(serialized_tour, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No suitable route found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error processing tour request: {e}")
            return Response({"error": f"Internal server error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
