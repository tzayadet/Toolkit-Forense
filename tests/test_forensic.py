import hashlib
import tempfile
import unittest
from pathlib import Path

from forensic import hash_file, scan_dir


class ForensicTests(unittest.TestCase):
    def test_hash_file_returns_sha256(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "evidence.bin"
            path.write_bytes(b"evidence")

            self.assertEqual(hash_file(path), hashlib.sha256(b"evidence").hexdigest())

    def test_scan_dir_records_metadata_and_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "one.txt").write_text("alpha", encoding="utf-8")
            (root / "two.pdf").write_bytes(b"beta")

            records = scan_dir(root)

            self.assertEqual(len(records), 2)
            self.assertTrue(all("sha256" in record for record in records))
            self.assertTrue(all("modified_utc" in record for record in records))

    def test_extension_filter_is_applied(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "one.txt").write_text("alpha", encoding="utf-8")
            (root / "two.pdf").write_bytes(b"beta")

            records = scan_dir(root, "pdf")

            self.assertEqual(len(records), 1)
            self.assertEqual(Path(records[0]["path"]).suffix, ".pdf")


if __name__ == "__main__":
    unittest.main()
