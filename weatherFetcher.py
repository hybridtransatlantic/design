import requests,json,math
import xml.etree.ElementTree as ET


def waypoints(lat1, lon1, lat2, lon2, N):
    lats = []
    lons = []

    lats.append(lat1)
    lons.append(lon1)

    fraction = 1.0 / float(N)
    f = fraction
    while (f < 1.0 - fraction):
        result = intermediatePoint(lat1, lon1, lat2, lon2, f)
        lats.append(result['lat'])
        lons.append(result['lon'])
        f = f + fraction

    lats.append(lat2)
    lons.append(lon2)

    return {"lats":lats,"lons":lons}



def greatCircleDist(lat1,lon1,lat2,lon2):
    R = 6371000.0
    phi1 = lat1 * 0.0174533
    phi2 = lat2 * 0.0174533
    deltaPhi = (lat2 - lat1) * 0.0174533
    deltaLambda = (lon2 - lon1) * 0.0174533
    a = math.sin(deltaPhi/2) * math.sin(deltaPhi/2) + math.cos(phi1)*math.cos(phi2) * math.sin(deltaLambda/2) * math.sin(deltaLambda/2)
    c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
    d = R * c
    return d / 1000.0


def intermediatePoint(lat1, lon1, lat2, lon2, fraction):
    R = 6371.0
    d = greatCircleDist(lat1, lon1, lat2, lon2)
    delta = d / R
    a = math.sin((1 - fraction)*delta) / math.sin(delta)
    b = math.sin(fraction * delta) / math.sin(delta)
    phi1 = lat1 * 0.0174533
    phi2 = lat2 * 0.0174533
    lambda1 = lon1 * 0.0174533
    lambda2 = lon2 * 0.0174533
    x = a * math.cos(phi1)*math.cos(lambda1) + b*math.cos(phi2)*math.cos(lambda2)
    y = a * math.cos(phi1) * math.sin(lambda1) + b * math.cos(phi2)*math.sin(lambda2)
    z = a * math.sin(phi1) + b * math.sin(phi2)
    phi_i = math.atan2(z, math.sqrt(x*x + y*y))
    lambda_i = math.atan2(y, x)
    return {"lat":phi_i * 57.2958, "lon":lambda_i * 57.2958}


def weatherCall(lon, lat, weatherKey):
    URL = "http://api.worldweatheronline.com/premium/v1/marine.ashx?key=" + weatherKey + "&format=json&q=" + str(
        lat) + "," + str(lon)
    response = requests.post(URL)
    return response.text


def getKeys():
    return json.load(open('/home/eli/PycharmProjects/design/API_keys.json'))['keys']


def fetchGtsreatCircleWeather(wypts, weatherKey):
    file = open('weatherData', 'a')
    numPts = len(wypts['lats'])
    for i in range(0,numPts):
        lat = wypts['lats'][i]
        lon = wypts['lons'][i]
        URL = "http://api.worldweatheronline.com/premium/v1/marine.ashx?key=" + weatherKey + "&format=json&q=" + str(lat) + "," + str(lon)
        response = requests.post(URL)
        file.write(response.text)

    file.close()

keys = getKeys()
weatherKey = keys['weather']
wypts = waypoints(42.836329, -70.973406,52.642808, -9.469758, 100.0)
print weatherCall(-40.5, 47, weatherKey)


