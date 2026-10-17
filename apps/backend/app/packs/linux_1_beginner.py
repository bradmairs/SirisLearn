"""Linux for beginners."""

from app.coursepacks import mcq, open_q
from app.packs._draw import AMBER, BLUE, GREEN, INK, MUTED, PURPLE, RED, arrow, box, line, svg, text, title

STACK = svg(
    title("The layers of a Linux system"),
    box(90, 50, 300, 40, "Applications (browser, Docker, nginx)", GREEN, size=13),
    box(90, 100, 300, 40, "Shell and utilities (bash, ls, cp)", BLUE, size=13),
    box(90, 150, 300, 40, "Kernel (Linux)", AMBER, size=13),
    box(90, 200, 300, 40, "Hardware (CPU, memory, disks)", INK, size=13),
    text(420, 75, "A", 15, GREEN, weight="bold"), text(420, 125, "B", 15, BLUE, weight="bold"),
    text(420, 175, "C", 15, AMBER, weight="bold"), text(420, 225, "D", 15, INK, weight="bold"),
    text(240, 272, "A distribution packages all of this together", 12, MUTED),
)

TREE = svg(
    title("The filesystem tree"),
    box(205, 45, 70, 32, "/", AMBER, size=15),
    *[line(240, 77, x, 120, MUTED) for x in (45, 115, 185, 255, 325, 395, 455)],
    box(15, 120, 60, 30, "bin", BLUE, size=12), box(85, 120, 60, 30, "etc", GREEN, size=12), box(155, 120, 60, 30, "home", PURPLE, size=12),
    box(225, 120, 60, 30, "var", BLUE, size=12), box(295, 120, 60, 30, "tmp", INK, size=12), box(365, 120, 60, 30, "usr", BLUE, size=12),
    box(430, 120, 45, 30, "dev", INK, size=11),
    line(185, 150, 185, 190, MUTED), box(140, 190, 90, 30, "brad", PURPLE, size=12),
    line(185, 220, 185, 245, MUTED), box(140, 245, 90, 30, "notes.txt", INK, size=11),
    line(255, 150, 255, 190, MUTED), box(225, 190, 60, 30, "log", BLUE, size=12),
    text(400, 230, "/home/brad/notes.txt", 12, MUTED),
)

PERMS = svg(
    title("-rwxr-x--- 1 brad dev  script.sh"),
    box(40, 70, 40, 50, "-", MUTED, size=16),
    box(90, 70, 110, 50, "rwx", GREEN, size=18), box(210, 70, 110, 50, "r-x", BLUE, size=18), box(330, 70, 110, 50, "---", RED, size=18),
    text(60, 145, "type", 12, MUTED), text(145, 145, "owner (brad)", 12, GREEN), text(265, 145, "group (dev)", 12, BLUE), text(385, 145, "others", 12, RED),
    text(145, 180, "7", 22, GREEN, weight="bold"), text(265, 180, "5", 22, BLUE, weight="bold"), text(385, 180, "0", 22, RED, weight="bold"),
    text(240, 230, "r = 4, w = 2, x = 1   →   chmod 750 script.sh", 14, INK),
    text(240, 262, "P: owner   Q: group   R: others", 12, MUTED),
)

PACKAGES = svg(
    title("Installing software with a package manager"),
    box(30, 70, 120, 60, "You", INK, sub="sudo apt install htop"),
    arrow(150, 100, 200, 100, BLUE),
    box(200, 70, 120, 60, "apt", BLUE, sub="resolves dependencies"),
    arrow(320, 100, 370, 100, GREEN, "download", dy=-10),
    box(370, 70, 90, 60, "Repository", GREEN, size=12, sub="signed"),
    arrow(260, 130, 260, 175, AMBER),
    box(170, 178, 180, 56, "installed + tracked", AMBER, sub="update, remove later"),
    text(240, 268, "apt (Debian/Ubuntu) · dnf (Fedora/RHEL) · pacman (Arch)", 12, MUTED),
)

PROCS = svg(
    title("A process's life"),
    box(30, 120, 90, 50, "started", BLUE, size=13),
    box(170, 70, 100, 50, "running", GREEN, size=13), box(170, 170, 100, 50, "sleeping", PURPLE, size=13),
    box(330, 120, 110, 50, "ended", RED, size=13),
    arrow(120, 140, 168, 100, BLUE), line(220, 120, 220, 170, MUTED, dash="4 4"),
    arrow(270, 95, 328, 135, RED, "exit / kill", dx=12, dy=-6, size=11), arrow(270, 195, 328, 155, RED),
    text(240, 262, "SIGTERM asks politely · SIGKILL (kill -9) forces", 12, MUTED),
)

