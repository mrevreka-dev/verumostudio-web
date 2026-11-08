/* Verumo Studio: cookieless, first-party page counter.
   Sends only: page path, external referrer host, utm_source, a coarse screen class.
   No cookies, no localStorage, no IDs, no fingerprinting. Honors DNT / GPC. */
(function () {
  var s = document.currentScript;
  var url = s && s.getAttribute('data-endpoint');
  if (!url) return;
  if (navigator.doNotTrack === '1' || navigator.globalPrivacyControl) return;
  var h = location.hostname;
  if (h === 'localhost' || h === '127.0.0.1' || location.protocol === 'file:') return;
  var ref = '';
  try {
    var r = new URL(document.referrer);
    if (r.hostname && r.hostname !== h) ref = r.hostname.replace(/^www\./, '');
  } catch (e) {}
  var utm = '';
  try { utm = (new URLSearchParams(location.search).get('utm_source') || '').slice(0, 40); } catch (e) {}
  var w = window.innerWidth || 0;
  var body = JSON.stringify({
    site: 'verumostudio',
    p: location.pathname.slice(0, 200),
    r: ref.slice(0, 100),
    u: utm,
    d: w < 600 ? 'm' : w < 1024 ? 't' : 'd'
  });
  try {
    if (navigator.sendBeacon) navigator.sendBeacon(url, new Blob([body], { type: 'text/plain' }));
    else fetch(url, { method: 'POST', body: body, keepalive: true, mode: 'no-cors' });
  } catch (e) {}
})();
