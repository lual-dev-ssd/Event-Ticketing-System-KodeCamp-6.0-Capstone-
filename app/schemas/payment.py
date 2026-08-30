from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID


class MoMoInitiateRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    event_id:UUID = Field(..., description="ID of the event to purchase a ticket for")
    phone_number:str = Field(..., description="MoMo phone number (e.g. 46733123456)")


class MoMoPayer(BaseModel):
    model_config = ConfigDict(extra="ignore")

    partyIdType: Optional[str] = Field(default="MSISDN", examples=["MSISDN"])
    partyId: Optional[str] = Field(default=None, examples=["46733123453"])

class MoMoCallbackPayload(BaseModel):
    model_config = ConfigDict(extra="ignore")

    externalId: str = Field(
        ..., 
        description="Ticket ID (UUID) to update in DB",
        examples=["b93103d8-b732-431a-b483-afec5a4a27f1"]
    )
    status: str = Field(
        ..., 
        description="SUCCESSFUL or FAILED",
        examples=["SUCCESSFUL"]
    )
    financialTransactionId: Optional[str] = Field(default=None, examples=["123456789"])
    amount: Optional[str] = Field(default=None, examples=["10.00"])
    currency: Optional[str] = Field(default=None, examples=["EUR"])
    payer: Optional[MoMoPayer] = None
    reason: Optional[str] = Field(default=None, examples=["NOT_ENOUGH_FUNDS"])