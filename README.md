# homebrew-godot

Homebrew tap installing the latest stable Godot releases on Linux, for both
the 4.x and 3.x series:

```bash
brew install pulseb/godot/godot@4   # latest 4.x, binary: godot4
brew install pulseb/godot/godot@3   # latest 3.x, binary: godot3
```

After installation, launch the editor with:

```bash
godot4    # or `godot`, an alias for godot@4
godot3
```

## Scope

- Linux only.
- `godot@4` tracks the latest stable Godot 4.x release through Homebrew's
	`livecheck` mechanism; `godot@3` tracks the 3.x series for legacy
	projects (maintained by the update script, see below).
- Both the Godot editor and command-line executable are provided by each
	installation; the binaries can coexist side by side.

## Installation

```bash
brew tap pulseb/godot
brew install pulseb/godot/godot@4   # and/or pulseb/godot/godot@3
```

The tap name is `pulseb/godot`: Homebrew derives it from the repository name
`homebrew-godot` by stripping the `homebrew-` prefix.

Homebrew 7+ may ask you to trust the tap first:

```bash
brew trust pulseb/godot
```

## Automation

A daily GitHub Actions workflow (`.github/workflows/update-formula.yml`)
checks the latest `x.y.z-stable` release of each series (4.x, 3.x) from the
[godotengine/godot](https://github.com/godotengine/godot) GitHub API,
downloads the Linux archives to compute their SHA-256 checksums, and pushes
the updated formulae to `main`.

The update script is [`scripts/update_formula.py`](scripts/update_formula.py)
(Python 3.12+, standard library only); asset URLs use `#{version}`
interpolation so only the `version` line and the `sha256` lines ever change.
The workflow runs on free GitHub-hosted runners and can also be triggered
manually via `workflow_dispatch`.

## Architecture support

Both formulae ship the official binaries for `x86_64` (Intel/AMD) and
`arm64` (ARM) Linux. The 32-bit and `.NET` (mono) variants are out of scope
for now. Godot 3.x publishes a native `arm64` editor build; the x86_64
formula uses the `x11.64` archive.

## Formula outline

Each formula installs the official Godot binaries (no build from source). It
declares `x86_64`/`arm64` archives via `Hardware::CPU` conditionals with
`#{version}` interpolated URLs, computes nothing at install time, and only
the `version` line and the `sha256` values change between releases.

See [`Formula/godot@4.rb`](Formula/godot@4.rb) and
[`Formula/godot@3.rb`](Formula/godot@3.rb) for the actual formulae.

## Requirements

- Linux with Homebrew for Linux installed.
- A supported host architecture published by Godot.
- The runtime libraries required by the Godot editor, including a working
	display server for graphical use.

## Development

Validate changes locally before pushing:

```bash
brew install --build-from-source Formula/godot@4.rb
brew install --build-from-source Formula/godot@3.rb
brew test pulseb/godot/godot@4
brew test pulseb/godot/godot@3
```

The update script can be run manually against formula copies:

```bash
python3 scripts/update_formula.py '/path/to/godot@4.rb' '/path/to/godot@3.rb'
```

The package should remain a binary distribution: building the full Godot
engine from source is outside the scope of this tap.

## License

This packaging project follows the license of its own repository. Godot is
distributed under the terms described in the official Godot repository:
<https://github.com/godotengine/godot/blob/master/LICENSE.txt>.