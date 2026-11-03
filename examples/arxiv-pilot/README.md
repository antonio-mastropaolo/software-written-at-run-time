# arXiv retrieval pilot

These are retained artifacts from the October 13, 2026 pilot described in the manuscript. The original program, identifier lists, and run summary are preserved byte for byte. `verify_pilot.py` was added for this public release.

| File | Content |
|---|---|
| `arxiv_digest.py` | Original Python program querying arXiv's public API |
| `agent-ids.txt` | 91 identifiers in the retained browser result |
| `program-ids.txt` | 98 identifiers in the retained program result |
| `runs.json` | Recorded action-type sequences, counts, timings, and truncated hashes |
| `verify_pilot.py` | Offline consistency checks and set comparison |

In `runs.json`, `script!` marks a script call with truncated output. The summary records three browser runs in a shared session, not three independent sessions. The program-run durations are the historical values recorded in that file; they are not measurements made for this repository release.

The historical key `rows_sha256_12` matches the first 12 characters of the SHA-256 hash of `program-ids.txt`. That file is a sorted, newline-terminated identifier list. The hash verifies this list; it does not verify complete metadata rows, HTTP responses, or the three runs independently. Only one retained list per condition is included.

The original program's full SHA-256 is `808561fa630e01f43f30da8b999f7bf3179c26f1a944fadf41bc4853b598ca73`.

Run from the repository root:

```sh
python3 examples/arxiv-pilot/verify_pilot.py
```

The script fails if the retained counts, program hash, or recorded identifier hash no longer agree. It prints the set difference so the seven additional identifiers can be inspected. A successful check establishes artifact consistency, not scientific correctness, a security guarantee, or a reproduction of the historical browser runs.
