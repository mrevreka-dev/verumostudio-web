"""Site içindeki href/src bağlantılarının gerçekten var olan dosyalara gittiğini doğrular."""
import pathlib
import re
import sys
from urllib.parse import urlsplit, unquote

ROOT = pathlib.Path(__file__).resolve().parents[2]
ATTR = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', re.I)


def hedef_var(sayfa: pathlib.Path, url: str) -> bool:
    parca = urlsplit(url)
    if parca.scheme or parca.netloc or url.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return True
    yol = unquote(parca.path)
    if not yol:
        return True
    aday = (ROOT / yol.lstrip("/")) if yol.startswith("/") else (sayfa.parent / yol)
    return aday.is_file() or (aday / "index.html").is_file() or aday.with_suffix(".html").is_file()


def main() -> int:
    hatalar = []
    for sayfa in sorted(ROOT.rglob("*.html")):
        if ".git" in sayfa.parts:
            continue
        for url in ATTR.findall(sayfa.read_text(encoding="utf-8", errors="replace")):
            if "{{" in url or "${" in url:
                continue
            if not hedef_var(sayfa, url.strip()):
                hatalar.append(f"{sayfa.relative_to(ROOT)} -> {url}")
    for h in hatalar:
        print("KIRIK:", h)
    print(f"{len(hatalar)} kırık bağlantı")
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main())