WILDCARD = svg(
    title("Wildcards expand before the command runs"),
    box(30, 60, 180, 50, "rm *.log", RED, size=16),
    arrow(210, 85, 260, 85, AMBER, "shell expands", dy=-10, size=11),
    box(265, 50, 185, 70, "rm app.log", RED, size=13, sub="db.log  old.log"),
    box(30, 160, 420, 80, "", INK), text(240, 185, "folder contents", 13, MUTED),
    text(100, 215, "app.log", 13, RED), text(190, 215, "db.log", 13, RED), text(270, 215, "old.log", 13, RED),
    text(350, 215, "notes.txt", 13, GREEN), text(420, 215, "a.conf", 13, GREEN),
    text(240, 268, "Check with: ls *.log  before  rm *.log", 13, MUTED),
)

L1 = {
    "title": "What Linux is",
    "minutes": 7,
    "photo_query": "Linux Tux penguin",
    "body": """Linux runs most of the world's servers, every Android phone, most home routers, smart TVs, the Raspberry Pi and the containers Docker runs. Learning it opens the door to self-hosting, cloud work and much of modern engineering software.

## The kernel and the rest

Strictly, **Linux** is a **kernel**: the core program that talks to the hardware, schedules processes, manages memory and enforces permissions. Linus Torvalds started it in 1991, and it's free and open source.

A kernel alone isn't usable. Around it sit:

- **Shell and utilities**: the command-line programs (`bash`, `ls`, `cp`, `grep`) mostly from the GNU project.
- **System services**: background programs managed by **systemd** on most systems.
- **Applications**: web servers, databases, desktops, Docker.

## Distributions

A **distribution** ("distro") bundles the kernel, tools, a package manager and defaults into an installable system. The families you'll meet:

- **Debian** and **Ubuntu**: very common on servers and home labs; use `apt` and `.deb` packages. Raspberry Pi OS is Debian-based.
- **Fedora**, **RHEL**, **Rocky Linux**, **AlmaLinux**: the Red Hat family, common in enterprises; use `dnf` and `.rpm`.
- **Arch**: rolling releases, hands-on, `pacman`.
- **Alpine**: tiny, used heavily for containers.

Most skills transfer across all of them; the package manager is the main day-to-day difference.

## Why the command line

Linux has desktops, but servers usually have no screen at all. You manage them through a **terminal** running a **shell**, locally or over **SSH**. The command line is precise, scriptable, works over slow links and lets you combine small tools to do big jobs.

A command looks like `program options arguments`, for example `ls -l /etc`: run `ls`, with the long-format option `-l`, on the directory `/etc`. Case matters: `File.txt` and `file.txt` are different files.

## Getting help

- `man ls` opens the manual page (press `q` to quit, `/word` to search).
- `ls --help` prints a short summary.
- `tldr ls` (if installed) shows practical examples.

> **Tip:** press **Tab** to auto-complete commands and file names, and the **Up arrow** to recall previous commands. They save more time than any other habit.

## In practice

If you don't have Linux handy, install Ubuntu in a VM, use WSL on Windows, or SSH into a Raspberry Pi. Open a terminal and try `whoami`, `hostname`, `uname -r` (kernel version) and `cat /etc/os-release` (which distro you're on).""",
    "key_points": [
        "Linux is a kernel; a distribution adds tools, services, a package manager and defaults.",
        "Debian/Ubuntu use apt, the Red Hat family uses dnf, Arch uses pacman, Alpine is tiny and container-friendly.",
        "Servers are managed through a shell in a terminal, often over SSH.",
        "man, --help and Tab completion are your everyday helpers; names are case-sensitive.",
    ],
    "figure_svg": STACK,
    "figure_caption": "Applications (A) and the shell and utilities (B) run on the kernel (C), which drives the hardware (D).",
    "questions": [
        mcq("Strictly speaking, what is 'Linux'?", ["A complete operating system with a desktop", "A kernel", "A company", "A programming language"], 1,
            "Linux is the kernel; distributions build complete systems around it."),
        mcq("In the diagram, which layer schedules processes and talks to the hardware?", ["A", "B", "C", "D"], 2,
            "C is the kernel.", STACK, "Four stacked layers: applications A, shell and utilities B, kernel C, hardware D."),
        mcq("Which package manager does Ubuntu use?", ["dnf", "pacman", "apt", "brew"], 2, "Debian and Ubuntu use apt with .deb packages."),
        mcq("What does `man grep` do?", ["Deletes grep", "Opens grep's manual page", "Runs grep as administrator", "Installs grep"], 1, "man shows the manual; q quits."),
        mcq("Which distribution is especially common as a tiny base for containers?", ["Fedora", "Alpine", "Ubuntu Desktop", "Arch"], 1, "Alpine is only a few megabytes."),
        mcq("In `ls -l /etc`, what is `-l`?", ["The program", "An option", "The argument", "A file"], 1, "ls is the program, -l an option, /etc the argument."),
        mcq("In the diagram, where do bash and ls live?", ["A", "B", "C", "D"], 1,
            "They're shell and utilities, layer B.", STACK, "Layers A to D: applications, shell and utilities, kernel, hardware."),
        open_q("What's the difference between the Linux kernel and a Linux distribution?", "The kernel is the core program that manages hardware, processes and memory; a distribution packages the kernel with tools, a package manager, services and defaults into a complete installable system.",
               ["kernel manages hardware and processes", "distribution adds tools, package manager and defaults"], "Ubuntu, Debian and Fedora all share the same kernel."),
        open_q("Why are servers usually managed from the command line instead of a desktop?", "Servers often have no screen, and the command line works over SSH and slow links, is precise and repeatable, and can be scripted and automated.",
               ["works remotely over SSH", "scriptable and repeatable", "no desktop needed"], "Everything you type can become a script."),
        open_q("Name two keyboard habits that save time in the shell and what they do.", "Tab completes command and file names, and the Up arrow recalls previous commands so you can rerun or edit them.",
               ["Tab completion", "Up arrow history"], "Ctrl+R searches history too."),
    ],
}

