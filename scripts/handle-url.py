#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit


def main():
    if len(sys.argv) != 2:
        raise ValueError("Usage: handle-url.py jetbrains://...")
    uri = sys.argv[1]
    parsed = urlsplit(uri)
    if parsed.scheme != "jetbrains":
        raise ValueError("Only jetbrains:// URLs are supported")
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    config = json.loads((config_home / "idea-code-links" / "config.json").read_text())
    if parsed.netloc == "idea" and parsed.path.startswith("/navigate/"):
        args = [config["idea"], uri]
    elif config.get("daemon"):
        args = [config["daemon"], "handleUri", uri]
    else:
        raise ValueError("No JetBrains Daemon configured for this URL")
    os.execv(args[0], args)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as error:
        print(f"idea-code-links: {error}", file=sys.stderr)
        sys.exit(1)
