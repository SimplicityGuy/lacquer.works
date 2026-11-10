#!/usr/bin/env python3
"""Validate the static site's basic HTML and local references."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.h1_count = 0
        self.title_count = 0
        self.in_title = False
        self.title_text = ""
        self.has_utf8_charset = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_by_name = dict(attrs)
        if tag == "meta" and (attrs_by_name.get("charset") or "").strip().lower() == "utf-8":
            self.has_utf8_charset = True
        if tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self.title_count += 1
            self.in_title = True

        element_id = attrs_by_name.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)

        for attribute in ("href", "src"):
            value = attrs_by_name.get(attribute)
            if value:
                self.references.append((attribute, value))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_text += data


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    page = root / "index.html"
    if not page.is_file():
        return [f"{page}: required site entry point is missing"]

    try:
        source = page.read_bytes().decode("utf-8")
    except UnicodeDecodeError as error:
        return [f"{page}: file is not valid UTF-8 ({error})"]

    parser = PageParser()
    try:
        parser.feed(source)
        parser.close()
    except Exception as error:  # HTMLParser is tolerant; report parser errors clearly.
        errors.append(f"{page}: unable to parse HTML ({error})")
        return errors

    if not parser.has_utf8_charset:
        errors.append(f"{page}: missing UTF-8 charset declaration")
    if parser.title_count != 1 or not parser.title_text.strip():
        errors.append(f"{page}: expected exactly one non-empty <title> (found {parser.title_count})")
    if parser.h1_count != 1:
        errors.append(f"{page}: expected exactly one <h1> (found {parser.h1_count})")
    for duplicate in sorted(parser.duplicate_ids):
        errors.append(f"{page}: duplicate id {duplicate!r}")

    ids_by_file = {page.resolve(): parser.ids}
    for attribute, reference in parser.references:
        parsed = urlsplit(reference)
        if parsed.scheme or parsed.netloc:
            continue

        decoded_path = unquote(parsed.path)
        if decoded_path.startswith("/"):
            target_path = (root / decoded_path.lstrip("/")).resolve()
        else:
            target_path = (page.parent / decoded_path).resolve() if decoded_path else page.resolve()
        try:
            target_path.relative_to(root.resolve())
        except ValueError:
            errors.append(f"{page}: {attribute} reference escapes the site root: {reference!r}")
            continue

        if parsed.fragment and target_path.is_dir():
            target_path = target_path / "index.html"

        if not target_path.exists():
            errors.append(f"{page}: {attribute} target does not exist: {reference!r}")
            continue

        if parsed.fragment:
            if target_path not in ids_by_file:
                try:
                    ids_by_file[target_path] = parse_page(target_path).ids
                except (UnicodeDecodeError, OSError, ValueError):
                    errors.append(f"{page}: cannot check fragment in non-HTML target: {reference!r}")
                    continue
            if unquote(parsed.fragment) not in ids_by_file[target_path]:
                errors.append(f"{page}: fragment target does not exist: {reference!r}")

    return errors


def main() -> int:
    argument_parser = argparse.ArgumentParser(description=__doc__)
    argument_parser.add_argument("site_root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = argument_parser.parse_args()

    errors = validate(args.site_root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Site check passed: UTF-8, title, one h1, unique IDs, and local references.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
