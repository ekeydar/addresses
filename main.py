import json
import requests
from bottle import route, run, abort, static_file

from math import radians, cos, sin, asin, sqrt

USERS = None

class User(object):
	def __init__(self,ju):
		self.name = ju['name']
		self.address = ju['address']
		self.coords = geocode(self.address)

	def get_distance_dict(self,loc):
		result = self.__dict__
		result['distance'] = haversine(self.coords,loc)
		return result

def geocode(address):
	#print self.name
	params=dict(address=address,sensor='false')
	r =  requests.get('http://maps.googleapis.com/maps/api/geocode/json',params=params)
	return r.json()['results'][0]['geometry']['location']

def haversine(loc1, loc2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [loc1['lng'], loc1['lat'], loc2['lng'], loc2['lat']])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def build_users(filename):
	fh = open(filename)
	input_users = json.load(fh)
	fh.close()
	users = []
	for u in input_users:
		users.append(User(u))
	return users

def find_distances_from(address):
	address_loc = geocode(address)
	result = []
	for u in USERS:
		result.append(u.get_distance_dict(address_loc))
	return result


USERS = build_users('input.json')

@route('/static/<path:path>')
def callback(path):
    return static_file(path,root='static')

run(host='localhost', port=8080,reloader=True)