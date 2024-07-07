import googlemaps.client
import requests
from geopy.distance import geodesic
from myapp.models import Place
import googlemaps
from datetime import datetime
import random

gmaps= googlemaps.Client( key= 'AIzaSyAJLe6L_bHnzqC6K3YO0ET_iw7D1gmo07I' )

def geocode_address(address):
    api_key = 'AIzaSyAJLe6L_bHnzqC6K3YO0ET_iw7D1gmo07I' 
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        response_data = response.json()
        if response_data['status'] == 'OK':
            location = response_data['results'][0]['geometry']['location']
            return (location['lat'], location['lng'])
        else:
            raise Exception(f"Geocoding error: {response_data['status']}")
    else:
        raise Exception(f"HTTP error: {response.status_code}")

def filter(user_lat, user_lng, kosher, vegan, max_distance_km):
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
    filtered_places = filter(user_lat, user_lng, kosher, vegan, 50)
    random.shuffle(filtered_places)
    
    if len(filtered_places) < num_stops:
        num_stops = len(filtered_places)
    

    waypoints = [f"{place.latitude},{place.longitude}" for place in filtered_places[:num_stops]]

    api_key = 'AIzaSyAJLe6L_bHnzqC6K3YO0ET_iw7D1gmo07I' 
    
    print(user_lat)
    print(user_lng)
    src = f"{user_lat},{user_lng}"
    now = datetime.now()
    result=gmaps.directions(src, src, mode="walking", waypoints=waypoints, optimize_waypoints=True, departure_time=now)
    waypoint_order = result[0]['waypoint_order']
    print(waypoint_order)
    optimal_route_places = [filtered_places[i] for i in waypoint_order]
    return optimal_route_places


