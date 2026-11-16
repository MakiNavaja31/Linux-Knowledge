#!/usr/bin/env python3
"""Builds the full deck and the short LinkedIn deck (Slides type file layout)."""
import html, json, os, sys, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
TITLE = "Linux under the Hood: Boot, Login, Services and Security (Intermediate Level)"
FOOT = "Linux under the Hood · Version 01 · CC BY 4.0"
warn = []


def e(s):
    return html.escape(s, quote=False)


def foot():
    return '<div class="foot"><p class="ft">%s</p><div class="pg"></div></div>' % e(FOOT)


def sec(sid, cls, body, footer=True):
    return '<section id="%s" class="%s">\n%s\n%s</section>\n' % (sid, cls, body, foot() if footer else "")


def head(eyebrow, title):
    if len(title) > 50:
        warn.append("title long (%d): %s" % (len(title), title))
    return '<p class="eyebrow">%s</p>\n<h2>%s</h2>' % (e(eyebrow), e(title))


def items(lst):
    out = []
    for it in lst:
        p, w = it[0], it[1]
        risk = len(it) > 2 and it[2]
        if len(p) > 54:
            warn.append("path long (%d): %s" % (len(p), p))
        if len(w) > 60:
            warn.append("why long (%d): %s" % (len(w), w))
        out.append('<div class="item%s"><p class="path">%s</p><p class="why">%s</p></div>'
                   % (" risk" if risk else "", e(p), e(w + (" Risky: back up first." if risk else ""))))
    return "\n".join(out)


def cmds(label, lst):
    if not lst:
        return ""
    tot = sum(len(c) + 4 for c in lst)
    if tot > 215:
        warn.append("cmds long (%d): %s" % (tot, lst[0]))
    return '<div class="cmds"><p class="cl">%s</p>%s</div>' % (
        e(label), "".join('<p class="cmd">%s</p>' % e(c) for c in lst))


def stage(sid, eyebrow, title, lead, files, custom, look, label="Look:", alt=False):
    if len(lead) > 285:
        warn.append("lead long (%d): %s" % (len(lead), sid))
    if len(files) > 4 or len(custom) > 4:
        warn.append("too many items: " + sid)
    body = "%s\n<p class=\"lead\">%s</p>\n<div class=\"cards\">\n<div class=\"card\"><h3>Files involved</h3>\n%s\n</div>\n<div class=\"card edit\"><h3>You can customize</h3>\n%s\n</div>\n</div>\n%s" % (
        head(eyebrow, title), e(lead), items(files), items(custom), cmds(label, look))
    return sid, sec(sid, "s alt" if alt else "s", body)


def bullets(lst, cls="bul"):
    return '<ul class="%s">%s</ul>' % (cls, "".join("<li>%s</li>" % e(x) for x in lst))


def code(title, lines):
    for ln in lines:
        if len(ln) > 108:
            warn.append("code line long (%d): %s" % (len(ln), ln))
    body = "<br>".join(e(ln).replace("  ", "&#160;&#160;") if ln else "&#160;" for ln in lines)
    return '<p class="codet">%s</p>\n<p class="code">%s</p>' % (e(title), body)


def table(headers, rows, widths):
    h = "".join('<th style="width:%d%%">%s</th>' % (w, e(x)) for x, w in zip(headers, widths))
    r = "".join('<tr%s>%s</tr>' % (' class="band"' if i % 2 else "", "".join("<td>%s</td>" % e(c) for c in row))
                for i, row in enumerate(rows))
    return '<table class="t"><tr class="th">%s</tr>%s</table>' % (h, r)


def card(title, inner, cls="card"):
    return '<div class="%s"><h3>%s</h3>\n%s\n</div>' % (cls, e(title), inner)


def para(text, cls="txt"):
    return '<p class="%s">%s</p>' % (cls, e(text))


ARROW = '<x-shape kind="arrow-right" class="arr"></x-shape>'
DOWN = '<x-shape kind="arrow-down" class="arrd"></x-shape>'


def box(title, sub="", cls="box"):
    return '<div class="%s"><p class="bt">%s</p>%s</div>' % (cls, e(title), ('<p class="bs">%s</p>' % e(sub)) if sub else "")


def flow(boxes):
    return '<div class="flow">%s</div>' % ARROW.join(boxes)


CC_SVG = ('<svg aria-label="Creative Commons Attribution (CC BY) license icons" width="150" height="64" viewBox="0 0 150 64">'
          '<circle cx="32" cy="32" r="28" fill="none" stroke="#17251C" stroke-width="5"/>'
          '<path d="M29 25 a8.5 8.5 0 1 0 0 14" fill="none" stroke="#17251C" stroke-width="5"/>'
          '<path d="M46 25 a8.5 8.5 0 1 0 0 14" fill="none" stroke="#17251C" stroke-width="5"/>'
          '<circle cx="110" cy="32" r="28" fill="none" stroke="#17251C" stroke-width="5"/>'
          '<circle cx="110" cy="19" r="5.5" fill="#17251C"/>'
          '<path d="M101 28 h18 v13 h-4.5 v13 h-9 v-13 h-4.5 z" fill="#17251C"/></svg>')

# ----------------------------------------------------------------------------- shared slides

def cover(short=False):
    body = (
        '<p class="eyebrow">%s</p>\n'
        '<div class="ctitle"><h1>Linux under the Hood</h1>\n'
        '<p class="csub">Boot, Login, Services and Security</p>\n'
        '<p class="clevel">Intermediate level · Version 01 · November 2026</p></div>\n'
        '<div class="ccred"><div class="ccleft"><p class="cname">Ángel Rodríguez Gil</p>\n'
        '<p class="cby">Created with Claude Fable 5.2 (AI assistance)</p></div>\n'
        '<div class="cclic">%s<p class="cby">CC BY 4.0</p></div></div>'
    ) % (e("Short version · the essentials of Linux Mint 22.x in 15 slides" if short else "A guided tour of Linux Mint 22.x, Cinnamon edition"), CC_SVG)
    return "cover", sec("cover", "s alt cover", body, footer=False)


def verified_slide(sid, eyebrow):
    left = card("Checked on a Linux Mint 22.3 machine", bullets([
        "File and folder paths, and the Mint menu names",
        "The order in which login files are read",
        "Defaults: AppArmor on, firewall drops incoming",
        "Every look command, with and without sudo, ran without error",
        "Examples run for real in a test: the cron line, the systemd timer and the alarm notification",
    ], "bul sm"), "card edit")
    right = card("Not verified", bullets([
        "Commands that change the system were not run: update-grub, update-initramfs, sysctl --system",
        "The autostart file at a real login, and a real failed login inside the alarm’s 15-minute window",
        "Third-party tools: package names confirmed, the tools themselves not run",
        "The key that opens the GRUB menu, and a real WireGuard connection",
        "The two VPN services themselves, their price and their terms",
    ], "bul sm"))
    body = "%s\n<div class=\"cards\">%s%s</div>\n%s" % (
        head(eyebrow, "What was verified, and what was not"), left, right,
        para("One machine is not every machine. Paths and defaults can differ on other editions and versions.", "note"))
    return sid, sec(sid, "s", body)


def legal_slide(sid, eyebrow):
    left = card("Disclaimer", bullets([
        "Educational material, provided as is, with no warranty",
        "Not affiliated with or endorsed by Linux Mint, Canonical, Docker or any vendor named here",
        "Read and understand a command before you run it. Back up before you edit system files",
        "A security baseline, not a guarantee",
    ], "bul sm"))
    right = ('<div class="card edit"><h3>License and credits</h3>\n<div class="licrow">%s<p class="lictx">CC BY 4.0</p></div>\n%s\n</div>' % (
        CC_SVG, bullets([
            "You may share and adapt this work, also commercially, if you give credit",
            "Author: Ángel Rodríguez Gil",
            "Created with AI assistance: Claude Fable 5.2 (Anthropic)",
            "Version 01, November 2026",
            "creativecommons.org/licenses/by/4.0",
        ], "bul sm")))
    body = "%s\n<div class=\"cards\">%s%s</div>" % (head(eyebrow, "Disclaimer, license and credits"), left, right)
    return sid, sec(sid, "s alt", body)


