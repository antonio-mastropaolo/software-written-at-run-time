"""Monthly digest: arXiv papers whose abstract mentions "coding agent",
listed in cs.SE or cs.CR (primary or cross-list), first submitted in a given month.

Uses arXiv's public API (https://info.arxiv.org/help/api/), read-only.
Follows the API terms: one request every 3 seconds, descriptive User-Agent.

    python arxiv_digest.py 2026-09 > digest-2026-09.csv
"""
import csv, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from calendar import monthrange

API = "https://export.arxiv.org/api/query"
UA = "UnreviewedProgramDemo/1.0 (research example)"
NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
PAGE = 100


def month_query(ym):
    y, m = map(int, ym.split("-"))
    last = monthrange(y, m)[1]
    return (f'abs:"coding agent" AND (cat:cs.SE OR cat:cs.CR) AND '
            f"submittedDate:[{y}{m:02d}010000 TO {y}{m:02d}{last}2359]")


def fetch(query, start):
    url = API + "?" + urllib.parse.urlencode({
        "search_query": query, "start": start, "max_results": PAGE,
        "sortBy": "submittedDate", "sortOrder": "descending"})
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return ET.fromstring(r.read())


def rows(feed):
    for e in feed.findall("a:entry", NS):
        yield {
            "id": e.findtext("a:id", namespaces=NS).rsplit("/abs/", 1)[1].split("v")[0],
            "submitted": e.findtext("a:published", namespaces=NS)[:10],
            "primary": e.find("x:primary_category", NS).get("term"),
            "categories": " ".join(c.get("term") for c in e.findall("a:category", NS)),
            "title": " ".join(e.findtext("a:title", namespaces=NS).split()),
            "first_author": e.find("a:author/a:name", NS).text,
        }


if __name__ == "__main__":
    query = month_query(sys.argv[1] if len(sys.argv) > 1 else "2026-09")
    t0, out, start, calls = time.time(), [], 0, 0
    while True:
        feed = fetch(query, start)
        calls += 1
        total = int(feed.findtext("{http://a9.com/-/spec/opensearch/1.1/}totalResults"))
        page = list(rows(feed))
        out += page
        start += PAGE
        if not page or start >= total:
            break
        time.sleep(3)
    w = csv.DictWriter(sys.stdout, fieldnames=list(out[0]) if out else ["id"])
    w.writeheader()
    w.writerows(out)
    print(f"# query: {query}\n# requests: {calls}, results: {len(out)} of {total}, "
          f"seconds: {time.time() - t0:.1f}", file=sys.stderr)
