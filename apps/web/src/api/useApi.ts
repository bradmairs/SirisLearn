import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "./client";

/**
 * Load a resource, and keep reloading every `pollMs` while `poll(data)` says
 * something is still being written (a course plan, a lesson). `reload()`
 * fetches again and restarts the polling.
 */
export function useApi<T>(path: string | null, options: { poll?: (data: T) => boolean; pollMs?: number } = {}) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [nonce, setNonce] = useState(0);
  const pollRef = useRef(options.poll);
  pollRef.current = options.poll;
  const pollMs = options.pollMs ?? 2500;

  useEffect(() => {
    setData(null);
    setLoading(true);
  }, [path]);

  useEffect(() => {
    if (!path) return;
    let timer: number | undefined;
    let alive = true;
    const tick = async () => {
      try {
        const value = await api<T>(path);
        if (!alive) return;
        setData(value);
        setError(null);
        if (pollRef.current?.(value)) timer = window.setTimeout(tick, pollMs);
      } catch (err) {
        if (alive) setError(err instanceof Error ? err.message : "Couldn't load this.");
      } finally {
        if (alive) setLoading(false);
      }
    };
    void tick();
    return () => {
      alive = false;
      window.clearTimeout(timer);
    };
  }, [path, pollMs, nonce]);

  const reload = useCallback(() => setNonce((n) => n + 1), []);
  return { data, error, loading, reload, setData };
}
