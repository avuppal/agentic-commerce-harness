# Data models for user behavioral telemetry

from pydantic import BaseModel
from datetime import datetime

class TelemetryEvent(BaseModel):
    """Base class for all telemetry events."""
    timestamp: datetime
    user_id: str
    session_id: str
    event_type: str
