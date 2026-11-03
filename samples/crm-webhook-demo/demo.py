"""Runnable CRM donation webhook integration demonstration."""
import hashlib
import hmac
import json
from decimal import Decimal, InvalidOperation

def sign(raw: bytes, secret: str) -> str:
    return hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()

def ingest(raw: bytes, signature: str, secret: str, processed: set, sink: list) -> bool:
    if not hmac.compare_digest(sign(raw, secret), signature):
        raise ValueError("invalid webhook signature")
    event = json.loads(raw)
    if event.get("type") != "gift.created":
        raise ValueError("unsupported event type")
    event_id = str(event.get("id", ""))
    donor_id = str(event.get("donor_id", ""))
    if not event_id or not donor_id:
        raise ValueError("missing event or donor ID")
    try:
        amount = Decimal(str(event["amount"]))
    except (KeyError, InvalidOperation) as exc:
        raise ValueError("invalid amount") from exc
    if not amount.is_finite() or amount <= 0:
        raise ValueError("amount must be positive and finite")
    if event_id in processed:
        return False
    # Demonstration only: a production implementation would atomically persist
    # event idempotency and an outbound delivery record.
    sink.append({"external_id": event_id, "contact_external_id": donor_id, "amount": str(amount), "currency": "USD"})
    processed.add(event_id)
    return True

if __name__ == "__main__":
    secret = "local-demo-secret"
    raw = json.dumps({"id":"evt-001","type":"gift.created","donor_id":"donor-123","amount":"25.00"}).encode()
    records, processed = [], set()
    print("first delivery:", ingest(raw, sign(raw, secret), secret, processed, records))
    print("duplicate delivery:", ingest(raw, sign(raw, secret), secret, processed, records))
    print("CRM-ready records:", records)
