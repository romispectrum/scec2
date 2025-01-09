from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CustomEvent(BaseModel):
    uid: str = Field(description="Unique identifier for the event")
    summary: str = Field(description="Summary or title of the event")
    description: str = Field(description="Detailed description of the event (default to empty string)")
    location: str = Field(description="Location of the event (default to empty string)")
    start: datetime = Field(description="Start time of the event")
    end: datetime = Field(description="End time of the event")
    attendees: List[str] = Field(default_factory=list, description="List of attendees (email addresses)")