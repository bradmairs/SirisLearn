"""Linux internals and administration: expert."""

from app.coursepacks import mcq, open_q
from app.packs._draw import AMBER, BLUE, GREEN, INK, MUTED, PURPLE, RED, arrow, box, line, svg, text, title

BOOT = svg(
    title("The boot sequence"),
    box(20, 60, 85, 50, "UEFI", INK, size=13, sub="firmware"),
    arrow(105, 85, 125, 85, MUTED),
    box(125, 60, 85, 50, "GRUB", BLUE, size=13, sub="bootloader"),
    arrow(210, 85, 230, 85, MUTED),
    box(230, 60, 100, 50, "kernel", AMBER, size=13, sub="+ initramfs"),
    arrow(330, 85, 350, 85, MUTED),
    box(350, 60, 110, 50, "systemd", GREEN, size=13, sub="PID 1"),
    arrow(405, 110, 405, 150, GREEN),
    box(300, 150, 160, 50, "default.target", GREEN, size=13, sub="services start"),
    text(65, 140, "1", 16, INK, weight="bold"), text(167, 140, "2", 16, BLUE, weight="bold"), text(280, 140, "3", 16, AMBER, weight="bold"),
    text(170, 230, "initramfs finds and mounts the real root filesystem", 12, MUTED),
)

MEMORY = svg(
    title("Where did the memory go? (free -h)"),
    box(30, 70, 420, 50, "", INK),
    '<rect x="32" y="72" width="150" height="46" fill="#5fd3ff" opacity="0.5"/>',
    '<rect x="182" y="72" width="200" height="46" fill="#8af5c8" opacity="0.35"/>',
    '<rect x="382" y="72" width="66" height="46" fill="#7c93a6" opacity="0.3"/>',
    text(107, 101, "used by apps", 12, INK), text(282, 101, "buff/cache", 12, INK), text(415, 101, "free", 12, INK),
    text(107, 145, "A", 15, BLUE, weight="bold"), text(282, 145, "B", 15, GREEN, weight="bold"), text(415, 145, "C", 15, MUTED, weight="bold"),
    text(240, 190, "'available' ≈ free + reclaimable cache", 13, INK),
    text(240, 222, "low 'free' is normal; low 'available' is not", 12, AMBER),
)

LVM = svg(
    title("LVM: pooling disks into flexible volumes"),
    box(30, 220, 120, 40, "/dev/sdb (PV)", INK, size=12), box(180, 220, 120, 40, "/dev/sdc (PV)", INK, size=12), box(330, 220, 120, 40, "/dev/sdd (PV)", INK, size=12),
    box(30, 140, 420, 50, "volume group: data (VG)", BLUE, size=13),
    arrow(90, 220, 90, 192, MUTED), arrow(240, 220, 240, 192, MUTED), arrow(390, 220, 390, 192, MUTED),
    box(30, 60, 200, 50, "lv_media (LV)", GREEN, size=13, sub="ext4 → /srv/media"), box(250, 60, 200, 50, "lv_db (LV)", AMBER, size=13, sub="xfs → /var/lib/db"),
    arrow(130, 140, 130, 112, MUTED), arrow(350, 140, 350, 112, MUTED),
)

HARDEN = svg(
    title("Mandatory access control"),
    box(30, 60, 190, 160, "", BLUE), text(125, 84, "DAC (permissions)", 13, BLUE, weight="bold"),
    text(125, 112, "owner decides", 12, INK), text(125, 134, "root bypasses it", 12, RED), text(125, 186, "A", 16, BLUE, weight="bold"),
    box(260, 60, 190, 160, "", GREEN), text(355, 84, "MAC (SELinux/AppArmor)", 13, GREEN, weight="bold"),
    text(355, 112, "policy decides", 12, INK), text(355, 134, "applies to root too", 12, GREEN), text(355, 156, "nginx may only read", 12, INK), text(355, 174, "/var/www", 12, INK),
    text(355, 206, "B", 16, GREEN, weight="bold"),
    text(240, 262, "both must allow an access", 12, MUTED),
)

PERF = svg(
    title("vmstat 1"),
    box(20, 55, 440, 170, "", INK),
    text(40, 80, "r  b   swpd  free   si  so   bi    bo   us sy id wa", 12, BLUE, anchor="start"),
    text(40, 108, "1  0      0  812M    0   0   12    40   10  3 86  1", 12, INK, anchor="start"),
    text(40, 132, "9  0      0  790M    0   0   10    38   88 10  2  0", 12, AMBER, anchor="start"),
    text(40, 156, "1  6      0  780M    0   0 9200  3100    5  4 41 50", 12, RED, anchor="start"),
    text(450, 132, "X", 15, AMBER, weight="bold", anchor="end"), text(450, 156, "Y", 15, RED, weight="bold", anchor="end"),
    text(240, 205, "r = runnable, b = blocked on I/O, wa = I/O wait %", 12, MUTED),
    text(240, 262, "8 CPUs", 12, MUTED),
)

BACKUP = svg(
    title("The 3-2-1 backup rule"),
    box(30, 70, 130, 90, "3 copies", BLUE, sub="live + 2 backups"),
    box(175, 70, 130, 90, "2 media", GREEN, sub="e.g. NAS + cloud"),
    box(320, 70, 130, 90, "1 off-site", AMBER, sub="survives fire/theft"),
    box(100, 190, 280, 50, "+ test restores", PURPLE, sub="untested backups aren't backups"),
)

