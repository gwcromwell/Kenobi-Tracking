# Kenobi Tracker

A real-time dog habit tracker for tracking Kenobi's daily water intake, bathroom outings, feedings, and accidents. Built as a single HTML file with no build tools — just open it in a browser.

## Features

### Water
- Log each watering with one tap
- Displays today's total count and time elapsed since the last watering
- Shows a timestamped list of today's waterings only

### Bathroom
- Record outings as pee, poop, or both
- Displays today's walk count and time elapsed since the last walk (derived from bathroom outing timestamps)
- Optional **Diaper Used** toggle — enable it before recording an outing to tag the entry; resets automatically after each record
- Shows a timestamped list of today's outings with color-coded badges

### Feeding
- Record breakfast, lunch, and dinner
- Optional **Add Pumpkin** toggle — enable it before recording a meal to log wet food with pumpkin instead of plain wet food; resets automatically after each record
- Shows today's feedings with meal and food-type badges
- Only today's records are shown; prior days are never displayed

### Accident / Incident
- Tracks the most recent accident with a large days-since counter
- Day count is calendar-based: an accident recorded any time today shows **0**, yesterday shows **1**, and so on
- The last accident date and time are displayed inside the counter box
- Tap the **Whoops** button to record a new accident

## Layout

The app uses a two-column card grid optimised to fit an iPad screen without scrolling:

| Row | Left | Right |
|-----|------|-------|
| 1 | Water | Bathroom |
| 2 | Feeding (full width) | |
| 3 | Accident / Incident (full width) | |

On phones (≤600px) all cards stack into a single column, and the Feeding card's list and buttons stack vertically for comfortable tap targets.

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
  waterLog:    string[]                      // ISO timestamp per watering
  bathroomLog: { time, type, diaper }[]      // type: "piss" | "poop" | "both"
  incidentTs:  string | null                 // ISO timestamp of last accident
  foodLog:     { time, meal, pumpkin }[]     // meal: "breakfast" | "lunch" | "dinner"
```

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
