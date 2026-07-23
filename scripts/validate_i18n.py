#!/usr/bin/env python3
"""Validate Chinese/English documentation parity and OpenAPI references."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CJK_RE = re.compile(r"[\u3400-\u9fff]")
OPENAPI_RE = re.compile(
    r'^openapi:\s*"(?P<file>[^"]+)\s+(?P<kind>[A-Z]+|webhook)\s+(?P<target>[^"]+)"\s*$',
    re.MULTILINE,
)
HTTP_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
USER_ID_FIELDS = {"uid", "userId", "brokerUserId"}
MILLISECOND_FIELD_RE = re.compile(r"timestamp$", re.IGNORECASE)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def mdx_pages(language: str) -> dict[str, Path]:
    root = ROOT / language
    return {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*.mdx")
    }


def normalized_navigation(language: dict) -> list:
    tabs = []
    for tab in language.get("tabs", []):
        sections = tab.get("groups") or tab.get("menu") or []
        normalized_sections = []
        for section in sections:
            if "groups" in section:
                normalized_sections.append(
                    {
                        "kind": "menu",
                        "groups": [
                            [
                                re.sub(r"^(cn|en)/", "", page)
                                for page in group.get("pages", [])
                            ]
                            for group in section["groups"]
                        ],
                    }
                )
            else:
                normalized_sections.append(
                    {
                        "kind": "group",
                        "pages": [
                            re.sub(r"^(cn|en)/", "", page)
                            for page in section.get("pages", [])
                        ],
                    }
                )
        tabs.append(normalized_sections)
    return tabs


def navigation_pages(language: dict) -> list[str]:
    pages: list[str] = []
    for tab in language.get("tabs", []):
        for section in tab.get("groups") or tab.get("menu") or []:
            if "groups" in section:
                for group in section["groups"]:
                    pages.extend(group.get("pages", []))
            else:
                pages.extend(section.get("pages", []))
    return pages


def contract_shape(value):
    if isinstance(value, list):
        return [contract_shape(item) for item in value]
    if isinstance(value, dict):
        ignored = {"description", "example", "examples", "summary", "tags", "title"}
        return {
            key: contract_shape(item)
            for key, item in value.items()
            if key not in ignored
        }
    return value


def operation_exists(spec: dict, kind: str, target: str) -> bool:
    if kind == "webhook":
        return target in spec.get("webhooks", {})
    if kind not in HTTP_METHODS:
        return False
    return kind.lower() in spec.get("paths", {}).get(target, {})


def validate_scalar_contracts(spec: dict, spec_path: str, errors: list[str]) -> None:
    """Validate cross-language JSON rules that protect JavaScript clients."""

    def visit(value, location: str) -> None:
        if isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, f"{location}[{index}]")
            return
        if not isinstance(value, dict):
            return

        properties = value.get("properties")
        if isinstance(properties, dict):
            for name, schema in properties.items():
                if not isinstance(schema, dict):
                    continue
                field_location = f"{location}.properties.{name}"
                if name in USER_ID_FIELDS and schema.get("type") != "string":
                    fail(
                        errors,
                        f"{spec_path}: {field_location} must use type string",
                    )
                if MILLISECOND_FIELD_RE.search(name) and (
                    schema.get("type"),
                    schema.get("format"),
                ) != ("integer", "int64"):
                    fail(
                        errors,
                        f"{spec_path}: {field_location} must use integer/int64 "
                        "Unix milliseconds",
                    )

        parameter_name = value.get("name")
        if (
            isinstance(parameter_name, str)
            and parameter_name in USER_ID_FIELDS
            and isinstance(value.get("schema"), dict)
        ):
            if value["schema"].get("type") != "string":
                fail(
                    errors,
                    f"{spec_path}: {location}.schema must use type string "
                    f"for {parameter_name}",
                )

        for key, item in value.items():
            visit(item, f"{location}.{key}")

    visit(spec, "$")


def validate() -> list[str]:
    errors: list[str] = []
    cn_pages = mdx_pages("cn")
    en_pages = mdx_pages("en")

    if set(cn_pages) != set(en_pages):
        for page in sorted(set(cn_pages) - set(en_pages)):
            fail(errors, f"missing English page: {page}")
        for page in sorted(set(en_pages) - set(cn_pages)):
            fail(errors, f"English-only page: {page}")

    docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    languages = docs["navigation"]["languages"]
    by_language = {item["language"]: item for item in languages}
    chinese = by_language["zh-Hans"]
    english = by_language["en"]
    if normalized_navigation(chinese) != normalized_navigation(english):
        fail(errors, "Chinese and English navigation page order or grouping differs")

    for language_key, language in (("cn", chinese), ("en", english)):
        seen: set[str] = set()
        for page in navigation_pages(language):
            if page in seen:
                fail(errors, f"duplicate {language_key} navigation page: {page}")
            seen.add(page)
            page_path = ROOT / f"{page}.mdx"
            if not page_path.exists():
                fail(errors, f"missing navigation page: {page}")

    for relative in sorted(set(cn_pages) & set(en_pages)):
        cn_content = cn_pages[relative].read_text(encoding="utf-8")
        en_content = en_pages[relative].read_text(encoding="utf-8")
        if CJK_RE.search(en_content):
            fail(errors, f"English page contains Chinese text: {relative}")

        cn_ref = OPENAPI_RE.search(cn_content)
        en_ref = OPENAPI_RE.search(en_content)
        if bool(cn_ref) != bool(en_ref):
            fail(errors, f"OpenAPI frontmatter exists in only one locale: {relative}")
            continue
        if not cn_ref:
            continue
        if (
            cn_ref.group("kind"),
            cn_ref.group("target"),
        ) != (
            en_ref.group("kind"),
            en_ref.group("target"),
        ):
            fail(errors, f"OpenAPI operation differs between locales: {relative}")

        for locale, reference in (("cn", cn_ref), ("en", en_ref)):
            spec_path = ROOT / reference.group("file").lstrip("/")
            if not spec_path.exists():
                fail(errors, f"{locale} page references missing OpenAPI file: {relative}")
                continue
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            if not operation_exists(spec, reference.group("kind"), reference.group("target")):
                fail(
                    errors,
                    f"{locale} page references missing operation "
                    f"{reference.group('kind')} {reference.group('target')}: {relative}",
                )

    for chinese_path, english_path in (
        ("openapi/b/openapi.json", "openapi/b/openapi.en.json"),
        ("openapi/b/webhooks.json", "openapi/b/webhooks.en.json"),
        ("openapi/c/openapi.json", "openapi/c/openapi.en.json"),
    ):
        chinese_content = (ROOT / chinese_path).read_text(encoding="utf-8")
        chinese_spec = json.loads(chinese_content)
        english_content = (ROOT / english_path).read_text(encoding="utf-8")
        if chinese_path.startswith("openapi/b/"):
            for spec_path, content in (
                (chinese_path, chinese_content),
                (english_path, english_content),
            ):
                if re.search(r'"uid"|平台用户 UID|platform user UID', content, re.IGNORECASE):
                    fail(errors, f"Broker OpenAPI exposes legacy UID terminology: {spec_path}")
        if CJK_RE.search(english_content):
            fail(errors, f"English OpenAPI contains Chinese text: {english_path}")
        english_spec = json.loads(english_content)
        if contract_shape(chinese_spec) != contract_shape(english_spec):
            fail(errors, f"OpenAPI contract shape differs: {chinese_path} vs {english_path}")
        validate_scalar_contracts(chinese_spec, chinese_path, errors)
        validate_scalar_contracts(english_spec, english_path, errors)

    return errors


def main() -> None:
    errors = validate()
    if errors:
        print("i18n validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print("i18n validation passed")


if __name__ == "__main__":
    main()