def fw_slide(sid, eyebrow):
    body = "%s\n%s\n%s\n<div class=\"legend\">%s%s</div>\n%s" % (
        head(eyebrow, "Firewall: what reaches your ports"),
        para("A firewall decides which packets may reach your ports. On Mint the front end is ufw, which writes rules for nftables in the kernel. The usual home policy: deny incoming, allow outgoing.", "lead"),
        flow([box("Internet"), box("Network card", "Wi-Fi or cable"), box("Firewall", "ufw / nftables", "box hi"),
              box("Open port", "a listening socket"), box("Program", "a service")]),
        '<div class="leg"><p class="tag ok">ALLOWED</p><p class="legt">A reply to a connection you started. The firewall is stateful, so it remembers your outgoing connections.</p></div>',
        '<div class="leg"><p class="tag no">DROPPED</p><p class="legt">A new connection from outside to a port that has no allow rule.</p></div>',
        para("A firewall is a second line of defense. It does not replace turning off services you don’t need.", "note"))
    return sid, sec(sid, "s", body)


def docker_slide(sid, eyebrow):
    lane1 = '<p class="lane">Normal traffic</p>' + flow([box("Internet"), box("Network card"), box("ufw rules", "incoming filter", "box hi"), box("Open port"), box("Program")])
    lane2 = '<p class="lane warnc">Traffic to a published Docker port</p>' + flow([box("Internet"), box("Network card"), box("Docker’s own rules", "forwarding (NAT)", "box warn"), box("Container")])
    body = "%s\n%s\n%s\n%s\n%s" % (
        head(eyebrow, "Docker can go around ufw"),
        para("When you publish a port (-p 8080:80), Docker writes its own firewall rules. Traffic to that port is forwarded to the container, and a ufw “deny” does not stop it.", "lead"),
        lane1, lane2,
        para("Don’t trust “ufw status” alone for containers. Test from another machine. Source: Docker documentation, “Packet filtering and firewalls”.", "note"))
    return sid, sec(sid, "s alt", body)


AUTO_ROWS = [
    ["When you log in to the desktop", "Startup Applications, or a .desktop file in ~/.config/autostart/"],
    ["In every terminal you open", "~/.bashrc"],
    ["Once per login (variables, PATH)", "~/.profile"],
    ["On a schedule, as your user", "crontab -e, or a systemd user timer in ~/.config/systemd/user/"],
    ["On a schedule, for the whole system", "/etc/cron.d/, /etc/cron.daily/ and the other /etc/cron.* folders"],
    ["Once at every boot", "an @reboot line in your crontab, or a systemd unit"],
    ["At boot, as a background service", "a systemd unit in /etc/systemd/system/"],
    ["When a login shell exits", "~/.bash_logout"],
]


def auto_map(sid, eyebrow):
    body = "%s\n%s\n%s" % (head(eyebrow, "Run things automatically: pick the place"),
                           para("Linux can run your commands at different moments. Choose the place that matches when you want it to run.", "lead"),
                           table(["You want it to run...", "Use"], AUTO_ROWS, [38, 62]))
    return sid, sec(sid, "s", body)


WIFI = ["Firewall active with deny incoming, and no Docker container published on all addresses",
        "Sharing and discovery services off if unused: file sharing, avahi, printing (check with ss)",
        "Don’t auto-connect to open networks. Prefer WPA2 or WPA3, or your phone’s hotspot",
        "Use a VPN for anything sensitive",
        "HTTPS only. Treat a certificate warning as a stop sign",
        "Lock the screen when you step away. Turn Bluetooth off if unused",
        "Install pending updates before you travel"]

WEEKLY = ["Update Manager: install pending updates",
          "ss -tulpn: any listener you can’t explain?",
          "sudo ufw status verbose: still active, still deny incoming?",
          "sudo docker ps: any container published on 0.0.0.0?",
          "last and sudo lastb: any login you don’t recognize?",
          "journalctl -p err -b: new errors since last week?",
          "Timeshift: is the latest snapshot recent? And the backup of your home folder?",
          "ls -l ~/.ssh: permissions still 700 and 600?"]

# ----------------------------------------------------------------------------- full deck

