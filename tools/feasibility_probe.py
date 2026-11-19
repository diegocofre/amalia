"""Bounded, read-only feasibility probe; no model weights or corpus downloads."""
import hashlib
import importlib.metadata
import math
import struct
import subprocess
from pathlib import Path
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone

MODELS = {
    "PleIAs/Pleias-1.2b-Preview": "6556074d10a57b04bdd46c8a34c97bca67f830ab",
    "swiss-ai/Apertus-v1.1-1.5B": "dbe8919b2f0389888bada6b3a19e81e0ef4286c1",
}
PHRASES = (
    "¿Vos sabés dónde queda la biblioteca popular?",
    "La investigación científica y la educación pública forman parte de nuestra sociedad.",
    "En la Patagonia, el viento y las distancias condicionan la vida cotidiana.",
    "Che, ¿tomamos unos mates y charlamos un rato?",
    "La reforma universitaria transformó las instituciones de educación superior.",
)
VERSION = "0.2"
OAI_ENDPOINTS = (
    "https://sedici.unlp.edu.ar/xoai/snrd",
    "https://sedici.unlp.edu.ar/xoai/request",
    "https://sedici.unlp.edu.ar/oai/snrd",
)
DATASETS = (
    "PleIAs/common_corpus", "latam-gpt/LatamGPT-Corpus-1.0",
    "spanish-ir/messirve", "latam-gpt/CHOCLO",
    "OpenAssistant/oasst1", "CohereLabs/aya_dataset",
)
NS = {"o": "http://www.openarchives.org/OAI/2.0/",
      "dc": "http://purl.org/dc/elements/1.1/"}
LIMIT = 24 * 1024 * 1024
FIELDS = ("architectures", "hidden_size", "intermediate_size", "num_hidden_layers",
          "num_attention_heads", "num_key_value_heads", "vocab_size",
          "max_position_embeddings", "hidden_act", "tie_word_embeddings",
          "torch_dtype", "dtype", "transformers_version")


def fetch(url, byte_range=None):
    headers = {"User-Agent": "Amalia-Feasibility/" + VERSION, "Accept-Encoding": "identity"}
    limit = LIMIT
    if byte_range is not None:
        start, end = byte_range
        limit = end - start + 1
        if not 0 < limit <= LIMIT:
            raise ValueError("invalid range")
        headers["Range"] = f"bytes={start}-{end}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        if byte_range is not None:
            expected = f"bytes {start}-{end}/"
            if response.status != 206 or not response.headers.get("Content-Range", "").startswith(expected):
                raise ValueError("server did not honor exact HTTP range; refusing payload")
        data = response.read(limit + 1)
    if len(data) > limit or (byte_range is not None and len(data) != limit):
        raise ValueError("unexpected response size")
    return data


def error_text(exc):
    return re.sub(r"https?://\S+", "[URL omitted]", f"{type(exc).__name__}: {exc}")[:300]


def safe(fn, *args):
    try:
        return fn(*args)
    except Exception as exc:
        return {"error": error_text(exc)}


def hub_info(kind, repo, revision=None):
    url = f"https://huggingface.co/api/{kind}/{repo}"
    if revision:
        url += f"/revision/{revision}"
    raw = fetch(url)
    info = json.loads(raw)
    card = info.get("cardData") or {}
    return {"sha": info.get("sha"), "metadata_sha256": sha(raw),
            "gated": info.get("gated"), "private": info.get("private"),
            "license": card.get("license"), "license_name": card.get("license_name"),
            "license_link": card.get("license_link"),
            "files": [f["rfilename"] for f in info.get("siblings", []) if "rfilename" in f]}


def parse_tensor_header(raw):
    header = json.loads(raw)
    counts = Counter()
    total_bytes = 0
    for name, tensor in header.items():
        if name == "__metadata__":
            continue
        shape, offsets = tensor["shape"], tensor["data_offsets"]
        if any(not isinstance(n, int) or n < 0 for n in shape):
            raise ValueError("invalid tensor shape")
        if len(offsets) != 2 or not 0 <= offsets[0] <= offsets[1]:
            raise ValueError("invalid tensor offsets")
        counts[tensor["dtype"]] += math.prod(shape)
        total_bytes += offsets[1] - offsets[0]
    return {"tensor_elements_by_dtype": dict(counts), "tensor_elements": sum(counts.values()),
            "payload_bytes_declared": total_bytes}


def weight_metadata(root, names):
    if "model.safetensors" in names:
        shards = ["model.safetensors"]
    elif "model.safetensors.index.json" in names:
        index = json.loads(fetch(root + "model.safetensors.index.json"))
        shards = sorted(set(index["weight_map"].values()))
    else:
        raise ValueError("standard checkpoint filenames not found")
    if not 1 <= len(shards) <= 16:
        raise ValueError("checkpoint outside bounded shard count")
    result = {}
    for name in shards:
        if "/" in name or chr(92) in name or not name.endswith(".safetensors"):
            raise ValueError("unexpected shard filename")
        url = root + name
        size = struct.unpack("<Q", fetch(url, (0, 7)))[0]
        if not 0 < size <= 4 * 1024 * 1024:
            raise ValueError("header outside bounded size")
        raw = fetch(url, (8, 7 + size))
        result[name] = {"header_bytes": size, "header_sha256": sha(raw),
                        **parse_tensor_header(raw)}
    return {"shards": result,
            "stored_tensor_elements": sum(x["tensor_elements"] for x in result.values()),
            "payload_bytes_declared": sum(x["payload_bytes_declared"] for x in result.values()),
            "note": "Includes buffers; not active or trainable parameter count."}


