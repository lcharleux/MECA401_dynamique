"""Reject incomplete static exports before serving them (standard library only)."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"img", "script"} and attrs.get("src"):
            self.urls.append(attrs["src"])
        if tag == "link" and attrs.get("href"):
            if set(attrs.get("rel", "").split()) & {
                "stylesheet", "icon", "preload", "modulepreload"
            }:
                self.urls.append(attrs["href"])


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("--base-url", default="", help="Préfixe URL du dépôt")
    base = args.parse_args().base_url.rstrip("/")
    root = Path(__file__).resolve().parents[1] / "_build" / "html"
    if not (root / "index.html").is_file():
        raise SystemExit("Export absent : exécuter make build.")
    missing = set()
    checked = set()
    pages = list(root.rglob("index.html"))
    for page in pages:
        parser = Assets()
        parser.feed(page.read_text(encoding="utf-8"))
        for url in parser.urls:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            path = unquote(parts.path)
            if base and path.startswith("/"):
                if not path.startswith(base + "/"):
                    missing.add(f"Préfixe {base} absent : {url}")
                    continue
                path = path[len(base):]
            asset = root / path.lstrip("/") if path.startswith("/") else page.parent / path
            checked.add(asset)
            if not asset.is_file() or asset.stat().st_size == 0:
                missing.add(url)
    if missing:
        raise SystemExit(
            "Export incomplet : ressources absentes. Relancer make build et corriger son erreur.\n"
            + "\n".join(sorted(missing))
        )
    print(f"Export vérifié : {len(pages)} pages, {len(checked)} ressources locales présentes.")


if __name__ == "__main__":
    main()
