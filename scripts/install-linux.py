#!/usr/bin/env python3
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def desktop_arg(value):
    value = str(value).replace("%", "%%")
    for char in ("\\", '"', "`", "$"):
        value = value.replace(char, "\\" + char)
    return '"' + value + '"'


def main():
    if len(sys.argv) != 2:
        raise ValueError("Usage: python3 scripts/install-linux.py /absolute/path/to/bin/idea")
    launcher = Path(sys.argv[1]).expanduser().resolve()
    if not launcher.is_file() or not os.access(launcher, os.X_OK):
        raise ValueError(f"IDEA launcher is not executable: {launcher}")
    if not shutil.which("xdg-mime"):
        raise ValueError("Install xdg-utils first")
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    data_home = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    config_dir = config_home / "idea-code-links"
    handler_dir = data_home / "idea-code-links"
    apps = data_home / "applications"
    for folder in (config_dir, handler_dir, apps):
        folder.mkdir(parents=True, exist_ok=True)
    desktop_id = "idea-code-links.desktop"
    previous = subprocess.check_output(
        ["xdg-mime", "query", "default", "x-scheme-handler/jetbrains"], text=True
    ).strip()
    previous_file = config_dir / "previous-handler.txt"
    if previous != desktop_id:
        previous_file.write_text(previous + "\n")
    daemon = data_home / "JetBrains/Daemon/bundles/current/jetbrainsd/bin/jetbrainsd"
    config = {"idea": str(launcher), "daemon": str(daemon) if daemon.is_file() else shutil.which("jetbrainsd")}
    (config_dir / "config.json").write_text(json.dumps(config, indent=2) + "\n")
    handler = handler_dir / "handle-url.py"
    shutil.copyfile(Path(__file__).with_name("handle-url.py"), handler)
    desktop = "\n".join([
        "[Desktop Entry]", "Version=1.0", "Type=Application",
        "Name=IntelliJ IDEA Code Links", "NoDisplay=true", "Terminal=false",
        "MimeType=x-scheme-handler/jetbrains;",
        f"Exec={desktop_arg(sys.executable)} {desktop_arg(handler)} %u", "",
    ])
    (apps / desktop_id).write_text(desktop)
    subprocess.run(["xdg-mime", "default", desktop_id, "x-scheme-handler/jetbrains"], check=True)
    if shutil.which("update-desktop-database"):
        subprocess.run(["update-desktop-database", str(apps)], check=True)
    print(f"Installed {desktop_id}")
    print(f"IDEA: {launcher}")
    print(f"Previous handler: {previous or '(none)'}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"idea-code-links: {error}", file=sys.stderr)
        sys.exit(1)
