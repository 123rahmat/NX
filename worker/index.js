// Cloudflare Worker "nx": serves the static site and sends the contact form
// straight to Gmail over SMTP (smtp.gmail.com:465, TLS) with a Gmail App Password.
// Secrets (Cloudflare dashboard -> nx -> Settings -> Variables and Secrets):
//   GMAIL_USER          your Gmail address (messages are sent from and to it)
//   GMAIL_APP_PASSWORD  16-character App Password from myaccount.google.com/apppasswords
import { connect } from 'cloudflare:sockets';

const MAX = { name: 100, contact: 150, city: 80, service: 100, budget: 80, message: 5000 };
const JSON_HDR = { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' };
const reply = (status, body) => new Response(JSON.stringify(body), { status, headers: JSON_HDR });

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname !== '/api/contact') return env.ASSETS.fetch(request);
    if (request.method !== 'POST') return reply(405, { success: false, message: 'POST only' });
    // Same-site posts only.
    const origin = request.headers.get('Origin');
    if (origin && new URL(origin).host !== url.host) return reply(403, { success: false, message: 'Forbidden' });
    if (!env.GMAIL_USER || !env.GMAIL_APP_PASSWORD) return reply(503, { success: false, message: 'Mail not configured' });
    if (Number(request.headers.get('Content-Length') || 0) > 20000) return reply(413, { success: false, message: 'Too large' });

    let d;
    try { d = await request.json(); } catch { return reply(400, { success: false, message: 'Bad request' }); }
    if (d._honey) return reply(200, { success: true }); // bot
    const f = {};
    for (const k of Object.keys(MAX)) f[k] = String(d[k] ?? '').replace(/\r/g, '').trim().slice(0, MAX[k]);
    if (f.name.length < 2 || f.contact.length < 2 || f.message.length < 10) return reply(400, { success: false, message: 'Missing fields' });

    const oneLine = (s) => s.replace(/\n+/g, ' ');
    const subject = 'New enquiry: ' + oneLine(f.name) + (f.service ? ' - ' + oneLine(f.service) : '');
    const text = [
      'Name: ' + f.name, 'Phone / email: ' + f.contact, 'City: ' + (f.city || '-'),
      'Service: ' + (f.service || '-'), 'Budget: ' + (f.budget || '-'), '', 'Message:', f.message, '',
      'Sent from the website contact form.'
    ].join('\n');
    const replyTo = /^[^\s@<>"]+@[^\s@<>"]+\.[^\s@<>"]{2,}$/.test(f.contact) ? f.contact : '';

    try {
      await sendMail(env, { subject, text, replyTo });
      return reply(200, { success: true });
    } catch (e) {
      console.log('smtp error', e && e.message);
      return reply(502, { success: false, message: 'Could not send' });
    }
  }
};

const b64 = (s) => { let bin = ''; for (const b of new TextEncoder().encode(s)) bin += String.fromCharCode(b); return btoa(bin); };

async function sendMail(env, { subject, text, replyTo }) {
  const user = env.GMAIL_USER, pass = env.GMAIL_APP_PASSWORD;
  // SMTP_TEST_PORT is only for local testing against a fake plain-text server.
  const sock = env.SMTP_TEST_PORT
    ? connect({ hostname: '127.0.0.1', port: Number(env.SMTP_TEST_PORT) })
    : connect({ hostname: 'smtp.gmail.com', port: 465 }, { secureTransport: 'on' });
  const w = sock.writable.getWriter(), r = sock.readable.getReader(), dec = new TextDecoder();
  let buf = '';
  async function read(expect) {
    // An SMTP reply ends at a line "NNN " (multi-line replies use "NNN-").
    for (;;) {
      const lines = buf.split('\r\n');
      for (let i = 0; i < lines.length - 1; i++) {
        if (/^\d{3} /.test(lines[i])) {
          buf = lines.slice(i + 1).join('\r\n');
          if (!lines[i].startsWith(String(expect))) throw new Error(lines[i]);
          return;
        }
      }
      const { value, done } = await r.read();
      if (done) throw new Error('connection closed');
      buf += dec.decode(value, { stream: true });
    }
  }
  const send = (s) => w.write(new TextEncoder().encode(s + '\r\n'));
  const timer = setTimeout(() => sock.close(), 15000);
  try {
    await read(220);
    await send('EHLO linqore'); await read(250);
    await send('AUTH LOGIN'); await read(334);
    await send(b64(user)); await read(334);
    await send(b64(pass.replace(/\s+/g, ''))); await read(235);
    await send('MAIL FROM:<' + user + '>'); await read(250);
    await send('RCPT TO:<' + user + '>'); await read(250);
    await send('DATA'); await read(354);
    const body = b64(text).replace(/.{1,76}/g, '$&\r\n');
    await send([
      'From: "Linqore website" <' + user + '>', 'To: <' + user + '>',
      replyTo ? 'Reply-To: <' + replyTo + '>' : null,
      'Subject: =?UTF-8?B?' + b64(subject) + '?=', 'Date: ' + new Date().toUTCString(),
      'Message-ID: <' + crypto.randomUUID() + '@linqore.site>',
      'MIME-Version: 1.0', 'Content-Type: text/plain; charset=UTF-8', 'Content-Transfer-Encoding: base64',
      '', body + '.'
    ].filter((x) => x !== null).join('\r\n'));
    await read(250);
    await send('QUIT');
  } finally {
    clearTimeout(timer);
    try { await sock.close(); } catch {}
  }
}
