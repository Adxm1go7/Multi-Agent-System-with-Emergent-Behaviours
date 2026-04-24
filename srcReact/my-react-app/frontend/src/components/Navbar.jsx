import "./Navbar.css";

export default function Navbar({ title = "Opinion Convergence" }) {
  return (
    <nav className="navbar">
      <span className="navbar-title">{title}</span>
    </nav>
  );
}