# gtk4-live-css

Arch's `gtk4` with one fix: switch your theme and the apps you already have open switch with it. No more restarting Nautilus.

## Why does this exist?

GTK 4 reads your colors from `~/.config/gtk-4.0/gtk.css` once, when an app starts, and never again. So your bar and terminal change instantly and Nautilus just sits there in the old colors. This package is Arch's normal `gtk4` + a small patch that makes GTK watch that file and reload it the moment it changes. Same recipe, same settings, it just replaces `gtk4` and everything else treats it like the real thing.

## Install

Add this to `/etc/pacman.conf` right after the `[extra]` section:

```ini
[saneaspect]
SigLevel = Optional TrustAll
Server = https://github.com/saneaspect/gtk4-live-css/releases/download/repo
```

Then:

```sh
sudo pacman -Syu gtk4-live-css
```

pacman's gonna ask if it should swap `gtk4` for `gtk4-live-css`. Say yes, restart your GTK 4 apps once, and you're done. Normal updates pull in new builds from here on. Wanna check? Open Nautilus, switch your theme, watch it change.

## How does it stay up to date?

A script on GitHub runs once a day. If Arch shipped a new `gtk4`, it grabs Arch's recipe, adds the patch, builds it on GitHub's computers, and uploads it to the `repo` release on this page. That release is what pacman downloads from. Every run shows up under the Actions tab.

## When does it break?

Some day the GTK devs will rewrite the file the patch touches and it won't fit anymore. Then the daily build fails, uploads nothing, and GitHub emails me. Your machine keeps the last good version until I fix the patch, which also means no new GTK updates until then. That's the one real cost of a patched package.

## Build it yourself

```sh
git clone https://github.com/saneaspect/gtk4-live-css
cd gtk4-live-css
./build.sh
sudo pacman -U gtk4-live-css-*.pkg.tar.zst
```

Takes 10 to 30 minutes and it'll pin every core on your CPU to 100% until it's done (at least that's what it did for me).

## About

Personal package, made for my own machines cuz I was sick of restarting Nautilus. Use it if you want, but there's no support and the packages aren't signed.
