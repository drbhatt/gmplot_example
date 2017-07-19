# _*_ coding:utf-8 _*_
# ----------------------------------------------------------------
# $Header: projAustin.py                  Rev. %I% %G%
# ----------------------------------------------------------------
# - Description:
#	This source file implements the solution for below
# https://itse-1402.github.io/project2/
#	
# - Installation:
#	Python 2.7.10
#	pip install gmplot
#	pip install flask <--- optional
#	pip install pygeocoder
#	pip install Geocoder
#
# - Usage:
#	download the json data from:
# https://data.austintexas.gov/api/views/ecmv-9xxi/rows.json?accessType=DOWNLOAD
#       place the rows.json into the same dir as projAustin.py
#	replace the gmplot.py to include titles for each marker
#       python projAustin.py
#
#	The output will be generated in the same dir called
#	map.html
#	Simply open austinmap.html into a browser to show the results
# ----------------------------------------------------------------

import json
import os
import sys
import urllib, urllib2
from pygeocoder import Geocoder
import gmplot


'''
from flask import Flask
app = Flask(__name__)
'''

# ------------------------------------------
# Function: decode_address_to_coordinates(address)
# Desc: This function returns the geo location in
# lat,longitude and takes the input of geo address
# credit:
# https://stackoverflow.com/questions/15285691/googlemaps-api-address-to-coordinates-latitude-longitude
#
# Params: address
#
# return: coordinates of latitude, longitude
# ------------------------------------------
def decode_address_to_coordinates(address):
        params = {
                'address' : address,
                'sensor' : 'false',
        }  
        url = 'http://maps.google.com/maps/api/geocode/json?' + urllib.urlencode(params)
        response = urllib2.urlopen(url)
        result = json.load(response)
        try:
                return result['results'][0]['geometry']['location']
        except:
                return None

# ------------------------------------------
# Function: get_config_file()
# Desc: This function returns the config
# file which stores the videos downloaded
# in json file format
#       
# Params: 
#
# return: location of config file
# ------------------------------------------
def get_config_file():
	config_file = os.path.dirname(os.path.realpath(__file__))
	config_file += "/rows.json"
	return config_file

# ------------------------------------------
# Function: load_json_file(dest_dir, url)
# Desc: This function loads the data from 
# json file and generates the data points
# onto a google map using gmplot module 
# which indirectly is using Google Map
#
# Params: 
#
# return: json data from the config_file
# ------------------------------------------
def load_json(zipcode):
	file=get_config_file()
	f = open(file, "r")
	data = json.loads(f.read())
	f.close()
	latitude = []
	longitude = []
	titles = []
	for entry in data["data"]:
		jsonEntry = json.loads(entry[12][0])
		if (jsonEntry["zip"] == zipcode):
			print jsonEntry	
			addr = jsonEntry["address"] + " " + jsonEntry["city"] +  " " + jsonEntry["state"] + " " + jsonEntry["zip"]
			lat = entry[12][1]
			lng = entry[12][2]
			#geoloc= decode_address_to_coordinates(addr)
			if lat != None:
				latitude.append(float(str(entry[12][1])))
				longitude.append(float(str(entry[12][2])))
				print entry[8]
				titles.append(entry[8])
	#initialize the map w/ latitude, longitude and zoom level
	gmap = gmplot.GoogleMapPlotter(latitude[0],longitude[0], 16)
	# Draw all points on the map using tomato color
	gmap.scatter(latitude, longitude, 'tomato', marker=True, titles=titles, edge_width=10)
	# Generate the map in an HTML file
	gmap.draw('austinmap.html')

'''
@app.route("/")
def main():
	return "Welcome!!"

if __name__ == "__main__":
	app.run()
'''

# ------------------------------------------
# We will only plot all restaurants found
# from the dataset provided where latitude
# and longitude info are available.  Addresses
# without longitude and latitude will not be
# plotted
# By default, zipcode 78728 is used to plot 
# restaurants found in zipcode and plotted 
# using gmplot module accordingly
#
# among many plot types available, we are 
# using Scatter points to plot the details
# ------------------------------------------
#zipcode = '78728'
zipcode = '78759'
load_json(zipcode)