L1 = {
    "title": "How Linux boots",
    "minutes": 9,
    "photo_query": "",
    "body": """When a server won't boot, knowing each stage tells you where to look and what to fix.

## 1. Firmware: UEFI

On power-on, the **UEFI** firmware (BIOS on older machines) initialises hardware and reads its boot entries (`efibootmgr -v` lists them). It loads a bootloader from the **EFI System Partition** (a small FAT32 partition, usually mounted at `/boot/efi`). **Secure Boot** verifies each step is signed.

## 2. Bootloader: GRUB

**GRUB** shows the menu, loads the chosen **kernel** and **initramfs** from `/boot`, and passes the **kernel command line** (`cat /proc/cmdline` shows it), which includes where the root filesystem is (`root=UUID=…`).

Configure GRUB in `/etc/default/grub`, then regenerate with `update-grub` (Debian) or `grub2-mkconfig -o /boot/grub2/grub.cfg` (RHEL). At the menu, press **e** to edit the command line for one boot, a lifesaver for recovery.

## 3. Kernel and initramfs

The kernel initialises CPUs, memory and drivers. The **initramfs** is a small temporary root filesystem with just enough tools and drivers (storage controllers, LVM, RAID, decryption) to find and mount the **real root filesystem**. Then it hands over. Rebuild it with `update-initramfs -u` or `dracut -f` after changing storage or crypto setup.

## 4. systemd

The kernel starts **systemd as PID 1**. It reads unit files and works towards the **default target** (`systemctl get-default`): usually `multi-user.target` on servers or `graphical.target` on desktops. Services start in parallel, ordered by their dependencies.

- `systemd-analyze` shows boot time; `systemd-analyze blame` lists the slowest units; `systemd-analyze critical-chain` shows what the boot waited on.

## When boot fails

- **GRUB rescue prompt**: the bootloader can't find its files (often after disk changes); boot a live USB, chroot in and reinstall GRUB.
- **Kernel panic**, "unable to mount root fs": a wrong `root=` or a missing driver in the initramfs.
- **Emergency mode**: often a bad `/etc/fstab` line. Log in, `journalctl -xb` to read why, fix fstab (add `nofail` for optional disks), `systemctl default`.
- **Forgotten root password**: edit the kernel line at GRUB, add `systemd.unit=rescue.target` (or `init=/bin/bash` and remount root read-write).

> **Tip:** keep at least one older kernel installed; if a new one misbehaves, pick the previous one from the GRUB menu.

## In practice

Run `systemd-analyze critical-chain`, read `/proc/cmdline`, list `/boot` and `efibootmgr -v`. In a VM, deliberately break fstab, boot into emergency mode and repair it, so you've practised before it matters.""",
    "key_points": [
        "UEFI loads the bootloader from the EFI System Partition; Secure Boot checks signatures.",
        "GRUB loads the kernel and initramfs and passes the command line (including root=).",
        "The initramfs mounts the real root; systemd (PID 1) then brings up the default target.",
        "Read failures by stage: GRUB rescue, kernel panic/root fs, emergency mode (often fstab); use systemd-analyze for slow boots.",
    ],
    "figure_svg": BOOT,
    "figure_caption": "Firmware (1) loads GRUB (2), which loads the kernel and initramfs (3); systemd then starts services.",
    "questions": [
        mcq("Where does UEFI load the bootloader from?", ["The MBR", "The EFI System Partition", "/home", "The initramfs"], 1, "A small FAT32 partition, usually mounted at /boot/efi."),
        mcq("In the diagram, what is the job of stage 3's initramfs?", ["Show the boot menu", "Find and mount the real root filesystem", "Start web servers", "Check signatures"], 1,
            "It contains the drivers and tools needed to reach the real root.",
            BOOT, "Boot chain: UEFI (1), GRUB (2), kernel plus initramfs (3), systemd PID 1, then default.target."),
        mcq("Which command lists the units that slowed boot the most?", ["journalctl -b", "systemd-analyze blame", "dmesg", "lsblk"], 1, "blame sorts units by start-up time."),
        mcq("A server drops to emergency mode after you added a USB backup disk to fstab. Most likely cause?", ["Bad kernel", "The fstab entry fails when the disk is absent (no nofail)", "GRUB is missing", "Secure Boot"], 1,
            "Add nofail for optional disks."),
        mcq("Where do you see the kernel command line the system booted with?", ["/etc/default/grub", "/proc/cmdline", "/boot/efi", "systemctl status"], 1, "It's what GRUB actually passed."),
        mcq("After changing GRUB settings in /etc/default/grub on Debian, what must you run?", ["update-grub", "dracut", "systemctl daemon-reload", "efibootmgr"], 0,
            "The config isn't read until grub.cfg is regenerated."),
        mcq("In the diagram, which component runs as PID 1?", ["GRUB", "The kernel", "systemd", "UEFI"], 2, "The kernel starts systemd as the first process.",
            BOOT, "Boot sequence ending with systemd (PID 1) starting default.target."),
        open_q("A new kernel update leaves the server unable to boot. How would you recover?", "Reboot and choose the previous kernel from the GRUB menu (advanced options), get the system up, then investigate or remove the bad kernel, rebuild its initramfs or hold the update.",
               ["pick the older kernel in GRUB", "boot, then fix or remove the new kernel"], "Keep at least one known-good kernel installed."),
        open_q("Why might a system boot fine but fail with 'unable to mount root fs' after moving its root onto LVM or an encrypted volume?", "The initramfs doesn't contain the LVM or decryption tools and drivers, or the root= on the command line is wrong; rebuilding the initramfs (update-initramfs or dracut) and fixing root= fixes it.",
               ["initramfs lacks the needed drivers or tools", "rebuild initramfs or fix root="], "Storage changes need initramfs changes."),
        open_q("Explain what systemd-analyze critical-chain tells you.", "It shows the chain of units the boot had to wait on in sequence, with how long each took, so you can see which dependency actually delayed reaching the default target.",
               ["the sequence the boot waited on", "time for each unit"], "blame lists slow units; critical-chain shows which ones mattered."),
    ],
}

