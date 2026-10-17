"""Linux power user: intermediate."""

from app.coursepacks import mcq, open_q
from app.packs._draw import AMBER, BLUE, GREEN, INK, MUTED, PURPLE, RED, arrow, box, line, svg, text, title

PIPES = svg(
    title("journalctl -u nginx | grep 404 | wc -l"),
    box(20, 90, 130, 60, "journalctl", BLUE, sub="all log lines"),
    arrow(150, 120, 180, 120, MUTED),
    box(180, 90, 120, 60, "grep 404", AMBER, sub="matching lines"),
    arrow(300, 120, 330, 120, MUTED),
    box(330, 90, 130, 60, "wc -l", GREEN, sub="count them"),
    text(85, 180, "stdout →", 12, MUTED), text(240, 180, "stdin → stdout", 12, MUTED), text(395, 180, "→ terminal", 12, MUTED),
    text(240, 230, "stderr (2) skips the pipe unless you add 2>&1", 12, RED),
    text(85, 210, "A", 15, BLUE, weight="bold"), text(240, 210, "B", 15, AMBER, weight="bold"), text(395, 210, "C", 15, GREEN, weight="bold"),
)

SCRIPT = svg(
    title("A script's exit code decides what runs next"),
    box(30, 60, 170, 50, "backup.sh", BLUE, size=14),
    arrow(115, 110, 70, 170, GREEN, "exit 0", dx=-30, size=12), arrow(115, 110, 170, 170, RED, "exit 1", dx=30, size=12),
    box(20, 172, 110, 50, "&& next step", GREEN, size=12), box(140, 172, 110, 50, "|| alert", RED, size=12),
    box(280, 60, 180, 160, "", MUTED), text(370, 84, "set -euo pipefail", 13, AMBER),
    text(370, 112, "-e: stop on error", 12, INK), text(370, 136, "-u: unset var = error", 12, INK), text(370, 160, "-o pipefail: fail if", 12, INK),
    text(370, 178, "any piped command fails", 12, INK),
    text(240, 262, "0 = success, anything else = failure", 12, MUTED),
)

SSH = svg(
    title("SSH key authentication"),
    box(20, 70, 160, 140, "", BLUE), text(100, 94, "Your laptop", 13, BLUE),
    box(35, 110, 130, 40, "private key", RED, size=12), text(100, 172, "~/.ssh/id_ed25519", 11, MUTED), text(100, 192, "never leaves here", 11, RED),
    box(300, 70, 160, 140, "", GREEN), text(380, 94, "Server", 13, GREEN),
    box(315, 110, 130, 40, "public key", GREEN, size=12), text(380, 172, "~/.ssh/authorized_keys", 11, MUTED),
    arrow(180, 130, 298, 130, AMBER, "proves it has the key", dy=-10, size=11),
    arrow(298, 160, 180, 160, MUTED, "challenge", dy=14, size=11),
    text(240, 262, "ssh-copy-id puts the public key on the server", 12, MUTED),
)

UNIT = svg(
    title("A systemd service unit"),
    box(40, 50, 400, 200, "", INK),
    text(60, 78, "[Unit]", 13, BLUE, anchor="start"), text(70, 98, "After=network-online.target", 12, INK, anchor="start"),
    text(60, 126, "[Service]", 13, AMBER, anchor="start"), text(70, 146, "ExecStart=/opt/app/run", 12, INK, anchor="start"),
    text(70, 166, "User=app   Restart=on-failure", 12, INK, anchor="start"),
    text(60, 194, "[Install]", 13, GREEN, anchor="start"), text(70, 214, "WantedBy=multi-user.target", 12, INK, anchor="start"),
    text(420, 146, "X", 16, AMBER, weight="bold"), text(420, 214, "Y", 16, GREEN, weight="bold"),
)

DISKS = svg(
    title("Disk, partition, filesystem, mount point"),
    box(30, 60, 420, 50, "", INK), text(60, 90, "/dev/sdb", 13, INK, anchor="start"),
    box(150, 68, 140, 34, "sdb1 (ext4)", BLUE, size=12), box(300, 68, 140, 34, "sdb2 (xfs)", PURPLE, size=12),
    arrow(220, 102, 140, 170, BLUE), arrow(370, 102, 360, 170, PURPLE),
    box(70, 172, 140, 46, "/srv/media", BLUE, size=13), box(290, 172, 140, 46, "/var/lib/docker", PURPLE, size=12),
    text(240, 252, "made permanent in /etc/fstab (by UUID)", 12, MUTED),
)

NET = svg(
    title("Is it the network? Work up the layers"),
    box(40, 222, 400, 34, "1  ip a / ip route: link up, address, gateway?", INK, size=12),
    box(40, 182, 400, 34, "2  ping 192.168.0.1 / 1.1.1.1: reachable?", BLUE, size=12),
    box(40, 142, 400, 34, "3  dig example.org: does DNS resolve?", PURPLE, size=12),
    box(40, 102, 400, 34, "4  ss -tlnp: is the service listening?", AMBER, size=12),
    box(40, 62, 400, 34, "5  curl -v http://host:port: does the app answer?", GREEN, size=12),
)