def dataset_probe(repo):
    info = hub_info("datasets", repo)
    info["files"] = info["files"][:100]
    return info


def git_info():
    root = Path(__file__).resolve().parent.parent
    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args],
                                       stderr=subprocess.DEVNULL, timeout=5, text=True).strip()
    return {"commit": git("rev-parse", "HEAD"),
            "tracked_tree_dirty": bool(git("status", "--porcelain", "--untracked-files=no"))}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def model_probe(model, revision):
    root = f"https://huggingface.co/{model}/resolve/{revision}/"
    info = safe(hub_info, "models", model, revision)
    result = {"revision": revision, "hub": info,
              "weights_metadata": safe(weight_metadata, root, info.get("files", []))}
    try:
        cfg = fetch(root + "config.json")
        config = json.loads(cfg)
        result.update(config_sha256=sha(cfg), config={k: config[k] for k in FIELDS if k in config})
    except Exception as exc:
        result["config_error"] = error_text(exc)
    try:
        import tokenizers
        raw = fetch(root + "tokenizer.json")
        tokenizer = tokenizers.Tokenizer.from_str(raw.decode("utf-8"))
        result.update(tokenizer_sha256=sha(raw), tokenizers_version=tokenizers.__version__,
                      phrase_token_counts=[len(tokenizer.encode(p, add_special_tokens=False).ids)
                                           for p in PHRASES])
    except Exception as exc:
        result["tokenizer_error"] = error_text(exc)
    return result


def classify(rights):
    """Only explicit standard CC URLs; never infer a license from openAccess."""
    kinds = set()
    for value in rights:
        for match in re.finditer(
            r"https?://creativecommons\.org/(?:licenses/([a-z-]+)/[0-9.]+|publicdomain/(zero|mark)/[0-9.]+)",
            value.lower(),
        ):
            kinds.add(match.group(1) or match.group(2))
    if any("nc" in k.split("-") or "nd" in k.split("-") for k in kinds):
        return "restricted_nc_or_nd"
    if not kinds:
        return "unknown"
    if kinds <= {"by", "zero"}:
        return "candidate_explicit_by_or_cc0"
    return "manual_review"


def oai_probe(endpoint):
    counts = Counter()
    seen = set()
    pages = []
    samples = []
    query = {"verb": "ListRecords", "metadataPrefix": "oai_dc"}
    result = {"endpoint": endpoint, "counts": {}, "pages": pages,
              "sampling": "first two pages, not representative"}
    try:
        for _ in range(2):
            raw = fetch(endpoint + "?" + urllib.parse.urlencode(query))
            root = ET.fromstring(raw)
            if root.tag != "{" + NS["o"] + "}OAI-PMH":
                raise ValueError("response is not OAI-PMH XML")
            error = root.find("o:error", NS)
            if error is not None:
                raise ValueError(f"OAI error: {error.get('code')}")
            for rec in root.findall("o:ListRecords/o:record", NS):
                header = rec.find("o:header", NS)
                if header is None:
                    continue
                identifier = header.findtext("o:identifier", namespaces=NS)
                if not identifier or identifier in seen:
                    continue
                seen.add(identifier)
                if header.get("status") == "deleted":
                    counts["deleted"] += 1
                    continue
                rights = [x.text or "" for x in rec.findall("o:metadata//dc:rights", NS)]
                kind = classify(rights)
                counts[kind] += 1
                handle = re.search(r"10915/\d+", identifier)
                if handle and len(samples) < 50:
                    samples.append({"handle": handle.group(), "category": kind,
                                    "license_urls": [u for value in rights for u in
                                        re.findall(r"https?://creativecommons\.org/[^\s<>]+", value)]})
            token = root.find("o:ListRecords/o:resumptionToken", NS)
            pages.append({"sha256": sha(raw), "bytes": len(raw)})
            if token is None or not token.text:
                break
            query = {"verb": "ListRecords", "resumptionToken": token.text}
    except Exception as exc:
        result["error"] = error_text(exc)
    result["samples"] = samples
    result["counts"] = dict(counts)
    result["unique_records"] = len(seen)
    return result


def main():
    result = {"schema_version": 2, "probe_version": VERSION,
              "script_sha256": sha(Path(__file__).read_bytes()), "git": safe(git_info),
              "utc": datetime.now(timezone.utc).isoformat(),
              "python": sys.version.split()[0], "models": {},
              "dependencies": sorted({(d.metadata.get("Name") or "", d.version) for d in importlib.metadata.distributions()}),
              "phrases": list(PHRASES), "notes": "No corpus documents or tensor payloads downloaded; only metadata and tokenizer files."}
    for model, revision in MODELS.items():
        print("Model:", model, file=sys.stderr, flush=True)
        try:
            result["models"][model] = model_probe(model, revision)
        except Exception as exc:
            result["models"][model] = {"revision": revision, "error": error_text(exc)}
    result["datasets"] = {}
    for repo in DATASETS:
        print("Dataset:", repo, file=sys.stderr, flush=True)
        result["datasets"][repo] = safe(dataset_probe, repo)
    result["sedici"] = {}
    for endpoint in OAI_ENDPOINTS:
        print("SEDICI:", endpoint, file=sys.stderr, flush=True)
        item = safe(oai_probe, endpoint)
        result["sedici"][endpoint] = item
        if item.get("unique_records", 0):
            break
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
