workbox.skipWaiting();
workbox.clientsClaim();

// Cache map tiles
workbox.routing.registerRoute(
  new RegExp('https://(?:a|b|c).tile.openstreetmap.org/.*\.png'),
  workbox.strategies.cacheFirst({
    cacheName: 'tile-cache',
    plugins: [
      new workbox.expiration.Plugin({
        maxEntries: 20000,
        maxAgeSeconds: 7 * 24 * 60 * 60,
        purgeOnQuotaError: true,
      })
    ],
  })
);

workbox.precaching.precacheAndRoute(self.__precacheManifest);