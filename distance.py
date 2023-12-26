from math import sqrt, radians, sin, cos, asin
from models import Building
from models import Deck

# function to calculate the distance between a deck and a building using the haversine formula
def calculate_distance(deck_lat, deck_long, target_lat, target_long):

    # convert degrees to radians
    deck_lat, deck_long, target_lat, target_long = map (radians, [deck_lat, deck_long, target_lat, target_long])
    
    # find the differences between lattitues and longitudes
    delta_lat = deck_lat - target_lat
    delta_long = deck_long - target_long

    # apply the haversine formula given the radius of earth is 3956 miles
    a = sin(delta_lat/2)**2 + cos(deck_lat) * cos(target_lat) * sin(delta_long/2)**2
    c = 2 * asin(sqrt(a))
    r = 3956
    distance = c * r
    
    # return the result
    return distance