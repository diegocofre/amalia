"""Bounded, read-only feasibility probe; no model weights or corpus downloads."""
import hashlib
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
OAI = "https://sedici.unlp.edu.ar/oai/snrd"
NS = {"o": "http://www.openarchives.org/OAI/2.0/",
      "dc": "http://purl.org/dc/elements/1.1/"}
LIMIT = 24 * 1024 * 1024
FIELDS = ("architectures", "hidden_size", "intermediate_size", "num_hidden_layers",
          "num_attention_heads", "num_key_value_heads", "vocab_size",
          "max_position_embeddings", "hidden_act", "tie_word_embeddings",
          "torch_dtype", "dtype", "transformers_version")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Amalia-Feasibility/0.1"})
    with urllib.request.urlopen(req, timeout=30) as response:
        data = response.read(LIMIT + 1)
    if len(data) > LIMIT:
        raise ValueError("response exceeds byte limit")
    return data


def sha(data):
    return hashlib.sha256(data).hexdigest()


def model_probe(model, revision):
    root = f"https://huggingface.co/{model}/resolve/{revision}/"
    cfg = fetch(root + "config.json")
    config = json.loads(cfg)
    result = {"revision": revision, "config_sha256": sha(cfg),
              "config": {k: config[k] for k in FIELDS if k in config}}
    try:
        import tokenizers
        raw = fetch(root + "tokenizer.json")
        tokenizer = tokenizers.Tokenizer.from_str(raw.decode("utf-8"))
        result.update(tokenizer_sha256=sha(raw), tokenizers_version=tokenizers.__version__,
                      phrase_token_counts=[len(tokenizer.encode(p, add_special_tokens=False).ids)
                                           for p in PHRASES])
    except Exception as exc:
        result["tokenizer_error"] = f"{type(exc).__name__}: {exc}"
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


def oai_probe():
    counts = Counter()
    seen = set()
    pages = []
    query = {"verb": "ListRecords", "metadataPrefix": "oai_dc"}
    result = {"endpoint": OAI, "counts": {}, "pages": pages,
              "sampling": "first two pages, not representative"}
    try:
        for _ in range(2):
            raw = fetch(OAI + "?" + urllib.parse.urlencode(query))
            root = ET.fromstring(raw)
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
                counts[classify(rights)] += 1
            token = root.find("o:ListRecords/o:resumptionToken", NS)
            pages.append({"sha256": sha(raw), "bytes": len(raw)})
            if token is None or not token.text:
                break
            query = {"verb": "ListRecords", "resumptionToken": token.text}
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    result["counts"] = dict(counts)
    result["unique_records"] = len(seen)
    return result


def main():
    result = {"utc": datetime.now(timezone.utc).isoformat(),
              "python": sys.version.split()[0], "models": {},
              "phrases": list(PHRASES), "notes": "No corpus documents or weights downloaded."}
    for model, revision in MODELS.items():
        try:
            result["models"][model] = model_probe(model, revision)
        except Exception as exc:
            result["models"][model] = {"revision": revision, "error": f"{type(exc).__name__}: {exc}"}
    result["sedici"] = oai_probe()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
