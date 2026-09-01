import {
  Cloud,
  LayoutDashboard,
  Server,
  ShieldCheck,
  HeartPulse,
  MessageSquare,
} from "lucide-react";

import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="logo">
        <Cloud size={28} />
        <span>AWS Assistant</span>
      </div>

      {/* Navigation */}
      <nav className="nav-menu">

        <NavLink to="/" className="nav-item">
          <LayoutDashboard size={20} />
          <span>Dashboard</span>
        </NavLink>

        <NavLink to="/resources" className="nav-item">
          <Server size={20} />
          <span>Resources</span>
        </NavLink>

        <NavLink to="/security" className="nav-item">
          <ShieldCheck size={20} />
          <span>Security</span>
        </NavLink>

        <NavLink to="/health" className="nav-item">
          <HeartPulse size={20} />
          <span>Health</span>
        </NavLink>

        <NavLink to="/assistant" className="nav-item">
          <MessageSquare size={20} />
          <span>AI Assistant</span>
        </NavLink>

      </nav>
    </aside>
  );
}

export default Sidebar;