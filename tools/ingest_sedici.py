"""Small SEDICI pilot: retain PDFs, extract text, measure, admit only reviewed hashes."""
import argparse
import io
import json
import re
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path
from urllib.parse import urlsplit

from tools.feasibility_probe import MODELS, fetch, git_info, safe, sha, error_text

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "configs/sedici-pilot.json"
LICENSE = "https://creativecommons.org/licenses/by/4.0/"
MAX_DOCS = 10
MAX_PAGES = 100


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as out:
        temp = Path(out.name)
        try:
            out.write(data)
        except BaseException:
            out.close()
            temp.unlink(missing_ok=True)
            raise
    try:
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def valid_document(doc):
    handle = doc.get("handle", "")
    source = f"https://sedici.unlp.edu.ar/handle/{handle}"
    url = urlsplit(doc.get("pdf_url", ""))
    return (
        isinstance(handle, str) and re.fullmatch(r"10915/\d+", handle)
        and doc.get("id") == "sedici-" + handle.split("/")[1]
        and doc.get("source_url") == source
        and url.scheme == "https" and url.netloc == "sedici.unlp.edu.ar"
        and url.path.startswith(f"/bitstream/handle/{handle}/")
        and doc.get("license") == "CC-BY-4.0" and doc.get("license_url") == LICENSE
        and doc.get("acquisition") == "approved_for_local_research"
        and bool(doc.get("rights_evidence")) and doc.get("review_date")
    )


def load_manifest(raw):
    data = json.loads(raw)
    docs = data["documents"]
    if data.get("schema_version") != 1 or not 1 <= len(docs) <= MAX_DOCS:
        raise ValueError("invalid pilot manifest or batch size")
    if any(not valid_document(d) for d in docs):
        raise ValueError("source lacks approved local acquisition or valid provenance")
    if len({d["id"] for d in docs}) != len(docs):
        raise ValueError("duplicate document IDs")
    return data


def get_pdf(doc, workspace):
    path = workspace / "raw/sedici" / (doc["id"] + ".pdf")
    cached = path.exists()
    data = path.read_bytes() if cached else fetch(doc["pdf_url"])
    if not data.startswith(b"%PDF-") or len(data) > 24 * 1024 * 1024:
        raise ValueError("not a bounded PDF")
    if not cached:
        atomic_write(path, data)
    return data, cached


def normalize(text):
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
    text, redactions = re.subn(r"(?i)[\w.+-]+@[\w.-]+\.[a-z]{2,}", "[EMAIL]", text)
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text.strip(), redactions


def extract_pdf(data, max_pages):
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    total = len(reader.pages)
    if reader.is_encrypted or not 1 <= total <= MAX_PAGES:
        raise ValueError("encrypted or oversized PDF")
    if max_pages is not None and not 1 <= max_pages <= total:
        raise ValueError("manifest page limit exceeds source")
    count = max_pages if max_pages is not None else total
    chunks = [(reader.pages[i].extract_text() or "") for i in range(count)]
    text, redactions = normalize("\n\n".join(chunks))
    if len(text) < 200:
        raise ValueError("insufficient extractable text; no automatic OCR")
    return text, {"pdf_pages": total, "extracted_pages": count,
                  "empty_pages": sum(not p.strip() for p in chunks),
                  "email_redactions": redactions}


def tokenizers_for_run(workspace):
    from tokenizers import Tokenizer

    result, info = {}, {}
    for model, revision in MODELS.items():
        path = workspace / "tokenizers" / revision / "tokenizer.json"
        try:
            raw = path.read_bytes() if path.exists() else fetch(
                f"https://huggingface.co/{model}/resolve/{revision}/tokenizer.json")
            tokenizer = Tokenizer.from_str(raw.decode("utf-8"))
            if not path.exists():
                atomic_write(path, raw)
            result[model] = tokenizer
            info[model] = {"revision": revision, "sha256": sha(raw)}
        except Exception as exc:
            info[model] = {"revision": revision, "error": error_text(exc)}
    return result, info


def admitted(doc, raw_hash, text_hash):
    approval = doc.get("training_approval")
    return (
        valid_document(doc) and isinstance(approval, dict)
        and approval.get("approved") is True
        and bool(approval.get("reviewer")) and bool(approval.get("review_date"))
        and bool(approval.get("rights_and_privacy_notes"))
        and approval.get("raw_sha256") == raw_hash
        and approval.get("text_sha256") == text_hash
    )


