class GodotAT3 < Formula
  desc "Free and open source 2D and 3D game engine (3.x LTS series)"
  homepage "https://godotengine.org/"
  version "3.6.3"
  license "MIT"

  # No livecheck block: github_latest would track the 4.x series. Updates
  # for the 3.x series are handled by scripts/update_formula.py, which
  # filters release tags to 3.x.

  if Hardware::CPU.intel?
    url "https://github.com/godotengine/godot/releases/download/#{version}-stable/Godot_v#{version}-stable_x11.64.zip"
    sha256 "9080483f1f9b1d05d6fb92d87a6cdae8d5aad5f52ae76ab1208759aa271b2895"
  else
    url "https://github.com/godotengine/godot/releases/download/#{version}-stable/Godot_v#{version}-stable_linux.arm64.zip"
    sha256 "63560002586ea1ebf534d2f2543808c512bc555312ee8342629e030c27c54647"
  end

  def install
    bin.install Dir["Godot_v*-stable_x11.64", "Godot_v*-stable_linux.arm64"].first => "godot3"
  end

  def caveats
    <<~EOS
      Godot 3.x is maintained for legacy projects only; new projects should
      use the godot@4 formula. This formula installs the binary as `godot3`
      so it can coexist with the godot@4 formula.
    EOS
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/godot3 --version")
  end
end
