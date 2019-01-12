import requests
import json


# Boundaries that define the North Texas area
lat_high = 35.93
lat_low = 29.43
long_high = -92.75
long_low = -101.23


# This feed lists all earthquakes for the last 30 days
urlData = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"


# Open the URL and read the data
r = requests.get(urlData)

# List for our earthquakes
earthQuakeData = []


def processData(data):

    count = data["metadata"]["count"]
    print(str(count) + " total earthquakes recorded over past 30 days.")

    for i in data["features"]:

        this_long = i["geometry"]["coordinates"][0]
        this_lat = i["geometry"]["coordinates"][1]

        if lat_low <= this_lat <= lat_high and long_low <= this_long <= long_high:
            print("Earthquake " + i["id"] + " near " + i["properties"]["place"] + " is local.")

            # Ignore non-earthquake events
            if i["properties"]["mag"] > 0:

                anEarthquake = {}

                #Let's start getting variables
                anEarthquake["id"] = i["id"] #unique id assigned by usgs
                anEarthquake["number_felt"] = i["properties"]["felt"] #number fo people who reported feeling it
                anEarthquake["depth"] = i["geometry"]["coordinates"][2] #depth in km
                anEarthquake["mag"] = i["properties"]["mag"] #magnitude float
                anEarthquake["place"] = i["properties"]["place"] #string describing location
                anEarthquake["event_time"] = i["properties"]["time"] #zulu time of event
                anEarthquake["event_time_zone"] = i["properties"]["tz"] #offset amount to account for time zone
                anEarthquake["url"] = i["properties"]["url"] #url to usgs page for this specific event
                anEarthquake["alert"] = i["properties"]["alert"] #color indicator of severity, green, yellow, red
                anEarthquake["significance"] = i["properties"]["sig"] #int representing metric used for significance using lots of variables
                anEarthquake["stations_reporting"] = i["properties"]["nst"] #number of stations reporting event, more is better
                anEarthquake["distance_to_station"] = i["properties"]["dmin"] #horizontal distance to nearest station

                earthQuakeData.append(anEarthquake)

    numOfLocalEarthQuakes = len(earthQuakeData)
    print(str(numOfLocalEarthQuakes) + " North Texas earthquakes recorded.")

    if numOfLocalEarthQuakes > 0:
        j = open("earthquakes.json","w+")
        json.dump(earthQuakeData, j, sort_keys=True, indent=4)
        j.close()
        print("Earthquakes saved")
    else: 
        print("No data saved")


#  If results exist
if (r.status_code == 200):
    # Process the results
    data = r.json()
    processData(data)
else:
    print("Received an error from server, cannot retrieve results " + str(r.status_code))