L1 = {
    "title": "Pipes, redirection and text tools",
    "minutes": 9,
    "photo_query": "",
    "body": """The Unix philosophy is many small tools that each do one job, joined together. The glue is **redirection** and **pipes**, and the most useful tools are the text processors.

## Standard streams

Every process starts with three streams: **stdin** (0, input), **stdout** (1, normal output) and **stderr** (2, errors). Redirection points them somewhere else:

- `cmd > out.txt` writes stdout to a file (overwriting); `>>` appends.
- `cmd 2> errors.txt` sends stderr to a file.
- `cmd > all.txt 2>&1` sends both to the same file (order matters: redirect stdout first).
- `cmd < input.txt` reads stdin from a file.
- `> /dev/null` throws output away.

## Pipes

`a | b` connects a's stdout to b's stdin. Only stdout goes through; errors still reach your terminal unless you add `2>&1` before the pipe.

`journalctl -u nginx | grep 404 | wc -l` counts 404 lines in nginx's log in three small steps.

## grep: find lines

- `grep -i error app.log` ignores case; `-v` inverts (lines *without* the match); `-n` shows line numbers; `-r` searches folders; `-c` counts.
- `grep -E "fail(ed|ure)"` uses extended regular expressions.

## sort, uniq, cut, wc

- `sort` sorts lines (`-n` numerically, `-r` reverse); `uniq -c` counts **adjacent** duplicates, so sort first.
- `cut -d, -f2 data.csv` takes the second comma-separated field.
- `wc -l` counts lines.

The classic "top talkers" pipeline: `cut -d' ' -f1 access.log | sort | uniq -c | sort -rn | head` lists the IPs making the most requests.

## sed and awk

- **sed** edits streams: `sed 's/old/new/g' file` replaces text; `sed -i` edits the file in place (keep a backup: `sed -i.bak`).
- **awk** works with columns: `awk '{print $1, $7}' access.log` prints fields 1 and 7; `awk -F, '$3 > 100' data.csv` filters rows where column 3 exceeds 100; `awk '{s+=$5} END {print s}'` sums a column.

## xargs and tee

- `xargs` turns input lines into arguments: `find . -name "*.tmp" -print0 | xargs -0 rm` (the `-print0`/`-0` pair copes with spaces in names).
- `tee` writes to a file *and* passes data on: `cmd | tee log.txt | grep warn`. With sudo: `echo "x" | sudo tee /etc/file` works where `sudo echo "x" > /etc/file` fails, because the redirect is done by your unprivileged shell.

> **Tip:** build pipelines one stage at a time, looking at the output each time, before adding the next `|`.

## In practice

Take a web server log and answer, with one pipeline each: how many requests today, the ten busiest IPs, and how many returned status 500.""",
    "key_points": [
        "stdin 0, stdout 1, stderr 2; > overwrites, >> appends, 2>&1 merges errors into stdout.",
        "Pipes send stdout to the next command's stdin; build pipelines one stage at a time.",
        "grep finds lines, sort | uniq -c counts, cut/awk pick columns, sed substitutes text.",
        "xargs turns lines into arguments; tee writes to a file and passes data on (sudo tee for root files).",
    ],
    "figure_svg": PIPES,
    "figure_caption": "Each command's stdout becomes the next one's stdin; stderr bypasses the pipe unless redirected.",
    "questions": [
        mcq("What does `>>` do?", ["Overwrites a file", "Appends to a file", "Reads from a file", "Pipes to another command"], 1, "> overwrites, >> appends."),
        mcq("In the diagram, what does stage B receive?", ["The count", "All of journalctl's output lines on its stdin", "Only errors", "Nothing"], 1,
            "The pipe connects A's stdout to B's stdin.",
            PIPES, "Pipeline: journalctl (A) piped to grep 404 (B) piped to wc -l (C); stderr bypasses the pipe."),
        mcq("Why does `sort | uniq -c` need the sort?", ["uniq is slow", "uniq only collapses adjacent duplicate lines", "sort adds counts", "It doesn't"], 1, "Unsorted duplicates aren't adjacent."),
        mcq("Which sends both stdout and stderr to all.txt?", ["cmd 2>&1 > all.txt", "cmd > all.txt 2>&1", "cmd | all.txt", "cmd 2> all.txt"], 1,
            "Redirect stdout first, then point stderr at it."),
        mcq("Which command replaces every 'http:' with 'https:' in a stream?", ["grep s/http:/https:/", "sed 's/http:/https:/g'", "awk replace", "cut -r"], 1, "sed's s///g substitutes globally."),
        mcq("Why does `sudo echo hi > /etc/motd` fail with Permission denied?", ["echo can't use sudo", "The redirect is done by your unprivileged shell, not by sudo", "motd is read-only", "You need -f"], 1,
            "Use echo hi | sudo tee /etc/motd."),
        mcq("In the diagram, what's needed for error messages to flow into grep too?", ["Nothing", "Add 2>&1 before the pipe", "Use >>", "Use tee"], 1,
            "stderr isn't piped by default.", PIPES, "Pipeline diagram noting stderr skips the pipe unless you add 2>&1."),
        open_q("Write a pipeline that shows the ten IP addresses with the most requests in access.log (IP is the first field).", "cut -d' ' -f1 access.log | sort | uniq -c | sort -rn | head (or awk '{print $1}' access.log | sort | uniq -c | sort -rn | head).",
               ["extract the first field", "sort then uniq -c to count", "sort -rn and head for the top ten"], "A pattern you'll reuse for anything countable."),
        open_q("Explain what `2>&1` means.", "It redirects file descriptor 2 (stderr) to wherever file descriptor 1 (stdout) currently points, so errors go to the same place as normal output.",
               ["stderr is descriptor 2, stdout 1", "send stderr where stdout goes"], "Order matters relative to other redirects."),
        open_q("Why use find -print0 with xargs -0 rather than plain find | xargs?", "Because file names can contain spaces or newlines; -print0 separates names with a null byte and xargs -0 splits on it, so every name is passed intact.",
               ["names may contain spaces", "null separator keeps names intact"], "Otherwise 'My File.tmp' becomes two arguments."),
    ],
}

