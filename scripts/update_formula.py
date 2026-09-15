#!/usr/bin/env python3
"""Update the Godot formulae to the latest stable release of each series.

For each formula in Formula/ (godot4.rb tracks the 4.x series, godot3.rb the
3.x series), fetches the latest matching stable release from the GitHub API,
downloads the Linux archives to compute their SHA-256 checksums (GitHub does
not publish checksum files for these assets), and rewrites the formula in
place. Asset URLs use `#{version}` interpolation, so only the `version` line
and the `sha256` lines ever change; the URL templates themselves identify the
archives to hash. Exits 0 without touching a formula when it is already up
to date or when no matching release exists.

Usage: update_formula.py [formula_path ...]
"""

import hashlib
import json
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

REPO = "godotengine/godot"
PER_PAGE = 100
MAX_PAGES = 10
TAG_STABLE_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)-stable$")
VERSION_RE = re.compile(r'version "([^"]+)"')
URL_RE = re.compile(r'url "(https://[^"]+\.zip)"')


@dataclass(frozen=True)
class Formula:
    """A formula file and the release series (major) it tracks."""

    path: Path
    major: int
    urls: tuple[str, ...]


def load_formula(path: Path) -> Formula | None:
    """Read the tracked major version and zip url templates from a formula."""
    text = path.read_text()
    version = VERSION_RE.search(text)
    if not version or not (match := re.match(r"(\d+)\.", version.group(1))):
        return None
    urls = tuple(URL_RE.findall(text))
    if not urls:
        return None
    return Formula(path=path, major=int(match.group(1)), urls=urls)


def api(url: str) -> object:
    request = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def latest_stable_tag(major: int) -> str | None:
    """Latest x.y.z-stable tag for the given major series, or None."""
    for page in range(1, MAX_PAGES + 1):
        releases = api(
            f"https://api.github.com/repos/{REPO}/releases"
            f"?per_page={PER_PAGE}&page={page}"
        )
        for release in releases:
            match = TAG_STABLE_RE.match(release["tag_name"])
            if match and int(match.group(1)) == major:
                return release["tag_name"]
        if len(releases) < PER_PAGE:
            break
    return None


def sha256_of(url: str) -> str:
    digest = hashlib.sha256()
    with urllib.request.urlopen(url, timeout=600) as response:
        while chunk := response.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def update_formula(text: str, tag: str, hashes: dict[str, str]) -> str:
    version = tag.removesuffix("-stable")
    text = VERSION_RE.sub(f'version "{version}"', text, count=1)
    for template, digest in hashes.items():
        anchor = re.escape(template)
        text = re.sub(
            rf'(url "{anchor}"\n\s*sha256 )"[0-9a-f]+"',
            rf'\g<1>"{digest}"',
            text,
        )
    return text


def update_formula_to(formula: Formula, tag: str) -> None:
    """Download assets for tag and rewrite the formula file in place."""
    version = tag.removesuffix("-stable")
    text = formula.path.read_text()
    current = VERSION_RE.search(text)
    if current and current.group(1) == version:
        print(f"{formula.path.name}: already at {tag}; nothing to do.")
        return

    prefix = f"https://github.com/{REPO}/releases/download/{tag}"
    hashes = {
        template: sha256_of(template.replace("#{version}-stable", tag))
        for template in formula.urls
    }

    formula.path.write_text(update_formula(text, tag, hashes))
    print(f"{formula.path.name}: updated to {tag} ({hashes})")


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    paths = (
        [Path(p) for p in sys.argv[1:]]
        if len(sys.argv) > 1
        else sorted((repo_root / "Formula").glob("*.rb"))
    )
    exit_code = 0
    for path in paths:
        formula = load_formula(path)
        if formula is None:
            print(f"{path.name}: skipped (no version or zip url found).")
            continue
        tag = latest_stable_tag(formula.major)
        if tag is None:
            print(f"{path.name}: no stable release found for series {formula.major}.x.")
            continue
        try:
            update_formula_to(formula, tag)
        except Exception as error:  # noqa: BLE001 - report and keep going
            print(f"{path.name}: FAILED to update to {tag}: {error}")
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
