#!/usr/bin/env python3
"""
Termux Setup Script
Installs X11 dependencies, Python libraries, downloads Chromium v146 aarch64,
installs the .deb package, and marks the package on hold to prevent updates.
"""

import os
import sys
import subprocess
import urllib.request
import shutil

CHROMIUM_URL = "https://github.com/AbdulQayoomBoohar/termuxchromium/releases/download/v146.0.7680.177/chromium_146.0.7680.177-1_aarch64.deb"
DEB_FILENAME = "chromium_146.0.7680.177-1_aarch64.deb"

def run(cmd, check=True):
    print(f"\n[+] Running: {cmd}")
    res = subprocess.run(cmd, shell=True)
    if check and res.returncode != 0:
        print(f"[-] Command failed with exit code {res.returncode}: {cmd}")
        sys.exit(res.returncode)
    return res.returncode

def download_file(url, output_path):
    print(f"\n[+] Downloading {url} -> {output_path}...")
    def reporthook(blocknum, blocksize, totalsize):
        read = blocknum * blocksize
        if totalsize > 0:
            percent = min(100.0, read * 100.0 / totalsize)
            mb_read = read / (1024 * 1024)
            mb_total = totalsize / (1024 * 1024)
            print(f"\r    Progress: {percent:.1f}% ({mb_read:.1f}/{mb_total:.1f} MB)", end="", flush=True)
    urllib.request.urlretrieve(url, output_path, reporthook=reporthook)
    print("\n[+] Download finished.")

def main():
    print("========================================")
    print("       Termux Chromium Environment Setup ")
    print("========================================")

    # 1. Update pkg repositories
    print("\n--- Step 1: Updating package repository ---")
    run("pkg update -y")

    # 2. Install x11-repo
    print("\n--- Step 2: Installing x11-repo ---")
    run("pkg install -y x11-repo")

    # 3. Install xvfb and xorg-server-xvfb
    print("\n--- Step 3: Installing xvfb and xorg-server-xvfb ---")
    run("pkg install -y xvfb xorg-server-xvfb")

    # 4. Install python (if not already installed)
    print("\n--- Step 4: Ensuring python & dependencies ---")
    run("pkg install -y python")

    # 5. Install Python libraries
    print("\n--- Step 5: Installing Python libraries (flask, pyppeteer, requests) ---")
    run("pip install --upgrade pip", check=False)
    run("pip install flask pyppeteer requests")

    # 6. Download Chromium deb package
    print("\n--- Step 6: Downloading Chromium package ---")
    if not os.path.exists(DEB_FILENAME):
        download_file(CHROMIUM_URL, DEB_FILENAME)
    else:
        print(f"[!] {DEB_FILENAME} already exists, skipping download.")

    # 7. Install Chromium .deb
    print("\n--- Step 7: Installing Chromium .deb package ---")
    # apt install handles local dependencies better than dpkg -i directly
    ret = run(f"apt install -y ./{DEB_FILENAME}", check=False)
    if ret != 0:
        print("[!] Trying dpkg -i fallback with apt-get fix-broken...")
        run(f"dpkg -i ./{DEB_FILENAME}", check=False)
        run("apt-get install -f -y")

    # 8. Lock Chromium version
    print("\n--- Step 8: Locking Chromium version to prevent updates ---")
    run("apt-mark hold chromium")

    print("\n========================================")
    print("   Setup Complete! Chromium is locked!  ")
    print("========================================")

if __name__ == "__main__":
    main()
