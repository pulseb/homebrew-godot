# homebrew-godot

Homebrew tap installing the latest stable Godot 4 release on Linux.

The goal is to make Godot available through the familiar Homebrew workflow:

```bash
brew install pulseb/godot/godot
```

After installation, launch the editor with:

```bash
godot
```

## Scope

- Linux only for the first release.
- Godot 4.x stable releases only.
- The formula tracks the latest stable Godot 4 release through Homebrew's
	`livecheck` mechanism.
- Both the Godot editor and command-line executable are provided by the
	installation.

## Installation

```bash
brew tap pulseb/godot
brew install pulseb/godot/godot
```

The tap name is `pulseb/godot`: Homebrew derives it from the repository name
`homebrew-godot` by stripping the `homebrew-` prefix.

Homebrew 7+ may ask you to trust the tap first:

```bash
brew trust pulseb/godot
```

## Automation

A daily GitHub Actions workflow (`.github/workflows/update-formula.yml`)
checks the latest `4.x.y-stable` release from the
[godotengine/godot](https://github.com/godotengine/godot) GitHub API,
downloads the Linux x86_64/arm64 archives to compute their SHA-256 checksums,
and pushes the updated formula to `main`.

The update script is [`scripts/update_formula.py`](scripts/update_formula.py)
(Python 3.12+, standard library only); asset URLs use `#{version}`
interpolation so only the `version` line and the two `sha256` lines ever
change. The workflow runs on free GitHub-hosted runners and can also be
triggered manually via `workflow_dispatch`.

## Architecture support

The formula ships the official binaries for `x86_64` (Intel/AMD) and
`arm64` (ARM) Linux. The `x86_32`/`arm32` and `.NET` (mono) variants are out
of scope for now.

## Formula outline

The formula installs the official Godot binaries (no build from source). It
declares per-architecture `on_intel` / `on_arm` blocks with `#{version}`
interpolated URLs, computes nothing at install time, and only the `version`
line and the two `sha256` values change between releases.

See [`Formula/godot.rb`](Formula/godot.rb) for the actual formula.

## Requirements

- Linux with Homebrew for Linux installed.
- A supported host architecture published by Godot.
- The runtime libraries required by the Godot editor, including a working
	display server for graphical use.

## Development

Validate changes locally before pushing:

```bash
brew install --build-from-source Formula/godot.rb
brew test pulseb/godot/godot
```

The update script can be run manually against a formula copy:

```bash
python3 scripts/update_formula.py /path/to/godot.rb
```

The package should remain a binary distribution: building the full Godot
engine from source is outside the scope of this tap.

## License

This packaging project follows the license of its own repository. Godot is
distributed under the terms described in the official Godot repository:
<https://github.com/godotengine/godot/blob/master/LICENSE.txt>.