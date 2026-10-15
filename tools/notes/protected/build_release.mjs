// Local release tool (Lane A / private CI only; never runs on Vercel).
//
//   real:      node tools/notes/protected/build_release.mjs real --private <miw-protected-notes checkout>
//                  --release-id lohan-r1 --out <dir>
//              writes <dir>/lohan-r1.pkg (for the private repo's releases/), the public pin
//              o3/lohan.pin.json, and prints the package sha256. The package is deterministic:
//              rebuilding from the same private commit gives the same bytes.
//   synthetic: node tools/notes/protected/build_release.mjs synthetic
//              (re)generates o3/synthetic/: 21 canary pages behind the same gate, no real
//              content and no replacements, plus their pin, for preview-only hosted checks.
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { buildPackage, makePin, GATE } from "../../../o3/release.mjs";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..", "..");
const STORE = { repo: "nickmarineengr-aiLiterate/miw-protected-notes", ref: null, path: null };
const arg = (k) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const stable = (o) => JSON.stringify(o, null, 1) + "\n";

const mode = process.argv[2];
if (mode === "real") {
  const id = arg("--release-id");
  if (!/^lohan-r\d+$/.test(id || "")) throw new Error("--release-id lohan-rN required");
  const r = buildPackage({ privateRoot: arg("--private"), publicTree: REPO, releaseId: id });
  const out = arg("--out");
  fs.mkdirSync(out, { recursive: true });
  fs.writeFileSync(path.join(out, `${id}.pkg`), r.bytes);
  const pin = makePin({ manifest: r.manifest, packageSha: r.sha256, replaceFiles: r.replaceFiles,
    store: { ...STORE, ref: id, path: `releases/${id}.pkg` } });
  fs.writeFileSync(path.join(REPO, "o3", "lohan.pin.json"), stable(pin));
  console.log(JSON.stringify({ release_id: id, package_sha256: r.sha256, bytes: r.bytes.length, totals: r.manifest.totals }));
} else if (mode === "synthetic") {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "o3-synth-"));
  const ov = path.join(tmp, "lohan", "overlay", "meoclass1", "oralnotes");
  const sp = path.join(tmp, "lohan", "source", "tools", "notes", "specs", "lohan");
  fs.mkdirSync(ov, { recursive: true }); fs.mkdirSync(sp, { recursive: true });
  for (let n = 1; n <= 21; n++) {
    fs.writeFileSync(path.join(ov, `lohan-notes-p${n}.html`),
      `<!DOCTYPE html>\n<html lang="en">\n<head><meta charset="utf-8"><meta name="robots" content="noindex">` +
      `<title>SYNTHETIC preview page ${n}</title></head>\n<body>\n${GATE}\n` +
      `<div class="topic-block" id="topic-p${n}-1" data-kw="synthetic"><p>SYNTH-CANARY-O3-PAGE-${n}: synthetic ` +
      `preview content for hosted gate checks. Not study material.</p></div>\n</body>\n</html>\n`);
    fs.writeFileSync(path.join(sp, `p${n}.json`), stable({ part: n, synthetic: true }));
  }
  const r = buildPackage({ privateRoot: tmp, publicTree: REPO, releaseId: "synthetic-r1" });
  const dir = path.join(REPO, "o3", "synthetic");
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, "lohan-synthetic.pkg"), r.bytes);
  const pin = makePin({ manifest: r.manifest, packageSha: r.sha256, replaceFiles: r.replaceFiles,
    store: { repo: "committed", ref: "synthetic-r1", path: "o3/synthetic/lohan-synthetic.pkg" } });
  fs.writeFileSync(path.join(dir, "lohan.synthetic.pin.json"), stable(pin));
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log(JSON.stringify({ synthetic: true, package_sha256: r.sha256, totals: r.manifest.totals }));
} else {
  throw new Error("usage: build_release.mjs real|synthetic");
}
