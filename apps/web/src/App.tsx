import { Suspense, lazy, useCallback, useEffect, useState } from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { Menu } from "lucide-react";
import { onUnauthorised, session } from "./api/client";
import { LogoMark } from "./components/Logo";
import { Dock, Sidebar } from "./components/Nav";
import { Loading } from "./components/PageHead";
import { Wallpaper } from "./components/Wallpaper";
import { Login } from "./screens/Login";
import { Today } from "./screens/Today";

const Library = lazy(() => import("./screens/Library").then((m) => ({ default: m.Library })));
const Course = lazy(() => import("./screens/Course").then((m) => ({ default: m.Course })));
const Lesson = lazy(() => import("./screens/Lesson").then((m) => ({ default: m.Lesson })));
const Quiz = lazy(() => import("./screens/Quiz").then((m) => ({ default: m.Quiz })));
const Review = lazy(() => import("./screens/Quiz").then((m) => ({ default: m.Review })));
const Exam = lazy(() => import("./screens/Quiz").then((m) => ({ default: m.Exam })));
const Practice = lazy(() => import("./screens/Quiz").then((m) => ({ default: m.Practice })));
const Insights = lazy(() => import("./screens/Insights").then((m) => ({ default: m.Insights })));
const Paths = lazy(() => import("./screens/Paths").then((m) => ({ default: m.Paths })));
const PathDetail = lazy(() => import("./screens/Paths").then((m) => ({ default: m.PathDetail })));
const Certificate = lazy(() => import("./screens/Certificate").then((m) => ({ default: m.Certificate })));
const History = lazy(() => import("./screens/History").then((m) => ({ default: m.History })));
const Awards = lazy(() => import("./screens/Awards").then((m) => ({ default: m.Awards })));
const Settings = lazy(() => import("./screens/Settings").then((m) => ({ default: m.Settings })));

export function App() {
  const [user, setUser] = useState<string | null>(session.token() ? session.user() : null);
  useEffect(() => onUnauthorised(() => setUser(null)), []);
  const signOut = useCallback(() => {
    session.clear();
    setUser(null);
  }, []);

  return (
    <BrowserRouter>
      <Wallpaper />
      {user === null ? <Login onLogin={setUser} /> : <Shell user={user} onSignOut={signOut} />}
    </BrowserRouter>
  );
}

function Shell({ user, onSignOut }: { user: string; onSignOut: () => void }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const closeMenu = useCallback(() => setMenuOpen(false), []);
  return (
    <div className="frame">
      <Sidebar user={user} open={menuOpen} onClose={closeMenu} onSignOut={onSignOut} />
      <header className="topbar">
        <button type="button" className="icon-link topbar__menu" onClick={() => setMenuOpen(true)} aria-label="Open menu">
          <Menu size={20} aria-hidden="true" />
        </button>
        <LogoMark size={30} />
        <span className="topbar__word">SIRIS<b>LEARN</b></span>
      </header>
      <main className="shell">
        <Suspense fallback={<Loading />}>
          <Routes>
            <Route path="/" element={<Today user={user} />} />
            <Route path="/library" element={<Library />} />
            <Route path="/course/:id" element={<Course />} />
            <Route path="/lesson/:id" element={<Lesson />} />
            <Route path="/lesson/:id/quiz" element={<Quiz />} />
            <Route path="/lesson/:id/practice" element={<Practice />} />
            <Route path="/review" element={<Review />} />
            <Route path="/insights" element={<Insights />} />
            <Route path="/paths" element={<Paths />} />
            <Route path="/path/:id" element={<PathDetail />} />
            <Route path="/course/:id/exam" element={<Exam />} />
            <Route path="/certificate/:id" element={<Certificate />} />
            <Route path="/history" element={<History />} />
            <Route path="/awards" element={<Awards />} />
            <Route path="/settings" element={<Settings onSignOut={onSignOut} />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Suspense>
      </main>
      <Dock />
    </div>
  );
}