def full():
    S = []
    S.append(cover())

    # 2.1 purpose + index
    idx = [["1", "Cover"], ["2", "Purpose and introduction to Linux Mint"], ["3", "The six blocks at a glance"],
           ["4", "Block 1 · System start-up"], ["5", "Block 2 · Login process"], ["6", "Block 3 · User access"],
           ["7", "Block 4 · Services and daemons"], ["8", "Block 5 · Network and firewall"],
           ["9", "Block 6 · Hardening, alarms and audit"], ["10", "Verification, sources, disclaimer and license"]]
    left = card("Purpose", bullets([
        "Show what Linux Mint does from the power button to a working, secured desktop",
        "Name the files involved at each step, and the ones you can customize",
        "Give safe commands to look at your own system before you change anything",
    ], "bul"), "card edit")
    right = card("Index", "".join('<div class="irow"><p class="inum">%s</p><p class="itx">%s</p></div>' % (e(a), e(b)) for a, b in idx))
    S.append(("purpose", sec("purpose", "s", "%s\n<div class=\"cards\">%s%s</div>" % (head("2.1 · Purpose and index", "Why this guide, and what is inside"), left, right))))

    # 2.2 Mint
    left = card("What it is", bullets([
        "A desktop Linux distribution based on Ubuntu LTS: Mint 22.x uses Ubuntu 24.04",
        "Its own desktop, Cinnamon, plus MATE and Xfce editions",
        "Its own tools: Update Manager, Timeshift, Backup Tool, Login Window",
        "Version 22.3 “Zena” came out in January 2026. It is a long term support release, supported until April 2029",
    ], "bul sm"))
    right = card("Scope of this guide", bullets([
        "Linux Mint 22.x, Cinnamon edition",
        "LightDM login screen, X11 session",
        "systemd as the first process",
        "Other editions and versions differ in the details",
        "For readers who already use the terminal and know basic Unix concepts",
    ], "bul sm"), "card edit")
    S.append(("mint", sec("mint", "s alt", "%s\n<div class=\"cards\">%s%s</div>\n%s" % (
        head("2.2 · Introduction", "What is Linux Mint?"), left, right,
        para("Release facts come from the Linux Mint 22.3 release notes. Scope checked on a Mint 22.3 machine.", "note")))))

    # 3.1 overview blocks 1-3
    def col(title, sub, steps, cls=""):
        return '<div class="ocol %s"><h3>%s</h3><p class="osub">%s</p>%s</div>' % (
            cls, e(title), e(sub), "".join('<p class="ostep">%s</p>' % e(s) for s in steps))
    S.append(("ov-123", sec("ov-123", "s", "%s\n<div class=\"ocols\">%s%s%s%s%s</div>\n%s" % (
        head("3.1 · Overview", "Blocks 1 to 3: from power-on to your desktop"),
        col("1 · System start-up", "Power button → login screen", ["UEFI firmware", "Shim and GRUB", "Linux kernel", "initramfs", "systemd (PID 1)"]),
        ARROW,
        col("2 · Login process", "Login screen → session scripts", ["LightDM greeter", "PAM authentication", "systemd-logind session", "Session scripts"]),
        ARROW,
        col("3 · User access", "Desktop → shell → logout", ["Cinnamon session", "Terminal and shell", "Run things automatically", "Logout"]),
        para("A linear story: each block hands over to the next. Logout returns you to the login screen of block 2.", "note")))))

    # 3.2 overview block 4
    chips = ["Unit files", "Enabling a service", "The target chain", "Other ways services start", "User services", "Not systemd: desktop autostart"]
    S.append(("ov-4", sec("ov-4", "s alt", "%s\n%s\n<div class=\"chips\">%s</div>\n<div class=\"cards\">%s%s</div>" % (
        head("3.2 · Overview", "Block 4: services and daemons"),
        para("A daemon is a background process with no terminal. A service is how systemd starts, watches and stops one. This is not a step in the story: it is a layer that runs under blocks 1 to 3.", "lead"),
        "".join('<p class="chip">%d · %s</p>' % (i + 1, e(c)) for i, c in enumerate(chips)),
        card("Starts in block 1", para("At the systemd step. System services are started on the way to graphical.target.", "txt")),
        card("Continues in block 2", para("At login, systemd-logind starts your own user manager, which runs your per-user services.", "txt"))))))

    # 3.3 overview blocks 5-6
    S.append(("ov-56", sec("ov-56", "s", "%s\n<div class=\"ocols\">%s%s</div>\n%s" % (
        head("3.3 · Overview", "Blocks 5 and 6: security"),
        col("5 · Network and firewall", "What can reach this machine?", ["Know your connection", "What is listening", "Firewall", "Docker and the firewall", "Public Wi-Fi checklist"], "wide"),
        col("6 · Hardening, alarms and audit", "Habits that keep it in good shape", ["SSH as a client", "Updates and sandboxing", "Accounts and sudo", "Logs and alarms", "Recovery and weekly checkup"], "wide"),
        para("Scenario: a home network, SSH used to connect out to other machines, Docker installed, and a laptop that sometimes joins public Wi-Fi.", "note")))))

    # ---------------- Block 1
    B = "Block 1 · System start-up"
    S.append(stage("b1-uefi", "4.1 · " + B, "UEFI firmware",
        "The firmware tests and initializes the hardware, reads its boot entries from NVRAM and loads an EFI program from the EFI System Partition (FAT32). Mint reuses Ubuntu’s folder name, so the entry is usually called “ubuntu”.",
        [("/boot/efi/EFI/ubuntu/shimx64.efi", "The first program loaded (a signed shim)"), ("/boot/efi/", "EFI System Partition, mounted here later")],
        [("Firmware setup screen", "Boot order and Secure Boot. The key depends on the maker"), ("NVRAM boot entries", "View or change them with efibootmgr")],
        ["efibootmgr", "ls /sys/firmware/efi"]))
    S.append(stage("b1-grub", "4.2 · " + B, "Shim and GRUB",
        "Shim is signed so that Secure Boot trusts it. It loads GRUB, which reads its menu, loads the kernel and the initramfs from /boot, and passes the kernel command line. The menu can be hidden (GRUB_TIMEOUT_STYLE=hidden).",
        [("/boot/grub/grub.cfg", "Generated menu. Never edit it by hand"), ("/boot/vmlinuz-*", "The kernel images"), ("/boot/initrd.img-*", "The initramfs images")],
        [("/etc/default/grub", "Timeout, hidden menu, kernel command line"), ("/etc/default/grub.d/*.cfg", "Drop-ins. Mint ships 50_linuxmint.cfg"), ("/etc/grub.d/", "Scripts that build the menu entries.", True)],
        ["cat /etc/default/grub", "sudo update-grub  (applies your changes)"], alt=True))
    S.append(stage("b1-kernel", "4.3 · " + B, "Linux kernel",
        "The kernel sets up memory and CPUs, initializes drivers and mounts the initramfs as a temporary root. It receives the command line that GRUB gave it, for example “quiet splash” and the root device.",
        [("/proc/cmdline", "The parameters the kernel received"), ("/boot/config-*", "Options the kernel was built with")],
        [("/etc/modprobe.d/*.conf", "Module options and blacklists"), ("/etc/modules-load.d/*.conf", "Modules to load at boot"), ("/etc/sysctl.d/*.conf", "Kernel runtime parameters")],
        ["cat /proc/cmdline", "uname -r", "sudo sysctl --system  (applies sysctl files)"]))
    S.append(stage("b1-initramfs", "4.4 · " + B, "initramfs",
        "A small filesystem in RAM with the drivers needed to reach the real root: disk controller, filesystem, and disk encryption if used. It mounts the root named in the command line (root=UUID=...) and then starts systemd.",
        [("/boot/initrd.img-*", "The image that is unpacked into RAM")],
        [("/etc/initramfs-tools/initramfs.conf", "Build options"), ("/etc/initramfs-tools/modules", "Extra modules to include"), ("/etc/initramfs-tools/hooks/", "Custom build hooks.", True)],
        ["ls -lh /boot/initrd.img-*", "sudo update-initramfs -u  (rebuilds the image)"], alt=True))
    S.append(stage("b1-systemd", "4.5 · " + B, "systemd (PID 1)",
        "systemd is the first process. It mounts what /etc/fstab lists and starts units in parallel, following their dependencies, until it reaches the default target. On Mint that is graphical.target, which starts LightDM.",
        [("/usr/lib/systemd/system/", "Units shipped by packages"), ("/usr/lib/systemd/system/default.target", "A link to graphical.target")],
        [("/etc/fstab", "Filesystems and swap to mount.", True), ("/etc/systemd/system/*.service", "Your own units"),
         ("/etc/systemd/system/<unit>.d/override.conf", "Safe override of a packaged unit"), ("/etc/systemd/system/default.target", "Created only by systemctl set-default")],
        ["systemctl get-default", "systemd-analyze", "systemd-analyze blame", "systemd-analyze critical-chain"]))

    # ---------------- Block 2
    B = "Block 2 · Login process"
    S.append(stage("b2-greeter", "5.1 · " + B, "LightDM greeter",
        "LightDM, the display manager, starts the X server and the greeter (slick-greeter on Mint), which draws the login screen. The sessions it offers come from the .desktop files in /usr/share/xsessions.",
        [("/etc/lightdm/lightdm.conf.d/70-linuxmint.conf", "Mint’s settings: greeter and session wrapper"), ("/usr/share/xsessions/*.desktop", "Available sessions, such as cinnamon.desktop")],
        [("/etc/lightdm/lightdm.conf.d/*.conf", "Autologin, default session, greeter choice"), ("Menu → Login Window", "Mint’s graphical tool for the login screen")],
        ["systemctl status lightdm", "ls /usr/share/xsessions", "ls /etc/lightdm/lightdm.conf.d"], alt=True))
    S.append(stage("b2-pam", "5.2 · " + B, "PAM authentication",
        "The greeter hands your user name and password to PAM (Pluggable Authentication Modules). pam_unix compares the password with the hash in /etc/shadow. Other modules apply limits and unlock the keyring with the same password.",
        [("/etc/passwd", "User names, UID, home, shell"), ("/etc/shadow", "Password hashes (root only)"), ("/etc/pam.d/lightdm", "PAM rules for the login screen"), ("/etc/pam.d/common-auth", "Shared authentication rules")],
        [("/etc/security/limits.conf and limits.d/", "Per-user resource limits"), ("/etc/pam.d/*", "A mistake here can lock you out.", True)],
        ["ls /etc/pam.d", "passwd  (changes your own password)"]))
    S.append(stage("b2-logind", "5.3 · " + B, "systemd-logind session",
        "pam_systemd registers the new session with systemd-logind. It creates the runtime directory /run/user/UID, assigns the seat and the virtual terminal, and starts your per-user systemd manager.",
        [("/run/user/<UID>/", "Per-user runtime directory, kept in RAM"), ("user@<UID>.service", "Your own “systemd --user” manager")],
        [("/etc/systemd/logind.conf", "Lid switch, idle action, session limits"), ("~/.config/systemd/user/", "Your own user services and timers")],
        ["loginctl list-sessions", "loginctl show-user $USER", "systemctl --user status"], alt=True))
    S.append(stage("b2-scripts", "5.4 · " + B, "Session scripts",
        "A wrapper, /usr/sbin/lightdm-session, loads the profile files. Then /etc/X11/Xsession runs the numbered scripts in Xsession.d, which start the agents and finally the session command: cinnamon-session-cinnamon.",
        [("/usr/sbin/lightdm-session", "The wrapper that starts the sequence"), ("/etc/profile and /etc/profile.d/*.sh", "System-wide environment"),
         ("/etc/X11/Xsession.d/", "Numbered scripts, run in order"), ("/usr/share/xsessions/cinnamon.desktop", "Names the session command")],
        [("~/.profile", "PATH and environment variables"), ("~/.xprofile", "Variables and commands for the GUI session"),
         ("~/.xsessionrc", "GUI environment, read from Xsession.d"), ("/etc/profile.d/*.sh", "System-wide additions (root)")],
        ["ls /etc/X11/Xsession.d", "cp ~/.profile ~/.profile.bak  (before you edit)"]))
    order = ["/etc/profile", "~/.profile", "/etc/xprofile", "~/.xprofile", "/etc/X11/Xsession.d/*  (among them: ~/.xsessionrc, the GPG and SSH agents)", "cinnamon-session-cinnamon"]
    left = card("Read in this order at graphical login", '<ol class="num">%s</ol>' % "".join("<li>%s</li>" % e(x) for x in order))
    right = card("Three rules", bullets([
        "Changes apply at the next login. A new terminal is not enough",
        "Never print output or run slow commands in these files",
        "A syntax error in ~/.profile can break the login. Keep a text console (Ctrl+Alt+F3) as a way back",
    ], "bul sm"), "card edit")
    S.append(("b2-order", sec("b2-order", "s alt", "%s\n<div class=\"cards\">%s%s</div>\n%s" % (
        head("5.5 · " + B, "The order of the login files"), left, right,
        para("Order read from /usr/sbin/lightdm-session on Mint 22.3. Files that don’t exist are skipped.", "note")))))

    # ---------------- Block 3
    B = "Block 3 · User access"
    S.append(stage("b3-cinnamon", "6.1 · " + B, "Cinnamon session",
        "cinnamon-session starts the window manager (Muffin), the panel with its applets, the desktop and the settings helpers. Then it launches every .desktop file in the autostart folders. Your saved settings come from dconf.",
        [("/etc/xdg/autostart/*.desktop", "System-wide autostart programs"), ("~/.config/dconf/user", "Your saved desktop settings (binary)")],
        [("~/.config/autostart/*.desktop", "Your own autostart programs"), ("~/.local/share/cinnamon/", "Applets, desklets and extensions you installed"),
         ("~/.config/cinnamon/spices/", "Settings of those applets and desklets"), ("~/.themes and ~/.icons", "Your themes and icons")],
        ["ls /etc/xdg/autostart", "cinnamon-settings  (System Settings)", "Menu → Startup Applications"]))
    left = card("Terminal window in Cinnamon", bullets([
        "A non-login, interactive shell",
        "Reads /etc/bash.bashrc and ~/.bashrc only",
        "Inherits the environment that the session set up at login",
    ], "bul sm"))
    right = card("Text console (Ctrl+Alt+F3) or SSH", bullets([
        "A login shell: getty or sshd, then login and PAM",
        "Bash reads /etc/profile, then the first one it finds of ~/.bash_profile, ~/.bash_login, ~/.profile",
        "Mint ships ~/.profile, which sources ~/.bashrc",
    ], "bul sm"))
    S.append(("b3-shell", sec("b3-shell", "s alt", "%s\n<div class=\"cards\">%s%s</div>\n%s" % (
        head("6.2 · " + B, "Terminal and shell: two kinds of shell"), left, right,
        para("Rule of thumb: variables and PATH go in ~/.profile. Aliases, prompt and functions go in ~/.bashrc.", "note big")))))
    S.append(stage("b3-shellfiles", "6.3 · " + B, "Terminal and shell: the files",
        "Bash reads different files depending on the kind of shell. Know which file you are editing and when it is read, or your change will seem to have no effect.",
        [("/etc/bash.bashrc", "System-wide settings for interactive shells"), ("/etc/profile", "System-wide settings for login shells")],
        [("~/.bashrc", "Aliases, prompt, functions, history"), ("~/.bash_aliases", "Aliases in their own file, read by the default .bashrc"),
         ("~/.bash_profile", "If it exists, login shells ignore ~/.profile.", True), ("~/.inputrc", "Readline key bindings")],
        ["source ~/.bashrc", "bash -l -c 'echo $PATH'", "echo $0"]))
    S.append(auto_map("b3-auto-map", "6.4 · " + B))
    fields = ["minute", "hour", "day of month", "month", "day of week", "command"]
    S.append(("b3-auto-cron", sec("b3-auto-cron", "s alt", "%s\n<div class=\"fields\">%s</div>\n%s\n<div class=\"cards\">%s%s</div>" % (
        head("6.5 · " + B, "cron: schedule a command"),
        "".join('<p class="field">%s</p>' % e(f) for f in fields),
        '<p class="code one">30 2 * * *  /home/me/bin/backup.sh &gt;&gt; /home/me/cron.log 2&gt;&amp;1</p>',
        card("Rules that save you time", bullets([
            "cron starts with a minimal environment: a short PATH and no desktop session. Use absolute paths",
            "Redirect the output to a log file, or you will never see the error",
            "The script needs a shebang line and chmod +x",
            "Run it by hand first. Then check the syntax with crontab -n <file>",
        ], "bul sm"), "card edit"),
        card("Alternatives", bullets([
            "A systemd user timer: logs in the journal, and Persistent=true catches up after the machine was off",
            "anacron runs the daily, weekly and monthly folders in /etc/cron.* on machines that are not always on",
            "Graphical commands such as notify-send need extra setup under cron",
        ], "bul sm"))))))
    S.append(("b3-auto-ex1", sec("b3-auto-ex1", "s", "%s\n%s\n%s\n%s" % (
        head("6.6 · " + B, "Example: a script on a schedule"),
        code("~/bin/hello-cron.sh  (a harmless test script)", ["#!/bin/bash", "echo \"$(date '+%F %T') hello from the scheduler\" >> /home/me/cron-test.log"]),
        code("crontab -e  (add these lines; replace “me” with your user name)", [
            "PATH=/usr/local/bin:/usr/bin:/bin",
            "# minute hour day-of-month month day-of-week  command",
            "*/5 * * * *  /home/me/bin/hello-cron.sh >> /home/me/cron.log 2>&1",
            "@reboot      /home/me/bin/hello-cron.sh >> /home/me/cron.log 2>&1"]),
        cmds("Create:", ["mkdir -p ~/bin", "chmod +x ~/bin/hello-cron.sh", "~/bin/hello-cron.sh", "crontab -n <file>", "crontab -e", "crontab -l"])))))
    S.append(("b3-auto-ex2", sec("b3-auto-ex2", "s alt", "%s\n<div class=\"cards\">%s%s</div>\n%s\n%s" % (
        head("6.7 · " + B, "Example: at login, and a systemd timer"),
        '<div class="half">%s</div>' % code("~/.config/autostart/my-login.desktop", ["[Desktop Entry]", "Type=Application", "Name=My login script", "Exec=/home/me/bin/hello-cron.sh", "Terminal=false"]),
        '<div class="half">%s</div>' % code("~/.config/systemd/user/hello.timer  (+ hello.service)", ["[Timer]", "OnCalendar=*-*-* 02:30:00", "Persistent=true", "[Install]", "WantedBy=timers.target"]),
        cmds("Enable:", ["systemctl --user daemon-reload", "systemctl --user enable --now hello.timer", "systemctl --user list-timers"]),
        para("hello.service holds [Service] Type=oneshot and ExecStart=%h/bin/hello-cron.sh. Tested: the cron line and the timer both fired. A timer fires within one minute of its set time by default. The autostart file was only syntax-checked.", "note")))))
    S.append(stage("b3-logout", "6.8 · " + B, "Logout",
        "Logging out ends the Cinnamon session. systemd-logind closes your session, and your user manager stops when no sessions remain, unless lingering is enabled. LightDM shows the greeter again.",
        [("~/.bash_logout", "Run by a login shell when it exits")],
        [("~/.bash_logout", "Cleanup commands, for example clear the screen"), ("loginctl enable-linger <user>", "Keeps your user services running after logout")],
        ["loginctl show-user $USER", "loginctl list-sessions"]))

    # ---------------- Block 4
    B = "Block 4 · Services and daemons"
    S.append(stage("b4-units", "7.1 · " + B, "Unit files",
        "A unit is a small text file that describes one thing systemd manages: a service, a mount, a socket, a timer or a target. systemd searches several directories. If a name exists in two of them, the higher one wins.",
        [("/usr/lib/systemd/system/", "Units shipped by packages. Don’t edit them"), ("/run/systemd/system/", "Runtime and generated units, gone after a reboot")],
        [("/etc/systemd/system/", "Your units and the enable links. Highest priority"), ("/etc/systemd/system/<unit>.d/override.conf", "Safe way to change a packaged unit")],
        ["systemctl cat cron.service", "systemctl show -p UnitPath --value", "sudo systemctl edit <unit>  (creates an override)"], alt=True))
    S.append(("b4-enable", sec("b4-enable", "s", "%s\n%s\n<div class=\"linkd\"><p class=\"code one\">/etc/systemd/system/multi-user.target.wants/cron.service</p>%s<p class=\"code one\">/usr/lib/systemd/system/cron.service</p></div>\n%s\n%s" % (
        head("7.2 · " + B, "Enabling a service"),
        para("A service starts at boot because of a symlink in a .wants directory. “systemctl enable” creates the link and “disable” removes it. The unit’s [Install] section says where it goes: WantedBy=multi-user.target.", "lead"),
        '<div class="linkmid">%s<p class="legt">symlink to</p></div>' % DOWN,
        para("Enabling does not start the service now. Use “start”, or “enable --now” to do both.", "note big"),
        cmds("Look:", ["systemctl is-enabled cron", "systemctl list-unit-files --state=enabled", "ls -l /etc/systemd/system/multi-user.target.wants"])))))
    layers = [("graphical.target", "starts LightDM, the login screen"), ("multi-user.target", "cron, NetworkManager and the other services"),
              ("basic.target", "sockets, timers and paths"), ("sysinit.target", "udev, mounts from /etc/fstab, swap")]
    S.append(("b4-targets", sec("b4-targets", "s alt", "%s\n<div class=\"cards\"><div class=\"lay\">%s</div><div class=\"card\"><h3>How to read it</h3>%s</div></div>\n%s" % (
        head("7.3 · " + B, "The target chain"),
        "".join('<div class="layer"><p class="bt">%s</p><p class="bs">%s</p></div>' % (e(a), e(b)) for a, b in layers),
        bullets(["Targets are named goals that group units", "Top to bottom: each target pulls in the one below it",
                 "Start order is the reverse: bottom first, graphical.target last",
                 "Units in the same step start in parallel. Only After= and Before= set an order between them"], "bul sm"),
        cmds("Look:", ["systemctl get-default", "systemctl list-dependencies graphical.target", "systemd-analyze critical-chain"])))))
    S.append(stage("b4-triggers", "7.4 · " + B, "Other ways services start",
        "Not every service is a boot-time link. Generators create units on the fly: the fstab generator turns /etc/fstab into mount units. Socket units start a service on a connection, timer units on a schedule, path units on a file change.",
        [("/usr/lib/systemd/system-generators/", "Programs that generate units at boot"), ("/run/systemd/generator/", "The units they generated (in RAM)")],
        [("/etc/fstab", "Becomes mount units.", True), ("/etc/systemd/system/*.timer and *.socket", "Your own timers and sockets"), ("/etc/cron.d/ and crontab -e", "Classic scheduled jobs (cron is itself a service)")],
        ["systemctl list-timers", "systemctl list-sockets", "ls /run/systemd/generator"]))
    S.append(stage("b4-user", "7.5 · " + B, "User services",
        "After login, systemd-logind starts user@UID.service, your own “systemd --user” manager. It runs per-user services such as the D-Bus user bus, dconf, the keyring and the audio server, with the same unit format.",
        [("/usr/lib/systemd/user/", "User units shipped by packages"), ("/etc/systemd/user/", "System-wide user units")],
        [("~/.config/systemd/user/", "Your own user units and timers"), ("loginctl enable-linger <user>", "Keeps them running after logout")],
        ["systemctl --user list-units --type=service", "systemctl --user list-timers", "systemctl --user status"], alt=True))
    left = card("A systemd unit", bullets(["A background daemon with no window", "Starts at boot or at login, without a desktop", "Logs go to the journal", "Lives in /etc/systemd/system/ or ~/.config/systemd/user/"], "bul sm"))
    right = card("A desktop autostart entry", bullets(["A program with a window or a tray icon: network applet, update manager, Bluetooth", "Started by cinnamon-session, not by systemd", "Exists only during your graphical session", "Lives in /etc/xdg/autostart/ or ~/.config/autostart/"], "bul sm"), "card edit")
    S.append(("b4-notsystemd", sec("b4-notsystemd", "s", "%s\n<div class=\"cards\">%s%s</div>\n%s" % (
        head("7.6 · " + B, "Not systemd: desktop autostart"), left, right,
        cmds("Look:", ["ls /etc/xdg/autostart", "ls ~/.config/autostart", "Menu → Startup Applications"])))))

    # ---------------- Block 5
    B = "Block 5 · Network and firewall"
    S.append(stage("b5-conn", "8.1 · " + B, "Know your connection",
        "NetworkManager manages Wi-Fi and cable. nmcli shows the active connection, your IP address, the gateway and the DNS servers. For Wi-Fi, check the security type: WPA2 or WPA3 is acceptable. WEP or an open network is not.",
        [("/etc/NetworkManager/NetworkManager.conf", "Main NetworkManager settings"), ("/etc/netplan/90-NM-*.yaml", "Saved networks with Wi-Fi passwords (root only)"), ("/run/NetworkManager/system-connections/", "The same networks, generated at runtime"), ("/etc/resolv.conf", "DNS resolver, a link managed by systemd-resolved")],
        [("Network settings (per connection)", "For example “Connect automatically”"), ("/etc/NetworkManager/conf.d/*.conf", "Drop-in settings")],
        ["nmcli device status", "nmcli -f SSID,SECURITY,SIGNAL device wifi list", "ip -br addr", "ip route", "resolvectl status"], alt=True))
    S.append(stage("b5-listen", "8.2 · " + B, "What is listening",
        "A port is only a risk if a program is listening on it. ss lists the listening sockets and the program behind each one. On a home desktop the list of network-wide listeners should be short, and you should know why each one is there.",
        [("/etc/services", "Names for the well-known port numbers")],
        [("/etc/avahi/avahi-daemon.conf", "Network discovery service (mDNS)"), ("/etc/cups/cupsd.conf", "Which addresses the print service listens on"), ("systemctl disable --now <unit>", "Turning a service off closes its port")],
        ["ss -tulpn", "sudo ss -tulpn  (names for all users)", "ss -tn state established"]))
    S.append(("b5-ss", sec("b5-ss", "s alt", "%s\n%s\n%s\n%s" % (
        head("8.3 · " + B, "How to read ss -tulpn"),
        para("Read the Local Address column. It tells you who can connect.", "lead"),
        table(["Local address", "Who can connect", "Typical example"], [
            ["127.0.0.1:631 or [::1]:631", "Only programs on this machine", "Printing service (CUPS)"],
            ["0.0.0.0:5353 or [::]:5353", "Any machine that can reach you", "Network discovery (mDNS, avahi)"],
            ["0.0.0.0:22", "Any machine that can reach you", "An SSH server, if you run one"],
            ["192.168.1.20:8080", "Machines on that network only", "A service bound to one address"]], [34, 33, 33]),
        para("If port 22 is listening, you are running an SSH server. That needs its own hardening, which this guide does not cover.", "note")))))
    S.append(fw_slide("b5-fw", "8.4 · " + B))
    S.append(stage("b5-fwfiles", "8.5 · " + B, "Firewall: files and commands",
        "ufw keeps its settings in /etc/ufw and /etc/default/ufw. Always confirm the state with “ufw status”: it must say “Status: active”. Mint includes a graphical front end, shown in the menu as Firewall Configuration.",
        [("/etc/ufw/ufw.conf", "ENABLED=yes or no"), ("/etc/ufw/user.rules", "Generated from your rules. Not for hand editing"), ("/var/log/ufw.log", "Blocked packets, when logging is on")],
        [("/etc/default/ufw", "Default policies, IPv6 on or off"), ("/etc/ufw/applications.d/", "Profiles that give an application a name"),
         ("Menu → Firewall Configuration", "Graphical front end (gufw), included in Mint"), ("/etc/ufw/*.rules edited by hand", "A mistake can open or lock ports.", True)],
        ["sudo ufw status verbose", "sudo ufw status numbered", "sudo nft list ruleset"], alt=True))
    S.append(docker_slide("b5-docker", "8.6 · " + B))
    left = card("Safer habits", bullets([
        "Publish to localhost only: -p 127.0.0.1:8080:80",
        "Publish only the ports you need",
        "Membership of the docker group equals root on that machine",
        "Don’t mount /var/run/docker.sock into containers you don’t trust",
    ], "bul sm"), "card edit")
    right = card("Where it matters", bullets([
        "Behind a home router the risk is smaller: the router blocks incoming connections",
        "On public Wi-Fi, a container published on all addresses can be reached by everyone on that network",
        "Check the ports: lines in your docker-compose.yml files",
    ], "bul sm"))
    S.append(("b5-docker2", sec("b5-docker2", "s", "%s\n<div class=\"cards\">%s%s</div>\n%s" % (
        head("8.7 · " + B, "Docker: safer habits"), left, right,
        cmds("Look:", ["sudo docker ps", "sudo docker network ls", "ss -tulpn", "getent group docker"])))))
    S.append(("b5-wifi", sec("b5-wifi", "s alt", "%s\n%s\n%s\n%s" % (
        head("8.8 · " + B, "Public Wi-Fi checklist (laptop)"),
        para("On a public network the router is not yours, and strangers share the same local network.", "lead"),
        bullets(WIFI, "bul chk"),
        cmds("Look:", ["nmcli -f NAME,AUTOCONNECT connection show", "sudo ufw status verbose", "ss -tulpn", "nmcli radio"])))))
    left = card("What a VPN does", bullets([
        "It encrypts the traffic between your laptop and the VPN server, so people on the same Wi-Fi can’t read it",
        "It does not make you anonymous. You move your trust from the Wi-Fi to the VPN provider",
        "Mint’s network settings include a VPN section. The OpenVPN plugin is installed, and NetworkManager also documents WireGuard (not tested here)",
        "You can also run a VPN to your own home router or server",
    ], "bul sm"))
    right = card("Two providers that publish independent audits", bullets([
        "Mullvad",
        "Proton VPN",
        "A starting point, not an endorsement. No affiliation. The services were not tested here",
        "Both offer official Linux apps for Ubuntu, Debian and Fedora. Proton has a Mint guide. Mullvad does not list Mint as supported",
    ], "bul sm"), "card edit")
    S.append(("b5-vpn", sec("b5-vpn", "s", "%s\n<div class=\"cards\">%s%s</div>\n%s" % (
        head("8.9 · " + B, "Public Wi-Fi: about VPNs"), left, right,
        para("Audit claims come from press coverage and a provider blog. Linux support comes from the providers’ own sites (see Sources).", "note")))))

    # ---------------- Block 6
    B = "Block 6 · Hardening, alarms and audit"
    S.append(stage("b6-ssh", "9.1 · " + B, "SSH as a client",
        "When you connect out to other machines, your private key is the secret to protect. Use an ed25519 key with a passphrase. Give servers only the public key. A “host key changed” warning is a reason to stop, not something to ignore.",
        [("~/.ssh/id_ed25519", "Private key. Never share it or copy it around"), ("~/.ssh/id_ed25519.pub", "Public key. Safe to share"),
         ("~/.ssh/known_hosts", "Fingerprints of servers you have connected to"), ("/etc/ssh/ssh_config and ssh_config.d/", "System-wide client defaults")],
        [("~/.ssh/config", "Host aliases, IdentityFile, ProxyJump"), ("Permissions: ~/.ssh 700, private keys 600", "ssh refuses keys that other users can read")],
        ["ls -ld ~/.ssh", "ls -l ~/.ssh", "ssh-add -l", "ssh -G <host>", "ssh -v <host>"], alt=True))
    S.append(("b6-sshcfg", sec("b6-sshcfg", "s", "%s\n<div class=\"cards\"><div class=\"half\">%s</div>%s</div>\n%s" % (
        head("9.2 · " + B, "SSH: a config example, and the agent"),
        code("~/.ssh/config  (example values)", ["Host home-server", "  HostName 192.168.1.20", "  User me", "  IdentityFile ~/.ssh/id_ed25519", "  ForwardAgent no", "", "Host remote-box", "  HostName remote.example.org", "  ProxyJump home-server"]),
        card("The agent, and hopping through a host", bullets([
            "ssh-agent keeps the unlocked key in memory, so you type the passphrase once",
            "Agent forwarding (-A, ForwardAgent yes) is risky: root on the remote machine can use your agent while you are connected",
            "Prefer ProxyJump (-J) to reach a machine through another one",
        ], "bul sm"), "card edit"),
        para("ssh parses this example correctly (checked with ssh -G). “ssh-add -l” reports an error when no key is loaded: that is normal.", "note")))))
    S.append(stage("b6-updates", "9.3 · " + B, "Updates and sandboxing",
        "Most real attacks use known bugs that updates already fix. Add software only from sources you trust: every extra repository is code that can run as root. AppArmor, on by default, confines programs to what a profile allows.",
        [("/etc/apt/sources.list.d/", "The repositories you have added"), ("/etc/apt/keyrings/ and /etc/apt/trusted.gpg.d/", "Keys that decide which repositories are trusted"),
         ("/etc/apparmor.d/", "AppArmor profiles"), ("/var/log/apt/history.log", "What was installed or removed, and when")],
        [("Menu → Update Manager", "Check and install updates"), ("Menu → Software Sources", "Choose and review repositories"), ("/etc/apparmor.d/local/", "Local additions to profiles")],
        ["apt list --upgradable", "ls /etc/apt/sources.list.d/", "sudo aa-status", "flatpak list"], alt=True))
    S.append(stage("b6-accounts", "9.4 · " + B, "Accounts and sudo",
        "Know who can become root and who has logged in. sudo rights come from the sudo group and from files in /etc/sudoers.d/. The docker group is root-equivalent too. A strong password plus an automatic screen lock protects an unattended laptop.",
        [("/etc/passwd and /etc/group", "Users and group membership"), ("/etc/sudoers", "Never edit it directly: use visudo"), ("/var/log/wtmp and /var/log/btmp", "Login records read by last and lastb")],
        [("/etc/sudoers.d/*", "Extra sudo rules. Edit only with visudo.", True), ("Menu → Screensaver", "Lock the screen after a short idle time")],
        ["id", "getent group sudo docker", "last -n 10", "sudo lastb -n 10", "sudo -l", "chage -l $USER"]))
    S.append(stage("b6-logs", "9.5 · " + B, "Logs and alarms",
        "systemd collects logs in the journal, and journalctl reads it. Logins, sudo and failed passwords are also written to /var/log/auth.log. A log only helps if someone looks, so an alarm turns an event into a desktop notification.",
        [("/var/log/auth.log", "Authentication log (written by rsyslog)"), ("/var/log/journal/", "The persistent journal"), ("/etc/systemd/journald.conf", "Journal size and retention")],
        [("~/.local/bin/", "Where your alarm script would live"), ("~/.config/systemd/user/", "Where its timer and service would live"), ("/etc/systemd/journald.conf", "Keep logs longer, or limit their size")],
        ["journalctl -p err -b", "journalctl _COMM=sudo --since today", "systemctl --user list-timers", "groups"], alt=True))
    S.append(("b6-alarm", sec("b6-alarm", "s", "%s\n%s\n<div class=\"cards\"><div class=\"half\">%s</div><div class=\"half\">%s</div></div>\n%s" % (
        head("9.6 · " + B, "Example: a desktop alarm for failed logins"),
        code("~/.local/bin/auth-alert.sh", [
            "#!/bin/bash",
            "n=$(journalctl --since \"-15 min\" --no-pager -q | grep -ci \"authentication failure\")",
            "if [ \"$n\" -gt 0 ]; then",
            "  notify-send -u critical \"Security alert\" \"$n failed authentication attempts in 15 minutes\"",
            "fi"]),
        code("auth-alert.service", ["[Service]", "Type=oneshot", "ExecStart=%h/.local/bin/auth-alert.sh"]),
        code("auth-alert.timer", ["[Timer]", "OnBootSec=5min", "OnUnitActiveSec=15min", "[Install]  WantedBy=timers.target"]),
        para("Tested: run by its timer as a user service, the notification was sent (with a wider time window, to find old entries). Not tested: a real failed login inside the 15-minute window. Your user must be able to read the journal (group adm or systemd-journal).", "note")))))
    S.append(stage("b6-recovery", "9.7 · " + B, "Recovery: Timeshift",
        "Security also means being able to recover. Timeshift, included in Mint, takes snapshots of the system files so you can roll back a bad update. By default it leaves out your personal files, so back up your home folder separately.",
        [("/etc/timeshift/timeshift.json", "Timeshift settings"), ("/timeshift/", "The snapshots, on the disk you chose")],
        [("Menu → Timeshift", "Schedule, location, what to include"), ("Menu → Backup Tool", "Backup of your personal files")],
        ["sudo timeshift --list", "df -h"], alt=True))
    S.append(("b6-weekly", sec("b6-weekly", "s", "%s\n%s\n%s" % (
        head("9.8 · " + B, "The weekly ten-minute checkup"),
        para("One pass through the look commands of blocks 5 and 6.", "lead"),
        bullets(WEEKLY, "bul chk")))))
    S.append(("b6-tools", sec("b6-tools", "s alt", "%s\n%s\n%s\n%s" % (
        head("9.9 · " + B, "Optional third-party tools"),
        para("None of these is needed for the checks above. Installing software is a change to your system.", "lead"),
        table(["Tool", "What it adds", "Install"], [
            ["nethogs", "Shows which program is using the network right now", "sudo apt install nethogs"],
            ["nmap", "Scans ports as an outsider would. Scan only your own machines", "sudo apt install nmap"],
            ["lynis", "Audits the system and suggests hardening steps", "sudo apt install lynis"],
            ["fail2ban", "Bans addresses after repeated failed logins. Only useful if you run a server", "sudo apt install fail2ban"],
            ["dconf-editor", "Browse and edit the desktop settings database", "sudo apt install dconf-editor"]], [16, 52, 32]),
        para("The package names were confirmed in the Mint 22.3 repositories. The tools themselves were not installed or run.", "note")))))

    # ---------------- Closing
    S.append(verified_slide("end-verified", "10.1 · Closing"))
    S.append(("end-sources", sec("end-sources", "s alt", "%s\n%s\n%s" % (
        head("10.2 · Closing", "Sources"),
        table(["Topic", "Source"], [
            ["Paths, defaults, file order, command checks", "Read-only checks on a Linux Mint 22.3 Cinnamon machine, November 2026"],
            ["Mint 22.3 release, base and support", "Linux Mint 22.3 release notes (linuxmint.com) and the Linux Mint blog"],
            ["Docker and ufw", "Docker documentation: “Packet filtering and firewalls” and “Port publishing and mapping”"],
            ["VPN audits and Linux apps", "TechRadar (Proton VPN audit); Mullvad blog (audit); mullvad.net and protonvpn.com (Linux apps)"],
            ["Concepts and explanations", "General Linux knowledge, written with Claude Fable 5.2"]], [36, 64]),
        para("Official documentation was used where it was found. It changes over time, so check it again before you rely on a detail.", "note")))))
    S.append(legal_slide("end-legal", "10.3 · Closing"))

    sections = {
        "s1": {"description": "Cover, purpose, index and what Linux Mint is.", "start": "cover"},
        "s2": {"description": "The six blocks at a glance.", "start": "ov-123"},
        "s3": {"description": "Block 1: system start-up, from firmware to systemd.", "start": "b1-uefi"},
        "s4": {"description": "Block 2: the login process.", "start": "b2-greeter"},
        "s5": {"description": "Block 3: user access, shells and automation.", "start": "b3-cinnamon"},
        "s6": {"description": "Block 4: services and daemons under systemd.", "start": "b4-units"},
        "s7": {"description": "Block 5: network and firewall.", "start": "b5-conn"},
        "s8": {"description": "Block 6: hardening, alarms and audit.", "start": "b6-ssh"},
        "s9": {"description": "Verification status, sources, disclaimer and license.", "start": "end-verified"},
    }
    return S, sections

