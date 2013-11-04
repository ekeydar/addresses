import json
import requests

from math import radians, cos, sin, asin, sqrt

class User(object):
	def __init__(self,ju):
		self.name = ju['name']
		self.address = ju['address']
		self.coords = self.geocode()

	def geocode(self):
		#print self.name
		params=dict(address=self.address,sensor='false')
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

def main():
	users = build_users('input.json')
	for u in users:
		print u.name
		print u.coords











if __name__ == '__main__':
	main()