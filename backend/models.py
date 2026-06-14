from pydantic import BaseModel
from typing import Optional
from enum import Enum

class DisputeReason(str, Enum):
    item_not_received = "item_not_received"
    item_not_as_described = "item_not_as_described"
    unauthorized_charge = "unauthorized_charge"
    duplicate_charge = "duplicate_charge"
    subscription_cancelled = "subscription_cancelled"
    other = "other"

class DisputeOutcome(str, Enum):
    approved = "approved"
    denied = "denied"
    needs_review = "needs_review"

class ExtractedEvidence(BaseModel):
    merchant_name: Optional[str] = None
    transaction_amount: Optional[float] = None
    transaction_date: Optional[str] = None
    dispute_reason: Optional[DisputeReason] = None
    customer_claim: Optional[str] = None
    evidence_strength: Optional[int] = None  # 1-10, Claude's assessment

class DisputeResult(BaseModel):
    extracted: ExtractedEvidence
    outcome: DisputeOutcome
    confidence: float
    explanation: str