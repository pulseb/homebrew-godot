#!/usr/bin/env python3
"""Update the Godot formula to the latest stable release.

Fetches the latest stable release from the GitHub API, downloads the Linux
x86_64/arm64 archives to compute their SHA-256 checksums (GitHub does not
publish checksum files for these assets), and rewrites Formula/godot.rb in
place. Asset URLs use `#{version}` interpolation, so only the `version` line
and the two `sha256` lines ever change. Exits 0 without touching the file
when the formula is already up to date or when the latest tag is not an
x.y.z-stable release.

Usage: update_formula.py [formula_path]
"""

import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

REPO = "godotengine/godot"
# on_intel block hosts the x86_64 asset, on_arm hosts the arm64 asset.
ARCH_BY_BLOCK = {"intel": "x86_64", "arm": "arm64"}
TAG_RE = re.compile(r"^(\d+\.\d+\.\d+)-stable$")
VERSION_RE = re.compile(r'version "[^"]+"')
SHA_RE = r'(on_{block} do.*?sha256 )"[0-9a-f]+"'


def api_latest() -> dict:
    url = f"https://api.github.com/repos/{REPO}/releases/latest"
    request = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def sha256_of(url: str) -> str:
    digest = hashlib.sha256()
    with urllib.request.urlopen(url, timeout=300) as response:
        while chunk := response.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def update_formula(text: str, tag: str, hashes: dict[str, str]) -> str:
    version = tag.removesuffix("-stable")
    text = VERSION_RE.sub(f'version "{version}"', text)
    for block, arch in ARCH_BY_BLOCK.items():
        text = re.sub(
            SHA_RE.format(block=block),
            rf'\g<1>"{hashes[arch]}"',
            text,
            count=1,
            flags=re.DOTALL,
        )
    return text


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    formula = Path(sys.argv[1]) if len(sys.argv) > 1 else repo_root / "Formula/godot.rb"
    text = formula.read_text()

    match = TAG_RE.match(api_latest()["tag_name"])
    if not match:
        print("Latest release is not an x.y.z-stable tag; nothing to do.")
        return 0
    tag = match.group(0)

    current = VERSION_RE.search(text)
    if current and current.group(0) == f'version "{tag.removesuffix("-stable")}"':
        print(f"Formula already at {tag}; nothing to do.")
        return 0

    prefix = f"https://github.com/{REPO}/releases/download/{tag}"
    hashes = {
        arch: sha256_of(f"{prefix}/Godot_v{tag}_linux.{arch}.zip")
        for arch in ARCH_BY_BLOCK.values()
    }

    formula.write_text(update_formula(text, tag, hashes))
    print(f"Formula updated to {tag}: {hashes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
