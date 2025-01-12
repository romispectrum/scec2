from ics import Event
from datetime import datetime, timezone

def create_ics_event(json_data: dict) -> Event:
    """
    Create an .ics event from a JSON dictionary.

    :param json_data: A dictionary containing event data.
    :return: A string containing the .ics content.
    """
    # Create an Event object
    event = Event()

    # Map JSON fields to the Event object
    event.uid = json_data.get("UID")
    event.name = json_data.get("SUMMARY")
    event.description = json_data.get("DESCRIPTION", "")
    event.location = json_data.get("LOCATION", "")
    event.begin = datetime.strptime(json_data.get("DTSTART"), '%Y%m%dT%H%M%S')
    event.end = datetime.strptime(json_data.get("DTEND"), '%Y%m%dT%H%M%S')
    event.created = format_iso8601_with_fractional_seconds(json_data.get("DTSTAMP"), "%Y%m%dT%H%M%S.%fZ") if "DTSTAMP" in json_data else None

    return event


def format_iso8601_with_fractional_seconds(date_str, input_format='%Y%m%dT%H%M%S.%fZ'):
    """
    Parses and formats an ISO 8601 date string with fractional seconds.
    Args:
        date_str (str): The date string to be converted.
        input_format (str): The format of the input date string.
    Returns:
        str: ISO 8601 formatted date string with UTC timezone.
    """
    try:
        # Parse the input date string
        dt = datetime.strptime(date_str, input_format)
        # Assign UTC timezone
        dt = dt.replace(tzinfo=timezone.utc)
        return dt.isoformat()
    except ValueError as e:
        return f"Error: {e}"
