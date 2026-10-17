import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import "./glass/glass.css";
import "./app.css";

// Offline support and notifications (built app only; the dev server has no sw.js caching).
if (import.meta.env.PROD && "serviceWorker" in navigator) {
  window.addEventListener("load", () => navigator.serviceWorker.register("/sw.js").catch(() => undefined));
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
