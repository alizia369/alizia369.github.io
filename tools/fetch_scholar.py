"""Fetch Google Scholar headline metrics into data/scholar.json.

Run by .github/workflows/scholar.yml. Only overwrites the file when a fetch succeeds,
so the site keeps the last good figures if Scholar blocks the request.
"""
import json
import pathlib
import sys
from datetime import datetime, timezone

SCHOLAR_ID = "BVBJ06QAAAAJ"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data" / "scholar.json"


def fetch(use_proxy):
    from scholarly import scholarly, ProxyGenerator
    if use_proxy:
        pg = ProxyGenerator()
        if not pg.FreeProxies():
            raise RuntimeError("no free proxy available")
        scholarly.use_proxy(pg)
    author = scholarly.search_author_id(SCHOLAR_ID)
    scholarly.fill(author, sections=["indices", "counts"])
    return author


def main():
    author, err = None, []
    for use_proxy in (False, True):
        try:
            author = fetch(use_proxy)
            if author.get("citedby"):
                break
        except Exception as e:  # Scholar often blocks cloud IPs
            err.append(f"{'proxy' if use_proxy else 'direct'}: {e}")
    if not author or not author.get("citedby"):
        print("::warning title=Scholar fetch failed::" + " | ".join(err)[:900])
        return 0
    old = json.loads(OUT.read_text()) if OUT.exists() else {}
    new = {
        "citations": int(author["citedby"]),
        "h_index": int(author.get("hindex", 0)),
        "i10_index": int(author.get("i10index", 0)),
        "citations_since_2021": int(author.get("citedby5y", 0)),
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "source": "Google Scholar",
    }
    # Guard against a bad parse: never accept a large drop
    if old.get("citations") and new["citations"] < 0.8 * old["citations"]:
        print(f"Suspicious drop {old['citations']} -> {new['citations']}; not saving.")
        return 0
    OUT.write_text(json.dumps(new, indent=1) + "\n")
    print(f"::notice title=Scholar figures saved::{new}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
