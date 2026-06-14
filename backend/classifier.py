import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import pandas as pd
from models import ExtractedEvidence, DisputeOutcome

# Generate synthetic training data
def generate_training_data(n=500):
    np.random.seed(42)
    data = []

    for _ in range(n):
        evidence_strength = np.random.randint(1, 11)
        amount = round(np.random.uniform(10, 2000), 2)
        reason = np.random.choice([
            "item_not_received",
            "item_not_as_described",
            "unauthorized_charge",
            "duplicate_charge",
            "subscription_cancelled",
            "other"
        ])

        # Realistic outcome logic
        if evidence_strength >= 7:
            outcome = "approved"
        elif evidence_strength <= 3:
            outcome = "denied"
        else:
            if reason == "unauthorized_charge":
                outcome = "approved"
            elif reason == "other":
                outcome = "denied"
            else:
                outcome = "needs_review"

        data.append({
            "evidence_strength": evidence_strength,
            "amount": amount,
            "reason": reason,
            "outcome": outcome
        })

    return pd.DataFrame(data)


def train_model():
    df = generate_training_data()

    reason_encoder = LabelEncoder()
    df["reason_encoded"] = reason_encoder.fit_transform(df["reason"])

    outcome_encoder = LabelEncoder()
    df["outcome_encoded"] = outcome_encoder.fit_transform(df["outcome"])

    X = df[["evidence_strength", "amount", "reason_encoded"]]
    y = df["outcome_encoded"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=outcome_encoder.classes_))

    return model, reason_encoder, outcome_encoder


# Train once on import
model, reason_encoder, outcome_encoder = train_model()


def predict_outcome(evidence: ExtractedEvidence) -> tuple[DisputeOutcome, float]:
    reason = evidence.dispute_reason.value if evidence.dispute_reason else "other"
    amount = evidence.transaction_amount or 0.0
    strength = evidence.evidence_strength or 5

    try:
        reason_encoded = reason_encoder.transform([reason])[0]
    except ValueError:
        reason_encoded = reason_encoder.transform(["other"])[0]

    X = pd.DataFrame([{
        "evidence_strength": strength,
        "amount": amount,
        "reason_encoded": reason_encoded
    }])

    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    confidence = round(float(max(proba)), 2)
    outcome_str = outcome_encoder.inverse_transform([pred])[0]

    return DisputeOutcome(outcome_str), confidence