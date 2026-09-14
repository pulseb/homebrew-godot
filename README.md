# Godot Brew

Homebrew packaging for the latest stable Godot 4 release on Linux.

The goal is to make Godot available through the familiar Homebrew workflow:

```bash
brew install godot
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

Add the tap and install (the tap name stays `pulseb/godot-brew`; the GitHub
repository is named `homebrew-godot` per Homebrew's tap convention):

```bash
brew tap pulseb/godot-brew https://github.com/pulseb/homebrew-godot
brew install godot
```

Homebrew 7+ may ask you to trust the tap first:

```bash
brew trust pulseb/godot-brew
```

## Automation

A daily GitHub Actions workflow (`update-formula.yml`) checks the latest
`4.x.y-stable` release from the [godotengine/godot](https://github.com/godotengine/godot)
GitHub API, downloads the Linux x86_64/arm64 archives to compute their
SHA-256 checksums, and pushes the updated formula to `main`. No self-hosted
runner or server is needed — GitHub-hosted runners are free for public
repositories. The workflow lives in `.github/workflows/` and can also be
triggered manually via `workflow_dispatch`.

The update script is [`scripts/update_formula.py`](scripts/update_formula.py)
(Python 3.12+, standard library only); asset URLs use `#{version}`
interpolation so only the `version` line and the two `sha256` lines ever
change.

## Architecture support

The formula ships the official binaries for `x86_64` (Intel/AMD) and
`arm64` (ARM) Linux. The `x86_32`/`arm32` and `.NET` (mono) variants are out
of scope for now.

## Formula outline

The formula should use the official Godot 4 Linux archive and select the
correct archive for the host architecture. The URL and SHA-256 value must be
updated for each upstream release.

```ruby
class Godot < Formula
	desc "Free and open source 2D and 3D game engine"
	homepage "https://godotengine.org/"
	license "MIT"

	on_intel do
		url "https://github.com/godotengine/godot/releases/download/4.x.y-stable/Godot_v4.x.y-stable_linux.x86_64.zip"
		sha256 "REPLACE_WITH_RELEASE_SHA256"
	end

	on_arm do
		url "https://github.com/godotengine/godot/releases/download/4.x.y-stable/Godot_v4.x.y-stable_linux.arm64.zip"
		sha256 "REPLACE_WITH_RELEASE_SHA256"
	end

	livecheck do
		url :stable
		regex(%r{/tag/(4\.\d+\.\d+)-stable}i)
	end

	def install
		bin.install Dir["Godot_v*-stable_linux.*"].first => "godot"
	end

	test do
		assert_match "4.", shell_output("#{bin}/godot --version")
	end
end
```

The final formula must use the exact archive names and checksums published by
Godot. Release automation should update the version, URLs, checksums, and
`livecheck` expectations together.

## Requirements

- Linux with Homebrew for Linux installed.
- A supported host architecture published by Godot.
- The runtime libraries required by the Godot editor, including a working
	display server for graphical use.

## Development

Validate changes locally before pushing:

```bash
brew install --build-from-source Formula/godot.rb  # or via a local tap
brew test godot
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