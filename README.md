# Termux Chromium

Chromium browser package for Termux (aarch64) — Chromium **v146.0.7680.177** packaged as a `.deb`, with a one-command setup script that prepares a full browser-automation environment on Android/Termux.

## Quick start

In Termux:

```bash
git clone https://github.com/AbdulQayoomBoohar/termuxchromium.git
cd termuxchromium
python setup_termux.py
```

## What the setup script does

`setup_termux.py` runs the whole install end to end:

1. Updates the Termux package repositories (`pkg update`)
2. Installs `x11-repo`
3. Installs Xvfb (`xvfb` and `xorg-server-xvfb`) for headless display support
4. Installs Python
5. Installs Python libraries: `flask`, `pyppeteer`, `requests`
6. Downloads `chromium_146.0.7680.177-1_aarch64.deb` from this repo's GitHub Releases
7. Installs the `.deb` (with a `dpkg` + fix-broken fallback)
8. Locks the Chromium version with `apt-mark hold chromium` so updates cannot break the setup

## Requirements

- Termux on an **aarch64** (64-bit ARM) Android device
- Internet connection for package and `.deb` downloads
- Enough free storage for Chromium and the X11/Python packages

## Notes

- The Chromium version is pinned on purpose: browser-automation setups break when the browser updates unexpectedly, so the script holds the package after install.
- If the `.deb` is already downloaded, the script skips the download step.

## Author

**Abdul Qayoom Boohar** — [GitHub](https://github.com/AbdulQayoomBoohar) · [Telegram](https://t.me/chaipiyo)
