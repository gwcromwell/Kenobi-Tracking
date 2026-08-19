# Kenobi Tracker — macOS Menu Bar Plugin

Shows last watering time and last bathroom outing time in the macOS menu bar, polling Firestore every 2 minutes.

```
💧 2h 15m  🐾 45m
```

## Prerequisites

- macOS with [xbar](https://xbarapp.com) installed (`brew install xbar`)
- Python 3 (pre-installed on macOS)

## Setup

### 1. Open Firestore reads (one-time Firebase console change)

The Firestore security rules need to allow unauthenticated reads. In the [Firebase console](https://console.firebase.google.com/project/dog-tracker-294ea/firestore/rules), update the rules to:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /trackers/{sessionId} {
      allow read: if true;                         // public read — UUID is the access control
      allow write: if request.auth != null;        // writes still require auth
    }
  }
}
```

### 2. Create the config file

Find your session UUID from the `?session=` parameter in the Kenobi Tracker URL, then create `~/.kenobi-tracker.conf`:

```
# Kenobi Tracker session ID
YOUR-SESSION-UUID-HERE
```

### 3. Install the plugin

Copy `kenobi.2m.py` to your xbar plugins folder (default: `~/Library/Application Support/xbar/plugins/`):

```bash
cp kenobi.2m.py ~/Library/Application\ Support/xbar/plugins/
chmod +x ~/Library/Application\ Support/xbar/plugins/kenobi.2m.py
```

Then click **Refresh All** in xbar. The widget appears in your menu bar within seconds.

## Customizing the poll interval

Rename the file to change how often it refreshes:

| Filename | Interval |
|---|---|
| `kenobi.1m.py` | Every minute |
| `kenobi.2m.py` | Every 2 minutes (default) |
| `kenobi.5m.py` | Every 5 minutes |

## Dropdown detail

Clicking the menu bar item shows:

```
💧 2h 15m  🐾 45m
---
Last watering: 10:45 AM (2h 15m ago)
Last outing: 12:32 PM (45m ago) · pee
```
