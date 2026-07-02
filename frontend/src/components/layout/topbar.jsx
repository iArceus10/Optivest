import { LogOut } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../../context/auth-context";

function getInitials(fullName) {
  if (!fullName) {
    return "OV";
  }

  const parts = fullName.trim().split(/\s+/).slice(0, 2);
  return parts.map((part) => part[0]?.toUpperCase() ?? "").join("");
}

function Topbar({ title, subtitle }) {
  const navigate = useNavigate();
  const { currentUser, logout } = useAuth();

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  }

  return (
    <>
      <div>
        <h2 className="topbar__title">{title}</h2>
        <p className="topbar__subtitle">{subtitle}</p>
      </div>

      <div className="topbar__actions">
        <div className="topbar__badge">
          <span className="topbar__badge-dot" />
          Backend integrated through Phase 8
        </div>

        <div className="topbar__user">
          <div className="topbar__user-avatar">
            {getInitials(currentUser?.full_name)}
          </div>

          <div className="topbar__user-meta">
            <p className="topbar__user-name">
              {currentUser?.full_name ?? "OptiVest User"}
            </p>
            <p className="topbar__user-email">
              {currentUser?.email ?? "Portfolio analytics workspace"}
            </p>
          </div>

          <button
            type="button"
            onClick={handleLogout}
            aria-label="Sign out"
            title="Sign out"
            style={{
              display: "grid",
              placeItems: "center",
              width: 36,
              height: 36,
              borderRadius: "50%",
              border: "1px solid var(--border-subtle)",
              color: "var(--text-secondary)",
              transition: "all var(--transition-base)",
            }}
          >
            <LogOut size={16} />
          </button>
        </div>
      </div>
    </>
  );
}

export default Topbar;