L2 = {
    "title": "Shell scripting basics",
    "minutes": 9,
    "photo_query": "",
    "body": """Anything you type more than twice belongs in a script. Bash scripts automate backups, deployments and checks, and run from cron or systemd timers.

## A first script

```
#!/usr/bin/env bash
set -euo pipefail

name="${1:-world}"
echo "Hello, ${name}"
```

- The **shebang** line `#!/usr/bin/env bash` says which interpreter runs it.
- Make it executable with `chmod +x hello.sh` and run `./hello.sh Brad`.
- `$1`, `$2`... are arguments; `$#` is how many; `"$@"` is all of them. `${1:-world}` uses a default when `$1` is missing.

## set -euo pipefail

Put this at the top of every script:

- `-e`: stop at the first failing command instead of ploughing on.
- `-u`: treat an unset variable as an error (catches typos like `$BACKUP_DRI`).
- `-o pipefail`: a pipeline fails if *any* command in it fails, not just the last.

## Variables and quoting

- Assign with no spaces: `dir=/srv/backup`. Read with `"$dir"`.
- **Always double-quote** variables: `rm -r "$dir"`. Unquoted, a value with spaces splits into several arguments, and an empty one can turn `rm -r "$dir/"` into something far worse.
- `$(command)` captures output: `today=$(date +%F)`.
- Single quotes are literal (`'$HOME'` stays as typed); double quotes expand variables.

## Exit codes and conditions

Every command returns an **exit code**: 0 for success, anything else for failure. `$?` holds the last one.

```
if ping -c1 -W2 192.168.0.1 >/dev/null; then
  echo "router up"
else
  echo "router down" >&2
  exit 1
fi
```

Tests use `[[ ... ]]`: `[[ -f file ]]` (file exists), `[[ -d dir ]]`, `[[ -z "$x" ]]` (empty), `[[ "$a" == "$b" ]]`, `(( n > 5 ))` for numbers.

`cmd1 && cmd2` runs cmd2 only if cmd1 succeeded; `cmd1 || cmd2` runs cmd2 only if it failed.

## Loops and functions

```
for f in /var/log/*.log; do
  gzip -k "$f"
done

backup() {
  local src=$1
  tar czf "/srv/backup/$(basename "$src")-$(date +%F).tgz" "$src"
}
backup /etc
```

`local` keeps a variable inside the function.

## Making scripts robust

- Check inputs early and print usage on mistakes.
- Write errors to stderr (`>&2`) and exit non-zero, so callers (cron, systemd, CI) know it failed.
- Clean up temporary files with a trap: `trap 'rm -f "$tmp"' EXIT`.
- Run **ShellCheck** on scripts: it catches quoting bugs and common mistakes.

> **Tip:** if a script grows past about a hundred lines or needs data structures, consider Python instead.

## In practice

Write `backup-etc.sh` that tars `/etc` into a dated file under `/srv/backup`, keeps the last seven, exits non-zero on failure, and passes ShellCheck.""",
    "key_points": [
        "Start scripts with a shebang and set -euo pipefail; make them executable with chmod +x.",
        "Always double-quote variables; $(...) captures output; ${1:-default} supplies defaults.",
        "Exit code 0 means success; use if, [[ ]], && and || to branch on it and exit non-zero on failure.",
        "Use loops, functions with local, trap for cleanup, and ShellCheck to catch mistakes.",
    ],
    "figure_svg": SCRIPT,
    "figure_caption": "Exit code 0 lets && continue; a failure triggers ||. set -euo pipefail makes failures stop the script.",
    "questions": [
        mcq("What does `set -e` do?", ["Echoes each command", "Stops the script when a command fails", "Exports variables", "Enables extended globbing"], 1, "-e exits on the first error."),
        mcq("In the diagram, when does the `|| alert` branch run?", ["When backup.sh exits 0", "When backup.sh exits non-zero", "Always", "Never"], 1,
            "|| runs the right side only if the left failed.",
            SCRIPT, "backup.sh exits 0 to && next step, or exits 1 to || alert; a side panel explains set -euo pipefail."),
        mcq("Why quote \"$dir\" in `rm -r \"$dir\"`?", ["It's faster", "So a value with spaces stays one argument and an empty value can't expand dangerously", "Bash requires it", "To make it read-only"], 1,
            "Unquoted variables split and glob."),
        mcq("What does `$(date +%F)` produce in a script?", ["The literal text", "The output of the date command, like 2026-10-17", "An error", "The exit code"], 1, "Command substitution."),
        mcq("Which test checks that a file exists?", ["[[ -d file ]]", "[[ -f file ]]", "[[ -z file ]]", "[[ -x dir ]]"], 1, "-f regular file; -d directory; -z empty string."),
        mcq("What exit code means success?", ["1", "0", "-1", "255"], 1, "0 is success; any non-zero is failure."),
        mcq("In the diagram, which option makes a pipeline fail if any command in it fails?", ["-e", "-u", "-o pipefail", "-x"], 2,
            "Without pipefail only the last command's status counts.", SCRIPT, "Panel listing -e, -u and -o pipefail."),
        open_q("Why should a script write errors to stderr and exit non-zero when something fails?", "So whatever runs it (cron, systemd, CI or another script) can tell it failed and react or alert, and so error messages don't get mixed into normal output.",
               ["callers can detect failure", "errors kept separate from output"], "Silent failures are the worst kind."),
        open_q("What does `trap 'rm -f \"$tmp\"' EXIT` achieve?", "It runs the cleanup command whenever the script exits, whether it finished normally or failed, so temporary files are always removed.",
               ["runs on any exit", "removes temporary files"], "Pairs well with set -e."),
        open_q("Explain `set -u` with an example of a bug it catches.", "It makes using an unset variable an error; for example if you mistype $BACKUP_DIR as $BACKUP_DRI, the script stops instead of silently using an empty value (which could make a path like /$BACKUP_DRI/ point at /).",
               ["unset variable is an error", "catches typos in variable names"], "Empty variables in paths are dangerous."),
    ],
}

