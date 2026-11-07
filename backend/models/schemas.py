
from pydantic import BaseModel, ConfigDict


class TicketResponse(BaseModel):
    ticket_id: str
    customer: str
    issue: str
    category: str
    priority: str
    status: str
    order_id: str
    amount: float

    model_config = ConfigDict(from_attributes=True)


class TicketStatusUpdate(BaseModel):
    status: str

class TicketCreate(BaseModel):
    customer: str
    issue: str
    category: str
    priority: str
    order_id: str
    amount: float


class TicketClassificationRequest(BaseModel):
    customer: str
    issue: str