L2 = {
    "title": "Processes, signals and memory",
    "minutes": 10,
    "photo_query": "",
    "body": """Expert troubleshooting depends on a clear model of how the kernel runs processes and manages memory.

## Process states

`ps -eo pid,stat,cmd` shows each process's state:

- **R** running or runnable (waiting for a CPU).
- **S** interruptible sleep (waiting for an event): most processes, most of the time.
- **D** uninterruptible sleep, usually waiting on disk or network storage I/O. Signals can't interrupt it; many D processes point to a storage problem (a hung NFS mount is the classic).
- **Z** zombie: finished, but its parent hasn't collected its exit status. Zombies use no CPU or memory, but a growing number means a buggy parent.
- **T** stopped (Ctrl+Z or SIGSTOP).

The **load average** counts R *and* D processes, so a high load with idle CPUs often means I/O trouble rather than CPU shortage.

## Signals

- **SIGTERM (15)** asks politely; **SIGKILL (9)** and **SIGSTOP** can't be caught or ignored.
- **SIGHUP (1)** traditionally means "reload configuration" for daemons.
- **SIGINT (2)** is Ctrl+C. **SIGCHLD** tells a parent a child exited.
- A process killed by signal N exits with code 128 + N (137 = 9, 143 = 15).

## Virtual memory

Each process sees its own **virtual address space**. The kernel maps pages to physical RAM on demand, shares identical pages (libraries, forked processes), and can back pages with files or swap.

- **RSS** is the resident memory a process uses now; **VSZ** is its virtual size (often huge and mostly meaningless).
- **Page cache**: the kernel uses free RAM to cache file data. That's why `free` shows little "free" memory on a healthy system. What matters is **available** (free plus reclaimable cache).
- **Swap** holds rarely used pages; `si`/`so` in `vmstat` show swapping in and out. Some swap use is fine; constant swapping (thrashing) is not.
- **Overcommit**: Linux lets processes allocate more than exists, betting they won't all use it.

## The OOM killer

When memory really runs out, the **OOM killer** picks a process to kill, scored by memory use (see `/proc/<pid>/oom_score`). You can protect critical processes with `oom_score_adj` (or `OOMScoreAdjust=` in a systemd unit). Kills are logged: `journalctl -k | grep -i oom`.

## /proc: the kernel's window

- `/proc/<pid>/status`, `/proc/<pid>/limits`, `/proc/<pid>/fd/` (open files), `/proc/<pid>/maps` (memory map).
- `/proc/meminfo`, `/proc/loadavg`, `/proc/pressure/*` (**PSI**: how much time tasks stall on CPU, memory or I/O, a great saturation signal).

> **Common misconception:** "Linux is using all my RAM, I need more." Usually it's page cache, which is released instantly when apps need it. Check `available`, swap activity and PSI before buying RAM.

## In practice

Read `free -h` and `/proc/meminfo` on a busy server and explain every line. Find a process's open files via `/proc/<pid>/fd`, and check `/proc/pressure/memory` during load.""",
    "key_points": [
        "States: R runnable, S sleeping, D uninterruptible (usually storage), Z zombie; load average counts R and D.",
        "SIGTERM is polite, SIGKILL can't be caught, SIGHUP often reloads config; exit 128+N means killed by signal N.",
        "Page cache makes 'free' look low; 'available' is what matters. Constant swapping and PSI reveal real pressure.",
        "The OOM killer picks victims by oom_score; tune with oom_score_adj; /proc exposes per-process detail.",
    ],
    "figure_svg": MEMORY,
    "figure_caption": "free -h: memory used by apps (A), reclaimable buffer/page cache (B) and truly free (C).",
    "questions": [
        mcq("A process in state D is usually waiting on what?", ["CPU time", "Storage I/O", "User input", "A signal"], 1, "Uninterruptible sleep, typically disk or network storage."),
        mcq("In the diagram, which region can the kernel give back to applications almost instantly?", ["A", "B", "C only", "None"], 1,
            "B is buffer/page cache, reclaimable on demand.",
            MEMORY, "A memory bar split into used by apps (A), buff/cache (B) and free (C), noting available is roughly free plus reclaimable cache."),
        mcq("Load average is 12 on an 8-CPU server, but the CPUs are mostly idle. What's the likely cause?", ["CPU shortage", "Processes blocked on I/O (D state) counted in the load", "Too much free memory", "Zombies"], 1,
            "Load includes uninterruptible tasks."),
        mcq("What exit code does a process killed by SIGKILL return?", ["9", "137", "143", "1"], 1, "128 + 9."),
        mcq("What does a zombie process consume?", ["Lots of memory", "Only a process table entry", "CPU time", "Disk space"], 1, "Its parent needs to reap it."),
        mcq("How can you make the OOM killer less likely to choose a critical service?", ["Give it more threads", "Lower its oom_score_adj (OOMScoreAdjust in systemd)", "Use nice", "Disable swap"], 1,
            "Negative values protect a process."),
        mcq("In the diagram, why is a small region C not a problem by itself?", ["Linux doesn't use RAM", "Unused RAM is used as cache, and available memory includes that cache", "C is swap", "The bar is wrong"], 1,
            "Look at available, not free.", MEMORY, "free -h memory breakdown."),
        open_q("Explain RSS versus VSZ and which you'd use to judge a process's real memory use.", "RSS is the physical memory the process has resident right now; VSZ is the size of its virtual address space, including mappings not in RAM. RSS (or better PSS, which shares shared pages fairly) reflects real use.",
               ["RSS is resident physical memory", "VSZ is virtual size, often huge", "use RSS or PSS"], "VSZ for a Java process can be many GB with little real use."),
        open_q("How would you tell whether a server genuinely needs more RAM?", "Check available memory rather than free, watch for sustained swapping in vmstat (si/so), memory pressure in /proc/pressure/memory, and OOM kills in the kernel log; frequent stalls or swapping mean it needs more RAM or less load.",
               ["available not free", "sustained swapping", "PSI memory pressure or OOM kills"], "Cache use alone isn't a reason."),
        open_q("A daemon should reload its configuration without restarting. What signal is traditionally used, and how would you send it?", "SIGHUP; send it with kill -HUP <pid> or systemctl reload service (which often does the same).",
               ["SIGHUP", "kill -HUP or systemctl reload"], "Check the daemon documents it."),
    ],
}

