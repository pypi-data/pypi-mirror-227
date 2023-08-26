from datetime import datetime


def validate_locations(data):
    if not isinstance(data, dict):
        raise ValueError("Invalid locations, locations must be a dictionary")

    for city, districts in data.items():
        # Check if city and districts are strings and if city starts with an uppercase letter
        if not isinstance(city, str) or " " in city:
            raise ValueError("Invalid city, city must be a string" + city)

        # Check if districts is a list
        if not isinstance(districts, list):
            raise ValueError("Invalid districts, districts must be a list")

        for district in districts:
            # Check if each district is a string and starts with an uppercase letter
            if not isinstance(district, str) or "  " in district:
                raise ValueError("Invalid district, district must be a string: " + district)

    return True


def validate_date(dates):
    if not isinstance(dates, (list, set)):
        raise ValueError("Invalid dates, dates must be a list or set")

    for date in dates:
        if not isinstance(date, str):
            raise ValueError("Invalid date, date must be strings: " + date)

    try:
        for date in dates:
            datetime.strptime(date, '%d.%m.%Y %H:%M')
        return True
    except ValueError:
        raise ValueError("Invalid date format, date must be in the format of dd.mm.yyyy hh:mm")


def validate_params(params):
    valid_elements = {"PM10", "PM 2.5", "SO2", "CO", "NO2", "NOX", "NO", "O3"}

    if params:
        if not set(params).difference(valid_elements) == set():
            raise ValueError("Invalid params, params must be a list of strings: " + str(valid_elements))
    # Convert the input list to a set and check if its difference with the valid_elements set is empty
    return True