L2 = {
    "title": "Finding your way: files and directories",
    "minutes": 8,
    "photo_query": "",
    "body": """Everything in Linux lives in one **tree of directories** starting at `/`, the **root**. There are no drive letters: extra disks are attached ("mounted") somewhere in the tree.

## Important directories

- `/home/<you>`: your files. `~` is shorthand for it.
- `/etc`: system-wide configuration files (text you can read and edit).
- `/var`: data that changes: logs in `/var/log`, databases, Docker's data in `/var/lib/docker`.
- `/usr`: installed programs and libraries; `/usr/bin` holds most commands.
- `/tmp`: temporary files, often cleared on reboot.
- `/dev`: devices as files (disks like `/dev/sda`).
- `/root`: the root user's home (not the same as `/`).

## Paths

- An **absolute path** starts from root: `/home/brad/notes.txt`.
- A **relative path** starts from where you are: if you're in `/home/brad`, `notes.txt` means the same file.
- `.` is the current directory, `..` its parent, `~` your home.

## Moving around

- `pwd` prints the working directory: where am I?
- `ls` lists a directory; `ls -l` adds details; `ls -a` shows **hidden files** (names starting with `.`, like `.bashrc`); `ls -lh` shows human-readable sizes.
- `cd /var/log` changes directory; `cd ..` goes up; `cd` or `cd ~` goes home; `cd -` goes back to where you were.

## Looking for things

- `find /etc -name "*.conf"` searches by name.
- `locate nginx.conf` searches a prebuilt index (fast; may need `updatedb`).
- `which python3` shows which program runs when you type a command.
- `tree` (if installed) draws a directory tree.

> **Common misconception:** `/root` is "the root of the filesystem". No: `/` is the root of the tree, and `/root` is just the home directory of the user called root.

## Everything is a file

Linux represents many things as files: devices in `/dev`, process information in `/proc` (try `cat /proc/cpuinfo`), and kernel settings in `/sys`. That means the same tools (`cat`, `ls`, `grep`) work on all of them.

## Spaces and special characters

File names can contain spaces, but the shell splits commands on spaces. Quote such names (`cd "My Documents"`) or escape the space (`cd My\\ Documents`). Tab completion adds the escapes for you, which is another reason to use it.

## In practice

Explore: `cd /etc`, `ls`, then `cat hostname` and `cat os-release`. Go to `/var/log` and `ls -lh` to see the logs and their sizes. Use `cd -` to jump back. Finally `cd` with no arguments to return home and run `ls -a` to see your hidden configuration files.""",
    "key_points": [
        "One tree starting at /; disks are mounted into it rather than given drive letters.",
        "/home holds users' files, /etc configuration, /var changing data and logs, /usr programs.",
        "Absolute paths start at /; relative paths start where you are; . is here, .. is up, ~ is home.",
        "pwd, ls, cd and find are the core navigation tools; dotfiles are hidden from plain ls.",
    ],
    "figure_svg": TREE,
    "figure_caption": "The single directory tree from / down to /home/brad/notes.txt.",
    "questions": [
        mcq("Where are system-wide configuration files kept?", ["/home", "/etc", "/tmp", "/dev"], 1, "/etc holds configuration, mostly plain text."),
        mcq("In the diagram, what is the absolute path of notes.txt?", ["/brad/notes.txt", "/home/brad/notes.txt", "~/home/notes.txt", "/var/brad/notes.txt"], 1,
            "Follow the tree from /: home, then brad, then notes.txt.",
            TREE, "A directory tree from / with branches bin, etc, home, var, tmp, usr and dev; home contains brad, which contains notes.txt; var contains log."),
        mcq("What does `cd ..` do?", ["Goes to your home directory", "Goes up one directory", "Goes to /", "Lists hidden files"], 1, ".. is the parent directory."),
        mcq("Which command shows hidden files such as .bashrc?", ["ls -l", "ls -a", "ls -h", "pwd"], 1, "Names starting with a dot are hidden unless you use -a."),
        mcq("Where would you look for an application's log files?", ["/etc", "/var/log", "/usr/bin", "/dev"], 1, "/var holds changing data, including logs."),
        mcq("You're in /home/brad. Which relative path refers to /home/brad/docs/plan.txt?", ["/docs/plan.txt", "docs/plan.txt", "../docs/plan.txt", "~/brad/docs/plan.txt"], 1,
            "Relative paths start from the current directory."),
        mcq("In the diagram, which directory would hold system logs?", ["etc", "home", "var/log", "tmp"], 2, "Logs live under /var/log.",
            TREE, "Directory tree with /var/log branching from var."),
        open_q("Explain the difference between an absolute and a relative path, with an example of each.", "An absolute path starts from the root, like /etc/hostname, and means the same thing wherever you are; a relative path starts from the current directory, like docs/plan.txt when you're in your home folder.",
               ["absolute starts from /", "relative starts from the current directory"], "Scripts usually use absolute paths so they work from anywhere."),
        open_q("What's the difference between / and /root?", "/ is the root of the whole filesystem tree; /root is the home directory of the root (administrator) user.",
               ["/ is the top of the tree", "/root is the root user's home"], "A classic confusion."),
        open_q("How would you find every file ending in .conf under /etc?", "Run find /etc -name \"*.conf\" (quoting the pattern so the shell doesn't expand it first).",
               ["use find", "search /etc", "-name with *.conf"], "locate is faster if its index is up to date."),
    ],
}