# ----------------------------------------------------------------------------- short deck

def short():
    S = []
    S.append(cover(short=True))
    left = card("What you get", bullets([
        "What Linux Mint does from the power button to a working, secured desktop",
        "The files involved at each step, and the ones you can customize",
        "Safe commands to look at your own system first",
    ], "bul"), "card edit")
    right = card("Scope", bullets([
        "Linux Mint 22.x, Cinnamon edition (based on Ubuntu 24.04)",
        "LightDM login screen, X11 session, systemd",
        "For readers who already use the terminal",
        "This is the short version of a longer deck of about 50 slides",
    ], "bul sm"))
    S.append(("purpose", sec("purpose", "s", "%s\n<div class=\"cards\">%s%s</div>" % (head("Purpose", "Why this guide"), left, right))))

    def col(title, sub, steps, cls=""):
        return '<div class="ocol %s"><h3>%s</h3><p class="osub">%s</p>%s</div>' % (
            cls, e(title), e(sub), "".join('<p class="ostep">%s</p>' % e(s) for s in steps))
    S.append(("ov-123", sec("ov-123", "s alt", "%s\n<div class=\"ocols\">%s%s%s%s%s</div>\n%s" % (
        head("The map", "Six blocks: three steps and three layers"),
        col("1 · System start-up", "Power button → login screen", ["UEFI firmware", "Shim and GRUB", "Linux kernel", "initramfs", "systemd (PID 1)"]),
        ARROW,
        col("2 · Login process", "Login screen → session scripts", ["LightDM greeter", "PAM authentication", "systemd-logind session", "Session scripts"]),
        ARROW,
        col("3 · User access", "Desktop → shell → logout", ["Cinnamon session", "Terminal and shell", "Run things automatically", "Logout"]),
        para("Under them: 4 · Services and daemons, 5 · Network and firewall, 6 · Hardening, alarms and audit.", "note big")))))

    S.append(("boot", sec("boot", "s", "%s\n%s\n%s\n%s" % (
        head("Block 1 · System start-up", "Who starts whom at boot"),
        table(["Stage", "What it does", "Where you customize it"], [
            ["UEFI firmware", "Tests hardware, loads the bootloader from the EFI partition", "Firmware setup screen, efibootmgr"],
            ["Shim and GRUB", "Secure Boot handover, loads kernel and initramfs", "/etc/default/grub, then sudo update-grub"],
            ["Linux kernel", "Memory, CPUs, drivers", "/etc/modprobe.d/, /etc/sysctl.d/"],
            ["initramfs", "Temporary root in RAM that finds the real root", "/etc/initramfs-tools/"],
            ["systemd (PID 1)", "Mounts /etc/fstab, starts services up to graphical.target", "/etc/systemd/system/, /etc/fstab"]], [20, 44, 36]),
        cmds("Look:", ["systemd-analyze", "systemd-analyze blame", "systemd-analyze critical-chain", "cat /proc/cmdline"]),
        para("“blame” lists slow units. “critical-chain” shows what actually delayed the boot. They are not the same thing.", "note")))))

    order = ["/etc/profile", "~/.profile", "/etc/xprofile", "~/.xprofile", "/etc/X11/Xsession.d/*  (among them: ~/.xsessionrc, the GPG and SSH agents)", "cinnamon-session-cinnamon"]
    left = card("After your password is accepted", '<ol class="num">%s</ol>' % "".join("<li>%s</li>" % e(x) for x in order))
    right = card("What to remember", bullets([
        "LightDM shows the login screen, PAM checks the password, systemd-logind opens the session",
        "Changes to these files apply at the next login",
        "A syntax error in ~/.profile can break the login. Keep Ctrl+Alt+F3 as a way back",
    ], "bul sm"), "card edit")
    S.append(("login", sec("login", "s alt", "%s\n<div class=\"cards\">%s%s</div>\n%s" % (
        head("Block 2 · Login process", "The order of the login files"), left, right,
        para("Order read from /usr/sbin/lightdm-session on Mint 22.3.", "note")))))

    left = card("Terminal window in Cinnamon", bullets(["A non-login, interactive shell", "Reads ~/.bashrc only", "Inherits the session’s environment"], "bul sm"))
    right = card("Text console or SSH", bullets(["A login shell", "Reads /etc/profile, then ~/.profile", "Mint’s ~/.profile sources ~/.bashrc"], "bul sm"))
    S.append(("shell", sec("shell", "s", "%s\n<div class=\"cards\">%s%s</div>\n%s" % (
        head("Block 3 · User access", "Why your change “did nothing”"), left, right,
        para("Variables and PATH go in ~/.profile. Aliases, prompt and functions go in ~/.bashrc.", "note big")))))

    S.append(auto_map("auto", "Block 3 · User access"))

    layers = [("graphical.target", "starts LightDM, the login screen"), ("multi-user.target", "cron, NetworkManager and the other services"),
              ("basic.target", "sockets, timers and paths"), ("sysinit.target", "udev, mounts from /etc/fstab, swap")]
    S.append(("services", sec("services", "s", "%s\n<div class=\"cards\"><div class=\"lay\">%s</div><div class=\"card\"><h3>Services in four facts</h3>%s</div></div>\n%s" % (
        head("Block 4 · Services and daemons", "How systemd starts services"),
        "".join('<div class="layer"><p class="bt">%s</p><p class="bs">%s</p></div>' % (e(a), e(b)) for a, b in layers),
        bullets(["Each target pulls in the one below it. Start order is bottom first",
                 "“Enabled” means a symlink in a .wants directory",
                 "Your overrides go in /etc/systemd/system/, never in /usr/lib/",
                 "Tray programs are started by the desktop’s autostart, not by systemd"], "bul sm"),
        cmds("Look:", ["systemctl list-dependencies graphical.target", "systemctl list-unit-files --state=enabled", "systemctl list-timers"])))))

    S.append(("listen", sec("listen", "s alt", "%s\n%s\n%s\n%s" % (
        head("Block 5 · Network and firewall", "What is listening? Read ss -tulpn"),
        para("A port is only a risk if a program is listening on it. The Local Address column tells you who can connect.", "lead"),
        table(["Local address", "Who can connect", "Typical example"], [
            ["127.0.0.1:631 or [::1]:631", "Only programs on this machine", "Printing service (CUPS)"],
            ["0.0.0.0:5353 or [::]:5353", "Any machine that can reach you", "Network discovery (mDNS, avahi)"],
            ["0.0.0.0:22", "Any machine that can reach you", "An SSH server, if you run one"]], [34, 33, 33]),
        cmds("Look:", ["ss -tulpn", "nmcli device status", "nmcli -f SSID,SECURITY device wifi list"])))))

    S.append(fw_slide("fw", "Block 5 · Network and firewall"))
    S.append(docker_slide("docker", "Block 5 · Network and firewall"))

    S.append(("wifi", sec("wifi", "s", "%s\n%s\n%s" % (
        head("Block 5 · Network and firewall", "Public Wi-Fi checklist (laptop)"),
        para("On a public network the router is not yours, and strangers share the same local network.", "lead"),
        bullets(WIFI, "bul chk")))))

    S.append(("weekly", sec("weekly", "s alt", "%s\n%s\n%s" % (
        head("Block 6 · Hardening, alarms and audit", "The weekly ten-minute checkup"),
        para("Also in the full deck: SSH keys, updates and AppArmor, a desktop alarm for failed logins, and Timeshift.", "lead"),
        bullets(WEEKLY, "bul chk")))))

    S.append(verified_slide("verified", "Honesty"))
    S.append(legal_slide("legal", "Closing"))
    sections = {
        "s1": {"description": "Cover, purpose and the map of the six blocks.", "start": "cover"},
        "s2": {"description": "Boot, login and user access.", "start": "boot"},
        "s3": {"description": "Services, network and security.", "start": "services"},
        "s4": {"description": "Verification status, disclaimer and license.", "start": "verified"},
    }
    return S, sections

