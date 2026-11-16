# Verification

What was checked for Version 01, how, and what was left unchecked. All checks ran on one machine: Linux Mint 22.3 "Zena", Cinnamon edition, X11 session, in November 2026. One machine is not every machine.

## Verified by reading the system (no changes made)

- **Paths:** the files and folders named in the guide exist where it says, including the LightDM, GRUB, initramfs, systemd, NetworkManager, ufw, apt, AppArmor and Timeshift paths.
- **Mint menu names:** Login Window, Firewall Configuration, Backup Tool, Timeshift, Update Manager, Software Sources, Startup Applications, Screensaver, Network.
- **Login file order:** read from `/usr/sbin/lightdm-session` and `/etc/X11/Xsession.d/`.
- **Defaults on the test machine:** AppArmor enabled, `ufw` active with "deny (incoming), allow (outgoing)", no SSH server running, keyring unlock present in `/etc/pam.d/lightdm`.
- **Look commands without sudo:** 32 of 36 commands ran with exit code 0. The other four behaved as expected: `ssh-add -l` returns 1 when no key is loaded, `crontab -l` returns 1 when the user has no crontab, and the two `docker` commands need `sudo` unless the user is in the `docker` group.
- **Look commands with sudo:** 19 commands ran with exit code 0, using `sudo-checks.sh` in this folder.

## Tested for real, then removed

- **cron:** a crontab line fired on schedule and wrote to its log.
- **systemd user timer:** a timer with `OnCalendar=` and `Persistent=true` started its service with result "success". It fired 11 seconds after the set time: timers fire within one minute by default (`AccuracySec`).
- **Desktop alarm:** the example script ran as a systemd user service from a timer, and `notify-send` returned success. The test used a 30-day window so that it would find old journal entries.

## Syntax checked only

- **Autostart `.desktop` file:** passes `desktop-file-validate`. Not tested at a real login.
- **SSH config example:** parsed by `ssh -G`.
- **Crontab example:** passes `crontab -n` (dry run).
- **Unit file examples:** pass `systemd-analyze verify`.

## Confirmed in official documentation

- **Linux Mint 22.3:** Ubuntu Noble (24.04) base, long term support until April 2029 (Linux Mint release notes).
- **Docker and ufw:** published container ports bypass `ufw` rules (Docker documentation, "Packet filtering and firewalls").
- **VPN providers:** Mullvad and Proton VPN publish official Linux apps for Ubuntu, Debian and Fedora. Proton has a Linux Mint install guide. Mullvad does not list Mint as officially supported.

## Not verified

- **Commands that change the system:** `update-grub`, `update-initramfs -u`, `sysctl --system`, `systemctl edit`, `systemctl enable` on system units.
- **A real failed login** inside the alarm's 15-minute window.
- **Third-party tools:** `nethogs`, `nmap`, `lynis`, `fail2ban`, `dconf-editor` and Flatseal. The package names exist in the Mint 22.3 repositories and on Flathub. The tools were not installed or run.
- **The key that opens the GRUB menu** (it needs a reboot).
- **A WireGuard connection.** NetworkManager 1.46 documents the connection type and the kernel module is present, but no connection was made.
- **The VPN services themselves,** their price and their terms.
- **The audit claims about the VPN providers,** which come from press coverage and a provider blog.
- **Exporting the slides to PDF** from the browser's print dialog.

## Errors found and corrected during verification

These were wrong in earlier drafts and are fixed in Version 01:

- `/etc/lightdm/lightdm.conf` does not exist on Mint 22.3. The settings are in `/etc/lightdm/lightdm.conf.d/70-linuxmint.conf`.
- `/etc/systemd/system/default.target` does not exist by default. The default link is `/usr/lib/systemd/system/default.target`.
- Installed Cinnamon applets live in `~/.local/share/cinnamon/`, not in `~/.config/cinnamon/`.
- Saved networks are stored in `/etc/netplan/90-NM-*.yaml`, not in `/etc/NetworkManager/system-connections/`, which is empty on the test machine.
- `/etc/timeshift/timeshift.json` is readable by all users, not only by root.
- `gufw` is already installed on Mint. `dconf-editor` is not.

## The sudo script

`sudo-checks.sh` runs read-only commands with `sudo` and changes nothing. For each command it prints the exit code and the number of output lines. For a few commands it also prints the first lines. For commands whose output is personal (failed logins, containers, saved networks) it prints only the exit code and the line count. Read it before you run it:

```bash
bash verification/sudo-checks.sh
```

It writes the same lines to `sudo-checks.log` next to the script. That log is ignored by git.
