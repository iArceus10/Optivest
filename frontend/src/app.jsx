import { Navigate, Route, Routes } from "react-router-dom";

import AppShell from "./components/layout/app-shell";
import ProtectedRoute from "./components/layout/protected-route";
import DashboardPage from "./pages/dashboard-page";
import LoginPage from "./pages/login-page";
import PortfolioPage from "./pages/portfolio-page";
import RegisterPage from "./pages/register-page";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />

      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route
        element={
          <ProtectedRoute>
            <AppShell />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/portfolios/:portfolioId" element={<PortfolioPage />} />
      </Route>

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}

export default App;