L3 = {
    "title": "Storage: LVM, RAID and advanced filesystems",
    "minutes": 10,
    "photo_query": "server hard drives RAID",
    "body": """Partitions are rigid. Real servers need storage that can grow, survive disk failures and take snapshots. That's what **LVM**, **RAID** and filesystems like **ZFS** and **Btrfs** provide.

## LVM

**Logical Volume Manager** adds a flexible layer between disks and filesystems:

- **Physical volumes (PV)**: disks or partitions given to LVM (`pvcreate /dev/sdb`).
- **Volume group (VG)**: a pool made of PVs (`vgcreate data /dev/sdb /dev/sdc`).
- **Logical volumes (LV)**: slices of the pool that hold filesystems (`lvcreate -L 500G -n media data`).

Growing a filesystem online: add a disk to the VG (`vgextend`), then `lvextend -r -L +200G data/media` (the `-r` resizes the filesystem too). ext4 can grow and shrink (offline); XFS can only grow. LVM **snapshots** capture a point in time, useful for consistent backups, but they slow writes while they exist, so keep them short-lived.

## RAID

RAID combines disks for redundancy or speed. With Linux's `mdadm` (or inside ZFS/Btrfs):

- **RAID 1**: mirror; survives one disk failure; half the raw capacity.
- **RAID 5**: striping with parity; survives one failure; loses one disk's capacity. Rebuilds on large disks are long and stressful, and a second failure (or unreadable sector) during rebuild loses the array.
- **RAID 6**: double parity; survives two failures.
- **RAID 10**: mirrored pairs, striped; fast, survives one failure per pair.

`cat /proc/mdstat` shows array status. Monitor it and replace failed disks promptly.

> **RAID is not a backup.** It protects against a disk dying, not against deletion, corruption, ransomware, fire or a bad command, which it faithfully copies to every disk.

## ZFS and Btrfs

Both combine volume management and filesystem, and add:

- **Checksums** on all data, detecting silent corruption ("bit rot"); with redundancy they **self-heal** from a good copy. Run regular **scrubs** to check everything.
- **Copy-on-write snapshots**: instant and space-efficient; send them to another machine (`zfs send | zfs receive`) for replicated backups.
- **Compression** (lz4 or zstd) that often makes storage both smaller and faster.

ZFS is mature and widely used on NAS systems (TrueNAS, Proxmox); it likes plenty of RAM for its cache (ARC) and is unforgiving of mistakes when creating pools. Btrfs is built into the kernel and suits single disks and mirrors; its RAID 5/6 modes are still not recommended.

## I/O performance basics

- `iostat -x 1` shows per-device utilisation, queue size and latency (`await`).
- SSDs need TRIM (`fstrim.timer`) to stay fast; check health with `smartctl -a /dev/sda`.
- Separate heavy I/O (databases, Docker data) from the OS disk where you can.

## In practice

In a VM with three spare virtual disks, build an LVM volume group, create and grow a logical volume with `lvextend -r`, then build a ZFS mirror, take a snapshot, delete a file and roll back.""",
    "key_points": [
        "LVM pools PVs into a VG and carves LVs; lvextend -r grows a volume and its filesystem online.",
        "RAID 1/5/6/10 trade capacity for redundancy; RAID protects against disk failure, never replaces backups.",
        "ZFS and Btrfs add checksums, self-healing with redundancy, scrubs, cheap snapshots, send/receive and compression.",
        "Watch iostat await, SMART health and TRIM; keep heavy I/O off the OS disk.",
    ],
    "figure_svg": LVM,
    "figure_caption": "Three physical volumes form one volume group, from which logical volumes are carved and formatted.",
    "questions": [
        mcq("In LVM, what is a volume group?", ["A single partition", "A pool built from physical volumes", "A filesystem type", "A RAID level"], 1, "PVs → VG → LVs."),
        mcq("In the diagram, which command adds space to lv_media and resizes its filesystem in one go?", ["pvcreate", "vgcreate", "lvextend -r", "mkfs"], 2,
            "lvextend -r grows the LV and the filesystem on it.",
            LVM, "Three physical volumes /dev/sdb, sdc and sdd feed volume group data, which holds lv_media (ext4, /srv/media) and lv_db (xfs, /var/lib/db)."),
        mcq("Which RAID level survives any two disk failures?", ["RAID 1", "RAID 5", "RAID 6", "RAID 0"], 2, "Double parity."),
        mcq("Why is RAID not a backup?", ["It's too slow", "It copies deletions, corruption and ransomware to every disk", "It only works with SSDs", "It can't be restored"], 1,
            "It protects against hardware failure only."),
        mcq("What does a ZFS scrub do?", ["Deletes old snapshots", "Reads all data and verifies checksums, repairing from redundancy", "Defragments the pool", "Encrypts data"], 1,
            "Catches silent corruption early."),
        mcq("Which filesystem can grow but not shrink?", ["ext4", "XFS", "Btrfs", "None"], 1, "XFS only grows."),
        mcq("In the diagram, how could you add capacity to the whole pool?", ["Format lv_db again", "Add another PV to the volume group with vgextend", "Delete /dev/sdb", "Create a new filesystem on sdc"], 1,
            "Adding a PV grows the VG; LVs can then be extended.", LVM, "LVM diagram with three PVs, one VG and two LVs."),
        open_q("Why is a RAID 5 rebuild on large disks risky?", "Rebuilding reads every sector of the remaining disks for many hours; with large disks the chance of hitting a second failure or an unreadable sector during that time is significant, and RAID 5 can't survive it, so the array is lost.",
               ["long rebuild reads everything", "second failure or read error loses the array"], "RAID 6 or mirrors are safer for big disks."),
        open_q("Explain how ZFS detects and repairs silent data corruption.", "It stores a checksum for every block and verifies it on read; if a block doesn't match and the pool has redundancy (a mirror or RAIDZ), it reads the good copy, returns that and rewrites the bad block. Scrubs check all data proactively.",
               ["checksums on every block", "repairs from redundant copy", "scrubs check everything"], "Without redundancy it detects but can't repair."),
        open_q("How would ZFS snapshots and send/receive support a backup strategy?", "Take regular snapshots, then send them (incrementally after the first) to a pool on another machine with zfs send | zfs receive, giving fast, consistent, versioned off-machine copies you can restore from.",
               ["regular snapshots", "incremental send to another machine", "versioned restores"], "Still keep an off-site copy."),
    ],
}

