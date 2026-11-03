# Which Program Did the Agent Run?

**Checking and Keeping the Code AI Agents Write**

Antonio Mastropaolo

[Read the manuscript](paper/Which_Program_Did_the_Agent_Run.pdf) · [Inspect the arXiv pilot](examples/arxiv-pilot) · [Run the record example](examples/retained-record)

This repository accompanies a preliminary write-up of an exploratory research idea: for consequential agent actions, retain a program that can be checked before execution and examined afterwards, together with a record linking the request, checks, inputs, and effects to that program. The manuscript develops the argument and reports a small retrieval pilot. It is an unpublished work in progress, with further evaluation needed to establish its benefits and limits.

The PDF is the November 2, 2026 draft, previously titled *Software Written at Run Time*. It is provided unchanged. The examples make parts of the idea inspectable; they do not constitute an implementation or validation of the full proposed framework.

## What the pilot shows

On October 13, 2026, a browser agent and a retained Python program were used to find September 2026 arXiv papers in `cs.SE` or `cs.CR` whose abstracts mention "coding agent."

| Recorded run | Browser actions | Browser result | API requests | Program result |
|---|---:|---:|---:|---:|
| 1 | 26 | 91 papers | 1 | 98 papers |
| 2 | 13 | 91 papers | 1 | 98 papers |
| 3 | 2 | 91 papers | 1 | 98 papers |

The retained program list includes all 91 browser-result identifiers and seven additional identifiers. The manuscript's timestamp analysis places six of these papers on September 30 in both UTC and US Eastern time. The seventh falls on September 1 in UTC and August 31 in Eastern time, so its inclusion depends on the intended time zone.

The browser runs shared a session. Their decreasing action counts are therefore not an independent-run efficiency comparison. This is one task, and agreement across three runs does not establish correctness or general reliability. The repository preserves action-type summaries and identifier lists; the original browser scripts, complete browser state, and raw API response bodies are not included. The reported hash can be checked against the identifier-list file, not all bibliographic fields. See the [pilot evidence notes](examples/arxiv-pilot/README.md).

## Examples

Python 3.10 or newer is sufficient. No third-party packages or model credentials are needed.

### Inspect the retained pilot evidence offline

```sh
python3 examples/arxiv-pilot/verify_pilot.py
```

This checks the original program hash, recorded action counts, list sizes, and identifier-list hash, then prints the seven-identifier difference. It checks the retained artifacts without rerunning the historical experiment.

To query the current arXiv service with the original program:

```sh
python3 examples/arxiv-pilot/arxiv_digest.py 2026-09 > digest-2026-09.csv
```

This makes live, read-only API requests. The program waits three seconds between pages; run only one instance and leave at least three seconds between separate invocations, following [arXiv's API terms](https://info.arxiv.org/help/api/tou.html). Service changes can change the result, and this script does not archive raw responses or provide retry handling.

### Inspect a small retained execution record

```sh
python3 examples/retained-record/retained_record.py
```

This newly added teaching example reads a synthetic local fixture, validates its fields, applies a fixed UTC month filter, and emits the selected records with hashes of the program, request, input, and output. It makes no network or model calls. Its data and output are illustrative and were not used in the October pilot. The record is not signed or stored in an append-only service, and the script is not a capability sandbox.

Run the offline checks with:

```sh
python3 -m unittest discover -s tests -v
```

## Reuse

The Python examples are available under the [MIT license](LICENSE). That license does not cover the manuscript PDF or third-party material within it. The paper is shared here as an unpublished preliminary manuscript; cite the draft rather than treating it as an accepted IEEE article.

## How to cite

Antonio Mastropaolo. 2026. *Which Program Did the Agent Run? Checking and Keeping the Code AI Agents Write*. Preliminary exploratory manuscript, November 2, 2026. https://github.com/antonio-mastropaolo/software-written-at-run-time

```bibtex
@unpublished{mastropaolo2026runtime,
  title  = {Which Program Did the Agent Run? Checking and Keeping the Code {AI} Agents Write},
  author = {Antonio Mastropaolo},
  year   = {2026},
  note   = {Preliminary exploratory manuscript, version of November 2, 2026},
  url    = {https://github.com/antonio-mastropaolo/software-written-at-run-time}
}
```

A machine-readable citation is provided in [CITATION.cff](CITATION.cff), and the BibTeX entry is available in [CITATION.bib](CITATION.bib). When discussing the code or retained artifacts, also identify the commit or release used.
