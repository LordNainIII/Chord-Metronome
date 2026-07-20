from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Chord Metronome — Practice and Chord Player")

HTML = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
  <meta name="theme-color" content="#111827" />
  <title>Chord Metronome</title>
  <style>
    :root {
      color-scheme: dark;
      --bg: #080b12;
      --panel: rgba(20, 25, 38, .86);
      --panel-2: #171d2b;
      --text: #f8fafc;
      --muted: #9ca3af;
      --accent: #8b5cf6;
      --accent-2: #22d3ee;
      --danger: #fb7185;
      --line: rgba(255,255,255,.10);
      --shadow: 0 24px 60px rgba(0,0,0,.38);
    }
    * { box-sizing: border-box; }
    html, body { margin: 0; min-height: 100%; background: var(--bg); color: var(--text); font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
    body {
      min-height: 100svh;
      background:
        radial-gradient(circle at 12% 0%, rgba(139,92,246,.24), transparent 34%),
        radial-gradient(circle at 100% 14%, rgba(34,211,238,.12), transparent 28%),
        var(--bg);
      padding: max(18px, env(safe-area-inset-top)) 16px max(24px, env(safe-area-inset-bottom));
    }
    button, input, select { font: inherit; }
    button { -webkit-tap-highlight-color: transparent; }
    .app { width: min(100%, 560px); margin: 0 auto; }
    .card { background:var(--panel); border:1px solid var(--line); border-radius:25px; box-shadow:var(--shadow); backdrop-filter: blur(18px); }
    .stage { padding:20px 18px 18px; text-align:center; overflow:hidden; position:relative; }
    .stage:before { content:""; position:absolute; width:180px; height:180px; border-radius:50%; background:rgba(139,92,246,.12); filter:blur(20px); top:30px; left:50%; transform:translateX(-50%); pointer-events:none; }
    .eyebrow { position:relative; text-transform:uppercase; letter-spacing:.17em; color:var(--muted); font-size:10px; font-weight:800; }
    .chord { position:relative; margin:6px 0 2px; font-size:clamp(78px, 23vw, 126px); line-height:1; letter-spacing:-.075em; font-weight:850; text-shadow:0 10px 40px rgba(139,92,246,.22); }
    .next { position:relative; color:var(--muted); font-size:13px; min-height:20px; }
    .diagram-wrap { position:relative; display:flex; justify-content:center; margin:10px 0 4px; min-height:178px; }
    .diagram-wrap.hidden { display:none; min-height:0; }
    .chord-diagram { width:150px; height:176px; overflow:visible; }
    .chord-diagram .string, .chord-diagram .fret { stroke:#64748b; stroke-width:2; }
    .chord-diagram .nut { stroke:#e2e8f0; stroke-width:6; }
    .chord-diagram .marker { fill:#60a5fa; stroke:#2563eb; stroke-width:3; }
    .chord-diagram .finger { fill:white; font-weight:800; font-size:15px; text-anchor:middle; dominant-baseline:middle; }
    .chord-diagram .open { fill:none; stroke:#94a3b8; stroke-width:3; }
    .chord-diagram .mute { stroke:#94a3b8; stroke-width:3; stroke-linecap:round; }
    .diagram-caption { color:var(--muted); font-size:10px; letter-spacing:.08em; text-transform:uppercase; margin-top:3px; }
    .bar-progress { position:relative; width:min(100%, 320px); height:5px; margin:17px auto 10px; overflow:hidden; border-radius:999px; background:rgba(255,255,255,.09); }
    .bar-progress-fill { width:0%; height:100%; border-radius:inherit; background:linear-gradient(90deg,var(--accent),var(--accent-2)); box-shadow:0 0 14px rgba(34,211,238,.42); transform-origin:left center; }
    .beats { display:flex; justify-content:center; gap:11px; margin:10px 0 17px; position:relative; }
    .beat { width:12px; height:12px; border-radius:50%; background:#343b4d; transition:transform .08s ease, background .08s ease, box-shadow .08s ease; }
    .beat.active { background:var(--accent-2); transform:scale(1.45); box-shadow:0 0 22px rgba(34,211,238,.9); }
    .beat.downbeat.active { background:var(--accent); box-shadow:0 0 24px rgba(139,92,246,.9); }
    .tempo-row { display:grid; grid-template-columns:48px 1fr 48px; gap:10px; align-items:center; margin-top:4px; }
    .icon-btn { height:48px; border-radius:16px; border:1px solid var(--line); background:var(--panel-2); color:var(--text); font-size:25px; cursor:pointer; }
    .icon-btn:active { transform:scale(.97); }
    .tempo { font-size:36px; font-weight:800; letter-spacing:-.04em; }
    .tempo small { color:var(--muted); font-size:11px; letter-spacing:.12em; margin-left:5px; }
    input[type=range] { width:100%; accent-color:var(--accent); margin:13px 0 2px; }
    .primary { width:100%; margin-top:15px; min-height:58px; border:0; border-radius:18px; color:white; cursor:pointer; font-weight:850; letter-spacing:.04em; background:linear-gradient(135deg,var(--accent),#6d5dfc 55%,var(--accent-2)); box-shadow:0 14px 34px rgba(109,93,252,.28); }
    .primary.stop { background:linear-gradient(135deg,#f43f5e,var(--danger)); }
    .controls { margin-top:14px; padding:17px; }
    .section-title { margin:0 0 12px; font-size:13px; color:#dbe2ee; }
    .grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
    label { display:block; color:var(--muted); font-size:11px; font-weight:700; letter-spacing:.04em; }
    select, .text-input { width:100%; margin-top:7px; border:1px solid var(--line); border-radius:14px; background:var(--panel-2); color:var(--text); padding:12px; outline:none; }
    .full { grid-column:1/-1; }
    .chord-tools { display:grid; grid-template-columns:1fr auto auto; gap:8px; margin-top:10px; }
    .chord-search { width:100%; border:1px solid var(--line); border-radius:12px; background:var(--panel-2); color:var(--text); padding:10px 12px; outline:none; }
    .small-btn { border:1px solid var(--line); border-radius:12px; background:var(--panel-2); color:#d7ddea; padding:9px 11px; cursor:pointer; }
    .chord-picks { display:flex; flex-wrap:wrap; gap:8px; margin-top:10px; max-height:280px; overflow:auto; padding-right:3px; }
    .chip { border:1px solid var(--line); border-radius:12px; background:var(--panel-2); color:#d7ddea; padding:9px 11px; cursor:pointer; min-width:42px; }
    .chip.selected { background:rgba(139,92,246,.20); border-color:rgba(167,139,250,.76); color:white; box-shadow:inset 0 0 0 1px rgba(139,92,246,.15); }
    .switch-row { display:flex; justify-content:space-between; align-items:center; margin-top:13px; padding-top:13px; border-top:1px solid var(--line); color:#dbe2ee; font-size:13px; }
    .switch { position:relative; width:47px; height:27px; }
    .switch input { opacity:0; width:0; height:0; }
    .slider { position:absolute; inset:0; background:#343b4d; border-radius:999px; cursor:pointer; transition:.2s; }
    .slider:before { content:""; position:absolute; width:21px; height:21px; left:3px; top:3px; background:white; border-radius:50%; transition:.2s; }
    .switch input:checked + .slider { background:var(--accent); }
    .switch input:checked + .slider:before { transform:translateX(20px); }
    .sequence { margin-top:14px; color:var(--muted); font-size:12px; line-height:1.7; padding:12px 13px; border-radius:14px; background:rgba(255,255,255,.035); border:1px solid var(--line); }
    .sequence strong { color:white; }
    .hint { margin:14px 4px 0; text-align:center; color:#697386; font-size:11px; line-height:1.5; }
    .top-tabs { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:14px; padding:5px; border:1px solid var(--line); border-radius:16px; background:rgba(20,25,38,.70); }
    .tab-btn { border:0; border-radius:12px; padding:12px; color:var(--muted); background:transparent; cursor:pointer; font-weight:800; }
    .tab-btn.active { color:white; background:linear-gradient(135deg,rgba(139,92,246,.55),rgba(34,211,238,.25)); box-shadow:inset 0 0 0 1px rgba(255,255,255,.08); }
    .page { display:none; }
    .page.active { display:block; }
    .player-card { padding:22px 18px; text-align:center; }
    .player-heading { margin:0 0 14px; font-size:20px; }
    .chord-picker-button { display:inline-flex; align-items:center; justify-content:center; gap:8px; min-width:132px; border:1px solid var(--line); border-radius:16px; background:var(--panel-2); color:white; padding:10px 16px; cursor:pointer; font-size:34px; font-weight:850; letter-spacing:-.04em; }
    .chord-picker-button .chevron { color:var(--muted); font-size:15px; transform:translateY(1px); }
    .player-diagram { display:flex; justify-content:center; min-height:184px; margin:6px 0 4px; cursor:pointer; border-radius:18px; }
    .player-diagram:active { background:rgba(255,255,255,.025); }
    .primary-player { width:100%; min-height:68px; border:1px solid rgba(255,255,255,.2); border-radius:16px; background:linear-gradient(135deg,#7c3aed 0%,#4f7df3 52%,#10bfe3 100%); color:white; cursor:pointer; font-weight:900; font-size:18px; letter-spacing:.03em; box-shadow:0 14px 32px rgba(65,113,255,.28), inset 0 1px 0 rgba(255,255,255,.18); display:flex; align-items:center; justify-content:center; gap:12px; transition:transform .12s ease, filter .12s ease; }
    .primary-player:hover { filter:brightness(1.06); }
    .primary-player:active { transform:scale(.985); }
    .play-icon { width:38px; height:38px; border-radius:999px; display:grid; place-items:center; background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.24); font-size:18px; line-height:1; padding-left:2px; }
    .play-mode { display:grid; grid-template-columns:1fr 1fr; gap:6px; margin-top:10px; padding:5px; border:1px solid var(--line); border-radius:14px; background:rgba(255,255,255,.025); }
    .mode-btn { border:0; border-radius:10px; padding:10px 8px; color:var(--muted); background:transparent; cursor:pointer; font-weight:750; }
    .mode-btn.active { color:white; background:var(--panel-2); box-shadow:inset 0 0 0 1px var(--line); }
    .strum-direction { display:flex; align-items:center; justify-content:center; gap:7px; margin-top:10px; color:var(--muted); font-size:12px; }
    .direction-btn { border:1px solid var(--line); border-radius:999px; background:var(--panel-2); color:#dce4f3; padding:7px 12px; cursor:pointer; font-weight:750; }
    .direction-btn.active { border-color:rgba(167,139,250,.8); color:white; background:rgba(139,92,246,.18); }
    .volume-row { margin-top:15px; text-align:left; }
    .picker-backdrop { position:fixed; inset:0; z-index:50; display:none; align-items:flex-end; background:rgba(0,0,0,.62); backdrop-filter:blur(6px); }
    .picker-backdrop.open { display:flex; }
    .picker-sheet { width:100%; max-height:82vh; padding:18px; border:1px solid var(--line); border-radius:24px 24px 0 0; background:#101522; box-shadow:0 -20px 60px rgba(0,0,0,.45); }
    .picker-handle { width:44px; height:4px; margin:0 auto 15px; border-radius:999px; background:#3a4255; }
    .picker-header { display:flex; justify-content:space-between; align-items:center; gap:12px; margin-bottom:12px; }
    .picker-title { margin:0; font-size:18px; }
    .picker-close { width:36px; height:36px; border:1px solid var(--line); border-radius:12px; background:var(--panel-2); color:white; cursor:pointer; font-size:18px; }
    .picker-search { width:100%; border:1px solid var(--line); border-radius:14px; background:var(--panel-2); color:white; padding:13px 14px; outline:none; }
    .picker-grid { display:flex; flex-wrap:wrap; gap:8px; max-height:55vh; overflow:auto; margin-top:12px; padding:1px 2px 14px; }
    .picker-option { min-width:48px; border:1px solid var(--line); border-radius:12px; background:var(--panel-2); color:#dce4f3; padding:10px 12px; cursor:pointer; }
    .picker-option.active { border-color:rgba(167,139,250,.85); background:rgba(139,92,246,.2); color:white; }
    @media (min-width: 620px) { body { padding-top:34px; } .stage { padding:27px 25px 23px; } .controls { padding:21px; } }
  </style>
</head>
<body>
  <main class="app">
    <nav class="top-tabs" aria-label="App pages">
      <button class="tab-btn active" id="practiceTab" type="button">Practice</button>
      <button class="tab-btn" id="playerTab" type="button">Chord Player</button>
    </nav>

    <div class="page active" id="practicePage">
    <section class="card stage">
      <div class="eyebrow" id="status">Ready</div>
      <div class="chord" id="currentChord">G</div>
      <div class="next" id="nextChord">Next: D</div>
      <div class="diagram-wrap" id="diagramWrap"><div><svg class="chord-diagram" id="chordDiagram" viewBox="0 0 150 176" aria-label="G chord diagram"></svg><div class="diagram-caption">Chord shape</div></div></div>
      <div class="bar-progress" aria-hidden="true"><div class="bar-progress-fill" id="barProgressFill"></div></div>
      <div class="beats" id="beats"></div>

      <div class="tempo-row">
        <button class="icon-btn" id="minus" aria-label="Decrease tempo">−</button>
        <div class="tempo"><span id="bpmValue">80</span><small>BPM</small></div>
        <button class="icon-btn" id="plus" aria-label="Increase tempo">+</button>
      </div>
      <input id="bpm" type="range" min="30" max="220" value="80" aria-label="Tempo" />
      <button class="primary" id="startStop">▶ START PRACTICE</button>
    </section>

    <section class="card controls">
      <h2 class="section-title">Practice settings</h2>
      <div class="grid">
        <label>Beats per bar
          <select id="beatsPerBar"><option>2</option><option>3</option><option selected>4</option><option>6</option></select>
        </label>
        <label>Change chord every
          <select id="changeEvery"><option value="1">1 beat</option><option value="2">2 beats</option><option value="4" selected>4 beats</option><option value="8">8 beats</option><option value="16">16 beats</option></select>
        </label>
        <label class="full">Practice mode
          <select id="mode"><option value="sequence">Play in selected order</option><option value="random">Choose chords randomly</option><option value="alternate">Alternate first two chords</option></select>
        </label>
      </div>

      <div style="margin-top:16px">
        <label>Select chords</label>
        <div class="chord-tools"><input class="chord-search" id="chordSearch" placeholder="Search e.g. C#m7 or sus4" aria-label="Search chords"><button class="small-btn" id="selectVisible" type="button">Select shown</button><button class="small-btn" id="clearChords" type="button">Clear</button></div>
        <div class="chord-picks" id="chordPicks"></div>
      </div>

      <div class="switch-row"><span>Show chord diagram</span><label class="switch"><input id="showDiagram" type="checkbox" checked><span class="slider"></span></label></div>
      <div class="switch-row"><span>Accent the first beat</span><label class="switch"><input id="accent" type="checkbox" checked><span class="slider"></span></label></div>
      <div class="switch-row"><span>Two-bar count-in</span><label class="switch"><input id="countIn" type="checkbox"><span class="slider"></span></label></div>
      <div class="switch-row"><span>Keep screen awake while playing</span><label class="switch"><input id="keepAwake" type="checkbox" checked><span class="slider"></span></label></div>
      <div class="sequence" id="sequencePreview"><strong>Sequence:</strong> G → D → Em → C</div>
    </section>
    <p class="hint">Keep this page open while practising. Your settings are saved automatically on this device.</p>
    </div>

    <div class="page" id="playerPage">
      <section class="card player-card">
        <h1 class="player-heading">Chord Player</h1>
        <button class="chord-picker-button" id="openChordPicker" type="button" aria-haspopup="dialog"><span id="playerChordName">G</span><span class="chevron">▼</span></button>
        <div class="player-diagram" id="playerDiagramTap" title="Tap to play"><svg class="chord-diagram" id="playerChordDiagram" viewBox="0 0 150 176" aria-label="G chord diagram"></svg></div>
        <button class="primary-player" id="playSelectedChord" type="button" aria-label="Play chord"><span class="play-icon" aria-hidden="true">▶</span><span>PLAY</span></button>
        <div class="play-mode" aria-label="Playback style">
          <button class="mode-btn active" id="strumMode" type="button">Strum</button>
          <button class="mode-btn" id="arpeggioMode" type="button">Arpeggio</button>
        </div>
        <div class="strum-direction" id="directionControls">Direction <button class="direction-btn active" id="downDirection" type="button">↓ Down</button><button class="direction-btn" id="upDirection" type="button">↑ Up</button></div>
        <div class="volume-row"><label>Volume<input id="playerVolume" type="range" min="0.15" max="1" step="0.05" value="0.7"></label></div>
      </section>
    </div>
  </main>

  <div class="picker-backdrop" id="chordPicker" role="dialog" aria-modal="true" aria-labelledby="pickerTitle">
    <div class="picker-sheet">
      <div class="picker-handle"></div>
      <div class="picker-header"><h2 class="picker-title" id="pickerTitle">Choose a chord</h2><button class="picker-close" id="closeChordPicker" type="button" aria-label="Close">×</button></div>
      <input class="picker-search" id="playerChordSearch" placeholder="Search chords…" autocomplete="off">
      <div class="picker-grid" id="playerChordGrid"></div>
    </div>
  </div>
  </main>

<script>
(() => {
  const ROOTS = [
    {name:'C', pc:0}, {name:'C#', pc:1}, {name:'Db', pc:1}, {name:'D', pc:2},
    {name:'D#', pc:3}, {name:'Eb', pc:3}, {name:'E', pc:4}, {name:'F', pc:5},
    {name:'F#', pc:6}, {name:'Gb', pc:6}, {name:'G', pc:7}, {name:'G#', pc:8},
    {name:'Ab', pc:8}, {name:'A', pc:9}, {name:'A#', pc:10}, {name:'Bb', pc:10}, {name:'B', pc:11}
  ];
  const QUALITIES = [
    {suffix:'', label:'major', pattern:[0,2,2,1,0,0], fingers:[1,3,4,2,1,1]},
    {suffix:'m', label:'minor', pattern:[0,2,2,0,0,0], fingers:[1,3,4,1,1,1]},
    {suffix:'7', label:'dominant 7', pattern:[0,2,0,1,0,0], fingers:[1,3,1,2,1,1]},
    {suffix:'maj7', label:'major 7', pattern:[0,2,1,1,0,0], fingers:[1,4,2,3,1,1]},
    {suffix:'m7', label:'minor 7', pattern:[0,2,0,0,0,0], fingers:[1,3,1,1,1,1]},
    {suffix:'6', label:'sixth', pattern:[0,2,2,1,2,0], fingers:[1,2,3,1,4,1]},
    {suffix:'m6', label:'minor sixth', pattern:[0,2,2,0,2,0], fingers:[1,2,3,1,4,1]},
    {suffix:'sus2', label:'suspended 2', pattern:[0,2,4,4,0,0], fingers:[1,2,3,4,1,1]},
    {suffix:'sus4', label:'suspended 4', pattern:[0,2,2,2,0,0], fingers:[1,2,3,4,1,1]},
    {suffix:'dim', label:'diminished', pattern:[0,1,2,0,2,0], fingers:[1,2,3,1,4,1]},
    {suffix:'aug', label:'augmented', pattern:[0,3,2,1,1,0], fingers:[1,4,3,2,1,1]},
    {suffix:'add9', label:'add 9', pattern:[0,2,2,1,0,2], fingers:[1,3,4,2,1,4]},
    {suffix:'9', label:'dominant 9', pattern:[0,2,0,1,0,2], fingers:[1,3,1,2,1,4]}
  ];
  const allChordNames = ROOTS.flatMap(root => QUALITIES.map(q => root.name + q.suffix));

  // Put the shapes guitarists encounter most often at the beginning, while
  // retaining the complete library beneath them.
  const COMMON_CHORDS = [
    'C','D','E','F','G','A','B',
    'Am','Bm','Dm','Em',
    'C7','D7','E7','G7','A7','B7',
    'Cmaj7','Dmaj7','Emaj7','Fmaj7','Gmaj7','Amaj7',
    'Am7','Bm7','Dm7','Em7',
    'Asus2','Asus4','Dsus2','Dsus4','Esus4','Gsus4',
    'Cadd9','Dadd9','Eadd9','Gadd9','Aadd9'
  ];
  const commonSet = new Set(COMMON_CHORDS);
  const chordNames = [
    ...COMMON_CHORDS.filter(name => allChordNames.includes(name)),
    ...allChordNames.filter(name => !commonSet.has(name))
  ];
  const openShapes = {
    C:{frets:[-1,3,2,0,1,0], fingers:[0,3,2,0,1,0]}, Cm:{frets:[-1,3,5,5,4,3], fingers:[0,1,3,4,2,1], baseFret:3, barre:3},
    D:{frets:[-1,-1,0,2,3,2], fingers:[0,0,0,1,3,2]}, Dm:{frets:[-1,-1,0,2,3,1], fingers:[0,0,0,2,3,1]},
    E:{frets:[0,2,2,1,0,0], fingers:[0,2,3,1,0,0]}, Em:{frets:[0,2,2,0,0,0], fingers:[0,2,3,0,0,0]},
    F:{frets:[1,3,3,2,1,1], fingers:[1,3,4,2,1,1], barre:1}, G:{frets:[3,2,0,0,0,3], fingers:[2,1,0,0,0,3]},
    A:{frets:[-1,0,2,2,2,0], fingers:[0,0,1,2,3,0]}, Am:{frets:[-1,0,2,2,1,0], fingers:[0,0,2,3,1,0]},
    B:{frets:[-1,2,4,4,4,2], fingers:[0,1,2,3,4,1], baseFret:2, barre:2}, Bm:{frets:[-1,2,4,4,3,2], fingers:[0,1,3,4,2,1], baseFret:2, barre:2}
  };
  function makeShape(name) {
    if (openShapes[name]) return openShapes[name];
    const root = ROOTS.find(r => name.startsWith(r.name) && QUALITIES.some(q => name === r.name + q.suffix));
    const quality = QUALITIES.find(q => name === root.name + q.suffix) || QUALITIES[0];
    // Use a movable E-family shape. Root fret is pitch class measured from E.
    let rootFret = (root.pc - 4 + 12) % 12;
    if (rootFret === 0) rootFret = 12;
    const frets = quality.pattern.map(offset => rootFret + offset);
    return {frets, fingers:quality.fingers, baseFret:rootFret, barre:rootFret};
  }
  const chordShapes = Object.fromEntries(chordNames.map(name => [name, makeShape(name)]));
  const defaults = { bpm:80, beatsPerBar:4, changeEvery:4, mode:'sequence', accent:true, countIn:false, showDiagram:true, keepAwake:true, selected:['G','D','Em','C'] };
  const saved = JSON.parse(localStorage.getItem('chordMetronomeSettings') || 'null');
  const state = {...defaults, ...(saved || {})};

  const $ = id => document.getElementById(id);
  const bpm = $('bpm'), bpmValue = $('bpmValue'), startStop = $('startStop');
  const currentChord = $('currentChord'), nextChord = $('nextChord'), status = $('status');
  const beatsEl = $('beats'), picksEl = $('chordPicks'), preview = $('sequencePreview'), chordSearch = $('chordSearch');
  const diagram = $('chordDiagram'), diagramWrap = $('diagramWrap');
  const barProgressFill = $('barProgressFill');
  const playerChordSearch = $('playerChordSearch'), playerChordName = $('playerChordName'), playerDiagram = $('playerChordDiagram');
  const playerChordGrid = $('playerChordGrid'), chordPicker = $('chordPicker');
  let playerChord = 'G', playerMode = 'strum', strumDirection = 'down';

  let audioCtx = null, isPlaying = false, schedulerId = null;
  let nextNoteTime = 0, beatIndex = 0, totalBeat = 0, chordIndex = 0, currentName = state.selected[0];
  let lookahead = 25, scheduleAhead = 0.12, barProgressAnimation = null, wakeLock = null;

  function save() {
    localStorage.setItem('chordMetronomeSettings', JSON.stringify(state));
  }

  function syncControls() {
    bpm.value = state.bpm; bpmValue.textContent = state.bpm;
    $('beatsPerBar').value = String(state.beatsPerBar);
    $('changeEvery').value = String(state.changeEvery);
    $('mode').value = state.mode; $('accent').checked = state.accent; $('countIn').checked = state.countIn; $('showDiagram').checked = state.showDiagram; $('keepAwake').checked = state.keepAwake;
    renderPicks(); renderBeats(); updateChordText(); toggleDiagram();
  }


  function svgEl(name, attrs={}) {
    const el = document.createElementNS('http://www.w3.org/2000/svg', name);
    Object.entries(attrs).forEach(([k,v]) => el.setAttribute(k, v));
    return el;
  }

  function renderChordDiagram(name, target = diagram) {
    const shape = chordShapes[name];
    target.innerHTML = '';
    target.setAttribute('aria-label', name + ' chord diagram');
    if (!shape) return;

    const x0=25, y0=35, stringGap=20, fretGap=28;
    const base = shape.baseFret || 1;

    for (let s=0; s<6; s++) target.appendChild(svgEl('line',{x1:x0+s*stringGap,y1:y0,x2:x0+s*stringGap,y2:y0+4*fretGap,class:'string'}));
    for (let f=0; f<=4; f++) target.appendChild(svgEl('line',{x1:x0,y1:y0+f*fretGap,x2:x0+5*stringGap,y2:y0+f*fretGap,class:f===0 && base===1 ? 'nut':'fret'}));

    if (base > 1) {
      const t=svgEl('text',{x:8,y:y0+18,fill:'#94a3b8','font-size':'13','font-weight':'700'}); t.textContent=base+'fr'; target.appendChild(t);
    }

    shape.frets.forEach((f,s) => {
      const x=x0+s*stringGap;
      if (f === 0) target.appendChild(svgEl('circle',{cx:x,cy:17,r:8,class:'open'}));
      if (f === -1) {
        target.appendChild(svgEl('line',{x1:x-6,y1:11,x2:x+6,y2:23,class:'mute'}));
        target.appendChild(svgEl('line',{x1:x+6,y1:11,x2:x-6,y2:23,class:'mute'}));
      }
      if (f > 0) {
        const displayFret = base > 1 ? f-base+1 : f;
        const cy=y0+(displayFret-.5)*fretGap;
        target.appendChild(svgEl('circle',{cx:x,cy,r:13,class:'marker'}));
        const finger=(shape.fingers||[])[s];
        if (finger) { const t=svgEl('text',{x,y:cy,class:'finger'}); t.textContent=finger; target.appendChild(t); }
      }
    });

    if (shape.barre) {
      const displayFret = base > 1 ? shape.barre-base+1 : shape.barre;
      const cy=y0+(displayFret-.5)*fretGap;
      target.insertBefore(svgEl('line',{x1:x0,y1:cy,x2:x0+5*stringGap,y2:cy,stroke:'#60a5fa','stroke-width':'18','stroke-linecap':'round'}), target.firstChild);
    }
  }

  function toggleDiagram() {
    diagramWrap.classList.toggle('hidden', !state.showDiagram);
  }

  function visibleChordNames() {
    const query = (chordSearch.value || '').trim().toLowerCase();
    return chordNames.filter(name => !query || name.toLowerCase().includes(query));
  }

  function renderPicks() {
    picksEl.innerHTML = '';
    visibleChordNames().forEach(name => {
      const b = document.createElement('button');
      b.className = 'chip' + (state.selected.includes(name) ? ' selected' : '');
      b.textContent = name;
      b.onclick = () => {
        if (state.selected.includes(name)) {
          if (state.selected.length > 1) state.selected = state.selected.filter(x => x !== name);
        } else state.selected.push(name);
        chordIndex = 0; currentName = state.selected[0];
        renderPicks(); updateChordText(); save();
      };
      picksEl.appendChild(b);
    });
  }

  function renderBeats(active = -1) {
    beatsEl.innerHTML = '';
    for (let i=0; i<state.beatsPerBar; i++) {
      const dot = document.createElement('div');
      dot.className = 'beat' + (i === 0 ? ' downbeat' : '') + (i === active ? ' active' : '');
      beatsEl.appendChild(dot);
    }
  }

  function nextSequentialIndex() { return (chordIndex + 1) % state.selected.length; }
  function randomIndex(exclude) {
    if (state.selected.length < 2) return 0;
    let i; do { i = Math.floor(Math.random() * state.selected.length); } while (i === exclude);
    return i;
  }
  function peekNext() {
    if (state.selected.length < 2) return state.selected[0];
    if (state.mode === 'alternate') return state.selected[chordIndex === 0 ? 1 : 0];
    return state.selected[nextSequentialIndex()];
  }
  function advanceChord() {
    if (state.mode === 'random') chordIndex = randomIndex(chordIndex);
    else if (state.mode === 'alternate') chordIndex = chordIndex === 0 ? 1 : 0;
    else chordIndex = nextSequentialIndex();
    currentName = state.selected[chordIndex];
  }
  function updateChordText() {
    currentName = state.selected[chordIndex] || state.selected[0];
    currentChord.textContent = currentName;
    nextChord.textContent = 'Next: ' + peekNext();
    renderChordDiagram(currentName);
    preview.innerHTML = '<strong>Sequence:</strong> ' + state.selected.join(' → ');
  }


  function showPage(page) {
    const practice = page === 'practice';
    $('practicePage').classList.toggle('active', practice);
    $('playerPage').classList.toggle('active', !practice);
    $('practiceTab').classList.toggle('active', practice);
    $('playerTab').classList.toggle('active', !practice);
    if (!practice) updatePlayerChord(playerChord);
  }

  function renderPlayerChordGrid() {
    const query = (playerChordSearch.value || '').trim().toLowerCase();
    playerChordGrid.innerHTML = '';
    chordNames.filter(name => !query || name.toLowerCase().includes(query)).forEach(name => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'picker-option' + (name === playerChord ? ' active' : '');
      button.textContent = name;
      button.onclick = () => { updatePlayerChord(name); closeChordPicker(); };
      playerChordGrid.appendChild(button);
    });
  }

  function openChordPicker() {
    playerChordSearch.value = '';
    renderPlayerChordGrid();
    chordPicker.classList.add('open');
    document.body.style.overflow = 'hidden';
    setTimeout(() => playerChordSearch.focus(), 50);
  }

  function closeChordPicker() {
    chordPicker.classList.remove('open');
    document.body.style.overflow = '';
  }

  function updatePlayerChord(name) {
    if (!chordShapes[name]) return;
    playerChord = name;
    playerChordName.textContent = name;
    renderChordDiagram(name, playerDiagram);
    renderPlayerChordGrid();
  }

  function setPlayerMode(mode) {
    playerMode = mode;
    $('strumMode').classList.toggle('active', mode === 'strum');
    $('arpeggioMode').classList.toggle('active', mode === 'arpeggio');
    $('directionControls').style.display = mode === 'strum' ? 'flex' : 'none';
    // Keep the primary action deliberately simple: icon + PLAY.
  }

  function setStrumDirection(direction) {
    strumDirection = direction;
    $('downDirection').classList.toggle('active', direction === 'down');
    $('upDirection').classList.toggle('active', direction === 'up');
  }

  function playCurrentSelection() {
    playChord(playerMode === 'arpeggio' ? 'arpeggio' : strumDirection);
  }

  function ensureAudioContext() {
    audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)({ latencyHint:'interactive' });
    return audioCtx.resume();
  }

  function midiToHz(midi) { return 440 * Math.pow(2, (midi - 69) / 12); }

  function pluckString(midi, when, volume=0.7) {
    const frequency = midiToHz(midi);
    const duration = 2.4;
    const length = Math.max(2, Math.floor(audioCtx.sampleRate * duration));
    const buffer = audioCtx.createBuffer(1, length, audioCtx.sampleRate);
    const data = buffer.getChannelData(0);
    const period = Math.max(2, Math.floor(audioCtx.sampleRate / frequency));
    for (let i=0; i<period && i<length; i++) data[i] = Math.random() * 2 - 1;
    const damping = 0.996 - Math.min(0.003, frequency / 200000);
    for (let i=period; i<length; i++) data[i] = damping * 0.5 * (data[i-period] + data[i-period+1]);

    const source = audioCtx.createBufferSource();
    const filter = audioCtx.createBiquadFilter();
    const gain = audioCtx.createGain();
    source.buffer = buffer;
    filter.type = 'lowpass';
    filter.frequency.value = Math.min(6500, frequency * 9);
    filter.Q.value = 0.45;
    gain.gain.setValueAtTime(Math.max(0.0001, volume * 0.34), when);
    gain.gain.exponentialRampToValueAtTime(0.0001, when + duration);
    source.connect(filter); filter.connect(gain); gain.connect(audioCtx.destination);
    source.start(when); source.stop(when + duration);
  }

  async function playChord(direction='down') {
    await ensureAudioContext();
    if ('audioSession' in navigator) { try { navigator.audioSession.type = 'playback'; } catch (_) {} }
    const shape = chordShapes[playerChord];
    const openMidi = [40,45,50,55,59,64];
    const notes = shape.frets.map((f,i) => f < 0 ? null : openMidi[i] + f)
      .map((midi,i) => ({midi,index:i})).filter(n => n.midi !== null);
    if (direction === 'up') notes.reverse();
    const spacing = direction === 'arpeggio' ? 0.22 : 0.045;
    const now = audioCtx.currentTime + 0.04;
    const volume = Number($('playerVolume').value);
    notes.forEach((note,i) => pluckString(note.midi, now + i * spacing, volume));
  }


  function resetBarProgress() {
    if (barProgressAnimation) {
      barProgressAnimation.cancel();
      barProgressAnimation = null;
    }
    barProgressFill.style.width = '0%';
  }

  function animateBarProgress() {
    resetBarProgress();
    const barDurationMs = (60 / state.bpm) * state.beatsPerBar * 1000;
    barProgressAnimation = barProgressFill.animate(
      [{ width: '0%' }, { width: '100%' }],
      { duration: barDurationMs, easing: 'linear', fill: 'forwards' }
    );
  }

  function clickSound(time, downbeat) {
    const master = audioCtx.createGain();
    const compressor = audioCtx.createDynamicsCompressor();
    compressor.threshold.value = -18;
    compressor.knee.value = 12;
    compressor.ratio.value = 8;
    compressor.attack.value = 0.001;
    compressor.release.value = 0.08;
    master.gain.value = downbeat && state.accent ? 1.25 : 0.9;
    master.connect(compressor);
    compressor.connect(audioCtx.destination);

    const osc = audioCtx.createOscillator();
    const oscGain = audioCtx.createGain();
    osc.type = 'square';
    osc.frequency.value = downbeat && state.accent ? 1500 : 1000;
    oscGain.gain.setValueAtTime(0.0001, time);
    oscGain.gain.exponentialRampToValueAtTime(0.95, time + 0.001);
    oscGain.gain.exponentialRampToValueAtTime(0.0001, time + 0.07);
    osc.connect(oscGain); oscGain.connect(master);
    osc.start(time); osc.stop(time + 0.075);

    const length = Math.max(1, Math.floor(audioCtx.sampleRate * 0.025));
    const buffer = audioCtx.createBuffer(1, length, audioCtx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < length; i++) data[i] = (Math.random() * 2 - 1) * (1 - i / length);
    const noise = audioCtx.createBufferSource();
    const noiseGain = audioCtx.createGain();
    noise.buffer = buffer;
    noiseGain.gain.setValueAtTime(downbeat && state.accent ? 0.7 : 0.45, time);
    noiseGain.gain.exponentialRampToValueAtTime(0.0001, time + 0.025);
    noise.connect(noiseGain); noiseGain.connect(master);
    noise.start(time); noise.stop(time + 0.03);
  }

  async function requestWakeLock() {
    if (!state.keepAwake || !isPlaying || !('wakeLock' in navigator)) return;
    try {
      wakeLock = await navigator.wakeLock.request('screen');
      wakeLock.addEventListener('release', () => { wakeLock = null; });
    } catch (error) {
      console.warn('Screen wake lock was not granted:', error);
    }
  }

  async function releaseWakeLock() {
    if (!wakeLock) return;
    try { await wakeLock.release(); } catch (_) {}
    wakeLock = null;
  }

  function scheduleNote(beat, time) {
    clickSound(time, beat === 0);
    const delay = Math.max(0, (time - audioCtx.currentTime) * 1000);
    setTimeout(() => {
      if (!isPlaying) return;
      renderBeats(beat);
      if (beat === 0) animateBarProgress();
      if (totalBeat > 0 && totalBeat % state.changeEvery === 0) {
        advanceChord(); updateChordText();
      }
      totalBeat++;
    }, delay);
  }

  function scheduler() {
    while (nextNoteTime < audioCtx.currentTime + scheduleAhead) {
      scheduleNote(beatIndex, nextNoteTime);
      nextNoteTime += 60 / state.bpm;
      beatIndex = (beatIndex + 1) % state.beatsPerBar;
    }
  }

  async function start() {
    if ('audioSession' in navigator) {
      try { navigator.audioSession.type = 'playback'; } catch (_) {}
    }
    audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)({ latencyHint: 'interactive' });
    await audioCtx.resume();
    isPlaying = true; beatIndex = 0; totalBeat = 0; chordIndex = 0; currentName = state.selected[0]; updateChordText();
    nextNoteTime = audioCtx.currentTime + 0.08;
    if (state.countIn) {
      status.textContent = 'Count in';
      totalBeat = -(state.beatsPerBar * 2);
    } else status.textContent = 'Practising';
    schedulerId = setInterval(scheduler, lookahead);
    await requestWakeLock();
    startStop.textContent = '■ STOP'; startStop.classList.add('stop');
  }

  function stop() {
    isPlaying = false; clearInterval(schedulerId); schedulerId = null;
    releaseWakeLock();
    renderBeats(); resetBarProgress(); status.textContent = 'Ready';
    startStop.textContent = '▶ START PRACTICE'; startStop.classList.remove('stop');
  }

  startStop.onclick = () => isPlaying ? stop() : start();
  $('minus').onclick = () => setBpm(state.bpm - 1);
  $('plus').onclick = () => setBpm(state.bpm + 1);
  function setBpm(v) { state.bpm = Math.max(30, Math.min(220, Number(v))); bpm.value=state.bpm; bpmValue.textContent=state.bpm; if (isPlaying) animateBarProgress(); save(); }
  bpm.oninput = e => setBpm(e.target.value);
  $('beatsPerBar').onchange = e => { state.beatsPerBar=Number(e.target.value); renderBeats(); if (isPlaying) animateBarProgress(); save(); };
  $('changeEvery').onchange = e => { state.changeEvery=Number(e.target.value); save(); };

  chordSearch.oninput = renderPicks;
  $('selectVisible').onclick = () => {
    state.selected = [...new Set([...state.selected, ...visibleChordNames()])];
    chordIndex = 0; currentName = state.selected[0]; renderPicks(); updateChordText(); save();
  };
  $('clearChords').onclick = () => {
    state.selected = [currentName || 'G']; chordIndex = 0; currentName = state.selected[0]; renderPicks(); updateChordText(); save();
  };

  $('mode').onchange = e => { state.mode=e.target.value; chordIndex=0; updateChordText(); save(); };
  $('showDiagram').onchange = e => { state.showDiagram=e.target.checked; toggleDiagram(); save(); };
  $('accent').onchange = e => { state.accent=e.target.checked; save(); };
  $('countIn').onchange = e => { state.countIn=e.target.checked; save(); };
  $('keepAwake').onchange = async e => {
    state.keepAwake=e.target.checked; save();
    if (state.keepAwake) await requestWakeLock(); else await releaseWakeLock();
  };
  document.addEventListener('visibilitychange', async () => {
    if (document.visibilityState === 'visible' && isPlaying) {
      if (audioCtx && audioCtx.state === 'suspended') await audioCtx.resume();
      await requestWakeLock();
    }
  });
  $('practiceTab').onclick = () => showPage('practice');
  $('playerTab').onclick = () => showPage('player');
  $('openChordPicker').onclick = openChordPicker;
  $('closeChordPicker').onclick = closeChordPicker;
  chordPicker.onclick = e => { if (e.target === chordPicker) closeChordPicker(); };
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeChordPicker(); });
  playerChordSearch.oninput = renderPlayerChordGrid;
  $('strumMode').onclick = () => setPlayerMode('strum');
  $('arpeggioMode').onclick = () => setPlayerMode('arpeggio');
  $('downDirection').onclick = () => setStrumDirection('down');
  $('upDirection').onclick = () => setStrumDirection('up');
  $('playSelectedChord').onclick = playCurrentSelection;
  $('playerDiagramTap').onclick = playCurrentSelection;
  setPlayerMode('strum');
  setStrumDirection('down');
  updatePlayerChord(playerChord);
  syncControls();
})();
</script>
</body>
</html>'''


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    return HTMLResponse(HTML)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "app": "chord-metronome"}