L4 = {
    "title": "Security hardening",
    "minutes": 10,
    "photo_query": "",
    "body": """Hardening reduces how many ways in there are and how far an intruder gets. No single control is enough; layers are.

## Reduce the attack surface

- Remove or disable services you don't use; `ss -tlnp` shows what's listening.
- Keep everything **patched**, automatically for security updates (`unattended-upgrades`, `dnf-automatic`), and reboot for kernel updates (or use live patching).
- Minimal installs: fewer packages, fewer vulnerabilities.

## Access control

- SSH: keys only, no root login, consider `AllowUsers`, ideally not exposed to the internet at all (VPN first). Add MFA with a PAM module for high-value hosts.
- **sudo**: give specific commands rather than full root where possible (`/etc/sudoers.d/`), keep `Defaults use_pty` and logging.
- Lock unused accounts; review `/etc/passwd`, `/etc/sudoers.d` and `~/.ssh/authorized_keys` regularly.

## Mandatory access control

Normal permissions are **discretionary (DAC)**: the owner decides, and root bypasses them. **SELinux** (RHEL family) and **AppArmor** (Ubuntu, Debian) add **mandatory access control (MAC)**: a system policy that confines each program regardless of user, so even root-run nginx can only read the files its policy allows.

- SELinux: `getenforce`, labels (`ls -Z`), and when something is blocked, `ausearch -m avc` or `sealert` explain why. Fix the label (`restorecon`, `semanage fcontext`) or toggle a boolean (`setsebool -P httpd_can_network_connect on`) instead of disabling SELinux.
- AppArmor: `aa-status`, profiles in `/etc/apparmor.d`, complain mode to learn a profile.

## Kernel and network hardening

- `sysctl` settings such as `net.ipv4.conf.all.rp_filter=1`, `kernel.kptr_restrict=2`, `kernel.dmesg_restrict=1`, and disabling IP forwarding unless the host routes.
- A default-deny firewall, with only required ports open to required sources.

## Detection and audit

- **auditd** records security-relevant events (who ran sudo, changes to `/etc/passwd`). Rules like `-w /etc/sudoers -p wa -k sudoers`.
- **fail2ban** bans IPs with repeated failures.
- **File integrity** monitoring (AIDE) detects changed system files.
- Centralise logs off the host, so an intruder can't quietly delete them.

## Benchmarks and tools

The **CIS Benchmarks** give detailed hardening checklists per distribution; **Lynis** audits a system and suggests improvements; OpenSCAP automates compliance checks.

> **Common misconception:** "Disable SELinux, it breaks things." It breaks things by blocking actions that don't fit policy, which is exactly the point. Learn to read its denials and fix the label or boolean.

## In practice

Run `lynis audit system` on a test server, work through its top suggestions, and add auditd rules watching `/etc/passwd`, `/etc/sudoers` and `/etc/ssh/sshd_config`.""",
    "key_points": [
        "Reduce attack surface: disable unused services, patch automatically, minimal installs.",
        "Tighten access: SSH keys only, no root login, scoped sudo, VPN before SSH where possible.",
        "SELinux/AppArmor enforce mandatory policy even on root; fix labels or booleans instead of disabling them.",
        "Detect and audit with auditd, fail2ban, file integrity checks and off-host logs; use CIS/Lynis as guides.",
    ],
    "figure_svg": HARDEN,
    "figure_caption": "Discretionary permissions (A) can be bypassed by root; mandatory access control (B) applies its policy to everyone.",
    "questions": [
        mcq("What distinguishes SELinux/AppArmor from normal file permissions?", ["They're faster", "A system policy confines programs even when they run as root", "They replace passwords", "They encrypt files"], 1,
            "MAC applies regardless of the user."),
        mcq("In the diagram, which model would stop a root-run nginx from reading /etc/shadow?", ["A, DAC", "B, MAC", "Neither", "Both equally"], 1,
            "Root bypasses DAC; MAC policy still confines nginx.",
            HARDEN, "DAC box A: owner decides, root bypasses it. MAC box B: policy decides, applies to root too, nginx may only read /var/www."),
        mcq("SELinux blocks nginx from connecting to a backend. What's the right fix?", ["setenforce 0 permanently", "Enable the httpd_can_network_connect boolean", "chmod 777", "Run nginx as root"], 1,
            "Use the boolean or label designed for it."),
        mcq("Which tool records who changed /etc/sudoers?", ["fail2ban", "auditd with a watch rule", "rsync", "ss"], 1, "auditd watches files and syscalls."),
        mcq("Why send logs to another host?", ["It saves disk", "An intruder can't easily delete the evidence", "It's faster", "systemd requires it"], 1, "Attackers often clean local logs."),
        mcq("What does Lynis do?", ["Signs packages", "Audits a system and suggests hardening steps", "Manages firewalls", "Backs up files"], 1, "A quick hardening review."),
        mcq("In the diagram, what must happen for an access to succeed?", ["Either model allows it", "Both DAC and MAC allow it", "Only MAC matters", "Only DAC matters"], 1,
            "Both checks apply.", HARDEN, "Comparison of DAC and MAC; both must allow an access."),
        open_q("Explain 'reduce the attack surface' with three concrete actions on a Linux server.", "Remove or disable services you don't need, keep the system patched automatically, and expose only required ports (ideally only to required networks), for example putting SSH behind a VPN.",
               ["disable unused services", "patch regularly", "limit exposed ports"], "Fewer doors, fewer break-ins."),
        open_q("Why give a user specific sudo commands instead of full root?", "So they can do the job they need (like restarting one service) without the power to change everything else; it limits mistakes and the damage if their account is compromised.",
               ["least privilege", "limits damage if compromised"], "Use /etc/sudoers.d drop-ins."),
        open_q("How would you investigate an SELinux denial?", "Check the audit log with ausearch -m avc (or sealert) to see which process was denied what access to which labelled file, then fix the file's label with restorecon or semanage fcontext, or enable the matching boolean, and test again.",
               ["read AVC denials with ausearch or sealert", "fix the label or boolean"], "Don't just disable it."),
    ],
}