# ----------------------------------------------------------------------------- output

FACES = {
    "inter": {"family": "Inter", "href": "https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap"},
    "space-grotesk": {"family": "Space Grotesk", "href": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300..700&display=swap"},
    "jetbrains-mono": {"family": "JetBrains Mono", "href": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap"},
}


def write(root, title, slides, sections):
    os.makedirs(os.path.join(root, "project", "slides"), exist_ok=True)
    ids = [sid for sid, _ in slides]
    assert len(ids) == len(set(ids)), "duplicate ids"
    for sid, htmltext in slides:
        with open(os.path.join(root, "project", "slides", sid + ".html"), "w", encoding="utf-8") as f:
            f.write(htmltext)
    at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    old = os.path.join(root, "project", "deck.json")
    if os.path.exists(old):
        at = json.load(open(old, encoding="utf-8")).get("createdOnFiles", {}).get("at", at)
    index = {"v": 5, "createdOnFiles": {"v": 1, "at": at},
             "lists": "css", "format": {"v": 1, "shared": ["project/deck.css"]}, "title": title, "cover": "cover",
             "order": ids, "sections": sections, "faces": FACES, "designSystems": []}
    with open(os.path.join(root, "project", "deck.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, "deck.css"), encoding="utf-8") as f:
        css = f.read()
    with open(os.path.join(root, "project", "deck.css"), "w", encoding="utf-8") as f:
        f.write(css)
    # local preview page (not part of the deck)
    prev = ['<!DOCTYPE html><html><head><meta charset="utf-8"><title>%s</title>' % html.escape(title)]
    for face in FACES.values():
        prev.append('<link rel="stylesheet" href="%s">' % face["href"])
    prev.append("<style>* { margin: 0 } body { font: 32px/1.2 sans-serif; background:#888 } body > section { width: 1920px !important; height: 1080px !important; overflow: hidden !important; box-sizing: border-box !important; position: relative; isolation: isolate; margin-bottom: 20px } aside { display: none !important } h1 { font-size: 96px; font-weight: 600 } h2 { font-size: 64px; font-weight: 600 } h3 { font-size: 44px; font-weight: 600 } p, li, h1, h2, h3, td, th { overflow-wrap: break-word } table { width: 100%; border-collapse: separate; border-spacing: 0; border: solid #0003; border-width: 2px 0 0 2px } th, td { padding: .35em .6em; text-align: left; border: solid #0003; border-width: 0 2px 2px 0 } x-shape { display: block } x-shape[kind=\"arrow-right\"] { clip-path: polygon(0 30%, 60% 30%, 60% 0, 100% 50%, 60% 100%, 60% 70%, 0 70%) } x-shape[kind=\"arrow-down\"] { clip-path: polygon(30% 0, 70% 0, 70% 60%, 100% 60%, 50% 100%, 0 60%, 30% 60%) } @media print { @page { size: 1920px 1080px; margin: 0 } body { background: none; zoom: 1 !important } body > section { margin: 0 !important; break-after: page } }</style>")
    prev.append("<style>%s</style></head><body>" % css)
    prev.extend(h for _, h in slides)
    prev.append("<script>function fit(){document.body.style.zoom=Math.min(1,(innerWidth-20)/1920)}fit();addEventListener('resize',fit)</script>")
    prev.append("</body></html>")
    with open(os.path.join(root, "preview.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(prev))
    return ids


if __name__ == "__main__":
    s, secs = full()
    ids = write(os.path.join(HERE, "full"), TITLE, s, secs)
    print("full:", len(ids), "slides")
    s2, secs2 = short()
    ids2 = write(os.path.join(HERE, "short"), "Linux under the Hood: the essentials (Short version)", s2, secs2)
    print("short:", len(ids2), "slides")
    for w in warn:
        print("WARN", w)
