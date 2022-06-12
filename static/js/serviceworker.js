var staticCacheName = 'djangopwa-v1';

self.oninstall = function (evt) {
    evt.waitUntil(caches.open(staticCacheName).then(function (cache) {
        return Promise.all(['/', '/home'].map(function (url) {
            return fetch(new Request(url, { redirect: 'manual' })).then(function (res) {
                return cache.put(url, res);
            });
        }));
    }));
};
self.onfetch = function (evt) {
    var url = new URL(evt.request.url);
    if (url.pathname != '/' && url.pathname != '/home') return;
    evt.respondWith(caches.match(evt.request, { cacheName: staticCacheName }));
};
