/* SirisLearn service worker: works offline and shows reminders.
 *
 * - The app shell (index.html and the hashed /assets/ files) is cached, so the
 *   app opens without a connection.
 * - Reading data (summary, courses, lessons, history, awards) is network-first
 *   with the last good copy as the fallback, so lessons you've opened before
 *   still open offline. Quizzes and everything that changes data need the
 *   network.
 * - Push messages from the server become notifications; tapping one opens the
 *   app at its link.
 */
const SHELL = "sirislearn-shell-v1";
const DATA = "sirislearn-data-v1";
const CACHED_API = /^\/api\/(summary|courses(\/[^/]+)?|lessons\/[^/]+|history|achievements|review|settings|suggestions)$/;

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(SHELL).then((c) => c.addAll(["/", "/manifest.webmanifest", "/siris-icon.png", "/siris-mark.svg"])));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => ![SHELL, DATA].includes(k)).map((k) => caches.delete(k)))).then(() => self.clients.claim()),
  );
});

self.addEventListener("message", (event) => {
  if (event.data === "sign-out") event.waitUntil(caches.delete(DATA));
});

async function networkFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  try {
    const response = await fetch(request);
    if (response.ok) cache.put(request, response.clone());
    return response;
  } catch (err) {
    const hit = await cache.match(request, { ignoreVary: true });
    if (hit) return hit;
    throw err;
  }
}

async function cacheFirst(request) {
  const cache = await caches.open(SHELL);
  const hit = await cache.match(request);
  if (hit) return hit;
  const response = await fetch(request);
  if (response.ok) cache.put(request, response.clone());
  return response;
}

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET") return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.startsWith("/assets/")) {
    event.respondWith(cacheFirst(request));
  } else if (CACHED_API.test(url.pathname)) {
    event.respondWith(networkFirst(request, DATA));
  } else if (request.mode === "navigate") {
    event.respondWith(fetch(request).catch(() => caches.match("/", { cacheName: SHELL })));
  }
});

self.addEventListener("push", (event) => {
  let data = {};
  try {
    data = event.data ? event.data.json() : {};
  } catch (err) {
    data = { title: "SirisLearn", body: event.data ? event.data.text() : "" };
  }
  event.waitUntil(
    self.registration.showNotification(data.title || "SirisLearn", {
      body: data.body || "",
      tag: data.tag || "sirislearn",
      icon: "/siris-icon.png",
      badge: "/siris-icon.png",
      data: { url: data.url || "/" },
    }),
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  const url = (event.notification.data && event.notification.data.url) || "/";
  event.waitUntil(
    self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((windows) => {
      for (const win of windows) {
        if ("focus" in win) {
          win.navigate(url);
          return win.focus();
        }
      }
      return self.clients.openWindow(url);
    }),
  );
});