L3 = {
    "title": "SSH and working remotely",
    "minutes": 8,
    "photo_query": "",
    "body": """SSH (Secure Shell) is how you work on servers: an encrypted connection for shells, file copies and tunnels. Setting it up properly is both safer and much more convenient.

## Keys instead of passwords

SSH key authentication uses a **key pair**:

- the **private key** stays on your computer (keep it secret, protect it with a passphrase);
- the **public key** goes on each server, in `~/.ssh/authorized_keys`.

When you connect, the server sends a challenge only the private key can answer. The key never crosses the network.

```
ssh-keygen -t ed25519 -C "brad@laptop"
ssh-copy-id brad@192.168.0.100
ssh brad@192.168.0.100
```

**Ed25519** keys are modern, short and fast. Use an **ssh-agent** (or your OS keychain) so you type the passphrase once per session.

## ~/.ssh/config

Stop typing long commands:

```
Host neo
    HostName 192.168.0.100
    User brad
    IdentityFile ~/.ssh/id_ed25519

Host pi
    HostName 192.168.0.42
    User pi
    ProxyJump neo
```

Now `ssh neo` just works, and `ssh pi` hops through `neo` automatically (**ProxyJump**), which is useful for reaching machines behind a single gateway.

## Copying files

- `scp file.txt neo:/tmp/` copies a file (simple, but doesn't resume).
- `rsync -avz --progress site/ neo:/srv/site/` synchronises folders efficiently, copying only what changed, preserving permissions, and resuming after interruptions. Add `--delete` to remove files deleted at the source (carefully: try `--dry-run` first). Mind the **trailing slash**: `site/` copies the contents, `site` copies the folder itself.

## Tunnels

- **Local forward**: `ssh -L 8080:localhost:80 neo` makes `localhost:8080` on your laptop reach port 80 on neo, handy for admin UIs bound to localhost.
- **Remote forward**: `ssh -R` exposes a local port on the server.
- **Dynamic**: `ssh -D 1080 neo` gives a SOCKS proxy through the server.

## Securing the server side

In `/etc/ssh/sshd_config`:

- `PasswordAuthentication no` once your key works (test in a second session before closing the first!).
- `PermitRootLogin no`.
- Optionally limit users with `AllowUsers`.

Then `sudo systemctl reload ssh`. Add **fail2ban** to ban IPs that keep failing, and avoid exposing SSH to the internet at all where a VPN like WireGuard can be used instead.

## Staying connected

`tmux` (or `screen`) keeps a session running on the server when your connection drops. `tmux new -s work`, then detach with **Ctrl+B D** and reattach later with `tmux attach -t work`. Long-running jobs survive Wi-Fi blips.

> **Watch out:** keep a working session open while changing sshd_config. A mistake can lock you out.

## In practice

Create an Ed25519 key, copy it to a server, add a `Host` entry in `~/.ssh/config`, then disable password logins after confirming key login works in a new terminal.""",
    "key_points": [
        "Use key pairs: the private key stays with you (with a passphrase); the public key goes in authorized_keys.",
        "~/.ssh/config gives hosts short names and ProxyJump hops through a gateway.",
        "rsync syncs folders efficiently and resumably; mind trailing slashes and test --delete with --dry-run.",
        "Disable password and root logins once keys work; use tunnels for local-only services and tmux for long jobs.",
    ],
    "figure_svg": SSH,
    "figure_caption": "The private key stays on your laptop and answers the server's challenge; the server holds only the public key.",
    "questions": [
        mcq("Where does your public key go on the server?", ["/etc/ssh/sshd_config", "~/.ssh/authorized_keys", "~/.ssh/known_hosts", "/root/.ssh/id_ed25519"], 1,
            "authorized_keys lists keys allowed to log in."),
        mcq("In the diagram, what crosses the network during login?", ["The private key", "A challenge and a response proving possession of the key", "The password", "The public key file"], 1,
            "The private key never leaves your laptop.",
            SSH, "Laptop holding the private key, server holding the public key in authorized_keys; a challenge goes to the laptop and proof goes back."),
        mcq("Which tool copies only changed files and can resume?", ["scp", "rsync", "cp", "ftp"], 1, "rsync compares and transfers differences."),
        mcq("What does `ssh -L 8080:localhost:80 neo` do?", ["Exposes your laptop's port 80 on neo", "Makes localhost:8080 on your laptop reach port 80 on neo", "Opens a SOCKS proxy", "Changes neo's SSH port"], 1,
            "A local forward tunnels a local port to the remote side."),
        mcq("Before setting PasswordAuthentication no, what should you do?", ["Reboot", "Confirm key login works in a new session while keeping one open", "Delete authorized_keys", "Disable the firewall"], 1,
            "Avoid locking yourself out."),
        mcq("What does ProxyJump do?", ["Speeds up SSH", "Connects through an intermediate host automatically", "Forwards X11", "Rotates keys"], 1, "Great for machines behind one gateway."),
        mcq("In the diagram, which key would an attacker need to steal to log in as you?", ["The public key on the server", "The private key on the laptop", "Either", "Neither"], 1,
            "The public key is safe to share.", SSH, "SSH key authentication diagram."),
        open_q("Explain the difference between rsync -a site/ dest/ and rsync -a site dest/.", "With the trailing slash, rsync copies the contents of site into dest; without it, it copies the site directory itself, creating dest/site.",
               ["trailing slash copies the contents", "no slash copies the folder itself"], "Use --dry-run when unsure."),
        open_q("List three changes that make an internet-facing SSH server safer.", "Disable password authentication in favour of keys, disable root login, and add fail2ban (or better, put SSH behind a VPN like WireGuard instead of exposing it).",
               ["keys only, no passwords", "no root login", "fail2ban or VPN"], "AllowUsers and a non-default port reduce noise too."),
        open_q("Why run a long job inside tmux on a server?", "Because the job keeps running in the tmux session even if your SSH connection drops, and you can reattach later to check on it.",
               ["survives disconnection", "reattach later"], "Ctrl+B D to detach, tmux attach to return."),
    ],
}

