# CRM Webhook Integration Demo (Portfolio Sample)

A small, independently runnable Python example of an integration pattern used for CRM and fundraising systems. **This is a new demonstration project, not a production customer implementation or an official Virtuous integration.** No external service credentials are required.

## What it demonstrates
- Validates signed incoming webhook events with HMAC-SHA256
- Normalizes gift events into a canonical donation record
- Prevents duplicate processing with an idempotency key
- Rejects malformed amounts and missing donor IDs
- Simulates delivery into a CRM using a local in-memory adapter
- Includes unit tests for signature validation and replay protection

## Run
Requires Python 3.10+. No dependencies.

```bash
python -m unittest discover -s samples/crm-webhook-demo -p "test_*.py"
python samples/crm-webhook-demo/demo.py
```

## Production considerations
Replace the in-memory adapter and idempotency set with a transactional database and persistent outbox. Store signing secrets in a secret manager, add retries with bounded exponential backoff and dead-letter handling, audit trails, privacy controls, rate limits and structured telemetry. Use actual CRM API mapping, authentication and donor consent requirements.

## Scope
This sample illustrates a design approach; it has not been deployed to a fundraising CRM.
