import requests,json,math
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from datetime import date


def today():
    now = date.today()
    return str(now.year) + '-' + str(now.month) + '-' + str(now.day)


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


def fetchGreatCircleWeather(wypts, weatherKey):
    file = open('weatherData', 'a')
    numPts = len(wypts['lats'])
    for i in range(0,numPts):
        lat = wypts['lats'][i]
        lon = wypts['lons'][i]
        URL = "http://api.worldweatheronline.com/premium/v1/marine.ashx?key=" + weatherKey + "&format=json&q=" + str(lat) + "," + str(lon)
        response = requests.post(URL)
        file.write(response.text)

    file.close()


def fetchGreatCircleWeatherToDict(wypts, weatherKey):
    output = {}
    numPts = len(wypts['lats'])
    for i in range(0, numPts):
        lat = wypts['lats'][i]
        lon = wypts['lons'][i]
        URL = "http://api.worldweatheronline.com/premium/v1/marine.ashx?key=" + weatherKey + "&format=json&q=" + str(
            lat) + "," + str(lon)
        response = requests.post(URL)
        key = str(lat) + ',' + str(lon)
        output[key] = textToDict(response.text)

    return output


def bearing(lat1, lon1, lat2, lon2):
    phi1 = lat1 * 0.0174533
    phi2 = lat2 * 0.0174533
    lambda1 = lon1 * 0.0174533
    lambda2 = lon2 * 0.0174533
    y = math.sin(lambda2 - lambda1) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1)*math.cos(phi2)*math.cos(lambda2-lambda1)
    bearing = math.atan2(y,x) * 57.2958
    return bearing


def textToDict(text):
    data = dict(bf.data(fromstring(text)))
    nestedData = data['data']['weather'][0]
    output = {}
    date = nestedData['date']['$']
    tmp = {}
    for i in nestedData['hourly']:
        tmp[str(i['time']['$']).zfill(4)] = {'WindGustKmph':i['WindGustKmph']['$'], 'pressure':i['pressure']['$'], 'winddirDegree':i['winddirDegree']['$'], 'windspeedKmph':i['windspeedKmph']['$']}
    output[date] = tmp
    return output


def getTodaysWeather():
    keys = getKeys()
    weatherKey = keys['weather']
    wypts = waypoints(42.836329, -70.973406, 52.642808, -9.469758, 100.0)
    result = fetchGreatCircleWeatherToDict(wypts, weatherKey)
    jsonOut = json.dumps(result)
    f = open(today(), 'w')
    f.write(jsonOut)
    f.close()

def weatherToWindComponents(weatherDataFile):
    dict = json.load(open(weatherDataFile))
    date = weatherDataFile.split('.')[0]
    for i in dict:
        lat = i.split(',')[0]
        lon = i.split(',')[1]
        brng = bearing(float(lat),float(lon),52.642808, -9.469758)
        for j in dict[i][date]:
            dir = (float(dict[i][date][j]['winddirDegree']) + 180) % 360
            spd = float(dict[i][date][j]['windspeedKmph']) * 0.277777777
            theta = brng - dir
            tailwind = spd * math.cos(theta * 0.0174533)
            crosswind = math.sqrt((spd * spd) - (tailwind * tailwind))
            print 'at time = ' + str(j)
            print 'wind speed = ' + str(spd) + ', at ' + str(dir) + ' (flippd by 180)'
            print 'bearing = ' + str(brng)
            print 'tailwind = ' + str(tailwind) + ', crosswind = ' + str(crosswind)
            print '--------------------------'


weatherToWindComponents('2017-12-17.json')


#print result
#response = weatherCall(-40.5, 47, weatherKey)
#print textToDict(response)