def process(doc, workspace, tokenizers):
    raw, cached = get_pdf(doc, workspace)
    text, metrics = extract_pdf(raw, doc.get("max_pages"))
    encoded = text.encode("utf-8")
    raw_hash, text_hash = sha(raw), sha(encoded)
    path = workspace / "processed/sedici" / doc["id"] / (text_hash + ".txt")
    if not path.exists():
        atomic_write(path, encoded)
    elif sha(path.read_bytes()) != text_hash:
        raise ValueError("existing processed artifact hash mismatch")
    accepted = admitted(doc, raw_hash, text_hash)
    record = {
        "id": doc["id"], "title": doc["title"], "authors": doc["authors"],
        "year": doc["year"], "source_url": doc["source_url"], "pdf_url": doc["pdf_url"],
        "license": doc["license"], "license_url": doc["license_url"],
        "domain": doc["domain"], "language": doc["language"], "country_context": doc["country_context"],
        "raw_sha256": raw_hash, "text_sha256": text_hash,
        "pdf_bytes": len(raw), "text_bytes": len(encoded), "characters": len(text),
        "cached_pdf": cached, "processed_path": path.relative_to(workspace).as_posix(),
        "status": "admitted" if accepted else "pending_review",
        "redistribution_approved": False, **metrics,
        "token_counts": {name: len(tok.encode(text, add_special_tokens=False).ids)
                         for name, tok in tokenizers.items()},
    }
    row = {k: record[k] for k in ("id", "title", "authors", "year", "source_url",
                                  "license", "license_url", "raw_sha256", "text_sha256",
                                  "domain", "language", "country_context")}
    row.update(text=text, training_approval=doc["training_approval"], redistribution_approved=False)
    return record, row if accepted else None


def jsonl(rows):
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
                   for row in rows).encode("utf-8")


def run_batch(manifest, workspace, tokenizers):
    records, rows, seen = [], [], set()
    for doc in manifest["documents"]:
        try:
            print("SEDICI:", doc["id"], file=sys.stderr, flush=True)
            record, row = process(doc, workspace, tokenizers)
            if row is not None:
                if row["text_sha256"] in seen:
                    record["status"] = "duplicate"
                else:
                    rows.append(row)
                    seen.add(row["text_sha256"])
            records.append(record)
        except Exception as exc:
            records.append({"id": doc["id"], "status": "error", "error": error_text(exc)})
    # Rebuild this source's eligible view from the reviewed manifest; never append duplicates.
    # It is not a frozen training snapshot and must not be used if the run has errors.
    output = jsonl(rows)
    atomic_write(workspace / "corpus/sedici.jsonl", output)
    return records, rows, sha(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=ROOT / "workspace")
    args = parser.parse_args()
    raw = MANIFEST.read_bytes()
    manifest = load_manifest(raw)
    workspace = args.workspace.resolve()
    tokenizers, info = tokenizers_for_run(workspace)
    records, rows, corpus_hash = run_batch(manifest, workspace, tokenizers)
    now = datetime.now(timezone.utc)
    run_id = "sedici-pilot-" + now.strftime("%Y%m%dT%H%M%S%fZ")
    report = {
        "schema_version": 1, "run_id": run_id, "utc": now.isoformat(),
        "git": safe(git_info), "script_sha256": sha(Path(__file__).read_bytes()),
        "python": sys.version.split()[0], "dependencies": {p: version(p) for p in ("pypdf", "tokenizers")},
        "manifest_sha256": sha(raw), "batch_id": manifest["batch_id"],
        "tokenizers": info, "documents": records,
        "summary": {key: sum(r["status"] == key for r in records)
                    for key in ("pending_review", "admitted", "duplicate", "error")},
        "eligible_corpus_sha256": corpus_hash, "eligible_documents": len(rows),
        "candidate_characters": sum(r.get("characters", 0) for r in records),
        "candidate_tokens": {name: sum(r.get("token_counts", {}).get(name, 0) for r in records)
                             for name in tokenizers},
        "notes": "Directed sample; not representative. Text extraction and email filtering are not full rights/privacy review. No training or redistribution authorized.",
    }
    data = (json.dumps(report, ensure_ascii=True, indent=2) + "\n").encode("utf-8")
    atomic_write(workspace / "runs" / (run_id + ".json"), data)
    sys.stdout.write(data.decode("ascii"))
    return int(report["summary"]["error"] > 0 or len(tokenizers) != len(MODELS))


if __name__ == "__main__":
    sys.exit(main())
