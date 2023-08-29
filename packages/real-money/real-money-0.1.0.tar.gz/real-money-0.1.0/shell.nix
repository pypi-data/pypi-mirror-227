with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "pip-env";
  buildInputs = [
    # System requirements.
    stdenv.cc.cc.lib
    readline
    gettext
    lzma
    xz
    zlib

    # Python requirements (enough to get a virtualenv going).
    python311Full
    python311Packages.virtualenv
    python311Packages.pip
    python311Packages.future
    python311Packages.setuptools
    python311Packages.wheel
  ];
  src = null;
  shellHook = ''
    # Allow the use of wheels.
    SOURCE_DATE_EPOCH=$(date +%s)

    # Augment the dynamic linker path
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${stdenv.cc.cc.lib}/lib/:/run/opengl-driver/lib/:${R}/lib/R/lib:${readline}/lib:${zlib}/lib/
  '';
}
