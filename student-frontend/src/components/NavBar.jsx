// src/components/NavBar.jsx
import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function NavBar() {
  const { user, logout } = useAuth();
  const nav = useNavigate();

  const onLogout = () => {
    logout();
    nav("/login");
  };

  return (
    <header className="site-navbar">
      <div className="brand" onClick={() => nav("/dashboard")}>VedaStudent</div>

      <nav className="nav-links">
        <NavLink to="/dashboard" className={({isActive}) => isActive ? "active": ""}>Dashboard</NavLink>
        <NavLink to="/invite" className={({isActive}) => isActive ? "active": ""}>Invite</NavLink>
        <NavLink to="/accept-invitation" className={({isActive}) => isActive ? "active": ""}>Accept Invite</NavLink>
      </nav>

      <div className="nav-actions">
        {user ? (
          <>
            <div className="user-chip">
              <span className="dot" /> {user.username || "—"} <small>({user.role || "user"})</small>
            </div>
            <button className="btn ghost" onClick={onLogout}>Logout</button>
          </>
        ) : (
          <NavLink to="/login" className="btn primary">Login</NavLink>
        )}
      </div>
    </header>
  );
}
