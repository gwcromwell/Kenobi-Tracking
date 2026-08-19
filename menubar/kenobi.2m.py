#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# <xbar.title>Kenobi Tracker</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author.github>gwcromwell</xbar.author.github>
# <xbar.desc>Shows last watering and last bathroom outing for Kenobi.</xbar.desc>
# <xbar.dependencies>python3</xbar.dependencies>

import json
import os
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


def fmt_local_time(iso_str):
    try:
        ts = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return ts.astimezone().strftime("%-I:%M %p")
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
        print_error(f"No session configured — create {CONF_FILE}")
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
    if water_log:
        last_water_ts = max(water_log)
        water_elapsed = elapsed(last_water_ts)
        water_time = fmt_local_time(last_water_ts)
    else:
        last_water_ts = None
        water_elapsed = "–"
        water_time = None

    bathroom_log = get_maps(fields, "bathroomLog")
    if bathroom_log:
        last_outing = max(bathroom_log, key=lambda e: map_str(e, "time"))
        last_outing_ts = map_str(last_outing, "time")
        outing_elapsed = elapsed(last_outing_ts)
        outing_time = fmt_local_time(last_outing_ts)
        type_labels = {"piss": "pee", "poop": "poop", "both": "both"}
        outing_type = type_labels.get(map_str(last_outing, "type"), "")
    else:
        last_outing_ts = None
        outing_elapsed = "–"
        outing_time = None
        outing_type = None

    print(f"💧 {water_elapsed}  🐾 {outing_elapsed}")
    print("---")

    if water_time:
        print(f"Last watering: {water_time} ({water_elapsed} ago)")
    else:
        print("Last watering: none recorded")

    if outing_time:
        type_suffix = f" · {outing_type}" if outing_type else ""
        print(f"Last outing: {outing_time} ({outing_elapsed} ago){type_suffix}")
    else:
        print("Last outing: none recorded")


if __name__ == "__main__":
    main()
