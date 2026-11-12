#!/usr/bin/env python3
"""Produce live evidence that a governance exception's product is NOT deployed (governance_exceptions X9).

Reads the named exception, sends one anonymous GET per live_probe_path to live_origin WITHOUT following
redirects and without cookies, and writes a JSON evidence file bound to this repository's HEAD commit and tree.
Read-only: it changes no file in the repository and no remote state.

  python tools/oral/verify_rulesapp_not_deployed.py --exception GX-S1-RULESAPP-FALLS-20261112 --out FILE
Exit 0 only if every probe returned exactly the exception's required_status and .vercelignore excludes the product.
Run it at release qualification and again immediately before any production push.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import http.client
import json
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import governance_exceptions as GX  # noqa: E402


def probe(origin: str, path: str, timeout: float = 20.0) -> dict:
    u = urllib.parse.urlsplit(origin)
    conn = (http.client.HTTPSConnection if u.scheme == "https" else http.client.HTTPConnection)(u.netloc, timeout=timeout)
    try:
        conn.request("GET", path, headers={"User-Agent": "miw-governance-evidence/1", "Cache-Control": "no-cache"})
        r = conn.getresponse()
        r.read(4096)
        return {"path": path, "status": r.status, "location": r.getheader("Location"), "redirect_followed": False}
    except OSError as e:
        return {"path": path, "status": None, "error": str(e), "redirect_followed": False}
    finally:
        conn.close()


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    eid = argv[argv.index("--exception") + 1]
    out = Path(argv[argv.index("--out") + 1])
    raw = (HERE / GX.exception_filename(eid)).read_bytes()
    exc = json.loads(raw.decode("utf-8"))
    dc = exc["deployment_condition"]
    facts = GX.RepoFacts()
    vi = facts.vercelignore()
    head = facts._git("rev-parse", "HEAD").stdout.strip()
    ev = {
        "kind": "DEPLOYMENT_EVIDENCE",
        "exception_id": eid,
        "exception_sha256": GX.sha256_bytes(raw),
        "product": exc["cross_product_item"]["product"],
        "origin": dc["live_origin"],
        "checked_at_utc": _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "commit": head,
        "tree": facts.head_tree(),
        "clean": facts.clean(),
        "vercelignore_sha256": hashlib.sha256(vi.encode("utf-8")).hexdigest(),
        "vercelignore_excludes": GX.vercelignore_excludes(vi, dc["vercelignore_rule"]),
        "probes": [probe(dc["live_origin"], p) for p in dc["live_probe_paths"]],
        "method": "anonymous GET, no cookies, redirects not followed",
    }
    ok = ev["vercelignore_excludes"] and all(p["status"] == dc["required_status"] for p in ev["probes"])
    ev["result"] = "NOT_DEPLOYED" if ok else "DEPLOYED_OR_UNKNOWN"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(ev, indent=1) + "\n", encoding="utf-8")
    for p in ev["probes"]:
        print("%-48s %s" % (p["path"], p["status"]))
    print("vercelignore_excludes=%s result=%s tree=%s" % (ev["vercelignore_excludes"], ev["result"], ev["tree"]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
