#!/bin/bash
# Read-only checks that need sudo. This script changes nothing on the system.
# It prints, per command: the exit code, the number of output lines, and at
# most a few first lines (none for commands whose output is personal).
LOG="$(dirname "$0")/sudo-checks.log"
: > "$LOG"
echo "Read-only checks for the Linux under the Hood guide."
echo "Type your password when sudo asks. Nothing is changed."
sudo -v || { echo "SUDO-FAILED" | tee -a "$LOG"; exit 1; }

chk() { # chk <lines-to-show> <label> <command...>
  local n="$1" label="$2"; shift 2
  local out rc first
  out=$("$@" 2>&1); rc=$?
  first=""
  [ "$n" -gt 0 ] && first=$(printf '%s\n' "$out" | head -n "$n" | cut -c1-110 | tr '\n' '|')
  printf '%-36s exit=%s lines=%s %s\n' "$label" "$rc" "$(printf '%s\n' "$out" | wc -l)" "$first" | tee -a "$LOG"
}

chk 4 "ufw status verbose"        sudo ufw status verbose
chk 0 "ufw status numbered"       sudo ufw status numbered
chk 6 "nft list tables"           sudo nft list tables
chk 0 "nft list ruleset"          sudo nft list ruleset
chk 3 "aa-status"                 sudo aa-status
chk 0 "lastb -n 3"                sudo lastb -n 3
chk 0 "timeshift --list"          sudo timeshift --list
chk 0 "docker ps (table format)"  sudo docker ps --format 'table {{.Names}}\t{{.Ports}}'
chk 0 "docker network ls"         sudo docker network ls
chk 0 "ss -tulpn"                 sudo ss -tulpn
chk 0 "lsof -i -P -n"             sudo lsof -i -P -n
chk 0 "sudo -l"                   sudo -l
chk 0 "tail /var/log/ufw.log"     sudo tail -n 2 /var/log/ufw.log
chk 8 "ls /boot/efi/EFI/ubuntu"   sudo ls /boot/efi/EFI/ubuntu
chk 1 "ls -ld system-connections" sudo ls -ld /etc/NetworkManager/system-connections
chk 3 "saved-network file modes"  sudo sh -c "ls -l /etc/NetworkManager/system-connections | awk 'NR>1{print \$1, \$3}' | sort | uniq -c"
chk 3 "iptables -S DOCKER-USER"   sudo iptables -S DOCKER-USER
chk 1 "docker rules in nft"       sudo sh -c "nft list ruleset | grep -ci docker"
chk 2 "journal as root, err"      sudo journalctl -p err -b -n 1 --no-pager -o cat
echo "DONE" | tee -a "$LOG"
echo "Finished. You can close this tab."
