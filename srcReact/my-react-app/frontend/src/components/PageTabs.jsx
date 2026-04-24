// PageTabs.jsx
// ── Tab bar matching Solara's "PAGE 0 / PAGE 1" tabs ──────────────────────
// Props:
//   pages       (array of {id, label}) — tab definitions
//   activePage  (number)               — currently selected page id
//   onPageChange (function)            — called with the new page id

import "./PageTabs.css";

export default function PageTabs({ pages = [], activePage, onPageChange }) {
  return (
    <div className="page-tabs">
      {pages.map(p => (
        <button
          key={p.id}
          className={`tab-btn ${activePage === p.id ? "tab-active" : ""}`}
          onClick={() => onPageChange(p.id)}
        >
          {p.label}
        </button>
      ))}
    </div>
  );
}