L4 = {
    "title": "systemd services, timers and the journal",
    "minutes": 9,
    "photo_query": "",
    "body": """The beginner course used `systemctl` to control services. Now you'll write your own: running your app as a service, scheduling jobs with timers, and reading the journal like a pro.

## Writing a service unit

Unit files you create go in `/etc/systemd/system/`. A service for an app in `/opt/notes`:

```
[Unit]
Description=Notes app
After=network-online.target
Wants=network-online.target

[Service]
User=notes
WorkingDirectory=/opt/notes
ExecStart=/opt/notes/venv/bin/python app.py
Restart=on-failure
RestartSec=5
Environment=PORT=8000

[Install]
WantedBy=multi-user.target
```

- **[Unit]**: description and ordering (`After`, `Wants`, `Requires`).
- **[Service]**: what to run, as which user, how to restart, environment (`EnvironmentFile=` for secrets).
- **[Install]**: what "enable" hooks it into; `multi-user.target` is the normal booted-system state.

Then `sudo systemctl daemon-reload` (after any unit change), `sudo systemctl enable --now notes`.

## Hardening for free

systemd can sandbox a service with a few lines: `NoNewPrivileges=yes`, `ProtectSystem=strict` (read-only OS), `ProtectHome=yes`, `PrivateTmp=yes`, `ReadWritePaths=/var/lib/notes`. `systemd-analyze security notes` scores how exposed a unit is.

## Overrides, not edits

Don't edit packaged unit files in `/lib/systemd/system`; updates overwrite them. `sudo systemctl edit nginx` creates a **drop-in** override that survives upgrades.

## Timers instead of cron

A **timer** unit triggers a service on a schedule. `backup.service` (with `Type=oneshot`) does the work; `backup.timer` schedules it:

```
[Timer]
OnCalendar=*-*-* 02:30:00
Persistent=true
RandomizedDelaySec=10m

[Install]
WantedBy=timers.target
```

`Persistent=true` runs a missed job after the machine was off. Enable with `systemctl enable --now backup.timer` and list with `systemctl list-timers`. Advantages over cron: logs in the journal, dependencies, resource limits and easy status checks. Cron (`crontab -e`) still works fine for simple jobs.

## The journal

- `journalctl -u notes --since "1 hour ago"`, or `--since today`.
- `-p warning` filters by priority; `-b -1` shows the previous boot (great after a crash).
- `-o json-pretty` for structured output; `--disk-usage` and `--vacuum-time=30d` manage its size.
- Make logs persist across reboots by creating `/var/log/journal` (or setting `Storage=persistent`).

> **Tip:** `systemctl status` shows the last few log lines; when a service fails to start, `journalctl -u name -e` jumps to the end of its full log.

## In practice

Turn a script you run by hand into a `oneshot` service plus a timer, enable it, check `systemctl list-timers`, then read its output with `journalctl -u`.""",
    "key_points": [
        "Unit files have [Unit] ordering, [Service] what/who/restart, and [Install] where enable hooks them in.",
        "Run daemon-reload after changes; use systemctl edit drop-ins instead of editing packaged units.",
        "Sandboxing options (NoNewPrivileges, ProtectSystem, PrivateTmp) harden services cheaply.",
        "Timers (OnCalendar, Persistent) replace cron with journal logging; journalctl filters by unit, time, priority and boot.",
    ],
    "figure_svg": UNIT,
    "figure_caption": "A service unit: [Unit] ordering, [Service] what to run (X), [Install] where enable attaches it (Y).",
    "questions": [
        mcq("Where should you put your own unit files?", ["/lib/systemd/system", "/etc/systemd/system", "/usr/bin", "/var/log"], 1, "/etc overrides and adds to the packaged units."),
        mcq("What must you run after creating or editing a unit file?", ["systemctl reboot", "systemctl daemon-reload", "journalctl --flush", "systemctl reset"], 1, "systemd rereads unit files."),
        mcq("In the diagram, what does the [Install] section marked Y control?", ["The command to run", "What `systemctl enable` hooks the service into", "The log format", "The user"], 1,
            "WantedBy=multi-user.target means enabling starts it at normal boot.",
            UNIT, "A unit file with [Unit] After=network-online.target, [Service] ExecStart, User and Restart (X), and [Install] WantedBy=multi-user.target (Y)."),
        mcq("How should you change a setting in a packaged nginx unit?", ["Edit /lib/systemd/system/nginx.service", "sudo systemctl edit nginx", "Copy it to /tmp", "Reinstall nginx"], 1,
            "Drop-ins survive package upgrades."),
        mcq("What does Persistent=true do in a timer?", ["Keeps the service running forever", "Runs a missed job when the machine comes back", "Saves logs", "Prevents disabling"], 1,
            "Missed schedules while off are caught up."),
        mcq("How do you see logs from the previous boot?", ["journalctl -b -1", "journalctl --old", "dmesg -1", "systemctl status -b"], 0, "-b -1 selects the previous boot."),
        mcq("In the diagram, which section (X) makes the service restart if it crashes?", ["[Unit]", "[Service]", "[Install]", "None"], 1,
            "Restart=on-failure lives in [Service].", UNIT, "Unit file with [Service] containing Restart=on-failure."),
        open_q("Give two advantages of a systemd timer over a cron job.", "Its output goes to the journal so you can read it with journalctl, you can check last and next run with list-timers and status, it can catch up missed runs with Persistent, and it gets systemd's dependencies, sandboxing and resource limits.",
               ["logs in the journal", "status and list-timers", "catch-up or dependencies or limits"], "Cron is still fine for simple jobs."),
        open_q("Why run an app's service as a dedicated user instead of root?", "So that if the app is compromised or buggy, it only has that user's limited permissions instead of full control of the system.",
               ["limits damage if compromised", "least privilege"], "Combine with systemd's sandboxing options."),
        open_q("A service fails to start. What commands do you use to find out why?", "systemctl status servicename to see the state and last lines, then journalctl -u servicename -e (or with --since) to read its full recent log for the error.",
               ["systemctl status", "journalctl -u for the full log"], "The error is almost always in the journal."),
    ],
}

