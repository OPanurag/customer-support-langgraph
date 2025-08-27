from pydantic import BaseModel, Field, ValidationError
from typing import Optional

class InputPayload(BaseModel):
    customer_name: str
    email: str
    query: str
    priority: Optional[str] = Field("Normal")
    ticket_id: Optional[str] = None
