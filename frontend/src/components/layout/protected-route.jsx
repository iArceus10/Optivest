import { Navigate, useLocation } from "react-router-dom";

import { useAuth } from "../../context/auth-context";

function ProtectedRoute({ children }) {
  const { isAuthenticated, isBootstrapping } = useAuth();
  const location = useLocation();

  if (isBootstrapping) {
    return (
      <div className="auth-page">
        <div className="auth-card" style={{ maxWidth: 480, width: "100%" }}>
          <p
            style={{
              margin: 0,
              color: "var(--text-secondary)",
              fontSize: "1rem",
              lineHeight: 1.7,
            }}
          >
            Restoring your OptiVest session and loading your analytics workspace…
          </p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <Navigate
        to="/login"
        replace
        state={{ from: location.pathname }}
      />
    );
  }

  return children;
}

export default ProtectedRoute;