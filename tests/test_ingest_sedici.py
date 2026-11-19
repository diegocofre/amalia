import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.ingest_sedici import (MANIFEST, admitted, get_pdf, load_manifest,
                                 normalize, run_batch, sha, valid_document)


class SediciTests(unittest.TestCase):
    def setUp(self):
        self.manifest = load_manifest(MANIFEST.read_bytes())
        self.doc = self.manifest["documents"][0]

    def test_restricted_source_rejected(self):
        self.assertFalse(valid_document(dict(self.doc, license="CC-BY-NC-4.0")))
        self.assertFalse(valid_document(dict(self.doc, acquisition="pending")))
        self.assertFalse(valid_document(dict(self.doc, pdf_url="https://example.org/file.pdf")))

    def test_hash_bound_admission(self):
        self.assertFalse(admitted(self.doc, "raw", "text"))
        approved = dict(self.doc, training_approval={
            "approved": True, "reviewer": "test", "review_date": "2026-11-19",
            "rights_and_privacy_notes": "synthetic fixture",
            "raw_sha256": "raw", "text_sha256": "text"})
        self.assertTrue(admitted(approved, "raw", "text"))
        self.assertFalse(admitted(approved, "changed", "text"))
        self.assertFalse(admitted(approved, "raw", "changed"))

    def test_cache_resumes_without_network(self):
        with tempfile.TemporaryDirectory() as folder:
            workspace = Path(folder)
            with patch("tools.ingest_sedici.fetch", return_value=b"%PDF-fixture") as fetch:
                self.assertEqual(get_pdf(self.doc, workspace), (b"%PDF-fixture", False))
                self.assertEqual(get_pdf(self.doc, workspace), (b"%PDF-fixture", True))
                self.assertEqual(fetch.call_count, 1)

    def test_redaction(self):
        self.assertEqual(normalize("Texto \r\n prueba@example.org"), ("Texto\n [EMAIL]", 1))

    def test_pending_and_duplicate_not_exported(self):
        pending, first, second = self.manifest["documents"]
        def fake(doc, *_):
            row = {"id": doc["id"], "text_sha256": "same", "text": "fixture"}
            if doc is pending:
                return {"id": doc["id"], "status": "pending_review"}, None
            return {"id": doc["id"], "status": "admitted"}, row
        with tempfile.TemporaryDirectory() as folder:
            workspace = Path(folder)
            with patch("tools.ingest_sedici.process", side_effect=fake):
                records, rows, digest = run_batch(self.manifest, workspace, {})
                self.assertEqual([r["status"] for r in records], ["pending_review", "admitted", "duplicate"])
                self.assertEqual(len(rows), 1)
                self.assertEqual(run_batch(self.manifest, workspace, {})[2], digest)
                data = (workspace / "corpus/sedici.jsonl").read_bytes()
                self.assertEqual(sha(data), digest)
                self.assertEqual(len(data.splitlines()), 1)
                self.assertEqual(json.loads(data)["id"], first["id"])


if __name__ == "__main__":
    unittest.main()
