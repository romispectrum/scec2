from datetime import datetime, timezone
from ics import Calendar, Event
import tempfile
from pydantic import BaseModel, Field


class EventModel(BaseModel):
    properties: dict = Field(description="Event properties like UID, summary, start and end")

    @property
    def uid(self):
        return self.properties.get("UID")

    @property
    def summary(self):
        return self.properties.get("SUMMARY")

    @property
    def description(self):
        return self.properties.get("DESCRIPTION", "")

    @property
    def location(self):
        return self.properties.get("LOCATION", "")

    @property
    def start(self):
        return datetime.fromisoformat(self.properties.get("DTSTART"))

    @property
    def end(self):
        return datetime.fromisoformat(self.properties.get("DTEND"))


def create_ics_event(event_data: dict) -> Event:
    """
    Create an .ics event from a JSON dictionary.
    """
    event = Event()
    event.uid = event_data.get("UID")
    event.name = event_data.get("SUMMARY")
    event.description = event_data.get("DESCRIPTION", "")
    event.location = event_data.get("LOCATION", "")

    if "DTSTART" in event_data:
        event.begin = datetime.fromisoformat(event_data["DTSTART"]).astimezone(timezone.utc)
    if "DTEND" in event_data:
        event.end = datetime.fromisoformat(event_data["DTEND"]).astimezone(timezone.utc)

    if "DTSTAMP" in event_data:
        event.created = datetime.fromisoformat(event_data["DTSTAMP"]).astimezone(timezone.utc)

    return event


def save_event_to_temp_file(calendar: Calendar) -> str:
    """
    Save the calendar containing the event to a temporary .ics file.
    """
    with tempfile.NamedTemporaryFile(suffix=".ics", delete=False, mode='w', encoding='utf-8') as tmp:
        tmp.write(str(calendar))
        tmp.flush()
        return tmp.name
