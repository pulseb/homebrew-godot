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

Once this formula is published in a Homebrew tap, users can install it with:

```bash
brew tap <tap-owner>/godot-brew
brew install godot
```

If the formula is eventually accepted into Homebrew core, the `brew tap` step
will no longer be necessary.

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

Before opening a pull request, validate the formula with Homebrew:

```bash
brew audit --strict --online Formula/godot.rb
brew install --build-from-source Formula/godot.rb
brew test godot
```

The package should remain a binary distribution: building the full Godot
engine from source is outside the scope of this tap.

## License

This packaging project follows the license of its own repository. Godot is
distributed under the terms described in the official Godot repository:
<https://github.com/godotengine/godot/blob/master/LICENSE.txt>.