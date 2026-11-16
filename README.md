# Linux under the Hood

**Boot, login, services and security on Linux Mint 22.x. Intermediate level. Version 01.**

A guided tour of what Linux Mint does from the power button to a working, secured desktop. For each step it names the files involved, the files you can customize, and safe commands to look at your own system before you change anything.

Author: Ángel Rodríguez Gil. Created with AI assistance (Claude Fable 5.2, Anthropic).

## What is in this repository

| Path | What it is |
|---|---|
| `index.html` | The interactive guide. One self-contained page: open it in any browser. It has step-by-step controls for blocks 1 to 3 and separate cards for blocks 4 to 6. |
| `slides/full.html` | The full slide deck (51 slides) as one web page. |
| `slides/short.html` | The short version (15 slides). |
| `slides/source/` | The generator (`gen.py`) and stylesheet (`deck.css`) that build both decks. |
| `verification/` | What was checked and how, plus the read-only script used for the checks that need `sudo`. |

The slide pages load three fonts from Google Fonts (Inter, Space Grotesk, JetBrains Mono). Offline, the browser falls back to system fonts.

## The six blocks

1. **System start-up:** UEFI firmware, Shim and GRUB, the kernel, initramfs, systemd.
2. **Login process:** LightDM greeter, PAM, systemd-logind, session scripts.
3. **User access:** the Cinnamon session, terminal and shell, running things automatically (autostart, cron, timers), logout.
4. **Services and daemons:** unit files, enabling, the target chain, timers and sockets, user services.
5. **Network and firewall:** your connection, listening ports, `ufw`, Docker and the firewall, a public Wi-Fi checklist.
6. **Hardening, alarms and audit:** SSH as a client, updates and AppArmor, accounts and sudo, logs and a desktop alarm, Timeshift and a weekly checkup.

## Scope

- Linux Mint 22.x, Cinnamon edition, LightDM login screen, X11 session, systemd.
- Checked on one Linux Mint 22.3 machine in November 2026. Other editions, versions and machines differ in the details.
- For readers who already use the terminal and know basic Unix concepts.

## How to view

- **The guide:** open `index.html` in a browser.
- **The slides:** open `slides/full.html` or `slides/short.html`. Each slide is a 1920×1080 page, scaled to the window.
- **PDF of the slides:** the slide pages include print rules (one slide per page). Printing to PDF from the browser has not been tested.
- **GitHub Pages:** if you enable Pages for this repository, `index.html` is served as the home page.

## Rebuild the slides

```bash
python3 slides/source/gen.py
```

This writes `slides/source/full/` and `slides/source/short/`. Each holds a `preview.html` (the standalone page) and a `project/` folder in the file layout used by Claude's Slides artifacts. Those folders are ignored by git.

## Verification

See [`verification/VERIFICATION.md`](verification/VERIFICATION.md) for the full list. In short:

- **Verified:** file paths and menu names, the order of the login files, defaults such as AppArmor and the firewall policy, and every look command (with and without `sudo`).
- **Tested for real:** a cron line, a systemd user timer and the desktop alarm notification.
- **Not verified:** commands that change the system, the autostart file at a real login, third-party tools (package names only), the key that opens the GRUB menu, a real WireGuard connection, and the VPN services themselves.

## Sources

- [Linux Mint 22.3 release notes](https://linuxmint.com/rel_zena.php)
- [Docker documentation: Packet filtering and firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/)
- [Docker documentation: Port publishing and mapping](https://docs.docker.com/engine/network/port-publishing/)
- [Mullvad VPN for Linux](https://mullvad.net/en/download/vpn/linux) and [Proton VPN on Linux](https://protonvpn.com/support/linux-vpn-setup)
- [TechRadar: Proton VPN no-logs audit](https://www.techradar.com/vpn/vpn-services/proton-vpn-aces-independent-no-logs-audit-for-the-fifth-consecutive-year)
- [Mullvad blog: audit of its WireGuard implementation](https://mullvad.net/nl/blog/2026/3/6/a-security-audit-of-gotatun-is-now-available)
- Read-only checks on a Linux Mint 22.3 Cinnamon machine, November 2026

## Disclaimer

Educational material, provided as is, with no warranty. Not affiliated with or endorsed by Linux Mint, Canonical, Docker or any vendor named here. Read and understand a command before you run it, and back up before you edit system files. This is a security baseline, not a guarantee.

## License

[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You may share and adapt this work, also commercially, if you give credit. See [`LICENSE.md`](LICENSE.md).

## Version history

- **Version 01** (November 2026): first public version.
