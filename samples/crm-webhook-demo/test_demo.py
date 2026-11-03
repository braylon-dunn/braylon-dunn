import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("crm_demo", Path(__file__).with_name("demo.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.secret = "test-secret"
        self.raw = json.dumps({"id":"evt-1","type":"gift.created","donor_id":"d-1","amount":"12.50"}).encode()
        self.processed, self.records = set(), []

    def test_success_and_idempotency(self):
        sig = mod.sign(self.raw, self.secret)
        self.assertTrue(mod.ingest(self.raw, sig, self.secret, self.processed, self.records))
        self.assertFalse(mod.ingest(self.raw, sig, self.secret, self.processed, self.records))
        self.assertEqual(len(self.records), 1)

    def test_bad_signature(self):
        with self.assertRaises(ValueError):
            mod.ingest(self.raw, "incorrect", self.secret, self.processed, self.records)

    def test_invalid_amount(self):
        raw = json.dumps({"id":"evt-2","type":"gift.created","donor_id":"d-1","amount":"-5"}).encode()
        with self.assertRaises(ValueError):
            mod.ingest(raw, mod.sign(raw, self.secret), self.secret, self.processed, self.records)

if __name__ == "__main__":
    unittest.main()