L3 = {
    "title": "Working with files",
    "minutes": 8,
    "photo_query": "",
    "body": """With navigation sorted, here are the commands that create, copy, move, read and delete files. They're the bulk of everyday shell work.

## Creating and copying

- `mkdir projects` makes a directory; `mkdir -p a/b/c` makes the whole chain.
- `touch notes.txt` creates an empty file (or updates the timestamp of an existing one).
- `cp notes.txt backup.txt` copies a file; `cp -r site/ site-backup/` copies a directory and everything in it (**recursive**).
- `mv notes.txt archive/` moves a file; `mv old.txt new.txt` renames it. Linux has no separate rename command: renaming is moving.

## Deleting, carefully

- `rm file.txt` deletes a file. There's **no recycle bin**: it's gone.
- `rm -r folder/` deletes a directory and its contents; `rmdir folder` only removes an empty one.
- `rm -i` asks before each deletion.

> **Watch out:** `rm -rf` deletes recursively and without asking. Read the command twice, especially with `sudo`, wildcards or variables. A stray space in `rm -rf / tmp/junk` is a disaster.

## Reading files

- `cat file` prints the whole file.
- `less file` shows it a screen at a time: arrows or space to scroll, `/word` to search, `q` to quit.
- `head -n 20 file` and `tail -n 20 file` show the start and end.
- `tail -f /var/log/syslog` **follows** a growing file live: essential for watching logs.

## Editing files

- `nano file` is the friendliest editor: type, then **Ctrl+O** to save and **Ctrl+X** to exit (shortcuts are listed along the bottom).
- `vim` is everywhere and very powerful, with a learning curve. If you get stuck in it: press **Esc**, type `:q!` and Enter to quit without saving.

## Wildcards

The shell expands patterns before the command runs:

- `*` matches anything: `ls *.log`.
- `?` matches one character: `ls file?.txt`.
- `[0-9]` matches one character from a set.

Check what a wildcard matches with `ls` or `echo` *before* using it with `rm`.

## Sizes and space

- `du -sh folder/` shows a folder's total size.
- `df -h` shows free space on each mounted filesystem.

## In practice

Make a sandbox: `mkdir -p ~/play && cd ~/play`. Create files with `touch a.txt b.txt c.log`, try `ls *.txt`, copy and rename them, edit one with nano, and delete the lot with `rm -i *`. Practising here makes the real thing safe.""",
    "key_points": [
        "mkdir, touch, cp (-r for folders) and mv (move or rename) create and organise files.",
        "rm deletes permanently; -r recurses and -f skips prompts, so check twice before rm -rf.",
        "cat, less, head and tail read files; tail -f follows logs live.",
        "nano is the easy editor (Ctrl+O save, Ctrl+X exit); wildcards like *.log expand before the command runs.",
    ],
    "figure_svg": WILDCARD,
    "figure_caption": "The shell expands *.log into a list of matching files before rm ever runs.",
    "questions": [
        mcq("How do you rename old.txt to new.txt?", ["rename old.txt new.txt", "mv old.txt new.txt", "cp old.txt new.txt", "rn old.txt new.txt"], 1, "Renaming is moving to a new name."),
        mcq("Which command copies a directory and everything in it?", ["cp site/ copy/", "cp -r site/ copy/", "mv -r site/ copy/", "dup site/"], 1, "-r copies recursively."),
        mcq("Where does a file go after `rm file.txt`?", ["The trash", "It's permanently deleted", "/tmp", "A backup folder"], 1, "No recycle bin on the command line."),
        mcq("Which command shows new lines of a log as they're written?", ["cat log", "head log", "tail -f log", "less -n log"], 2, "-f follows the file."),
        mcq("In nano, which keys save the file?", ["Ctrl+S", "Ctrl+O", "Esc :w", "Ctrl+X"], 1, "Ctrl+O writes Out; Ctrl+X exits."),
        mcq("In the diagram, which files will `rm *.log` delete?", ["Only app.log", "app.log, db.log and old.log", "Everything in the folder", "notes.txt and a.conf"], 1,
            "*.log matches every name ending in .log.",
            svg(box(30, 80, 420, 80, "", INK), text(100, 125, "app.log", 13, RED), text(190, 125, "db.log", 13, RED), text(270, 125, "old.log", 13, RED),
                text(350, 125, "notes.txt", 13, GREEN), text(420, 125, "a.conf", 13, GREEN), title("Folder contents"), text(240, 220, "rm *.log", 18, RED, weight="bold")),
            "A folder containing app.log, db.log, old.log, notes.txt and a.conf, with the command rm *.log underneath."),
        mcq("You're stuck in vim and want to quit without saving. What do you type?", ["Ctrl+C", "Esc then :q!", "exit", "Ctrl+X"], 1, "Esc leaves insert mode; :q! quits discarding changes."),
        open_q("Looking at the diagram, why is it a good idea to run `ls *.log` before `rm *.log`?", "Because the shell expands the wildcard into the list of matching files before rm runs, ls shows exactly which files would be deleted, so you can catch mistakes before deleting anything permanently.",
               ["see exactly what the pattern matches", "rm is permanent"], "Same trick works with echo.",
               WILDCARD, "rm *.log is expanded by the shell into rm app.log db.log old.log; the folder also holds notes.txt and a.conf, which aren't matched."),
        open_q("Explain what each part of `rm -rf old-site/` does and why it deserves care.", "rm deletes, -r recurses into the directory to delete everything inside, -f forces it without asking or complaining; together they permanently remove the whole folder with no confirmation, so a typo can delete the wrong thing.",
               ["-r recursive", "-f no prompts", "permanent and unconfirmed"], "Read it twice, especially with sudo."),
        open_q("How would you check how much space a folder uses and how much free space the disk has?", "Use du -sh folder to see the folder's total size and df -h to see free space on each mounted filesystem.",
               ["du -sh for the folder", "df -h for free space"], "-h means human-readable units."),
    ],
}

