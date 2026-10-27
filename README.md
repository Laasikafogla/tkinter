# HackHub ⚡

**HackHub** is a hackathon management desktop GUI application built strictly with **Python 3.10+** and standard library **`tkinter`/`ttk`** (no external packages or databases required). It features an in-memory data store, role-based workflows, live evaluation matrices, custom-drawn podium and charts on canvas, and a cohesive dark indigo UI theme (`clam`).

---

## 🚀 Features

### 1. Role-Based Access & Authentication
- **Organizer**: Oversees event progression, manages teams (including disqualification & reinstatement), configures judging rounds and evaluation criteria, assigns panels, and publishes final standings.
- **Judge**: Dedicated workspace showing assigned panel teams, fixed round criteria, live weighted score calculation (`sum((score / max) * weight)`), and automatic saving on field exit (`<FocusOut>`).
- **Volunteer**: Live schedule of panels and teams with check-in toggles. Scores are strictly hidden to preserve confidentiality.
- **Participant**: Team registration and profile management with repository URL validator (`http://` or `https://`) and browser launch. Profiles lock automatically once judging begins.
- **Demo Logins**: One-click demo login buttons directly on the sign-in screen for rapid role testing.

### 2. Organizer Console
- **Status Stepper**: `DRAFT` ➔ `REGISTRATION_OPEN` ➔ `JUDGING` ➔ `COMPLETED` with safety confirmation dialogs before each stage advance.
- **Team Management**: Real-time search filter, sortable columns, and disqualification reason auditing with reinstatement capability.
- **Rounds & Evaluation Criteria**: Support for 1 to 5 rounds with live weight verification (`Total weight: 100%` required to save criteria).
- **Panels & Auto-balancing**: Assign judges and teams to panels, automated team distribution, and enforcement of a single final round panel.
- **Results & Advancement**: Ranked standings per panel, missing score checks preventing premature round closure, and Top-N advancement.

### 3. Live Leaderboard & Visualizations
- **Top 3 Podium**: Custom-rendered Gold, Silver, and Bronze blocks on a `tk.Canvas`.
- **Score Comparison Bar Chart**: Horizontal bar chart drawn on a `tk.Canvas`.
- **Tie-Breaking Rule**: Earlier registration timestamp wins in case of score ties.
- **Auto-Refresh**: Live updates every 10 seconds with manual refresh support.

---

## 🛠️ Design & Theme

- **Engine**: Tkinter / TTK with `clam` theme.
- **Palette**: Dark Indigo:
  - Background: `#0F0826`
  - Cards: `#1B1540`
  - Borders: `#2E2663`
  - Primary: `#7957FF` (Hover: `#9B76FF`)
  - Accent / Success: `#34D399`
  - Warning: `#FBBF24`
  - Error: `#F87171`

---

## 📂 Project Architecture

```text
tkinter/
├── main.py     # Application entry point
├── store.py    # In-memory Store class & sample data (no UI dependencies)
├── ui.py       # Tkinter/TTK screens, widgets, theme, and navigator
└── README.md   # Documentation
```

---

## 💻 Getting Started

### Prerequisites
- Python 3.10 or higher (with `tkinter` standard library included).

### Run Application
From the project directory:

```bash
python3 main.py
```

### Preloaded Demo Credentials
You can log in manually or click any demo button on the login screen:
- **Organizer**: `alice@hackhub.io` / `password123`
- **Judge**: `bob@hackhub.io` / `password123`
- **Participant**: `charlie@hackhub.io` / `password123`
- **Volunteer**: `victor@hackhub.io` / `password123`
