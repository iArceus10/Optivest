import { Outlet, useLocation } from "react-router-dom";

import Sidebar from "./sidebar";
import Topbar from "./topbar";

function resolvePageMetadata(pathname) {
  if (pathname.startsWith("/portfolios/")) {
    return {
      title: "Portfolio Workspace",
      subtitle:
        "Inspect portfolio composition, review analytics, and compare optimization and risk outputs in a single workspace.",
    };
  }

  return {
    title: "Dashboard",
    subtitle:
      "Manage portfolios, launch analytics workflows, and monitor the health of your investment ideas from one terminal.",
  };
}

function AppShell() {
  const location = useLocation();
  const pageMeta = resolvePageMetadata(location.pathname);

  return (
    <div className="app-shell">
      <aside className="app-shell__sidebar">
        <Sidebar />
      </aside>

      <div className="app-shell__content">
        <header className="app-shell__topbar">
          <Topbar
            title={pageMeta.title}
            subtitle={pageMeta.subtitle}
          />
        </header>

        <main className="app-shell__main">
          <div className="page-container">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}

export default AppShell;