import OpenWeather
from urllib2 import HTTPError, URLError
from prettytable import PrettyTable as PT

try:
    locality = raw_input('Enter a Zip or City: ')
    current_weather = OpenWeather.get_weather(locality)

    def get(attrib1, attrib2):
        return current_weather[attrib1][attrib2]

    # Last Update
    date = get('last-update', 'date')
    update = ' '.join(['Last Station Update:', date])

    # COLUMN 1

    # City
    name = get('city', 'name')
    # Current
    curr = str(get('temp', 'current'))
    locality_curr = ': '.join([name, curr])

    # Temp
    hi = 'High: ' + str(get('temp', 'hi'))
    lo = 'Low: ' + str(get('temp', 'lo'))

    # Humidity
    val = str(get('humidity', 'value'))
    unit = get('humidity', 'unit')
    humid = ' '.join(['Humidity:', val, unit])

    # Pressure
    val = str(get('pressure', 'value'))
    unit = get('pressure', 'unit')
    pressure = ' '.join(['Pressure:', val, unit])

    # Precipitation
    val = str(get('precipitation', 'value'))
    unit = get('precipitation', 'unit')
    mode = get('precipitation', 'mode')
    precip_type = 'Precipitation: '
    precip = ' '.join([mode + ', ', val, unit])

    # COLUMN 2

    # Weather
    weather = get('weather', 'description')

    # Clouds
    clouds = 'Clouds: ' + get('clouds', 'name')

    # Visibility
    val = str(get('visibility', 'value'))
    unit = get('visibility', 'unit')
    visibility = ' '.join(['Visibility:', val, unit])

    # Wind
    code = get('wind-direct', 'code')
    degrees = '(' + str(get('wind-direct', 'degrees')) + ')'
    speed = str(get('wind-speed', 'speed'))
    unit = get('wind-speed', 'unit')
    name = get('wind-speed', 'name')
    wind_type = 'Wind: ' + name
    wind = ' '.join([code, degrees, speed, unit])

    # Coords
    lon = str(get('coord', 'lon'))
    lat = str(get('coord', 'lat'))
    coords = 'Geo-Coords: ' + ', '.join([lon, lat])

    # Sun
    rise = 'Sunrise: ' + get('sun', 'rise')
    set_ = 'Sunset: ' + get('sun', 'set')

    table = PT()
    table.add_column(locality_curr, [hi, lo, '', humid, pressure, '', precip_type, precip, ''])
    table.add_column(weather, [clouds, visibility, '', wind_type, wind, '',  coords, rise, set_])
    print ' ' + update
    print table
except HTTPError:
    print 'Data Not Found.'
except URLError:
    print 'No Connection.'
