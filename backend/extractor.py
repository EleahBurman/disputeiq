import os
import anthropic
import json
from dotenv import load_dotenv
from models import ExtractedEvidence, DisputeReason

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_evidence(text: str) -> ExtractedEvidence:
    prompt = f"""You are a dispute analyst. Extract structured information from the following dispute evidence text.

Return ONLY a JSON object with these exact fields:
- merchant_name: string or null
- transaction_amount: number or null
- transaction_date: string (YYYY-MM-DD format) or null
- dispute_reason: one of ["item_not_received", "item_not_as_described", "unauthorized_charge", "duplicate_charge", "subscription_cancelled", "other"] or null
- customer_claim: a one sentence summary of the customer's claim or null
- evidence_strength: integer 1-10 rating how strong the evidence is (10 = very strong) or null

Dispute evidence:
{text}

Return only the JSON object, no explanation, no markdown."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    data = json.loads(raw)

    # Map dispute_reason string to enum safely
    if data.get("dispute_reason"):
        try:
            data["dispute_reason"] = DisputeReason(data["dispute_reason"])
        except ValueError:
            data["dispute_reason"] = DisputeReason.other

    return ExtractedEvidence(**data)