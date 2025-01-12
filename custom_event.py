from datetime import datetime

from pydantic import BaseModel, Field


class CustomEvent(BaseModel):
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
