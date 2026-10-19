#!/usr/bin/env python3
"""Turn Arch's stock gtk4 PKGBUILD into the gtk4-live-css one.

    derive-pkgbuild.py arch/PKGBUILD > PKGBUILD

Arch's version, build options and dependency lists stay as they are. What changes:
  - it builds one package, gtk4-live-css, which provides and conflicts with gtk4.
    Arch's package_gtk4() becomes package(). The _pick calls in there already move
    the demo, docs and icon-cache files out, and the other split packages get dropped.
  - gtk4-user-css-live-reload.patch gets added to source and applied in prepare()
Every edit asserts the text it expects, so if Arch reshapes the PKGBUILD this blows up
instead of quietly building an unpatched or half-renamed package.
"""
import hashlib, re, sys
from pathlib import Path

here = Path(__file__).resolve().parent
patch = "gtk4-user-css-live-reload.patch"
s = Path(sys.argv[1]).read_text()

def once(old, new):
    global s
    assert s.count(old) == 1, f"expected exactly one match for: {old!r}"
    s = s.replace(old, new)

# one package instead of pkgbase + four split packages
m = re.search(r"^pkgbase=gtk4\npkgname=\(\n(?:  .*\n)+?\)\n", s, re.M)
assert m, "pkgbase=gtk4 / pkgname=( ... ) block not found"
s = s[:m.start()] + "pkgname=gtk4-live-css\n" + s[m.end():]
once('pkgdesc="GObject-based multi-platform GUI toolkit"',
     'pkgdesc="GObject-based multi-platform GUI toolkit, with the user gtk.css reloaded live"')

# add the patch to source and b2sums, apply it in prepare()
m = re.search(r"^source=\(\n(?:  .*\n)+?\)\n", s, re.M)
assert m, "source=( ... ) block not found"
s = s[:m.end() - 2] + f"  {patch}\n)\n" + s[m.end():]
b2 = hashlib.blake2b((here / patch).read_bytes(), digest_size=64).hexdigest()
m = re.search(r"^b2sums=\((?:'[0-9a-f]+'\s*)+\)", s, re.M)
assert m, "b2sums=( ... ) block not found"
s = s[:m.end() - 1] + f"\n        '{b2}')" + s[m.end():]
once("prepare() {\n  cd gtk\n", f"prepare() {{\n  cd gtk\n  patch -Np1 -i ../{patch}\n")

# package_gtk4() becomes package() and stands in for gtk4
once("package_gtk4() {\n", "package() {\n")
once("  provides=(libgtk-4.so)\n",
     '  provides=("gtk4=$epoch:$pkgver" libgtk-4.so)\n  conflicts=(gtk4)\n')
for fn in ("gtk4-demos", "gtk4-docs", "gtk-update-icon-cache"):
    m = re.search(rf"^package_{re.escape(fn)}\(\) \{{\n.*?^\}}\n\n?", s, re.M | re.S)
    assert m, f"package_{fn}() not found"
    s = s[:m.start()] + s[m.end():]

sys.stdout.write(s)
