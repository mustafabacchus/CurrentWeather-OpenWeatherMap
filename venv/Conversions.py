import tzlocal
from datetime import datetime
from pytz import timezone


def utc_2_local(time_utc):
    # Format for display
    print_format = '%Y-%m-%d %I:%M%p %Z'
    # Get local timezone
    local_zone = str(tzlocal.get_localzone())
    # Prepare incoming format
    from_time = datetime.strptime(time_utc, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone('UTC'))

    # Define zone for UTC time
    utc = from_time.astimezone(timezone('UTC'))

    # Convert to local timezone
    to_time = utc.astimezone(timezone(local_zone))
    result = to_time.strftime(print_format)
    return result


def format_utc(time):
    print_format = '%Y-%m-%d %H:%M %Z'
    original_time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone('UTC'))
    utc = original_time.astimezone(timezone('UTC'))
    result = utc.strftime(print_format)
    return result


def meters_2_miles(meters):
    miles = meters / 1609.344
    return miles


def mps_2_mph(mps):
    mph = mps * 2.23694
    return mph


def hpa_2_inhg(hpa):
    inhg = hpa * 0.029529983071445
    return inhg


def mm_2_in(mm):
    in_ = mm * 0.0393701
    return in_
