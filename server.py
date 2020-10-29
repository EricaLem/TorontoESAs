# server.py
import json
import requests
import pandas as pd
from geojson import Point, Feature

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

# read the settings.py configuration file from the environment variable 
app.config.from_envvar('APP_CONFIG_FILE', silent=True)

# get the Mapbox Access Token from the configuration file
MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']

"""Routes"""

@app.route("/")
def index():
	# Add review
	return render_template("success.html", message="we have that ESA in our DB")

@app.route('/mapbox_js')
def mapbox_js():
	"""Map"""
	return render_template("mapbox_js.html", ACCESS_KEY=MAPBOX_ACCESS_KEY)


"""Functions"""

# Function to create the API URL with all geo-coordinates and the Mapbox access token
def create_route_url():
	# Create a string with all the geo coordinates
	lat_longs = ";".join(["{0},{1}".format(point["long"], point["lat"]) for point in ROUTE])
	# Create a url with the geo coordinates and access token
	url = ROUTE_URL.format(lat_longs, MAPBOX_ACCESS_KEY)
	return url

def get_route_data():
	# Get the route url
	route_url = create_route_url()
	# Perform a GET request to the route API
	result = requests.get(route_url)
	# Convert the return value to JSON
	data = result.json()

	# Create a geoJSON object from the routing data
	geometry = data["routes"][0]["geometry"]
	route_data = Feature(geometry = geometry, properties = {})
	return route_data


if __name__ == "__main__":
# To interact with app via the command line
	with app.app_context():
		main()