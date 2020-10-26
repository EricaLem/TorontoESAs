import datetime
import os, csv, urllib, json
import requests
import pandas as pd
# import plotly.express as px

# DATABASE_URL = 'postgres://postgres:Growitall1!@localhost:5432/postgres'
# DATABASE_URL = 'postgres://usjpqmbuiezlph:d4c775438eacbcc8d4a583224c8a3fabedeae8418197c9103fb7889edc06eaff@ec2-18-213-176-229.compute-1.amazonaws.com:5432/ddie9l9dn3k4kf'
# postgres://usjpqmbuiezlph:d4c775438eacbcc8d4a583224c8a3fabedeae8418197c9103fb7889edc06eaff@ec2-18-213-176-229.compute-1.amazonaws.com:5432/ddie9l9dn3k4kf

from flask import Flask, render_template, request, jsonify
from sqlalchemy.orm import defer, joinedload, load_only
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://usjpqmbuiezlph:d4c775438eacbcc8d4a583224c8a3fabedeae8418197c9103fb7889edc06eaff@ec2-18-213-176-229.compute-1.amazonaws.com:5432/ddie9l9dn3k4kf"
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Tie the database to the Flask application
db.init_app(app)

# APIs
# 1. Currency exchange API
fixerIOAPIKey = "5ac26b3a348bf9eeaf676b5ee443a122"


# Routes
@app.route("/")
def index():
    """Home page"""
    # 2. Toronto ESAs API
    # Get the ESA dataset metadata by passing package_id to the package_search endpoint:
    url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
    params = { "id": "ef5a083a-5c2a-4207-9131-dfc917917069"}
    response = urllib.request.urlopen(url, data=bytes(json.dumps(params), encoding="utf-8"))
    package = json.loads(response.read())
    #print(package["result"])

    # Get the data by passing the resource_id to the datastore_search endpoint
    # See https://docs.ckan.org/en/latest/maintaining/datastore.html for detailed parameters options:
    for idx, resource in enumerate(package["result"]["resources"]):
        if resource["datastore_active"]:
            url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search"
            p = { "id": resource["id"] }
            r = urllib.request.urlopen(url, data=bytes(json.dumps(p), encoding="utf-8"))
            data = json.loads(r.read())
            #print(data["result"]["records"][1]["ESA_NAME"])
            #df = pd.DataFrame(data["result"]["records"])
            break
    headline = "Toronto's Environmentally Significant Areas (ESAs)"
    ESAZ = data["result"]["records"]
    esaList = []
    for i in ESAZ:
        e = i['ESA_NAME']
        esaList.append(e)

    return render_template("index.html", headline=headline, esaList=esaList)

@app.route("/map", methods=["GET"])
def map():
    """See them on a map"""
    us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
    fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                            color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

    # Add review
    return render_template("map.html")


@app.route("/welcome", methods=["POST"])
def welcome():
    """Leave a review"""

    # Get form information
    esaName = request.form.get("esaName")
    ## ERROR MESSAGE
    # try:
    #     flight_id = int(request.form.get("flight_id"))
    # except ValueError:
    #    return render_template("error.html", message="invalid flight number")

    # Make sure ESA exists
    esaObject = ESA.query.get(esaName)
    ## ERROR MESSAGE
    if esaObject is None:
        return render_template("error.html", message="no such ESA")

    # Add review
    return render_template("success.html", message="we have that ESA in our DB")

@app.route("/convertcurrency", methods=["POST"])
def convertcurrency():
    """Convert currency"""
    # Query for currency exchange rate
    currency = request.form.get("currency")
    # Make API call requesting exchange rate
    # This is an AJAX request to the web server (i.e. Flask)
    # which will GET the exchange rate from fixer.io
    # and then JS script runs to update the DOM and render the information on the page
    res = requests.get("http://data.fixer.io/api/latest", params = {
        "access_key": fixerIOAPIKey, "symbols": currency })

    # Make sure request succeeded
    if res.status_code != 200:
        return jsonify({"success": False})

    # Make sure currency is in response
    data = res.json()
    print ("BLARGITY")
    print (f"BLARGITY is {data}")
    if currency not in data["rates"]:
        return jsonify({"success": False})

    return jsonify({"success": True, "rate": data["rates"][currency]})


if __name__ == "__main__":
# To interact with app via the command line
    with app.app_context():
        main()