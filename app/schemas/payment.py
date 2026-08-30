from pydantic import BaseModel, Field
from typing import Optional

class MoMoPayer(BaseModel):
    partyIdType: Optional[str] = Field(default="MSISDN", examples=["MSISDN"])
    partyId: Optional[str] = Field(default=None, examples=["46733123453"])

class MoMoCallbackPayload(BaseModel):
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