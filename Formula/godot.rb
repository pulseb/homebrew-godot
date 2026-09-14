class Godot < Formula
  desc "Free and open source 2D and 3D game engine"
  homepage "https://godotengine.org/"
  version "4.7.2"
  license "MIT"

  on_intel do
    url "https://github.com/godotengine/godot/releases/download/#{version}-stable/Godot_v#{version}-stable_linux.x86_64.zip"
    sha256 "cadd3204e728a35d3f13adb7fd0d7902636b79f6b95c40c265eb73b6c35329e4"
  end

  on_arm do
    url "https://github.com/godotengine/godot/releases/download/#{version}-stable/Godot_v#{version}-stable_linux.arm64.zip"
    sha256 "5dd0d86405cf7e8adf79fb6377b38ba682a2846cb378ffe5364f38c01ad29b9d"
  end

  livecheck do
    url "https://github.com/godotengine/godot/releases/latest"
    strategy :github_latest
    regex(/^v?(\d+(?:\.\d+)+)-stable$/i)
  end

  def install
    bin.install Dir["Godot_v*-stable_linux.*"].first => "godot"
  end

  def caveats
    <<~EOS
      The editor binary requires a display server (Wayland/X11).
      For CLI-only usage, run: godot --headless
    EOS
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/godot --version")
  end
end
