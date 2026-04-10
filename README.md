# Kenobi Tracker

A real-time dog habit tracker for tracking Kenobi's daily water intake, bathroom outings, feedings, and accidents. Built as a single HTML file with no build tools — just open it in a browser.

## Features

### Water
- Log each watering with one tap
- Displays today's total count and time elapsed since the last watering
- Shows a timestamped list of today's waterings only

### Bathroom
- Record outings as pee, poop, or both
- Optional **Diaper Used** toggle — enable it before recording an outing to tag the entry; resets automatically after each record
- Shows a timestamped list of today's outings with color-coded badges

### Feeding
- Record breakfast, lunch, and dinner
- Optional **Add Pumpkin** toggle — enable it before recording a meal to log wet food with pumpkin instead of plain wet food; resets automatically after each record
- Shows today's feedings with meal and food-type badges

### Accident / Incident
- Tracks the most recent accident with a large days-since counter
- Day count is calendar-based: an accident recorded any time today shows **0**, yesterday shows **1**, and so on
- Tapping "Record Accident Now" overwrites the previous timestamp

## Sharing

Multiple devices can view and update the same session in real time. Tap **Copy Sharing Link** and send the URL to another person. Anyone with the link reads from and writes to the same data.

Sessions are identified by a UUID in the `?session=` query parameter. Opening the app without a session parameter generates a new UUID automatically.

## Data & Sync

- **Primary storage:** Google Firebase Firestore — all writes go here and are pushed to every connected device instantly via a real-time listener.
- **Offline cache:** `localStorage` is written on every sync, so the last known state renders immediately on page load even before Firebase responds.
- **Authentication:** Anonymous Firebase Auth is used silently to satisfy Firestore security rules. No account or login is required.

### Firestore document shape

```
trackers/{sessionId}
  waterLog:    string[]          // ISO timestamp per watering
  bathroomLog: { time, type, diaper }[]
  incidentTs:  string | null     // ISO timestamp of last accident
  foodLog:     { time, meal, pumpkin }[]
```

`meal` is `"breakfast"`, `"lunch"`, or `"dinner"`.  
`type` is `"piss"`, `"poop"`, or `"both"`.

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Vanilla HTML/CSS/JS — no framework |
| Database | Firebase Firestore |
| Auth | Firebase Anonymous Auth |
| Hosting | Static file (no server required) |

## Running Locally

No build step needed. Open `index.html` directly in a browser or serve it with any static file server:

```bash
npx serve .
```

The app connects to the existing Firebase project automatically.
