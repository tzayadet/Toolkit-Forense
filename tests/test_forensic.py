import hashlib
import tempfile
import unittest
from pathlib import Path

from forensic_inventory import hash_file, scan_dir


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

    def test_hash_file_rejects_symbolic_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            outside = Path(tmp) / "outside.txt"
            outside.write_text("outside evidence", encoding="utf-8")
            link = Path(tmp) / "linked.txt"
            try:
                link.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("Symbolic links are not available in this environment")

            with self.assertRaisesRegex(ValueError, "symbolic link"):
                hash_file(link)

    def test_scan_skips_symbolic_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "evidence"
            root.mkdir()
            outside = Path(tmp) / "outside.txt"
            outside.write_text("outside evidence", encoding="utf-8")
            link = root / "linked.txt"
            try:
                link.symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("Symbolic links are not available in this environment")

            self.assertEqual(scan_dir(root), [])

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
