#!/usr/bin/env python3
"""Set distinct Broker authentication placeholders in generated OpenAPI specs."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = {
    "BrokerAppID": "<broker_app_id>",
    "BrokerTimestamp": "<unix_timestamp>",
    "BrokerSignature": "<base64_signature>",
}


def main() -> None:
    for name in ("openapi.json", "openapi.en.json"):
        path = ROOT / "openapi" / "b" / name
        spec = json.loads(path.read_text(encoding="utf-8"))
        schemes = spec["components"]["securitySchemes"]
        for scheme_name, placeholder in DEFAULTS.items():
            schemes[scheme_name]["x-default"] = placeholder
        path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