L5 = {
    "title": "Disks, filesystems and mounts",
    "minutes": 9,
    "photo_query": "hard disk drive",
    "body": """Adding a disk to a server, or working out why one is full, needs a clear picture of the layers: **disk → partition → filesystem → mount point**.

## Seeing disks

- `lsblk` shows block devices as a tree: disks (`sda`, `nvme0n1`), their partitions (`sda1`, `nvme0n1p1`) and where each is mounted.
- `lsblk -f` adds filesystem types, labels and **UUIDs**.
- `sudo blkid` lists UUIDs too.

Device names like `/dev/sdb` can change between boots when disks are added; **UUIDs don't**, so use them in configuration.

## Partitions and filesystems

- Partition a new disk with `fdisk`, `parted` or `gdisk` (GPT is the modern partition table).
- Create a filesystem with `mkfs`: `sudo mkfs.ext4 /dev/sdb1`. **ext4** is the dependable default; **XFS** suits large files and is the RHEL default; **Btrfs** and **ZFS** add snapshots and checksums.

> **Watch out:** `mkfs` on the wrong device erases it. Check with `lsblk` twice and read the device name out loud.

## Mounting

A filesystem becomes usable when it's **mounted** onto a directory:

```
sudo mkdir -p /srv/media
sudo mount /dev/sdb1 /srv/media
```

To mount at boot, add a line to `/etc/fstab`:

```
UUID=3f2c...  /srv/media  ext4  defaults,noatime  0  2
```

Fields: device, mount point, type, options, dump, fsck order. Test with `sudo mount -a` (mounts everything in fstab) before rebooting: a bad fstab line can stop the system booting normally. For external drives that may be absent, add `nofail`.

Network shares mount the same way: NFS (`server:/export /mnt/nas nfs defaults 0 0`) or SMB/CIFS with a credentials file.

## Space: df and du

- `df -h` shows space per mounted filesystem. `df -i` shows **inodes**: a disk can be "full" with lots of tiny files even when bytes remain.
- `du -sh /var/*` shows which directories are big; `sudo du -xh / --max-depth=1 | sort -h` finds the culprit on the root filesystem; `ncdu` is an interactive version.
- Space not freed after deleting a big log? A process still has the file open. `sudo lsof +L1` lists deleted-but-open files; restart that process.

Common space hogs: `/var/log`, the systemd journal, Docker (`docker system df`), old kernels and package caches.

## Swap

**Swap** is disk space used as overflow memory. A little prevents sudden out-of-memory kills; heavy swapping means the machine needs more RAM. `swapon --show` and `free -h` show it.

## In practice

Run `lsblk -f` and `df -h` on your server and match each mount to its disk. Then find the five biggest directories under `/var` with `du`.""",
    "key_points": [
        "Disk → partition → filesystem → mount point; lsblk -f shows the whole picture.",
        "Use UUIDs in /etc/fstab, test with mount -a, and add nofail for drives that may be missing.",
        "ext4 is the safe default; XFS for large files; Btrfs and ZFS add snapshots and checksums.",
        "df -h for free space, df -i for inodes, du to find big directories, lsof +L1 for deleted-but-open files.",
    ],
    "figure_svg": DISKS,
    "figure_caption": "Disk /dev/sdb holds two partitions with filesystems, each mounted into the directory tree.",
    "questions": [
        mcq("Which command shows disks, partitions and mount points as a tree?", ["df", "lsblk", "mount -a", "fdisk -l only"], 1, "lsblk; add -f for filesystems and UUIDs."),
        mcq("Why use UUIDs instead of /dev/sdb1 in /etc/fstab?", ["They're shorter", "Device names can change between boots; UUIDs don't", "fstab requires them", "They're faster"], 1, "Adding a disk can reorder names."),
        mcq("In the diagram, where is the XFS filesystem mounted?", ["/srv/media", "/var/lib/docker", "/dev/sdb", "/"], 1,
            "sdb2 (xfs) is mounted at /var/lib/docker.",
            DISKS, "Disk /dev/sdb with partitions sdb1 (ext4) mounted at /srv/media and sdb2 (xfs) mounted at /var/lib/docker."),
        mcq("What should you do after editing /etc/fstab, before rebooting?", ["Nothing", "sudo mount -a to test it", "Run mkfs again", "Delete /etc/mtab"], 1, "A bad line can break booting."),
        mcq("df -h shows free space but writes fail with 'No space left on device'. What should you check?", ["CPU", "Inodes with df -i", "Swap", "The UUID"], 1, "Many tiny files can exhaust inodes."),
        mcq("You deleted a 20 GB log but df shows no change. Why?", ["df is cached", "A process still has the deleted file open", "ext4 delays deletes for a day", "The file moved to trash"], 1,
            "Space is freed when the last handle closes; lsof +L1 finds it."),
        mcq("In the diagram, what makes these mounts happen automatically at boot?", ["lsblk", "/etc/fstab entries", "mkfs", "swap"], 1,
            "fstab lists filesystems to mount at boot.", DISKS, "Disk and mount diagram noting fstab by UUID."),
        open_q("Describe the steps to add a new empty disk and mount it at /srv/data permanently.", "Identify it with lsblk, partition it (e.g. with parted, GPT), create a filesystem with mkfs.ext4, make the /srv/data directory, find the UUID with lsblk -f or blkid, add a UUID line to /etc/fstab, and test with mount -a.",
               ["identify and partition", "mkfs to create a filesystem", "fstab entry by UUID and mount -a"], "Double-check the device name before mkfs."),
        open_q("How would you find what's filling up the root filesystem?", "Run df -h to confirm which filesystem is full, then sudo du -xh / --max-depth=1 | sort -h (or ncdu) and drill into the largest directories; check usual suspects like /var/log, the journal and Docker.",
               ["df to confirm", "du sorted or ncdu to find big directories", "check logs, journal, Docker"], "-x stays on one filesystem."),
        open_q("What's the purpose of nofail in an fstab line?", "It lets the system boot normally even if that device is missing, which matters for external or network drives that might not be connected.",
               ["boot continues if the device is missing", "for external or network drives"], "Otherwise boot can drop to emergency mode."),
    ],
}

