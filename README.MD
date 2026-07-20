# Chord Metronome

A mobile-first guitar chord-change practice app. The Python/FastAPI app serves the interface, while the browser Web Audio API schedules precise metronome clicks.

## Features

- 30–220 BPM metronome
- Accent on beat one
- 2, 3, 4 or 6 beats per bar
- Change chord every 1, 2, 4, 8 or 16 beats
- Ordered, random and two-chord alternating modes
- Mobile-first UI
- Settings saved locally in the browser
- Two-bar count-in option

## Run locally

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r requirements.txt
uvicorn chordmetronome:app --reload
```

Open `http://127.0.0.1:8000`.

## Deploy to Vercel

1. Put all files in one GitHub repository.
2. Import the repository into Vercel.
3. Leave the framework preset on automatic detection.
4. Deploy.

`index.py` exposes the FastAPI `app` object using an entry-point name Vercel recognises.

## Important browser behaviour

A user must press **Start Practice** before sound can play because mobile browsers block automatic audio. The app also stops when the tab is hidden, preventing timing drift after returning to it.