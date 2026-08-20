#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# <xbar.title>Kenobi Tracker</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author.github>gwcromwell</xbar.author.github>
# <xbar.desc>Shows last watering and last bathroom outing for Kenobi.</xbar.desc>
# <xbar.dependencies>python3</xbar.dependencies>

import json
import os
import subprocess
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.error import URLError

CONF_FILE = os.path.expanduser("~/.kenobi-tracker.conf")
PROJECT_ID = "dog-tracker-294ea"
# API key is already public in index.html; session UUID is the access control
API_KEY = "AIzaSyAjf5_FXec1K3e56QgBeENn4P3jblJX2Ys"


def load_session_id():
    try:
        with open(CONF_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    return line
    except FileNotFoundError:
        pass
    return None


def prompt_session_id():
    """Show a native macOS dialog asking for the session ID."""
    script = (
        'display dialog "Enter your Kenobi Tracker session ID'
        ' (copy it from the ?session= parameter in the app URL):" '
        'default answer "" '
        'with title "Kenobi Tracker Setup" '
        'buttons {"Cancel", "Save"} default button "Save"'
    )
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    for part in result.stdout.strip().split(", "):
        if part.startswith("text returned:"):
            return part[len("text returned:"):].strip()
    return None


def save_session_id(session_id):
    with open(CONF_FILE, "w") as f:
        f.write(f"# Kenobi Tracker session ID\n{session_id}\n")


def elapsed(iso_str):
    try:
        ts = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        secs = max(0, int((datetime.now(timezone.utc) - ts).total_seconds()))
        mins = secs // 60
        hours = mins // 60
        if hours >= 24:
            return f"{hours // 24}d"
        if hours > 0:
            rem = mins % 60
            return f"{hours}h {rem}m" if rem else f"{hours}h"
        return f"{mins}m"
    except Exception:
        return "?"


def fetch_doc(session_id):
    url = (
        f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}"
        f"/databases/(default)/documents/trackers/{session_id}?key={API_KEY}"
    )
    with urlopen(url, timeout=10) as resp:
        return json.loads(resp.read())


def get_strings(fields, key):
    try:
        vals = fields[key]["arrayValue"].get("values", [])
        return [v["stringValue"] for v in vals if "stringValue" in v]
    except (KeyError, TypeError):
        return []


def get_maps(fields, key):
    try:
        vals = fields[key]["arrayValue"].get("values", [])
        return [v["mapValue"]["fields"] for v in vals if "mapValue" in v]
    except (KeyError, TypeError):
        return []


def map_str(m, key):
    try:
        return m[key]["stringValue"]
    except (KeyError, TypeError):
        return ""


def print_error(msg):
    print("⚠️ Kenobi")
    print("---")
    print(f"{msg} | color=red")


def main():
    session_id = load_session_id()
    if not session_id:
        session_id = prompt_session_id()
        if session_id:
            save_session_id(session_id)
        else:
            print_error("Tap to set up — run the plugin again to enter your session ID")
            return

    try:
        doc = fetch_doc(session_id)
    except URLError as e:
        print_error(f"Network error: {getattr(e, 'reason', e)}")
        return
    except Exception as e:
        print_error(f"Error: {e}")
        return

    fields = doc.get("fields", {})

    water_log = get_strings(fields, "waterLog")
    water_elapsed = elapsed(max(water_log)) if water_log else "–"

    bathroom_log = get_maps(fields, "bathroomLog")
    if bathroom_log:
        last_outing_ts = map_str(max(bathroom_log, key=lambda e: map_str(e, "time")), "time")
        outing_elapsed = elapsed(last_outing_ts)
    else:
        outing_elapsed = "–"

    print(f"💧 {water_elapsed}  🐾 {outing_elapsed}")


if __name__ == "__main__":
    main()
