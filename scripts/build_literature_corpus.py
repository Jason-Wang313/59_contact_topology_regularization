import csv
import hashlib
import json
import math
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

QUERIES = [
    "robot contact manipulation topology",
    "contact-rich robot learning tactile topology",
    "robot manipulation contact graph learning",
    "robot tactile perception contact state",
    "sim-to-real contact-rich policy learning",
    "robot control contact invariance",
    "contact sequence learning robotics",
    "robot affordance contact representation",
    "manipulation contact planning topology",
    "deformable object contact topology",
    "robot grasp contact map learning",
    "in-hand manipulation contact representation",
    "contact-rich imitation learning robotics",
    "robot assembly contact reasoning",
    "robotic contact model learning",
    "topological regularization machine learning contact",
]

def norm(s):
    if not s:
        return ""
    return re.sub(r"\s+", " ", s).strip()

def doi_key(doi):
    return doi.lower().strip().replace("https://doi.org/", "") if doi else ""

def fetch_crossref(query, rows=100, offset=0):
    url = "https://api.crossref.org/works"
    params = {"query": query, "rows": rows, "offset": offset}
    r = requests.get(url, params=params, timeout=40, headers={"User-Agent": "codex-literature-sweep/1.0"})
    r.raise_for_status()
    return r.json()["message"]["items"]

def fetch_arxiv(query, start=0, max_results=50):
    url = "http://export.arxiv.org/api/query"
    params = {"search_query": f"all:{query}", "start": start, "max_results": max_results, "sortBy": "relevance", "sortOrder": "descending"}
    r = requests.get(url, params=params, timeout=40, headers={"User-Agent": "codex-literature-sweep/1.0"})
    r.raise_for_status()
    return r.text

rows = []
seen = set()
source_counts = {}

def add_item(item, source, query):
    title = norm((item.get("title") or [""])[0])
    if not title:
        return
    doi = doi_key(item.get("DOI", ""))
    key = doi or hashlib.sha1(title.lower().encode("utf-8")).hexdigest()
    if key in seen:
        return
    seen.add(key)
    authors = item.get("author", [])
    author = "; ".join(
        [f"{a.get('family','')}, {a.get('given','')}".strip(", ") for a in authors[:8] if a.get("family") or a.get("given")]
    )
    rows.append({
        "id": key[:12],
        "source": source,
        "query": query,
        "title": title,
        "year": str(item.get("published-print", item.get("published-online", item.get("created", {}))).get("date-parts", [[None]])[0][0] or ""),
        "venue": norm((item.get("container-title") or [""])[0]),
        "doi": doi,
        "url": item.get("URL", ""),
        "authors": author,
        "abstract": norm(re.sub(r"<.*?>", " ", item.get("abstract", "")))[:800],
    })

for q in QUERIES:
    try:
        for offset in range(0, 300, 100):
            items = fetch_crossref(q, rows=100, offset=offset)
            for item in items:
                add_item(item, "crossref", q)
    except Exception as e:
        source_counts[f"crossref::{q}"] = str(e)

    try:
        # Collect a smaller arXiv slice for robotics-heavy queries
        txt = fetch_arxiv(q, start=0, max_results=50)
        entries = re.split(r"<entry>", txt)[1:]
        for ent in entries:
            title_m = re.search(r"<title>(.*?)</title>", ent, re.S)
            if not title_m:
                continue
            title = norm(re.sub(r"\s+", " ", title_m.group(1)))
            title = title.replace("arXiv:", "")
            if not title:
                continue
            key = hashlib.sha1(("arxiv:" + title.lower()).encode("utf-8")).hexdigest()
            if key in seen:
                continue
            seen.add(key)
            summary_m = re.search(r"<summary>(.*?)</summary>", ent, re.S)
            author_names = re.findall(r"<name>(.*?)</name>", ent)
            year_m = re.search(r"<published>(\d{4})-", ent)
            rows.append({
                "id": key[:12],
                "source": "arxiv",
                "query": q,
                "title": title,
                "year": year_m.group(1) if year_m else "",
                "venue": "arXiv",
                "doi": "",
                "url": "",
                "authors": "; ".join(author_names[:8]),
                "abstract": norm(summary_m.group(1))[:800] if summary_m else "",
            })
    except Exception as e:
        source_counts[f"arxiv::{q}"] = str(e)

rows.sort(key=lambda r: (r["query"], r["year"], r["title"]))

with open(DOCS / "related_work_matrix.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "source", "query", "title", "year", "venue", "doi", "url", "authors", "abstract"])
    writer.writeheader()
    writer.writerows(rows)

meta = {
    "generated_at": datetime.utcnow().isoformat() + "Z",
    "n_rows": len(rows),
    "queries": QUERIES,
    "source_errors": source_counts,
}
with open(DOCS / "related_work_matrix_meta.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)

print(json.dumps(meta, indent=2))
