import {FILES} from './files.gen.js';
const SEC = {'x-content-type-options': 'nosniff', 'referrer-policy': 'strict-origin-when-cross-origin', 'x-frame-options': 'DENY'};
export default {
  fetch(req) {
    const url = new URL(req.url);
    let path = url.pathname === '/' ? '/index.html' : url.pathname;
    const f = Object.hasOwn(FILES, path) ? FILES[path] : null;
    if (!f || !['GET', 'HEAD'].includes(req.method)) return new Response('Not found', {status: 404, headers: SEC});
    const body = Uint8Array.from(atob(f.b64), (c) => c.charCodeAt(0));
    return new Response(req.method === 'HEAD' ? null : body, {headers: {...SEC, 'content-type': f.type, 'cache-control': path.startsWith('/assets/') ? 'public, max-age=604800' : 'public, max-age=300'}});
  },
};