L5 = {
    "title": "Performance troubleshooting",
    "minutes": 10,
    "photo_query": "",
    "body": """"The server is slow" isn't a diagnosis. A method and the right tools turn it into one in minutes.

## The 60-second checklist

Brendan Gregg's classic first look:

1. `uptime`: load averages, trending up or down?
2. `dmesg -T | tail`: kernel errors, OOM kills, disk errors.
3. `vmstat 1`: run queue (`r`), blocked (`b`), swapping (`si/so`), CPU split (`us sy id wa st`).
4. `mpstat -P ALL 1`: is one CPU pinned while others idle (a single-threaded bottleneck)?
5. `pidstat 1`: which processes use the CPU.
6. `iostat -xz 1`: per-disk `%util`, queue and `await` latency.
7. `free -m`: memory and cache.
8. `sar -n DEV 1`: network throughput per interface.
9. `sar -n TCP,ETCP 1`: connection rates and retransmits.
10. `top` or `htop`: confirm the picture.

## Reading vmstat

- `r` consistently above the number of CPUs: **CPU saturation**.
- `b` above zero and high `wa`: tasks **blocked on I/O**.
- `si`/`so` non-zero and sustained: **swapping**, so memory pressure.
- High `sy`: lots of kernel time (system calls, interrupts, contention).
- `st` (steal) on a VM: the hypervisor is giving your CPU time to someone else.

## Pressure stall information

`/proc/pressure/cpu`, `memory` and `io` report the percentage of time tasks were stalled waiting for that resource. They're the most direct "is this resource the bottleneck?" signal, and systemd and container platforms use them too.

## Going deeper

- **perf**: `perf top` shows hot functions live; `perf record -g` + `perf report` profiles with call stacks; **flame graphs** visualise where CPU time goes.
- **strace -c -p <pid>**: counts system calls (expensive on busy processes; use briefly).
- **eBPF tools** (bcc, bpftrace): `biolatency` (disk latency histogram), `execsnoop` (short-lived processes), `tcpretrans`, `opensnoop`. Low overhead and safe for production.

## Common culprits

- One single-threaded process at 100% of one core while the "total CPU" looks fine.
- A disk at 100% util with high await: slow storage, a failing disk, or one process hammering it (`iotop`).
- Memory pressure causing swapping, which slows *everything*.
- Network retransmits or DNS timeouts adding seconds to requests.
- Noisy neighbours on shared VMs (high steal).

> **Tip:** change one thing at a time and measure before and after. Tuning without measurement is guessing.

## In practice

Generate load in a VM (`stress-ng --cpu 8`, then `--io 4`, then `--vm 2 --vm-bytes 90%`) and watch how each shows up in vmstat, iostat and `/proc/pressure`.""",
    "key_points": [
        "Start with a checklist: uptime, dmesg, vmstat, mpstat, pidstat, iostat, free, sar.",
        "vmstat: r above CPU count = CPU saturation; b and wa = I/O blocking; si/so = swapping; st = steal.",
        "PSI (/proc/pressure) directly measures stalls on CPU, memory and I/O.",
        "Go deeper with perf and flame graphs, strace -c, and eBPF tools like biolatency and execsnoop.",
    ],
    "figure_svg": PERF,
    "figure_caption": "vmstat on an 8-CPU host: row X shows CPU saturation; row Y shows tasks blocked on I/O.",
    "questions": [
        mcq("In vmstat output, what does the r column count?", ["Reads per second", "Runnable tasks waiting for or using a CPU", "Restarts", "RAM in use"], 1, "r above the CPU count means saturation."),
        mcq("In the diagram, what does row X show on this 8-CPU host?", ["I/O bottleneck", "CPU saturation: 9 runnable, 88% user, 2% idle", "Swapping", "Idle system"], 1,
            "More runnable tasks than CPUs and almost no idle time.",
            PERF, "vmstat rows: a normal row, row X with r=9 and 88% user CPU, row Y with b=6, high bi/bo and 50% I/O wait."),
        mcq("In the diagram, what does row Y point to?", ["CPU shortage", "Tasks blocked on disk I/O (b=6, wa=50%)", "Network retransmits", "Memory leak"], 1,
            "Blocked tasks with high I/O wait and heavy block traffic.", PERF, "vmstat output with row Y showing b=6 and wa=50."),
        mcq("What does non-zero, sustained si/so mean?", ["Disk errors", "The system is swapping, a sign of memory pressure", "Network traffic", "Normal operation"], 1, "Swap in and out."),
        mcq("On a VM, what does high st (steal) indicate?", ["Malware", "The hypervisor is giving your CPU time to other guests", "A disk fault", "Swapping"], 1, "Noisy neighbours or an overcommitted host."),
        mcq("Which tool gives a histogram of disk I/O latency with low overhead?", ["strace", "biolatency (eBPF)", "ping", "du"], 1, "eBPF tools are production-safe."),
        mcq("Total CPU use is 13% on an 8-core server, but the app is slow and one core shows 100%. What's likely?", ["Disk failure", "A single-threaded bottleneck", "Too much RAM", "DNS"], 1,
            "mpstat -P ALL reveals per-core saturation."),
        open_q("Describe how you'd tell whether a slow server is short of CPU, memory or I/O.", "Use vmstat (r versus CPU count, si/so for swapping, b and wa for I/O), iostat for disk utilisation and latency, free for available memory, and /proc/pressure for direct stall percentages on CPU, memory and I/O.",
               ["vmstat columns", "iostat for disks", "PSI or free for memory"], "Check each resource for saturation."),
        open_q("Why should you use strace sparingly on a busy production process?", "Because strace intercepts every system call through ptrace, which can slow the process dramatically; eBPF-based tools give similar insight with far lower overhead.",
               ["strace adds heavy overhead", "eBPF tools are lighter"], "Keep strace runs short with -c."),
        open_q("What is a flame graph and what question does it answer?", "A visualisation of sampled stack traces where width shows how much CPU time each function (and its callers) consumed; it answers 'where is the CPU time actually going?' at a glance.",
               ["sampled stacks", "width is time spent", "shows where CPU time goes"], "Generated from perf record data."),
    ],
}

