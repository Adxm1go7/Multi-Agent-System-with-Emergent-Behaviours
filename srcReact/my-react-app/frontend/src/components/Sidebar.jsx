// Sidebar.jsx
// ── Left control panel matching Solara's sidebar ───────────────────────────
// Props:
//   params      (array)    — list of parameter configs (see shape below)
//   onReset     (function) — called when Reset is clicked
//   onStep      (function) — called when Step is clicked
//   onPlay      (function) — called when Play/Pause is clicked
//   isPlaying   (bool)     — whether the sim is currently running
//   info        (object)   — key/value pairs shown in the Information section
//   playInterval (number)  — current play interval ms value (controlled)
//   onPlayIntervalChange (function) — called with new play interval value
//
// Each param in `params` has this shape:
// {
//   key: string,           — matches the state key in App.jsx
//   label: string,         — display label
//   type: "slider"         — continuous slider
//       | "select"         — dropdown
//       | "checkbox",      — toggle
//   value: any,            — current value (controlled from App.jsx)
//   onChange: function,    — called with new value
//   // slider only:
//   min: number,
//   max: number,
//   step: number,
//   // select only:
//   options: string[],
// }

import "./Sidebar.css";

function SliderParam({ label, value, min, max, step, onChange }) {
  return (
    <div className="param">
      <label className="param-label">{label}</label>
      <input
        type="range"
        min={min} max={max} step={step}
        value={value}
        onChange={e => onChange(step % 1 === 0 ? parseInt(e.target.value) : parseFloat(e.target.value))}
        className="param-slider"
      />
      {/* Show current value to the right */}
      <span className="param-value">{value}</span>
    </div>
  );
}

function NumberInputParam({ label, value, onChange, placeholder }) {
  return (
    <div className="param">
      <label className="param-label">{label}</label>
      <input
        type="number"
        value={value}
        onChange={e => onChange(e.target.value)}
        placeholder={placeholder}
        className="param-select"   // reuse your existing input styling
      />
    </div>
  );
}

function SelectParam({ label, value, options, onChange }) {
  return (
    <div className="param">
      <label className="param-label">{label}</label>
      <select
        value={value}
        onChange={e => onChange(e.target.value)}
        className="param-select"
      >
        {options.map(opt => (
          <option key={opt} value={opt}>{opt}</option>
        ))}
      </select>
    </div>
  );
}

function CheckboxParam({ label, value, onChange }) {
  return (
    <div className="param param-checkbox">
      <input
        type="checkbox"
        checked={value}
        onChange={e => onChange(e.target.checked)}
        id={`cb-${label}`}
      />
      <label htmlFor={`cb-${label}`} className="param-label">{label}</label>
    </div>
  );
}

export default function Sidebar({
  params = [],
  onReset,
  onStep,
  onPlay,
  isPlaying,
  info = {},
  playInterval,
  onPlayIntervalChange,
  seed,
  onSeedChange,
}) {
  return (
    <aside className="sidebar">

      {/* ── Controls section ───────────────────────────────── */}
      <section className="sidebar-section">
        <h3 className="sidebar-heading">Controls</h3>

        {/* Play interval slider — mirrors Solara's built-in control */}
        <SliderParam
          label="Play Interval (ms)"
          value={playInterval}
          min={50} max={1000} step={50}
          onChange={onPlayIntervalChange}
        />

        <div className="param">
          <label className="param-label">Random Seed (blank = random)</label>
          <input
            type="number"
            value={seed}
            onChange={e => onSeedChange(e.target.value)}
            placeholder="e.g. 42"
            className="param-select"   // reuse the same styling as your dropdowns
          />
        </div>

        {/* Action buttons */}
        <div className="btn-row">
          <button className="btn btn-reset" onClick={onReset}>RESET</button>
          <button className="btn btn-play" onClick={onPlay}>
            {isPlaying ? "⏸" : "▶"}
          </button>
          <button className="btn btn-step" onClick={onStep}>STEP</button>
        </div>
      </section>

      {/* ── Model Parameters section ────────────────────────── */}
      <section className="sidebar-section">
        <h3 className="sidebar-heading">Model Parameters</h3>
        {params.map(p => {
          if (p.type === "slider") return (
            <SliderParam key={p.key} label={p.label} value={p.value}
              min={p.min} max={p.max} step={p.step} onChange={p.onChange} />
          );
          if (p.type === "select") return (
            <SelectParam key={p.key} label={p.label} value={p.value}
              options={p.options} onChange={p.onChange} />
          );
          if (p.type === "checkbox") return (
            <CheckboxParam key={p.key} label={p.label} value={p.value}
              onChange={p.onChange} />
          );
          if (p.type === "numberinput") return (
            <NumberInputParam key={p.key} label={p.label} value={p.value}
              onChange={p.onChange} placeholder={p.placeholder} />
          );
          return null;
        })}
      </section>

      {/* ── Information section ─────────────────────────────── */}
      <section className="sidebar-section">
        <h3 className="sidebar-heading">Information</h3>
        {Object.entries(info).map(([key, val]) => (
          <div key={key} className="info-row">
            <span className="info-key">{key}:</span>
            <span className="info-val">{val}</span>
          </div>
        ))}
      </section>

    </aside>
  );
}