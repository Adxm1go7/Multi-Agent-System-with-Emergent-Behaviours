/*May not be used*/

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