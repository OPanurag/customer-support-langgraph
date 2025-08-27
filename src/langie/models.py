from pydantic import BaseModel, Field
from typing import Optional

class InputPayload(BaseModel):
    customer_name: str
    email: str
    query: str
    priority: Optional[str] = Field(default="Normal")
    ticket_id: Optional[str] = None
