import urllib2 as urllib
import xml.etree.ElementTree as ET
import Credentials
from Conversions import *


def get_weather(locality):
    # Construct URL
    base = 'http://api.openweathermap.org/data/2.5/weather?'
    mode = 'mode=xml'
    accuracy = 'type=like'
    units = 'units=imperial'
    # Check for zip or city
    try:
        # Append zip syntax
        int(locality)
        city = 'zip=' + locality
    except ValueError:
        # Append city syntax
        city = 'q=' + locality
    country = 'us'
    location = ','.join([city, country])
    appid = 'appid=' + Credentials.appid()
    link = '&'.join([base, mode, accuracy, units, location, appid])
    # Open link
    conn = urllib.urlopen(link)
    # Save link data
    dump = conn.read()
    # Close link
    conn.close()
    # Convert link data to ElementTree
    weather = ET.fromstring(dump)

    current_weather = {}

    def store(attrib, val):
        current_weather[attrib] = val

    # City
    for info in weather.findall('city'):
        city_id = info.get('id')
        name = info.get('name')
        store('city', {'id': city_id, 'name': name.upper()})

    # Coords
    for info in weather.findall('city/coord'):
        lon = float(info.get('lon'))
        lat = float(info.get('lat'))
        store('coord', {'lon': lon, 'lat': lat})

    # Sunrise/set
    for info in weather.findall('city/sun'):
        value_rise = info.get('rise')
        rise = ' '.join([value_rise.split('T')[0], value_rise.split('T')[1]])
        rise = format_utc(rise)
        value_set = info.get('set')
        set_ = ' '.join([value_set.split('T')[0], value_set.split('T')[1]])
        set_ = format_utc(set_)
        store('sun', {'rise': rise, 'set': set_})

    # Temperature
    for info in weather.findall('temperature'):
        current = round(float(info.get('value')), 2)
        hi = round(float(info.get('max')), 2)
        lo = round(float(info.get('min')), 2)
        unit = info.get('unit')
        store('temp', {'current': current, 'hi': hi, 'lo': lo, 'unit': unit})

    # Humidity
    for info in weather.findall('humidity'):
        value = float(info.get('value'))
        unit = info.get('unit')
        store('humidity', {'value': value, 'unit': unit})

    # Pressure
    for info in weather.findall('pressure'):
        value = float(info.get('value'))
        value = round(hpa_2_inhg(value), 2)
        unit = 'in/hg'
        store('pressure', {'value': value, 'unit': unit})

    # Wind speed
    for info in weather.findall('wind/speed'):
        speed = float(info.get('value'))
        speed = int(round(mps_2_mph(speed)))
        unit = 'mph'
        name = info.get('name')
        store('wind-speed', {'speed': speed, 'unit': unit, 'name': name})

    # Wind direction
    for info in weather.findall('wind/direction'):
        degrees = float(info.get('value'))
        code = info.get('code')
        direction = info.get('name')
        store('wind-direct', {'degrees': degrees, 'code': code, 'direction': direction})

    # Clouds
    for info in weather.findall('clouds'):
        value = float(info.get('value'))
        name = info.get('name')
        store('clouds', {'value': value, 'name': name.title()})

    # Visibility
    for info in weather.findall('visibility'):
        value = float(info.get('value'))
        value = int(round(meters_2_miles(value)))
        unit = 'mi'
        store('visibility', {'value': value, 'unit': unit})

    # Precipitation
    for info in weather.findall('precipitation'):
        try:
            value = float(info.get('value'))
            value = round(mm_2_in(value), 2)
        except TypeError:
            value = 0
        unit = 'in'
        mode = info.get('mode')
        if mode == 'no':
            mode = 'none'
        store('precipitation', {'value': value, 'unit': unit, 'mode': mode.title()})

    # Current weather
    for info in weather.findall('weather'):
        description = info.get('value')
        store('weather', {'description': description.title()})

    # Last update
    for info in weather.findall('lastupdate'):
        value = info.get('value')
        date = ' '.join([value.split('T')[0], value.split('T')[1]])
        date = utc_2_local(date)
        store('last-update', {'date': date})
    return current_weather