L6 = {
    "title": "Automation and backups",
    "minutes": 9,
    "photo_query": "",
    "body": """Servers you configure by hand drift, and servers without tested backups eventually lose data. Automation and backups are what separate a hobby box from a dependable system.

## Configuration as code

Write down the desired state of your systems in files kept in git, and let a tool apply it.

- **Ansible** connects over SSH (no agent), reads **inventory** (which hosts) and **playbooks** (YAML lists of tasks using modules like `apt`, `copy`, `template`, `service`, `user`).
- Good tasks are **idempotent**: running them twice changes nothing the second time. `apt: name=nginx state=present` is idempotent; `shell: apt-get install nginx` isn't guaranteed to be.
- `ansible-playbook site.yml --check --diff` shows what *would* change without changing it.
- Group related tasks into **roles**; keep secrets in **Ansible Vault**.

Other approaches: Salt, Puppet, Chef, and NixOS (the whole OS defined declaratively). For containers, Compose files in git play the same role.

## Scheduling

systemd timers (with logs in the journal and `Persistent=`) or cron. Whatever runs unattended must **report failure**: exit non-zero, and alert (email, push notification, a monitoring check) when it does. A silent failing backup job is the classic disaster.

## Backups: 3-2-1

Keep **3** copies of your data, on **2** different kinds of media, with **1** off-site. Add one more rule: **test restores** regularly.

Tools:

- **restic** and **BorgBackup**: deduplicated, encrypted, incremental backups to local disks, SFTP, S3-compatible storage or Backblaze B2. `restic backup /srv`, `restic snapshots`, `restic restore`.
- **rsync** with hard links (or `rsnapshot`) for simple versioned copies.
- **ZFS/Btrfs snapshots** with send/receive for fast replication.

## Back up the right things

- **Data**: databases, Docker volumes, documents, photos.
- **Configuration**: `/etc`, compose files, `.env` files (encrypted), your Ansible repo.
- **Databases need consistent dumps**: `pg_dump` or `mysqldump` (or a snapshot) rather than copying live data files mid-write.

## Retention and protection

- Keep a sensible history: for example 7 daily, 4 weekly, 12 monthly (`restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune`).
- Protect against **ransomware**: the backup target shouldn't be writable (or deletable) by the machine being backed up. Use append-only modes or immutable object storage.
- **Encrypt** off-site backups and store the key somewhere you'll still have after a disaster.

> **Untested backups aren't backups.** Schedule a restore test: pick a random file and a whole database each quarter and restore them to a scratch location.

## In practice

Set up restic to back up `/etc` and your Docker volumes nightly to a NAS and weekly to B2, with a retention policy, failure alerts and a documented restore procedure. Then do the restore.""",
    "key_points": [
        "Keep configuration as code in git; Ansible applies idempotent tasks over SSH (check with --check --diff).",
        "Unattended jobs must exit non-zero and alert on failure.",
        "3-2-1: three copies, two media, one off-site, and regularly tested restores.",
        "Use restic/Borg, consistent database dumps, retention policies, encryption and append-only targets against ransomware.",
    ],
    "figure_svg": BACKUP,
    "figure_caption": "3 copies, 2 kinds of media, 1 off-site, and restores that are actually tested.",
    "questions": [
        mcq("What does it mean for an automation task to be idempotent?", ["It runs quickly", "Running it again changes nothing if the system is already in the desired state", "It runs only once ever", "It needs root"], 1,
            "Safe to re-run any time."),
        mcq("In the diagram, why the '1 off-site' copy?", ["Speed", "To survive fire, theft or flood at the main site", "To save money", "Because RAID requires it"], 1,
            "A disaster at one location can destroy every local copy.",
            BACKUP, "Three boxes: 3 copies (live + 2 backups), 2 media (e.g. NAS + cloud), 1 off-site (survives fire/theft), plus test restores."),
        mcq("Which Ansible command previews changes without making them?", ["ansible-playbook site.yml --check --diff", "ansible-vault view", "ansible-inventory", "ansible all -m ping"], 0,
            "Check mode with a diff."),
        mcq("Why dump a PostgreSQL database with pg_dump rather than copying its data files?", ["It's smaller", "Copying live files mid-write can give an inconsistent, unrestorable copy", "pg_dump is required by law", "Data files are encrypted"], 1,
            "Dumps (or snapshots) are consistent."),
        mcq("How do you protect backups from ransomware on the backed-up machine?", ["Use RAID", "Make the backup target append-only or immutable from that machine", "Back up more often", "Use rsync"], 1,
            "The attacker can't delete what it can't modify."),
        mcq("Which tool provides deduplicated, encrypted, incremental backups to cloud storage?", ["cron", "restic", "ss", "lvm"], 1, "restic (or Borg)."),
        mcq("In the diagram, what turns a backup plan into something you can rely on?", ["More copies", "Testing restores", "Compression", "Encryption alone"], 1,
            "Untested backups aren't backups.", BACKUP, "3-2-1 diagram with a 'test restores' box."),
        open_q("Explain why a shell command like `shell: apt-get install nginx` in Ansible is worse than the apt module.", "The apt module checks the current state and only acts if needed, reporting changed or ok, so it's idempotent and works with check mode; a raw shell command runs every time, always reports a change and can't be previewed.",
               ["module checks state and is idempotent", "shell runs every time", "check mode works with modules"], "Use modules whenever one exists."),
        open_q("Design a retention policy for daily backups and explain the trade-off.", "For example keep 7 daily, 4 weekly and 12 monthly snapshots: recent changes can be restored precisely, older history is kept at lower resolution, and storage stays bounded. More retention costs more space; less risks losing the version you need.",
               ["daily, weekly and monthly tiers", "trade-off between history and storage"], "Match it to how long problems take to notice."),
        open_q("What should an unattended backup job do when it fails, and why?", "Exit non-zero and send an alert (email, push, monitoring), so someone knows immediately; a silently failing backup is discovered only when you need to restore and it isn't there.",
               ["exit non-zero", "alert someone", "silent failures are discovered too late"], "Alert on success going stale too."),
    ],
}

