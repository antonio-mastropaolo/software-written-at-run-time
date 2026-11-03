"""Illustrate a fixed UTC filter and a hash-linked record using synthetic data."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

REQUEST = {"month": "2026-09", "time_zone": "UTC", "operation": "select_by_published_month"}


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def select(records, month):
    year, month_number = map(int, month.split("-"))
    start = datetime(year, month_number, 1, tzinfo=timezone.utc)
    next_year, next_month = (year + 1, 1) if month_number == 12 else (year, month_number + 1)
    end = datetime(next_year, next_month, 1, tzinfo=timezone.utc)
    if not isinstance(records, list):
        raise ValueError("records must be a list")
    selected, seen = [], set()
    for record in records:
        if not isinstance(record, dict) or set(record) != {"id", "published", "title"}:
            raise ValueError("Each record must contain exactly id, published, and title")
        if any(not isinstance(value, str) or not value for value in record.values()):
            raise ValueError("Record fields must be nonempty strings")
        if record["id"] in seen:
            raise ValueError("Duplicate identifier")
        seen.add(record["id"])
        published = datetime.fromisoformat(record["published"].replace("Z", "+00:00"))
        if published.tzinfo is None:
            raise ValueError("Submission timestamps must include a time zone")
        if start <= published.astimezone(timezone.utc) < end:
            selected.append(record)
    return sorted(selected, key=lambda record: record["id"])


def run(fixture_path=None):
    path = Path(fixture_path) if fixture_path is not None else Path(__file__).with_name("fixture.json")
    input_bytes = path.read_bytes()
    selected = select(json.loads(input_bytes)["records"], REQUEST["month"])
    return {
        "kind": "illustrative execution record",
        "evidence": "synthetic fixture; not an observation from the October pilot",
        "program_sha256": sha256(Path(__file__).read_bytes()),
        "request": REQUEST,
        "request_sha256": sha256(canonical_bytes(REQUEST)),
        "input_sha256": sha256(input_bytes),
        "checks": ["required fields and string types", "unique identifiers", "explicit timestamp time zones"],
        "selected": selected,
        "output_sha256": sha256(canonical_bytes(selected)),
        "effects": {"network_requests": 0, "model_calls": 0, "output": "stdout"},
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
