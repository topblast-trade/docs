#!/usr/bin/env python3
"""Generate the User API OpenAPI specification.

The root openapi.json remains the temporary source for User APIs under the
/api/v1/trade/ prefix. Broker APIs are generated from go-uc and must not be
overwritten by this script.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "openapi.json"
OUTPUTS = {"c": ROOT / "openapi" / "c" / "openapi.json"}
HTTP_METHODS = {"get", "post", "put", "patch", "delete", "options", "head"}
LEGACY_AUTH_HEADERS = {"x-api-key", "x-timestamp", "x-signature", "authorization"}


def is_c_side(path: str) -> bool:
    return path.startswith("/api/v1/trade/")


def remove_legacy_auth_parameters(spec: dict) -> None:
    for path_item in spec.get("paths", {}).values():
        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            parameters = operation.get("parameters", [])
            operation["parameters"] = [
                parameter
                for parameter in parameters
                if not (
                    parameter.get("in") == "header"
                    and parameter.get("name", "").lower() in LEGACY_AUTH_HEADERS
                )
            ]
            if not operation["parameters"]:
                operation.pop("parameters", None)
            operation.pop("security", None)


def configure_b_auth(spec: dict) -> None:
    schemes = spec.setdefault("components", {}).setdefault("securitySchemes", {})
    schemes.clear()
    schemes.update(
        {
            "BrokerApiKey": {
                "type": "apiKey",
                "in": "header",
                "name": "x-api-key",
                "description": "Broker API key.",
            },
            "RequestTimestamp": {
                "type": "apiKey",
                "in": "header",
                "name": "x-timestamp",
                "description": "Request timestamp in seconds or milliseconds.",
            },
            "RequestSignature": {
                "type": "apiKey",
                "in": "header",
                "name": "x-signature",
                "description": "Base64-encoded HMAC-SHA256 request signature.",
            },
        }
    )
    spec["security"] = [
        {"BrokerApiKey": [], "RequestTimestamp": [], "RequestSignature": []}
    ]


def configure_c_auth(spec: dict) -> None:
    schemes = spec.setdefault("components", {}).setdefault("securitySchemes", {})
    schemes.clear()
    schemes["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "User access token returned by the login flow.",
    }
    spec["security"] = [{"BearerAuth": []}]


def configure_tags(spec: dict, side: str) -> None:
    """Declare the tags used to group operations inside each API tab."""
    descriptions = {
        "密钥管理": "Manage end-user API keys.",
        "资产管理": "Query balances and transfer assets.",
        "用户管理": "Register, update, and manage broker users.",
        "交易查询": "Query end-user spot and futures trading data.",
        "内部接口-用户鉴权": "Internal user authentication operations.",
        "内部接口-券商管理": "Internal broker management operations.",
        "内部接口-对冲配置": "Internal hedging configuration operations.",
        "内部接口-用户管理": "Internal user management operations.",
    }
    used = []
    for path_item in spec.get("paths", {}).values():
        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            for tag in operation.get("tags", []):
                if tag not in used:
                    used.append(tag)

    spec["tags"] = [
        {"name": tag, "description": descriptions.get(tag, f"{side.upper()}-side API operations.")}
        for tag in used
    ]
    spec["x-api-side"] = side.upper()


def build(source: dict, side: str) -> dict:
    spec = copy.deepcopy(source)
    if side == "c":
        spec["paths"] = {
            path: item for path, item in spec.get("paths", {}).items() if is_c_side(path)
        }
        spec["info"]["title"] = "topblast Trading REST API"
        spec["servers"] = [
            {
                "url": "https://api.topblast.trade",
                "description": "生产环境",
            }
        ]
        configure_auth = configure_c_auth
    else:
        spec["paths"] = {
            path: item for path, item in spec.get("paths", {}).items() if not is_c_side(path)
        }
        spec["info"]["title"] = "topblast Broker REST API"
        configure_auth = configure_b_auth

    remove_legacy_auth_parameters(spec)
    configure_auth(spec)
    configure_tags(spec, side)
    return spec


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    for side, output in OUTPUTS.items():
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(build(source, side), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"generated {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
