#!/usr/bin/env python3
"""Keep only successful responses in the published OpenAPI specifications."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OPENAPI_FILES = (
    ROOT / "openapi" / "b" / "openapi.json",
    ROOT / "openapi" / "b" / "openapi.en.json",
    ROOT / "openapi" / "c" / "openapi.json",
    ROOT / "openapi" / "c" / "openapi.en.json",
)
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}


def keep_success_responses(spec: dict) -> int:
    removed = 0
    for path_item in spec.get("paths", {}).values():
        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            responses = operation.get("responses")
            if not isinstance(responses, dict):
                continue
            for status in list(responses):
                if not str(status).startswith("2"):
                    del responses[status]
                    removed += 1
    return removed


def main() -> None:
    for openapi_file in OPENAPI_FILES:
        spec = json.loads(openapi_file.read_text(encoding="utf-8"))
        removed = keep_success_responses(spec)
        openapi_file.write_text(
            json.dumps(spec, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"updated {openapi_file.relative_to(ROOT)}: removed {removed} responses")


if __name__ == "__main__":
    main()
