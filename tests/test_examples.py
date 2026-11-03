import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path
from shutil import copyfile

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pilot = load("pilot", "examples/arxiv-pilot/verify_pilot.py")
record = load("record", "examples/retained-record/retained_record.py")
digest = load("digest", "examples/arxiv-pilot/arxiv_digest.py")


class ExamplesTest(unittest.TestCase):
    def test_retained_evidence(self):
        self.assertEqual(len(pilot.verify()["program_only"]), 7)

    def test_modified_original_program_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            for name in ("arxiv_digest.py", "agent-ids.txt", "program-ids.txt", "runs.json"):
                copyfile(ROOT / "examples/arxiv-pilot" / name, destination / name)
            with (destination / "arxiv_digest.py").open("a") as stream:
                stream.write("\n# Changed program\n")
            with self.assertRaisesRegex(ValueError, "program hash mismatch"):
                pilot.verify(destination)

    def test_month_boundaries(self):
        records = [
            {"id": "before", "published": "2026-08-31T23:59:59Z", "title": "a"},
            {"id": "first", "published": "2026-09-01T00:00:00Z", "title": "b"},
            {"id": "last", "published": "2026-09-30T23:59:59Z", "title": "c"},
            {"id": "after", "published": "2026-10-01T00:00:00Z", "title": "d"},
        ]
        self.assertEqual([r["id"] for r in record.select(records, "2026-09")], ["first", "last"])

    def test_time_zone_conversion(self):
        rows = [{"id": "boundary", "published": "2026-08-31T22:04:00-04:00", "title": "a"}]
        self.assertEqual(len(record.select(rows, "2026-09")), 1)

    def test_invalid_inputs_are_rejected(self):
        valid = {"id": "one", "published": "2026-09-30T12:00:00Z", "title": "a"}
        for field, value in [("published", "2026-09-30T12:00:00"), ("title", 42)]:
            invalid = dict(valid, **{field: value})
            with self.assertRaises(ValueError):
                record.select([invalid], "2026-09")
        with self.assertRaises(ValueError):
            record.select([valid, valid], "2026-09")

    def test_record_is_deterministic_and_hash_detects_change(self):
        first, second = record.run(), record.run()
        self.assertEqual(first, second)
        changed = copy.deepcopy(first["selected"])
        changed[0]["title"] = "Different content"
        self.assertNotEqual(record.sha256(record.canonical_bytes(changed)), first["output_sha256"])

    def test_original_query_includes_last_day_and_leap_year(self):
        self.assertIn("202609302359", digest.month_query("2026-09"))
        self.assertIn("202402292359", digest.month_query("2024-02"))


if __name__ == "__main__":
    unittest.main()