L4 = {
    "title": "Users, permissions and sudo",
    "minutes": 9,
    "photo_query": "",
    "body": """Linux is multi-user from the ground up. Every file has an **owner**, a **group** and **permissions** saying who can do what. Understanding them explains most "Permission denied" errors.

## Users and groups

- Each user has a name and a numeric **UID**; `id` shows yours.
- Users belong to **groups**, so you can grant access to a team at once (`groups` lists yours).
- **root** (UID 0) is the administrator and can do anything.

## Reading permissions

`ls -l script.sh` shows something like `-rwxr-x--- 1 brad dev 1204 Oct 17 script.sh`:

- The first character is the type: `-` file, `d` directory, `l` symbolic link.
- Then three sets of three: **owner**, **group**, **others**.
- `r` read, `w` write, `x` execute, `-` not allowed.

So here: brad can read, write and run it; members of `dev` can read and run it; everyone else gets nothing.

For **directories**, `r` lets you list names, `w` lets you create and delete files inside, and `x` lets you enter it (`cd`) and reach files within.

## Changing permissions: chmod

Two styles:

- **Symbolic**: `chmod u+x script.sh` (add execute for the user/owner), `chmod go-w file` (remove write from group and others).
- **Numeric**: each set is a sum of r=4, w=2, x=1. `chmod 750 script.sh` gives `rwx` (7) to the owner, `r-x` (5) to the group and nothing (0) to others. Common values: **644** for normal files, **755** for programs and directories, **600** for private files like SSH keys.

## Changing ownership: chown

`sudo chown brad:dev report.txt` sets the owner to brad and the group to dev. Use `-R` to change a whole directory tree.

## sudo: borrowing root

Logging in as root all the time is risky: one mistake has unlimited reach. Instead, administrators use **sudo** to run a single command as root: `sudo apt update`. sudo asks for *your* password, logs what you did, and only works for users allowed in the sudoers configuration (often the `sudo` or `wheel` group).

> **Common misconception:** "Permission denied? Just chmod 777." That gives everyone full control and is almost never right. Work out who needs access and grant only that.

## In practice

Create a script: `echo 'echo hello' > hi.sh`. Try `./hi.sh` (Permission denied), then `chmod u+x hi.sh` and run it again. Look at `ls -l` before and after. Then check `ls -l ~/.ssh`: private keys should be `-rw-------` (600), or SSH will refuse to use them.""",
    "key_points": [
        "Every file has an owner, a group and read/write/execute permissions for owner, group and others.",
        "Numeric modes add r=4, w=2, x=1 per set: 644 files, 755 programs and directories, 600 private keys.",
        "chmod changes permissions, chown changes owner and group.",
        "sudo runs one command as root with logging; avoid working as root and avoid chmod 777.",
    ],
    "figure_svg": PERMS,
    "figure_caption": "-rwxr-x--- read as owner rwx (7), group r-x (5), others --- (0): chmod 750.",
    "questions": [
        mcq("In `-rw-r--r--`, what can the group do?", ["Read and write", "Read only", "Nothing", "Execute"], 1, "Owner rw-, group r--, others r--."),
        mcq("In the diagram, which set of permissions belongs to group R?", ["rwx", "r-x", "---", "-"], 2,
            "R is others, with no permissions at all.",
            PERMS, "Permission string -rwxr-x--- split into owner P (rwx, 7), group Q (r-x, 5) and others R (---, 0)."),
        mcq("Which numeric mode means rwxr-xr-x?", ["644", "755", "777", "700"], 1, "7 = rwx, 5 = r-x."),
        mcq("How do you make script.sh executable by its owner?", ["chmod u+x script.sh", "chown +x script.sh", "sudo script.sh", "chmod 600 script.sh"], 0, "u+x adds execute for the user (owner)."),
        mcq("What permissions should an SSH private key have?", ["777", "755", "644", "600"], 3, "Only the owner should read or write it; SSH refuses looser keys."),
        mcq("What does `sudo` do?", ["Switches to another distro", "Runs one command with root privileges", "Deletes a user", "Shows permissions"], 1,
            "It's logged and limited to allowed users."),
        mcq("In the diagram, what does the 5 for the group mean?", ["read and write", "read and execute", "write only", "everything"], 1,
            "5 = 4 (read) + 1 (execute).", PERMS, "Numeric breakdown of rwxr-x---: owner 7, group 5, others 0."),
        open_q("Why is chmod 777 almost always the wrong fix for 'Permission denied'?", "It gives every user on the system read, write and execute access, so anyone could change or delete the file; the right fix is to grant only the user or group that needs access.",
               ["gives everyone full access", "grant only what's needed"], "Find out which user needs what first."),
        open_q("Explain what read, write and execute mean on a directory.", "Read lets you list the names in it, write lets you create, rename and delete files inside it, and execute lets you enter it and access the files within.",
               ["read lists names", "write creates or deletes entries", "execute lets you enter"], "A directory without x is a locked door even if you can see the names."),
        open_q("Why do administrators use sudo instead of logging in as root?", "Because sudo grants root only for one command at a time, logs who ran what, uses each person's own password, and reduces the chance of a careless mistake with unlimited power.",
               ["root only for one command", "logged and accountable", "fewer accidental mistakes"], "Least privilege in daily practice."),
    ],
}

