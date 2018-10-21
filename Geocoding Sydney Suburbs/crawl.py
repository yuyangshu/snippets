import googlemaps
import pickle

with open("api.key", 'r') as f:
    api_key = f.read().strip()

gmaps = googlemaps.Client(key=api_key)
geolocation = dict()

with open ("suburbs.txt", 'r') as f:
    rows = f.readlines()
    for row in rows:
        if len(row) < 2 or row[0] == "#": continue
        name, pcode = row.strip().split(', ')
        geocode_result = gmaps.geocode(name + " NSW " + pcode)[0]['geometry']['location']
        geolocation[name] = (int(pcode), float(geocode_result['lat']), float(geocode_result['lng']))

with open("suburbs_geolocations", 'wb') as f:
    pickle.dump(geolocation, f)