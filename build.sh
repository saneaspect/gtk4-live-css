#!/usr/bin/env bash
# Build gtk4-live-css locally, the same way the workflow does.
#
#   ./build.sh            Arch's gtk4 at the version the committed PKGBUILD names
#   ./build.sh latest     Arch's current gtk4 (then commit the regenerated PKGBUILD)
#
# Needs gtk4's makedepends installed. makepkg tells you which ones are missing.
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d arch ]; then
  git clone -q https://gitlab.archlinux.org/archlinux/packaging/packages/gtk4.git arch
fi
git -C arch fetch -q --tags origin
git -C arch checkout -q -- PKGBUILD
if [ "${1:-}" = latest ]; then
  tag=$(git -C arch tag -l '[0-9]-*' --sort=version:refname | tail -1)
else
  eval "$(grep -E '^(epoch|pkgver|pkgrel)=' PKGBUILD)"
  tag="$epoch-$pkgver-$pkgrel"
fi
git -C arch checkout -q "$tag"
echo "==> Arch packaging tag $tag"

python3 derive-pkgbuild.py arch/PKGBUILD > PKGBUILD
cp PKGBUILD gtk4-user-css-live-reload.patch arch/
(cd arch && PKGDEST="$PWD/.." makepkg -Cf --noconfirm)
echo "==> built: $(ls -1 gtk4-live-css-*.pkg.tar.zst | tail -1)"