L6 = {
    "title": "Networking tools and firewalls",
    "minutes": 9,
    "photo_query": "",
    "body": """"Is it the network?" is one of the most common questions in operations. Working **up the layers** with a few tools answers it quickly.

## 1. Interfaces, addresses and routes

- `ip a` (ip address) shows interfaces, whether they're UP, and their IP addresses.
- `ip route` shows the routing table; the `default via` line is your **gateway**.
- `ip neigh` shows the ARP table (neighbours on the LAN).

The old `ifconfig` and `route` are deprecated; learn the `ip` commands.

## 2. Reachability

- `ping -c4 192.168.0.1` tests the gateway; `ping -c4 1.1.1.1` tests the internet by IP.
- `traceroute` or `mtr 1.1.1.1` shows each hop and where packets get lost or slow.

If pinging an IP works but names don't, it's DNS.

## 3. DNS

- `dig example.org` asks your configured resolver; `dig @1.1.1.1 example.org` asks a specific one; `dig +short` trims the output.
- `resolvectl status` (systemd-resolved) shows which DNS servers are in use; `/etc/hosts` overrides names locally.

## 4. Is the service listening?

- `ss -tlnp` lists **t**CP **l**istening sockets, **n**umeric, with **p**rocesses (`-u` for UDP).
- A service bound to `127.0.0.1:8080` is only reachable locally; `0.0.0.0:8080` (or `*:8080`) listens on all interfaces.
- `ss -tnp` shows established connections.

## 5. Does the application answer?

- `curl -v http://192.168.0.100:8080/health` shows the connection, request and response headers.
- `curl -I` fetches headers only; `-k` ignores certificate errors when testing.
- `nc -zv host 5432` checks whether a TCP port accepts connections.

## Firewalls

Linux filters packets with **netfilter**, configured today with **nftables** (iptables is the older interface). Friendlier front ends:

- **UFW** (Ubuntu): `sudo ufw allow 22/tcp`, `sudo ufw allow from 192.168.0.0/24 to any port 8080`, `sudo ufw enable`, `sudo ufw status numbered`.
- **firewalld** (RHEL family): zones and `firewall-cmd --add-service=https --permanent`.

A good default is to **deny incoming, allow outgoing**, then open only the ports you need, ideally only to the networks that need them.

> **Remember:** Docker writes its own netfilter rules for published ports, which can bypass UFW. Bind container ports to specific addresses instead of relying on the host firewall.

## Capturing traffic

When all else fails, look at the packets: `sudo tcpdump -i eth0 port 53` shows DNS traffic on eth0. Add `-w capture.pcap` to save for Wireshark.

## In practice

Pick a service in your home lab and trace a request through all five steps: interface and route, ping, DNS, `ss` to confirm it listens on the right address, and `curl -v`. Then review `ufw status` and close anything you don't recognise.""",
    "key_points": [
        "Work up the layers: ip a / ip route, ping and mtr, dig for DNS, ss -tlnp for listeners, curl -v for the app.",
        "If IPs work but names don't, it's DNS; 127.0.0.1 listeners are local-only, 0.0.0.0 is all interfaces.",
        "nftables underlies firewalls; UFW and firewalld are front ends. Default deny incoming, open only what's needed.",
        "Docker's rules can bypass UFW; tcpdump captures packets when everything else looks fine.",
    ],
    "figure_svg": NET,
    "figure_caption": "Troubleshoot bottom-up: link and routes, reachability, DNS, listening sockets, then the application.",
    "questions": [
        mcq("Which command shows your default gateway?", ["ip a", "ip route", "ss -tlnp", "dig"], 1, "The 'default via' line in ip route."),
        mcq("Pinging 1.1.1.1 works but `ping example.org` fails. What's the likely problem?", ["The cable", "DNS", "The firewall on the website", "The gateway"], 1, "IP connectivity is fine; name resolution isn't."),
        mcq("In the diagram, which step tells you whether the service is listening on the right address?", ["1", "3", "4", "5"], 2,
            "Step 4, ss -tlnp, lists listening sockets and their addresses.",
            NET, "Five stacked troubleshooting steps: 1 ip a / ip route, 2 ping, 3 dig, 4 ss -tlnp, 5 curl -v."),
        mcq("`ss -tlnp` shows 127.0.0.1:8080 for your app. Why can't other machines reach it?", ["It's UDP", "It only listens on the loopback interface", "Port 8080 is blocked by default", "It's not running"], 1,
            "Bind to 0.0.0.0 or a LAN address to accept remote connections."),
        mcq("Which UFW command allows port 8080 only from the 192.168.0.0/24 network?", ["ufw allow 8080", "ufw allow from 192.168.0.0/24 to any port 8080", "ufw deny 8080", "ufw open lan 8080"], 1,
            "Restrict by source network."),
        mcq("Which tool shows each hop and where packets are lost?", ["dig", "mtr", "ss", "curl"], 1, "mtr combines traceroute and ping."),
        mcq("In the diagram, which step would you take first if the server has just been plugged into a new switch?", ["1", "2", "3", "5"], 0,
            "Start at the bottom: is the link up with the right address and route?", NET, "Bottom-up network troubleshooting steps."),
        open_q("A web app on your server isn't reachable from your laptop. Walk through how you'd find the cause.", "Check the server's interface and route (ip a, ip route), ping it from the laptop, check name resolution with dig if using a name, check the app listens on the right address and port with ss -tlnp, check the firewall (ufw status), then curl -v from the laptop to see the response.",
               ["check addresses and reachability", "check DNS", "check it's listening on the right address", "check the firewall and curl"], "Bottom-up saves guesswork."),
        open_q("Why is 'deny incoming, allow outgoing' a sensible firewall default?", "It blocks everything you haven't deliberately opened, so a forgotten or new service isn't exposed, while still letting the server reach updates and other services it needs.",
               ["blocks unexpected services", "only opened ports are exposed", "outgoing still works for updates"], "Then allow specific ports to specific networks."),
        open_q("When would you reach for tcpdump?", "When the higher-level tools disagree or show nothing obvious and you need to see whether packets actually arrive or leave, for example to confirm DNS queries go out or that SYNs reach the server.",
               ["to see the actual packets", "when other tools don't explain it"], "Save to .pcap and open in Wireshark for detail."),
    ],
}