L5 = {
    "title": "Installing and updating software",
    "minutes": 7,
    "photo_query": "",
    "body": """On Linux you rarely download installers from websites. Instead, a **package manager** installs software from trusted **repositories**, keeps track of what's installed, and updates everything at once.

## Packages and repositories

A **package** is an archive of a program plus metadata: its version and what other packages it **depends** on. A **repository** is a server full of packages, signed by the distribution so your system can verify they haven't been tampered with.

## apt on Debian and Ubuntu

- `sudo apt update` refreshes the list of available packages (it doesn't upgrade anything).
- `sudo apt upgrade` installs newer versions of what you have.
- `sudo apt install htop` installs a package and its dependencies.
- `sudo apt remove htop` removes it; `sudo apt autoremove` cleans up dependencies nothing needs any more.
- `apt search nginx` and `apt show nginx` find and describe packages.

## dnf on Fedora and the Red Hat family

The same ideas: `sudo dnf install htop`, `sudo dnf upgrade`, `sudo dnf remove htop`. dnf refreshes its metadata automatically.

## Updates matter

Most security incidents exploit known, already-fixed vulnerabilities. Keep systems updated:

- Run updates regularly, and read what's being changed for big upgrades.
- On Debian/Ubuntu, **unattended-upgrades** can install security updates automatically.
- Some updates (a new kernel, core libraries) need a **reboot** to take effect. Ubuntu creates `/var/run/reboot-required` when one is needed.

## Other ways software arrives

- **Snap** and **Flatpak**: self-contained app packages that bundle their dependencies, common for desktop apps.
- **Docker images**: the usual way to run server apps in a home lab, keeping them separate from the host.
- **Language package managers** (`pip`, `npm`): for libraries in a project, ideally inside a virtual environment, not system-wide.
- **Third-party repositories** (for example Docker's own apt repository): add only from sources you trust, because their packages run as root during install.

> **Common misconception:** `apt update` upgrades your software. It only refreshes the catalogue; `apt upgrade` does the upgrading. They're usually run together: `sudo apt update && sudo apt upgrade`.

## In practice

On an Ubuntu or Debian machine: `sudo apt update`, then `apt list --upgradable` to see what's pending, then `sudo apt upgrade`. Install `htop` and run it to see your system's processes, then remove it again with `sudo apt remove htop`.""",
    "key_points": [
        "Package managers install signed packages from repositories and resolve dependencies.",
        "apt update refreshes the catalogue; apt upgrade installs newer versions; apt install/remove add and remove.",
        "dnf does the same on the Red Hat family; keep systems updated, and reboot for kernel updates.",
        "Snap/Flatpak, Docker and language package managers are other routes; add third-party repos only from trusted sources.",
    ],
    "figure_svg": PACKAGES,
    "figure_caption": "apt resolves dependencies, downloads signed packages from a repository, and tracks what it installed.",
    "questions": [
        mcq("What does `sudo apt update` do?", ["Upgrades all packages", "Refreshes the list of available packages", "Installs updates automatically every day", "Updates the kernel"], 1,
            "It refreshes the catalogue; apt upgrade does the upgrading."),
        mcq("Which command installs nginx on Ubuntu?", ["sudo dnf install nginx", "sudo apt install nginx", "sudo get nginx", "sudo nginx install"], 1, "apt on Debian/Ubuntu."),
        mcq("In the diagram, what does apt do before downloading?", ["Reboots", "Resolves dependencies", "Deletes old packages", "Builds from source"], 1,
            "It works out which other packages are needed.",
            PACKAGES, "You run sudo apt install htop; apt resolves dependencies, downloads from a signed repository, and installs and tracks the package."),
        mcq("Why are repository packages signed?", ["To make them smaller", "So your system can verify they're genuine and untampered", "For licensing", "To speed up downloads"], 1,
            "Signatures protect against tampering."),
        mcq("What removes dependencies that nothing uses any more?", ["apt clean", "apt autoremove", "apt purge-all", "apt update"], 1, "autoremove cleans up orphaned dependencies."),
        mcq("Which update usually needs a reboot to take effect?", ["A new text editor", "A new kernel", "A new font", "A Python library"], 1, "The running kernel is replaced only at boot."),
        mcq("In the diagram, which tool would you use on Fedora instead of apt?", ["pacman", "dnf", "brew", "snap"], 1, "dnf is the Red Hat family's package manager.",
            PACKAGES, "Package manager diagram listing apt (Debian/Ubuntu), dnf (Fedora/RHEL) and pacman (Arch)."),
        open_q("Explain the difference between apt update and apt upgrade.", "apt update downloads the latest list of available packages and versions from the repositories; apt upgrade then installs newer versions of the packages you already have.",
               ["update refreshes the package list", "upgrade installs newer versions"], "Usually run together."),
        open_q("Why should you be careful adding third-party repositories?", "Packages from a repository are installed with root privileges and updated automatically, so an untrustworthy or compromised repository could install malicious software on your system.",
               ["packages install as root", "untrusted source could be malicious"], "Only add repos from vendors you trust."),
        open_q("Why keep a Linux server updated, and how can you automate it on Ubuntu?", "Because most attacks use known vulnerabilities that updates already fix; on Ubuntu, unattended-upgrades can install security updates automatically, with reboots scheduled when the kernel changes.",
               ["updates fix known vulnerabilities", "unattended-upgrades automates security updates"], "Monitor reboot-required too."),
    ],
}

