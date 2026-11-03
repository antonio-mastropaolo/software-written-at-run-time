"""Check the retained pilot artifacts without contacting arXiv."""
import hashlib
import json
from pathlib import Path


def verify(root=None):
    root = Path(root) if root is not None else Path(__file__).resolve().parent
    runs = json.loads((root / "runs.json").read_text(encoding="utf-8"))
    agent_ids = (root / "agent-ids.txt").read_text(encoding="utf-8").splitlines()
    program_bytes = (root / "program-ids.txt").read_bytes()
    program_ids = program_bytes.decode("utf-8").splitlines()
    program_hash = hashlib.sha256((root / "arxiv_digest.py").read_bytes()).hexdigest()
    ids_hash = hashlib.sha256(program_bytes).hexdigest()

    def require(condition, message):
        if not condition:
            raise ValueError(message)

    require(len(agent_ids) == len(set(agent_ids)) == 91, "Browser identifier count or uniqueness changed")
    require(len(program_ids) == len(set(program_ids)) == 98, "Program identifier count or uniqueness changed")
    require(set(agent_ids) <= set(program_ids), "Browser list is no longer contained in the program list")
    require([len(run["steps"]) for run in runs["agent"]["runs"]] == [26, 13, 2], "Recorded action counts changed")
    require(len(runs["program"]["runs"]) == 3, "Expected three recorded program runs")
    require(program_hash[:16] == runs["program"]["sha256_16"], "Original program hash mismatch")
    for run in runs["agent"]["runs"]:
        require(run["papers"] == len(agent_ids), "Browser count differs from its retained list")
    for run in runs["program"]["runs"]:
        require(run["papers"] == len(program_ids), "Program count differs from its retained list")
        require(run["requests"] == 1, "Recorded request count changed")
        require(run["rows_sha256_12"] == ids_hash[:12], "Recorded identifier-list hash mismatch")
    return {
        "status": "retained artifacts agree",
        "browser_identifiers": len(agent_ids),
        "program_identifiers": len(program_ids),
        "program_only": sorted(set(program_ids) - set(agent_ids)),
        "program_sha256": program_hash,
        "identifier_file_sha256": ids_hash,
        "scope": "Offline consistency check; no historical run was repeated.",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