PACK = {
    "id": "linux-intermediate",
    "version": 1,
    "topic": "Linux",
    "title": "Linux power user",
    "summary": "Pipes and text tools, shell scripts, SSH done properly, writing systemd services and timers, disks and mounts, and network troubleshooting. For people comfortable with the basics who run their own servers.",
    "icon": "binary",
    "level": "intermediate",
    "length": "short",
    "area": "technology",
    "tags": ["linux", "command-line", "sysadmin", "bash", "networking"],
    "sections": [
        {"title": "The shell", "summary": "Combine tools, automate with scripts and work remotely.", "lessons": [
            {"title": L1["title"], "summary": "Combine commands with redirection, pipes and text tools.", "lesson": L1},
            {"title": L2["title"], "summary": "Write robust bash scripts with error handling.", "lesson": L2},
            {"title": L3["title"], "summary": "Use SSH keys, config, rsync and tunnels securely.", "lesson": L3},
        ]},
        {"title": "The system", "summary": "Services, storage and networking on a real server.", "lessons": [
            {"title": L4["title"], "summary": "Write services and timers and read the journal.", "lesson": L4},
            {"title": L5["title"], "summary": "Add disks, mount filesystems and find what's using space.", "lesson": L5},
            {"title": L6["title"], "summary": "Troubleshoot networks layer by layer and configure a firewall.", "lesson": L6},
        ]},
    ],
}