L6 = {
    "title": "Processes and services",
    "minutes": 8,
    "photo_query": "",
    "body": """Every running program is a **process**. Servers also run long-lived **services** in the background. Knowing how to see, stop and manage them is core admin work.

## Seeing processes

- `ps aux` lists every process with its **PID** (process ID), owner, CPU and memory use, and command.
- `ps aux | grep nginx` filters the list (the `|` pipe sends one command's output into another).
- `top` shows a live, updating view; **htop** is a friendlier version with colours and scrolling. Press `q` to quit.
- `pgrep nginx` prints just the PIDs of matching processes.

Processes are mostly **sleeping** (waiting for input, a timer or the disk) and briefly **running** on a CPU.

## Stopping processes: signals

You stop a process by sending it a **signal**:

- `kill 1234` sends **SIGTERM**: "please shut down". Well-behaved programs save their work and exit.
- `kill -9 1234` sends **SIGKILL**: the kernel ends it immediately. Nothing is saved or cleaned up, so use it only when SIGTERM fails.
- `pkill nginx` signals processes by name.
- **Ctrl+C** in a terminal sends SIGINT to the program running there.

## Services and systemd

Background services (web servers, databases, SSH, Docker) are managed by **systemd** on almost every modern distribution. Each service is a **unit**:

- `systemctl status nginx` shows whether it's running, its PID and the latest log lines.
- `sudo systemctl start nginx` / `stop` / `restart` control it now.
- `sudo systemctl enable nginx` makes it start at boot; `disable` stops that. (`enable --now` does both.)
- `systemctl list-units --type=service` lists services.

## Logs with journalctl

systemd collects service logs in the **journal**:

- `journalctl -u nginx` shows nginx's logs.
- `journalctl -u nginx -f` follows them live.
- `journalctl -b` shows everything since the last boot; `-p err` filters to errors.

> **Common misconception:** `enable` starts a service. It only sets it to start at boot; use `start` (or `enable --now`) to run it now.

## Resource checks

- `free -h` shows memory use.
- `uptime` shows how long the system has run and the **load average** (roughly, how many processes want CPU on average over 1, 5 and 15 minutes).

## In practice

Run `systemctl status ssh` (or `sshd`) to see a real service. Start a long command like `sleep 600 &`, find it with `pgrep sleep`, and end it politely with `kill`. Then follow a service's logs with `journalctl -u ssh -f` while you log in from another terminal.""",
    "key_points": [
        "Every program is a process with a PID; ps, top/htop and pgrep show them.",
        "kill sends SIGTERM (polite); kill -9 sends SIGKILL (forced, no cleanup) as a last resort.",
        "systemctl start/stop/restart/status controls services; enable/disable sets start at boot.",
        "journalctl -u <service> reads a service's logs; -f follows them.",
    ],
    "figure_svg": PROCS,
    "figure_caption": "Processes start, alternate between running and sleeping, and end on exit or when signalled.",
    "questions": [
        mcq("What is a PID?", ["A package ID", "A process ID", "A permission ID", "A port ID"], 1, "Each running process has a unique process ID."),
        mcq("Which signal does a plain `kill 1234` send?", ["SIGKILL", "SIGTERM", "SIGSTOP", "SIGHUP"], 1, "SIGTERM asks the process to exit cleanly."),
        mcq("Why prefer SIGTERM over SIGKILL?", ["SIGTERM is faster", "SIGTERM lets the program save work and clean up", "SIGKILL needs root", "SIGTERM restarts it"], 1,
            "SIGKILL ends it immediately with no cleanup."),
        mcq("How do you make nginx start automatically at boot?", ["sudo systemctl start nginx", "sudo systemctl enable nginx", "sudo nginx --boot", "sudo systemctl status nginx"], 1,
            "enable sets boot start; start runs it now."),
        mcq("Which command follows a service's logs live?", ["journalctl -u nginx -f", "systemctl logs nginx", "tail nginx", "ps nginx"], 0, "-f follows the journal."),
        mcq("In the diagram, which state are most processes in most of the time?", ["Running", "Sleeping", "Ended", "Started"], 1,
            "Most processes wait for input, timers or disk, so they're sleeping.",
            PROCS, "Process states: started, running, sleeping, ended, with exit or kill arrows to ended."),
        mcq("In the diagram's footnote, what does SIGKILL (kill -9) do?", ["Asks politely", "Forces the process to end immediately", "Pauses it", "Restarts it"], 1,
            "SIGKILL can't be caught or ignored.", PROCS, "Process lifecycle diagram noting SIGTERM asks politely and SIGKILL forces."),
        open_q("A web service is misbehaving. Describe how you'd check on it and restart it with systemd.", "Run systemctl status on it to see its state and recent log lines, read more with journalctl -u servicename, fix the cause if it's clear, then restart it with sudo systemctl restart servicename and check status again.",
               ["systemctl status", "journalctl -u for logs", "systemctl restart and recheck"], "Logs before restarts: a restart can hide the evidence."),
        open_q("What's the difference between systemctl enable and systemctl start?", "start runs the service now; enable configures it to start automatically at boot but doesn't start it now (enable --now does both).",
               ["start runs it now", "enable sets it to start at boot"], "A classic gotcha after installing a service."),
        open_q("Explain what the pipe in `ps aux | grep nginx` does.", "It sends the output of ps aux into grep as input, so grep filters the full process list down to the lines containing nginx.",
               ["sends output of one command into the next", "grep filters the list"], "Pipes let small tools combine into bigger ones."),
    ],
}

