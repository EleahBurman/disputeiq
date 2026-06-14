from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import PyPDF2
import io

from models import DisputeResult, ExtractedEvidence
from extractor import extract_evidence
from classifier import predict_outcome

app = FastAPI(title="DisputeIQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://disputeiq-zeta.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

@app.get("/")
def health_check():
    return {"status": "DisputeIQ API is running"}

@app.post("/analyze", response_model=DisputeResult)
async def analyze_dispute(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    # Get text from either the form field or the uploaded PDF
    if file:
        contents = await file.read()
        dispute_text = extract_text_from_pdf(contents)
    elif text:
        dispute_text = text
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Provide either text or a PDF file")

    # Run the pipeline
    extracted = extract_evidence(dispute_text)
    outcome, confidence = predict_outcome(extracted)

    return DisputeResult(
        extracted=extracted,
        outcome=outcome,
        confidence=confidence,
        explanation=f"Based on evidence strength of {extracted.evidence_strength}/10 and dispute reason '{extracted.dispute_reason.value.replace('_', ' ') if extracted.dispute_reason else 'unknown'}'.  This dispute was classified as {outcome.value.replace('_', ' ')}."
    )