PACK = {
    "id": "linux-advanced",
    "version": 1,
    "topic": "Linux",
    "title": "Linux internals and administration",
    "summary": "How Linux boots and manages processes and memory, advanced storage (LVM, RAID, ZFS), hardening with SELinux/AppArmor and auditing, performance troubleshooting, automation and backups. For experienced administrators.",
    "icon": "binary",
    "level": "advanced",
    "length": "short",
    "area": "technology",
    "tags": ["linux", "sysadmin", "security", "performance", "storage"],
    "sections": [
        {"title": "Internals", "summary": "Boot, processes, memory and storage under the hood.", "lessons": [
            {"title": L1["title"], "summary": "Follow and repair each stage of the boot process.", "lesson": L1},
            {"title": L2["title"], "summary": "Read process states, signals and memory like an expert.", "lesson": L2},
            {"title": L3["title"], "summary": "Build flexible, resilient storage with LVM, RAID and ZFS.", "lesson": L3},
        ]},
        {"title": "Running servers", "summary": "Harden, tune, automate and protect production systems.", "lessons": [
            {"title": L4["title"], "summary": "Harden servers in layers and audit what happens.", "lesson": L4},
            {"title": L5["title"], "summary": "Diagnose slow systems methodically with the right tools.", "lesson": L5},
            {"title": L6["title"], "summary": "Automate configuration and build backups you can trust.", "lesson": L6},
        ]},
    ],
}