PACK = {
    "id": "linux-beginner",
    "version": 1,
    "topic": "Linux",
    "title": "Linux from scratch",
    "summary": "Find your way around a Linux system from the command line: files, permissions, software, processes and services. For beginners setting up a server, Raspberry Pi or home lab.",
    "icon": "binary",
    "level": "beginner",
    "length": "short",
    "area": "technology",
    "tags": ["linux", "command-line", "sysadmin", "self-hosting"],
    "sections": [
        {"title": "Finding your way", "summary": "What Linux is and how to move around and work with files.", "lessons": [
            {"title": L1["title"], "summary": "Explain the kernel, distributions and why the command line matters.", "lesson": L1},
            {"title": L2["title"], "summary": "Navigate the directory tree with paths, ls, cd and find.", "lesson": L2},
            {"title": L3["title"], "summary": "Create, copy, move, read, edit and delete files safely.", "lesson": L3},
        ]},
        {"title": "Running the system", "summary": "Users, software and the programs running on your machine.", "lessons": [
            {"title": L4["title"], "summary": "Read and set permissions and use sudo properly.", "lesson": L4},
            {"title": L5["title"], "summary": "Install, update and remove software with a package manager.", "lesson": L5},
            {"title": L6["title"], "summary": "See and stop processes and manage services with systemd.", "lesson": L6},
        ]},
    ],
}
