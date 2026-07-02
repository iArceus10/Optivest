import { BarChart3, LayoutDashboard } from "lucide-react";
import { NavLink } from "react-router-dom";

import { APP_NAV_ITEMS } from "../../utils/constants";

function Sidebar() {
  return (
    <div className="sidebar">
      <div className="sidebar__brand">
        <div className="brand-mark">
          <BarChart3 size={24} strokeWidth={2.6} />
        </div>

        <div>
          <h1 className="sidebar__brand-title">OptiVest</h1>
          <p className="sidebar__brand-copy">
            Portfolio optimization terminal
          </p>
        </div>
      </div>

      <nav className="sidebar__nav" aria-label="Primary navigation">
        {APP_NAV_ITEMS.map((item) => (
          <NavLink
            key={item.href}
            to={item.href}
            className={({ isActive }) =>
              [
                "sidebar__nav-link",
                isActive ? "sidebar__nav-link--active" : "",
              ]
                .filter(Boolean)
                .join(" ")
            }
          >
            <LayoutDashboard size={18} />
            <div>
              <div style={{ fontWeight: 700 }}>{item.label}</div>
              <div
                style={{
                  color: "var(--text-faint)",
                  fontSize: "0.84rem",
                  marginTop: 4,
                }}
              >
                {item.description}
              </div>
            </div>
          </NavLink>
        ))}
      </nav>

      <div className="sidebar__footer">
        <p className="sidebar__footer-label">Version 1</p>
        <p className="sidebar__footer-value">
          Clean portfolio analytics productization.
        </p>
      </div>
    </div>
  );
}

export default Sidebar;