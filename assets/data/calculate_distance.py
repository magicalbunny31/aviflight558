# calculates the distance in km from two locations
# this is basically the haversine formula

from math import radians, cos, sin, asin, sqrt


def calculate_distance(lon1: float, lat1: float, lon2: float, lat2: float):
   earth_radius = 6371 # earth's radius in km

   lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

   distance_lon = lon2 - lon1 
   distance_lat = lat2 - lat1 

   a = sin(distance_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(distance_lon / 2) ** 2
   c = 2 * asin(sqrt(a))
   
   return round(c * earth_radius, 2)