"""Build the Linqore static site.

    python3 scripts/build_site.py

Reads scripts/content.json and writes every page, sitemap.xml and robots.txt
into the repository root. Shared look and behaviour live in assets/site.css
and assets/site.js. Edit content in content.json or in this file, then rerun.
"""
import hashlib, html, json, pathlib
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parent.parent
A = json.loads((ROOT / "scripts" / "content.json").read_text())
BASE = "https://123rahmat.github.io/NX/"
C = A["contact"]
PHONE, TEL = C["phone"], C["phone"].replace(" ", "")
# Form destination. Replace the email with the FormSubmit alias once activated, to keep the address out of the page.
FORM_TO = C["email"]
WA = "https://wa.me/" + C["wa"] + "?text=" + quote("Hi Linqore, I'd like to discuss a project.")
e = html.escape


def lc(t):
    """Lower-case a label for use mid-sentence, keeping acronyms such as IoT."""
    return " ".join(w if any(ch.isupper() for ch in w[1:]) else w.lower() for w in t.split())

# Content hashes for cache-busting: a changed file gets a new URL, so browsers and CDNs never serve a stale copy.
def _v(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:10]


V = {k: _v(k) for k in ("assets/site.css", "assets/site.js", "assets/logo.svg", "assets/apple-touch-icon.png")}

CSP = ("default-src 'none'; script-src 'self'; style-src 'self'; font-src 'self'; img-src 'self' data:; "
       "connect-src https://formsubmit.co; base-uri 'none'; form-action 'none'; object-src 'none'; "
       "manifest-src 'self'; upgrade-insecure-requests")

# ---------------------------------------------------------------- icons
def I(paths, extra=""):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}>{paths}</svg>')

ICON = {
    "web": I('<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M3 8h18M7 21h10M12 18v3"/>'),
    "chip": I('<rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M10 10h4v4h-4zM9 3v4M15 3v4M9 17v4M15 17v4M3 9h4M3 15h4M17 9h4M17 15h4"/>'),
    "cloud": I('<path d="M7 18a4.5 4.5 0 0 1-.5-9 6 6 0 0 1 11.5 1.5A3.75 3.75 0 0 1 17.5 18z"/><path d="M12 12v6M9.5 14.5 12 12l2.5 2.5"/>'),
    "phone": I('<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>'),
    "sim": I('<path d="M3 17l4-5 4 3 5-7 5 6"/><path d="M3 21h18"/>'),
    "tool": I('<path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8-1.3-1.3a4 4 0 0 0-5-5z"/><path d="m10 18-4 4-4-4 4-4"/>'),
    "check": I('<path d="m5 12.5 4.5 4.5L19 7.5"/>'),
    "arr": I('<path d="M5 12h14M13 6l6 6-6 6"/>', ' class="arr"'),
    "down": I('<path d="m6 9 6 6 6-6"/>'),
    "mail": I('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 7 8.5-7"/>'),
    "call": I('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>'),
    "pin": I('<path d="M12 21s-7-6.1-7-11.5a7 7 0 0 1 14 0C19 14.9 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>'),
    "shield": I('<path d="M12 3 5 6v6c0 4.5 3 7.7 7 9 4-1.3 7-4.5 7-9V6z"/><path d="m9 12 2 2 4-4"/>'),
    "layers": I('<path d="m12 3 9 5-9 5-9-5z"/><path d="m3 13 9 5 9-5"/>'),
    "doc": I('<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>'),
    "wave": I('<path d="M2 12h3l3-7 4 14 3-9 2 2h5"/>'),
    "wifi": I('<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19.5" r="1"/>'),
    "bt": I('<path d="m7 7 10 10-5 4V3l5 4L7 17"/>'),
    "cable": I('<path d="M5 3v6a3 3 0 0 0 3 3h8a3 3 0 0 1 3 3v6"/><path d="M3 3h4M17 21h4"/>'),
    "signal": I('<path d="M4 20v-3M9 20v-7M14 20V9M19 20V4"/>'),
}
WAICON = ('<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.7c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.7 10.7 0 1 1 16 26.7zm5.9-8c-.3-.2-1.9-1-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.8 8.8 0 0 1-4.4-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6 0-.9.4s-1.2 1.1-1.2 2.7 1.2 3.2 1.4 3.4 2.4 3.6 5.7 5c2.1.9 3 1 4 .8.7-.1 1.9-.8 2.2-1.5s.3-1.4.2-1.5-.3-.2-.6-.4z"/></svg>')
LOGO = '<svg viewBox="0 0 64 64" aria-hidden="true"><g transform="translate(0.00 0.00) scale(1.0000)"><rect width="64" height="64" rx="16" fill="#1D5FD6"/><g transform="translate(8 8) scale(.75)"><rect x="20.5" y="20.5" width="23" height="23" rx="6.5" fill="none" stroke="#FFFFFF" stroke-width="5.5" transform="rotate(45 32 32)"/><circle cx="32" cy="32" r="5" fill="#FFFFFF"/><path d="M32 14V8.6" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" transform="rotate(0 32 32)"/><circle cx="32" cy="6.4" r="4" fill="#22D3EE" transform="rotate(0 32 32)"/><path d="M32 14V8.6" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" transform="rotate(90 32 32)"/><circle cx="32" cy="6.4" r="4" fill="#22D3EE" transform="rotate(90 32 32)"/><path d="M32 14V8.6" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" transform="rotate(180 32 32)"/><circle cx="32" cy="6.4" r="4" fill="#22D3EE" transform="rotate(180 32 32)"/><path d="M32 14V8.6" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" transform="rotate(270 32 32)"/><circle cx="32" cy="6.4" r="4" fill="#22D3EE" transform="rotate(270 32 32)"/></g></g></svg>'
FAVICON = "data:image/svg+xml," + quote('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><g transform="translate(0.00 0.00) scale(1.0000)"><rect width="64" height="64" rx="16" fill="#1D5FD6"/><g transform="translate(8 8) scale(.75)"><rect x="20.5" y="20.5" width="23" height="23" rx="6.5" fill="none" stroke="#FFFFFF" stroke-width="5.5" transform="rotate(45 32 32)"/><circle cx="32" cy="32" r="5" fill="#FFFFFF"/><path d="M32 14V8.6" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" transform="rotate(0 32 32)"/><circle cx="32" cy="6.4" r="4" fill="#22D3EE" transform="rotate(0 32 32)"/><path d="M32 14V8.6" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" transform="rotate(90 32 32)"/><circle cx="32" cy="6.4" r="4" fill="#22D3EE" transform="rotate(90 32 32)"/><path d="M32 14V8.6" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" transform="rotate(180 32 32)"/><circle cx="32" cy="6.4" r="4" fill="#22D3EE" transform="rotate(180 32 32)"/><path d="M32 14V8.6" stroke="#FFFFFF" stroke-width="3.4" stroke-linecap="round" transform="rotate(270 32 32)"/><circle cx="32" cy="6.4" r="4" fill="#22D3EE" transform="rotate(270 32 32)"/></g></g></svg>')

# ---------------------------------------------------------------- services
SERVICES = [
 {"slug": "web-development", "icon": "web", "nav": "Web development", "short": "Websites, portals and admin panels",
  "title": "Web Development Company in Islamabad | Linqore",
  "desc": "Linqore builds fast, secure company websites, customer portals and admin panels. Clear scope and quotation before work starts.",
  "h1": "Websites, portals and admin panels that work as hard as you do",
  "intro": "We build company websites, customer portals and admin systems that load fast, stay secure and are easy for your team to manage. Every project starts with a written scope and quotation.",
  "build": [("Company websites", "Fast, mobile-first sites that explain what you do and turn visitors into enquiries."),
            ("Customer portals", "Secure areas where customers log in, track orders or view their data."),
            ("Admin panels", "Internal tools to manage records, users and content without technical help."),
            ("IoT web dashboards", "Live charts, history and alerts for connected devices and machines.")],
  "tech": ["HTML and CSS", "JavaScript", "REST APIs", "Databases", "HTTPS", "Responsive design"],
  "projects": ["fingerprint", "power"],
  "faq": [("How long does a company website take?", "A typical company website takes two to four weeks, depending on the number of pages and how quickly content is ready. You get a timeline with your quotation."),
          ("Will my website work on mobile phones?", "Yes. Every site we build is designed for phones first and tested on phone, tablet and desktop screens."),
          ("Can you connect my website to devices or machines?", "Yes. We build web dashboards that show live data from sensors and devices and send commands back to them.")]},
 {"slug": "embedded-systems", "icon": "chip", "nav": "Embedded systems", "short": "Firmware for ESP32, STM32 and Arduino",
  "title": "Embedded Systems and Firmware Development | Linqore",
  "desc": "Embedded firmware for ESP32, STM32 and Arduino: sensors, motor and relay control, low power and fault handling. Simulation before hardware.",
  "h1": "Embedded systems and firmware, tested before the hardware exists",
  "intro": "We write the code that runs on the device: reading sensors, controlling motors and relays, saving power and handling faults safely. We model the system first in MATLAB/Simulink or Proteus, so mistakes show up before parts are bought.",
  "build": [("Microcontroller firmware", "Reliable C and C++ firmware for ESP32, STM32 and Arduino boards."),
            ("Sensor and control systems", "Reading sensors, driving relays and motors, and reacting to faults."),
            ("Low-power devices", "Battery-friendly designs with sleep modes and efficient scheduling."),
            ("Simulation and testing", "Run the firmware against a model of the machine, tank or building first.")],
  "tech": ["ESP32", "STM32 (ARM Cortex-M)", "Arduino", "Raspberry Pi", "C and C++", "MATLAB/Simulink", "Proteus", "UART, SPI, I2C", "RS-485, CAN"],
  "projects": ["plug", "solar", "health"],
  "faq": [("Which microcontrollers do you work with?", "Mainly ESP32, STM32 (ARM Cortex-M), Arduino and Raspberry Pi. Tell us what you already use and we work with it."),
          ("Do I need hardware before we start?", "No. We can simulate the system first and advise on suitable boards and sensors before you buy anything."),
          ("Can you fix or extend existing firmware?", "Yes. We can review existing code, fix faults and add features.")]},
 {"slug": "iot-solutions", "icon": "cloud", "nav": "IoT solutions", "short": "Devices, connectivity and cloud",
  "title": "IoT Solutions and Cloud Connectivity | Linqore",
  "desc": "End-to-end IoT systems: devices, Wi-Fi, GSM and Bluetooth connectivity, MQTT and HTTP cloud, remote control, alerts and over-the-air updates.",
  "h1": "IoT solutions that connect devices, data and people",
  "intro": "We connect devices securely to a server, with data storage, remote commands, alerts and over-the-air updates, all designed as one system. We choose the link that suits the site and the protocol your systems already speak.",
  "build": [("Remote monitoring", "Live readings from sensors, meters and machines, viewable from anywhere."),
            ("Remote control", "Switch relays, change settings and send commands from a dashboard or phone."),
            ("Alerts", "SMS, app or email alerts when a value crosses a limit or a device goes offline."),
            ("Over-the-air updates", "Update device firmware remotely without visiting the site.")],
  "tech": ["Wi-Fi", "GSM and LTE", "Bluetooth (BLE)", "MQTT", "HTTP/HTTPS", "TCP and UDP", "WebSocket", "Modbus", "CoAP", "TLS"],
  "projects": ["power", "fingerprint", "health"],
  "faq": [("What if the site has no Wi-Fi?", "We use GSM or LTE mobile data, or SMS alerts, for remote sites without Wi-Fi."),
          ("Is the data secure?", "Data in transit is encrypted with TLS, and devices authenticate to the server."),
          ("Can you connect to systems we already use?", "Yes. We integrate with existing servers, industrial equipment over Modbus and RS-485, and third-party APIs.")]},
 {"slug": "mobile-apps", "icon": "phone", "nav": "Mobile apps and dashboards", "short": "Android, iOS and web dashboards",
  "title": "Mobile App and Dashboard Development | Linqore",
  "desc": "Android and iOS apps and web dashboards that show live data, send commands and raise alerts, built for the people who use them every day.",
  "h1": "Mobile apps and dashboards your team will actually use",
  "intro": "We build screens that show what your system is doing, send commands and raise alerts, designed for the people who use them every day. Apps are designed together with the firmware and connection, so the whole system works as one.",
  "build": [("Android and iOS apps", "Control devices, view live data and receive alerts on a phone."),
            ("Web dashboards", "Charts, history and reports in the browser for operators and managers."),
            ("Device setup apps", "Pair and configure devices over Bluetooth or Wi-Fi from a phone."),
            ("User and access management", "Enrol and remove users and control who can see and do what.")],
  "tech": ["Android", "iOS", "Web dashboard", "REST APIs", "MQTT", "WebSocket", "Bluetooth setup", "Push alerts"],
  "projects": ["rfid", "plug", "fingerprint"],
  "faq": [("Do you build for both Android and iPhone?", "Yes. We build apps for Android and iOS, and web dashboards that work in any browser."),
          ("Can the app control my device?", "Yes. Apps can send commands, change schedules and settings, and show live status."),
          ("Can I get a dashboard without a mobile app?", "Yes. A web dashboard works on phones and computers without installing anything.")]},
]
SVC_LINK = {"Websites and web platforms": "web-development", "Embedded firmware": "embedded-systems",
            "Connectivity and cloud": "iot-solutions", "Dashboards and mobile apps": "mobile-apps",
            "Simulation and testing": "embedded-systems", "Integration and support": "iot-solutions"}
PROJ = {p["v"]: p for p in A["projects"]["items"]}

# ---------------------------------------------------------------- project visuals (inline animated SVG)
def pv(v):
    s = {
     "fingerprint": '<g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" opacity=".9" transform="translate(200 125)">' +
        "".join(f'<path d="M{-r} 10a{r} {r} 0 0 1 {2*r} 0" opacity="{1-i*.12:.2f}"/>' for i, r in enumerate([12, 22, 32, 42, 52, 62])) +
        '<path d="M-62 10v18M62 10v14M-42 10v26M42 10v24M-22 10v30M22 10v28M0 0v44"/>'
        '<rect class="a-scan" x="-75" y="-60" width="150" height="3" rx="1.5" fill="#22D3EE" stroke="none" opacity=".8"/></g>',
     "rfid": '<g transform="translate(200 125)"><rect x="-80" y="-48" width="110" height="72" rx="10" fill="rgba(143,180,255,.1)" stroke="currentColor" stroke-width="2"/>'
        '<rect x="-64" y="-30" width="26" height="20" rx="3" fill="none" stroke="#22D3EE" stroke-width="2"/><path d="M-64 6h70M-64 14h44" stroke="currentColor" stroke-width="2" opacity=".6"/>'
        '<g fill="none" stroke="#22D3EE" stroke-width="2.5" stroke-linecap="round"><path class="a-pulse" d="M48 -18a26 26 0 0 1 0 36"/><path class="a-pulse" d="M60 -30a42 42 0 0 1 0 60" opacity=".7"/><path class="a-pulse" d="M72 -42a58 58 0 0 1 0 84" opacity=".45"/></g></g>',
     "plug": '<g transform="translate(200 125)" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="-90" y="-44" width="70" height="88" rx="16"/><path d="M-65 -14v14M-45 -14v14"/><circle cx="-55" cy="24" r="5"/>'
        '<circle cx="50" cy="0" r="40" stroke="#22D3EE"/><path d="M50 -24v24l16 10" stroke="#22D3EE"/><path class="a-dash" d="M-20 0h50"/></g>',
     "power": '<g fill="none" stroke-width="2.5" stroke-linecap="round"><path d="M20 160h360" stroke="rgba(143,180,255,.2)"/>'
        '<path class="a-draw" stroke="#22D3EE" d="M20 125c30-60 50-60 80 0s50 60 80 0 50-60 80 0 50 60 80 0 40-50 40-50"/>'
        '<path class="a-draw" stroke="currentColor" opacity=".6" d="M20 135c30-40 50-40 80 0s50 40 80 0 50-40 80 0 50 40 80 0 40-30 40-30"/></g>'
        '<g font-family="IBM Plex Mono,monospace" font-size="13" fill="currentColor" text-anchor="end"><text x="376" y="36">V 229.8</text><text x="376" y="56" fill="#22D3EE">A 4.12</text><text x="376" y="76" class="a-blink">MQTT</text></g>',
     "solar": '<g transform="translate(70 70) skewX(-12)" fill="rgba(143,180,255,.08)" stroke="currentColor" stroke-width="1.5">' +
        "".join(f'<rect x="{c*36}" y="{r*28}" width="32" height="24" rx="2"/>' for r in range(4) for c in range(4)) +
        '<rect x="72" y="28" width="32" height="24" rx="2" fill="rgba(217,119,6,.35)" stroke="#F59E0B" class="a-pulse"/></g>'
        '<g fill="none" stroke-width="2.5"><path d="M250 190V70M250 190h120" stroke="rgba(143,180,255,.3)"/><path class="a-draw" stroke="#22D3EE" d="M252 90h70c20 0 30 10 38 40l8 58"/></g><circle cx="330" cy="104" r="5" fill="#22D3EE" class="a-pulse"/>',
     "vision": '<g transform="translate(200 128)"><g fill="currentColor" opacity=".55"><circle cx="-60" cy="-38" r="14"/><path d="M-82 40c0-38 8-58 22-58s22 20 22 58z"/><circle cx="50" cy="-30" r="12"/><path d="M31 40c0-32 7-50 19-50s19 18 19 50z"/></g>'
        '<g fill="none" stroke="#22D3EE" stroke-width="2"><rect class="a-pulse" x="-92" y="-62" width="64" height="108" rx="3"/><rect class="a-pulse" x="22" y="-52" width="56" height="98" rx="3"/></g>'
        '<g font-family="IBM Plex Mono,monospace" font-size="11" fill="#22D3EE"><text x="-92" y="-68">person 0.97</text><text x="22" y="-58">person 0.94</text></g></g>',
     "health": '<g fill="none" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 130h360" stroke="rgba(143,180,255,.15)"/>'
        '<path class="a-draw" stroke="#22D3EE" d="M20 130h80l14-36 20 82 18-70 12 24h56l14-36 20 82 18-70 12 24h96"/></g>'
        '<path class="a-pulse" fill="#F87171" d="M330 52c-6-10-24-8-24 6 0 12 24 26 24 26s24-14 24-26c0-14-18-16-24-6z"/>'
        '<g font-family="IBM Plex Mono,monospace" font-size="13" fill="currentColor"><text x="24" y="82">HR 76</text><text x="24" y="102">SpO2 98%</text></g>',
    }[v]
    return f'<svg viewBox="0 0 400 250" aria-hidden="true" preserveAspectRatio="xMidYMid meet">{s}</svg>'


# ---------------------------------------------------------------- page arts (inner hero illustrations)
def art(kind):
    common = '<svg viewBox="0 0 320 240" fill="none" aria-hidden="true">'
    body = {
     "services": '<g stroke="currentColor" stroke-width="1.6"><rect x="20" y="30" width="120" height="80" rx="10"/><rect x="180" y="30" width="120" height="80" rx="10"/><rect x="100" y="140" width="120" height="80" rx="10" stroke="#22D3EE"/><path class="a-dash" d="M80 110v30h40M240 110v30h-40"/></g>',
     "projects": '<g stroke="currentColor" stroke-width="1.6"><rect x="30" y="40" width="260" height="160" rx="14"/><path d="M30 80h260"/><circle cx="52" cy="60" r="5"/><circle cx="70" cy="60" r="5"/><path class="a-draw" stroke="#22D3EE" stroke-width="2.4" d="M50 170l40-30 30 18 40-50 40 26 50-40"/></g>',
     "about": '<g stroke="currentColor" stroke-width="1.6"><circle cx="160" cy="120" r="80"/><circle cx="160" cy="120" r="50" stroke="#22D3EE"/><circle cx="160" cy="120" r="8" fill="#22D3EE"/><circle cx="240" cy="120" r="6" fill="currentColor"/><circle cx="104" cy="64" r="6" fill="currentColor"/><circle cx="110" cy="166" r="6" fill="currentColor"/></g>',
     "contact": '<g stroke="currentColor" stroke-width="1.6"><rect x="40" y="60" width="240" height="140" rx="14"/><path d="m44 66 116 80 116-80" stroke="#22D3EE"/><circle class="a-pulse" cx="270" cy="60" r="16" fill="#0F7A43" stroke="none"/></g>',
     "web-development": '<g stroke="currentColor" stroke-width="1.6"><rect x="20" y="36" width="280" height="176" rx="12"/><path d="M20 68h280"/><circle cx="40" cy="52" r="5"/><circle cx="58" cy="52" r="5"/><circle cx="76" cy="52" r="5"/><rect x="40" y="88" width="120" height="14" rx="4" fill="rgba(143,180,255,.25)" stroke="none"/><rect x="40" y="112" width="90" height="8" rx="4" fill="rgba(143,180,255,.15)" stroke="none"/><rect class="a-pulse" x="40" y="140" width="70" height="26" rx="6" stroke="#22D3EE"/><rect x="180" y="88" width="100" height="100" rx="8" stroke="#22D3EE"/><path class="a-draw" stroke="#22D3EE" stroke-width="2.2" d="M192 170l20-24 18 12 26-34"/></g>',
     "embedded-systems": '<g stroke="currentColor" stroke-width="1.6"><rect x="100" y="60" width="120" height="120" rx="12"/><rect x="128" y="88" width="64" height="64" rx="6" stroke="#22D3EE"/>' + "".join(f'<path d="M{120+i*20} 60V36M{120+i*20} 180v24M100 {80+i*20}H76M220 {80+i*20}h24"/>' for i in range(5)) + '<circle class="a-blink" cx="160" cy="120" r="8" fill="#22D3EE" stroke="none"/><path class="a-dash" d="M76 100H30M244 140h46" stroke="#22D3EE"/></g>',
     "iot-solutions": '<g stroke="currentColor" stroke-width="1.6"><path d="M118 92a34 34 0 0 1 66-10 26 26 0 0 1 18 50H122a22 22 0 0 1-4-40z" stroke="#22D3EE"/><rect x="34" y="180" width="44" height="36" rx="6"/><rect x="138" y="190" width="44" height="36" rx="6"/><rect x="242" y="180" width="44" height="36" rx="6"/><path class="a-dash" d="M56 180l70-48M160 190v-58M264 180l-70-48"/><circle class="a-ring" cx="160" cy="108" r="10" stroke="#22D3EE"/></g>',
     "mobile-apps": '<g stroke="currentColor" stroke-width="1.6"><rect x="104" y="20" width="112" height="204" rx="18"/><path d="M146 34h28"/><rect x="118" y="54" width="84" height="54" rx="6" stroke="#22D3EE"/><path class="a-draw" stroke="#22D3EE" stroke-width="2.2" d="M124 98l16-14 14 8 20-22 22 12"/><rect x="118" y="120" width="84" height="22" rx="6"/><rect x="118" y="150" width="84" height="22" rx="6"/><circle class="a-pulse" cx="190" cy="131" r="5" fill="#16A34A" stroke="none"/><circle cx="190" cy="161" r="5" fill="#D97706" stroke="none"/><rect x="132" y="190" width="56" height="18" rx="9" fill="#1D5FD6" stroke="none"/></g>',
     "legal": '<g stroke="currentColor" stroke-width="1.6"><path d="M160 30 90 58v56c0 44 30 76 70 92 40-16 70-48 70-92V58z"/><path d="m130 118 22 22 40-44" stroke="#22D3EE" stroke-width="2.4"/></g>',
    }[kind]
    return common + body + "</svg>"


# ---------------------------------------------------------------- shared shell
def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"

ORG = {"@type": "ProfessionalService", "@id": BASE + "#org", "name": "Linqore", "url": BASE,
       "image": BASE + "og-image.png", "logo": BASE + "og-image.png", "telephone": PHONE,
       "description": "Engineering and software for connected products: embedded systems, IoT platforms, web applications and mobile apps.",
       "address": {"@type": "PostalAddress", "addressLocality": C["city"], "addressCountry": "PK"},
       "areaServed": {"@type": "Country", "name": "Pakistan"}, "currenciesAccepted": "PKR",
       "contactPoint": {"@type": "ContactPoint", "telephone": PHONE, "contactType": "customer service", "availableLanguage": ["English", "Urdu"]}}

def crumbs_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(trail)]}

def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def page(path, title, desc, body, schemas=(), cur=""):
    """path: '' for home or 'slug/' for sub pages."""
    rel = "../" * path.count("/")
    url = BASE + path
    def nav_a(href, label, key):
        return f'<a href="{rel}{href}"{" aria-current=\"page\"" if cur == key else ""}>{label}</a>'
    dd_items = "".join(
        f'<a href="{rel}{s["slug"]}/"{" aria-current=\"page\"" if cur == s["slug"] else ""}><span class="ico">{ICON[s["icon"]]}</span><span><b>{e(s["nav"])}</b><small>{e(s["short"])}</small></span></a>'
        for s in SERVICES)
    svc_cur = cur == "services" or cur in {s["slug"] for s in SERVICES}
    header = f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap">
<a class="brand" href="{rel or './'}" ><img src="{rel}assets/logo.svg?v={V['assets/logo.svg']}" alt="Linqore" width="122" height="32"></a>
<button class="burger" type="button" aria-controls="nav" aria-expanded="false" aria-label="Menu"><span></span></button>
<nav class="nav" id="nav" aria-label="Main">
{nav_a("", "Home", "home") if path else '<a href="./" aria-current="page">Home</a>'}
<div class="dd{" cur" if svc_cur else ""}"><button type="button" aria-expanded="false" aria-haspopup="true">Services {ICON["down"]}</button>
<div class="dd-menu">{dd_items}<a class="all" href="{rel}services/">All services {ICON["arr"]}</a></div></div>
{nav_a("projects/", "Projects", "projects")}
{nav_a("about/", "About", "about")}
{nav_a("contact/", "Contact", "contact")}
<a class="btn cta" href="{rel}contact/">Get a quote</a>
</nav></div></header>'''
    footer = f'''<footer class="ftr"><div class="wrap">
<div class="cols">
<div><a class="brand" href="{rel or './'}"><img src="{rel}assets/logo.svg?v={V['assets/logo.svg']}" alt="Linqore" width="122" height="32"></a><p>Engineering and software for connected products: embedded systems, IoT platforms, web applications and mobile apps.</p></div>
<div><h2 class="fh">Services</h2><ul>{"".join(f'<li><a href="{rel}{s["slug"]}/">{e(s["nav"])}</a></li>' for s in SERVICES)}</ul></div>
<div><h2 class="fh">Company</h2><ul><li><a href="{rel}projects/">Projects</a></li><li><a href="{rel}about/">About us</a></li><li><a href="{rel}contact/">Contact</a></li><li><a href="{rel}privacy/">Privacy policy</a></li><li><a href="{rel}terms/">Terms of use</a></li></ul></div>
<div><h2 class="fh">Contact</h2><ul><li><a href="tel:{TEL}">{e(PHONE)}</a></li><li><a href="{WA}" target="_blank" rel="noopener noreferrer">WhatsApp</a></li><li><a href="{rel}contact/">Send a request</a></li><li>{e(C["city"])}</li></ul></div>
</div>
<div class="bot"><span>&copy; <span id="yr">2026</span> Linqore. All rights reserved.</span><span>Digital solutions &middot; {e(C["city"])}</span></div>
</div></footer>
<a class="wa-fab" href="{WA}" target="_blank" rel="noopener noreferrer" aria-label="Chat with us on WhatsApp">{WAICON}<span>WhatsApp</span></a>'''
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="{CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0B1426">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="website"><meta property="og:site_name" content="Linqore"><meta property="og:locale" content="en_PK">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}og-image.png">
<link rel="icon" href="{FAVICON}">
<link rel="apple-touch-icon" href="{rel}assets/apple-touch-icon.png?v={V['assets/apple-touch-icon.png']}">
<link rel="preload" href="{rel}fonts/plex-sans-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{rel}assets/site.css?v={V['assets/site.css']}">
<script src="{rel}assets/site.js?v={V['assets/site.js']}"></script>
{"".join(ld(s) for s in schemas)}
</head>
<body>
{header}
<main id="main">
{body}
</main>
{footer}
</body>
</html>
'''
    out = ROOT / path / "index.html" if path else ROOT / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    return path


def phero(kick, h1, lead, trail, art_kind, rel="../"):
    cr = "".join(f'<li><a href="{rel}{u}">{e(n)}</a></li>' if i < len(trail) - 1 else f'<li aria-current="page">{e(n)}</li>'
                 for i, (n, u) in enumerate(trail))
    return f'''<section class="phero"><div class="grid-bg"></div><div class="wrap">
<div><ol class="crumbs">{cr}</ol><h1>{e(h1)}</h1><p class="lead">{e(lead)}</p></div>
<div class="art">{art(art_kind)}</div></div></section>'''


def tags(items):
    return '<ul class="tags">' + "".join(f"<li>{e(t)}</li>" for t in items) + "</ul>"


def proj_card(p, rel):
    cat = p["cat"]
    yr = f'<span>{e(p["year"])}</span>' if p.get("year") else ""
    return (f'<article class="proj spot" data-cat="{e(cat)}" data-rv><div class="pv">{pv(p["v"])}<span class="badge">{e(p["status"])}</span></div>'
            f'<div class="pb"><div class="cat">{e(cat)}{yr}</div><h3>{e(p["t"])}</h3><p>{e(p["d"])}</p>{tags(p["tags"][:5])}</div></article>')


def cta_band(rel, title="Ready to build something that works in the real world?", text="Share your idea or requirement. We will reply with a clear scope, timeline and quotation, with no obligation.", cls="sec"):
    return f'''<section class="{cls}"><div class="wrap"><div class="cta-band" data-rv><div><h2>{e(title)}</h2><p>{e(text)}</p></div>
<div class="btns"><a class="btn btn-l" href="{rel}contact/">Get a quotation {ICON["arr"]}</a><a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener noreferrer">{WAICON} WhatsApp</a></div></div></div></section>'''


def faq_html(items):
    return '<div class="faq">' + "".join(f"<details data-rv><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in items) + "</div>"


pages = []

# ---------------------------------------------------------------- HOME
H = A["hero"]
pipe_icons = ["sim", "chip", "wifi", "layers"]
CYCLE = '''<figure class="cycle" aria-label="Our work cycle: simulation, embedded system, IoT connectivity, data and apps">
<svg class="cy-ring" viewBox="0 0 400 400" aria-hidden="true"><defs><linearGradient id="cyg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3B82F6"/><stop offset="1" stop-color="#22D3EE"/></linearGradient></defs><circle class="trk" cx="200" cy="200" r="130"/><circle class="flw" cx="200" cy="200" r="130"/><circle class="in" cx="200" cy="200" r="84"/></svg>
<div class="cy-orbit" aria-hidden="true"><span></span></div>
<div class="cy-hub"><span class="cy-logo">{LOGO}</span><b>Your product</b><small>One team &middot; one scope</small></div>
{STAGES}
<figcaption class="sr">We simulate the system, build the embedded device, connect it through IoT and turn its data into dashboards and apps.</figcaption>
</figure>
'''
STAGES = "".join(
    f'<div class="cy-st s{i+1}"><span class="cy-ic">{ICON[pipe_icons[i]]}</span><span class="cy-tx"><small>0{i+1}</small><b>{e(p["t"])}</b><em>{e(p["m"].replace(chr(183), "·").split(" · ")[0])}</em></span></div>'
    for i, p in enumerate(A["pipeline"]))
CYCLE = CYCLE.replace("{LOGO}", LOGO).replace("{STAGES}", STAGES)
TECH = ["ESP32", "STM32", "Arduino", "Raspberry Pi", "MQTT", "HTTP/HTTPS", "Wi-Fi", "GSM / LTE", "Bluetooth LE", "Modbus",
        "RS-485", "CAN", "MATLAB/Simulink", "Proteus", "Python", "PyTorch", "Android", "iOS", "REST APIs", "TLS"]
MARQ = '<section class="marq" aria-label="Technologies we work with"><div class="marq-wrap"><div class="marq-in">' + \
    "".join(f"<span>{e(t)}</span>" for t in TECH) + "".join(f'<span aria-hidden="true">{e(t)}</span>' for t in TECH) + "</div></div></section>"

# Services bento: one tile per service, each with its own small animated illustration.
BV = {
 "web": '<svg viewBox="0 0 320 150" aria-hidden="true"><rect x="10" y="10" width="300" height="130" rx="10" class="bv-frame"/><path d="M10 34h300" class="bv-line"/><circle cx="26" cy="22" r="4" class="bv-dot"/><circle cx="40" cy="22" r="4" class="bv-dot"/><circle cx="54" cy="22" r="4" class="bv-dot"/><rect x="28" y="50" width="120" height="12" rx="4" class="bv-fill"/><rect x="28" y="70" width="90" height="7" rx="3.5" class="bv-soft"/><rect x="28" y="84" width="104" height="7" rx="3.5" class="bv-soft"/><rect x="28" y="104" width="62" height="20" rx="6" class="bv-acc bv-pulse"/><rect x="176" y="48" width="116" height="76" rx="8" class="bv-frame"/><path d="M188 110l22-24 18 12 26-30 26 16" class="bv-draw"/></svg>',
 "fw": '<svg viewBox="0 0 220 300" aria-hidden="true"><rect x="50" y="40" width="120" height="120" rx="18" class="bv-frame"/><rect x="80" y="70" width="60" height="60" rx="10" class="bv-acc"/><circle cx="110" cy="100" r="9" class="bv-hole"/>' + "".join(f'<path d="M{70+i*20} 40V24M{70+i*20} 160v16M50 {60+i*20}H34M170 {60+i*20}h16" class="bv-line"/>' for i in range(5)) + '<g class="bv-code"><text x="24" y="210">while (1) {</text><text x="40" y="232">read_sensors();</text><text x="40" y="254">control();</text><text x="24" y="276">}<tspan class="bv-blink">_</tspan></text></g></svg>',
 "con": '<svg viewBox="0 0 220 150" aria-hidden="true"><circle cx="60" cy="96" r="10" class="bv-acc"/><path d="M60 72a24 24 0 0 1 24 24M60 52a44 44 0 0 1 44 44M60 32a64 64 0 0 1 64 64" class="bv-wave"/><path d="M146 46a18 18 0 0 1 34-6 14 14 0 0 1 8 26h-40a12 12 0 0 1-2-20z" class="bv-frame"/><path d="M128 96h40" class="bv-dash"/></svg>',
 "dash": '<svg viewBox="0 0 220 150" aria-hidden="true"><path d="M20 128h180" class="bv-line"/>' + "".join(f'<rect x="{30+i*34}" y="{128-h}" width="20" height="{h}" rx="5" class="bv-bar" style-delay="{i}"/>' for i, h in enumerate([46, 78, 58, 98, 70])) + '<circle cx="190" cy="26" r="6" class="bv-acc bv-pulse"/></svg>',
 "sim": '<svg viewBox="0 0 220 150" aria-hidden="true"><path d="M20 120V24M20 120h184" class="bv-line"/><path d="M24 96c20-50 36-50 56 0s36 50 56 0 36-50 56 0" class="bv-draw"/><circle cx="80" cy="96" r="5" class="bv-acc"/><circle cx="136" cy="96" r="5" class="bv-acc"/></svg>',
 "int": '<svg viewBox="0 0 320 150" aria-hidden="true">' + "".join(f'<path d="M160 75L{x} {y}" class="bv-dash"/><rect x="{x-22}" y="{y-14}" width="44" height="28" rx="8" class="bv-frame"/>' for x, y in [(50, 34), (50, 116), (270, 34), (270, 116)]) + '<circle cx="160" cy="75" r="22" class="bv-acc"/><circle cx="160" cy="75" r="8" class="bv-hole"/></svg>',
}
BENTO_KEYS = [("Websites and web platforms", "web", "b-web"), ("Embedded firmware", "fw", "b-fw"),
              ("Connectivity and cloud", "con", "b-con"), ("Dashboards and mobile apps", "dash", "b-dash"),
              ("Simulation and testing", "sim", "b-sim"), ("Integration and support", "int", "b-int")]
_SV = {s["t"]: s for s in A["services"]["items"]}
BENTO = "".join(
    f'<a class="tile spot {cls}" href="{SVC_LINK[t]}/" data-rv><div class="tv">{BV[k].replace(" style-delay=", " data-d=")}</div>'
    f'<div class="tt"><h3>{e(t)}</h3><p>{e(_SV[t]["d"])}</p><span class="more">Learn more {ICON["arr"]}</span></div></a>'
    for t, k, cls in BENTO_KEYS)

home = f'''<section class="hero"><canvas id="net" aria-hidden="true"></canvas><div class="wrap">
<div>
<span class="eyebrow">{e(H["eyebrow"].replace(chr(183), "·"))}</span>
<h1>From device to dashboard, <span class="grad">engineered as one system.</span></h1>
<p class="lead">{e(H["lead"])}</p>
<div class="btns"><a class="btn btn-p" href="contact/">{e(H["cta1"])} {ICON["arr"]}</a><a class="btn btn-g" href="services/">{e(H["cta2"])}</a></div>
<ul class="checks">{"".join(f"<li>{ICON['check']}{e(x)}</li>" for x in H["points"])}</ul>
</div>
{CYCLE}</div></section>
{MARQ}

<section class="proof"><div class="wrap"><div class="stats" data-rv>
<div><b>7</b><span>Systems delivered, device to app</span></div><div><b>6</b><span>Engineering disciplines in one team</span></div>
<div><b>4</b><span>Connectivity options: Wi-Fi, GSM, BLE, wired</span></div><div><b>100%</b><span>Written scope before work starts</span></div>
</div></div></section>

<section class="sec dk"><div class="wrap">
<div class="sec-h" data-rv><span class="kick">Services</span><h2>{e(A["services"]["title"])}</h2><p>{e(A["services"]["sub"])}</p></div>
<div class="bento">{BENTO}</div>
</div></section>


<section class="sec dk"><div class="wrap">
<div class="sec-h row" data-rv><div><span class="kick">Selected projects</span><h2>{e(A["projects"]["title"])}</h2><p>{e(A["projects"]["sub"])}</p></div><a class="btn btn-g" href="projects/">See all projects {ICON["arr"]}</a></div>
<div class="pgrid">{"".join(proj_card(PROJ[k], "") for k in ["fingerprint", "power", "solar"])}</div>
</div></section>

<section class="sec dk2"><div class="wrap quote" data-rv><blockquote>&ldquo;{e(A["quote"]["text"])}&rdquo;</blockquote><cite>{e(A["quote"]["by"])}</cite></div></section>

{cta_band("", cls="sec dk")}'''
pages.append(page("", "Linqore | Embedded Systems, IoT, Web and Mobile App Development",
    "Linqore designs, builds and supports embedded systems, IoT platforms, web applications and mobile apps, engineered together as one system. Based in Islamabad.",
    home, [dict(ORG, **{"@context": "https://schema.org"}), {"@context": "https://schema.org", "@type": "WebSite", "name": "Linqore", "url": BASE}], "home"))

# ---------------------------------------------------------------- SERVICES overview
svc = phero("Services", "Engineering services for connected products", A["services"]["sub"], [("Home", ""), ("Services", "services/")], "services") + f'''
<section class="sec"><div class="wrap">
<div class="sec-h" data-rv><span class="kick">Core services</span><h2>Choose the service you need</h2></div>
<div class="cards two">{"".join(f'<a class="card" href="../{s["slug"]}/" data-rv><div class="ico-b">{ICON[s["icon"]]}</div><h3>{e(s["nav"])}</h3><p>{e(s["intro"])}</p>{tags(s["tech"][:5])}<span class="more">Explore {e(lc(s["nav"]))} {ICON["arr"]}</span></a>' for s in SERVICES)}</div>
</div></section>
<section class="sec dark"><div class="wrap">
<div class="sec-h" data-rv><span class="kick">Our process</span><h2>From model to monitored system</h2></div>
<div class="process">{"".join(f'<div class="step" data-rv><div class="n">{ICON[pipe_icons[i]]}</div><h3>{e(p["t"])}</h3><p>{e(p["d"])}</p><span class="m">{e(p["m"].replace(chr(183), "·"))}</span></div>' for i, p in enumerate(A["pipeline"]))}</div>
</div></section>
{cta_band("../")}'''
pages.append(page("services/", "Services: Web, Embedded, IoT and Mobile Apps | Linqore",
    "Linqore services: web development, embedded firmware, IoT connectivity and cloud, mobile apps and dashboards, simulation, integration and support.",
    svc, [crumbs_ld([("Home", ""), ("Services", "services/")])], "services"))

# ---------------------------------------------------------------- SERVICE detail pages
for s in SERVICES:
    trail = [("Home", ""), ("Services", "services/"), (s["nav"], s["slug"] + "/")]
    body = phero(s["nav"], s["h1"], s["intro"], trail, s["slug"]) + f'''
<section class="sec"><div class="wrap split">
<div data-rv><span class="kick">What we build</span><h2 class="h2">{e(s["nav"])} services</h2>
<ul class="list">{"".join(f'<li>{ICON["check"]}<div><b>{e(a)}</b><span>{e(b)}</span></div></li>' for a, b in s["build"])}</ul></div>
<div class="card" data-rv><div class="ico-b">{ICON[s["icon"]]}</div><h3>Technologies</h3><p>Tools and platforms we use for {e(lc(s["nav"]))}.</p>{tags(s["tech"])}
<div class="sp"></div><a class="btn btn-p" href="../contact/?service={quote(s["nav"])}">Discuss your project {ICON["arr"]}</a></div>
</div></section>
<section class="sec alt"><div class="wrap">
<div class="sec-h" data-rv><span class="kick">Related work</span><h2>Projects using {e(lc(s["nav"]))}</h2></div>
<div class="pgrid">{"".join(proj_card(PROJ[k], "../") for k in s["projects"])}</div>
</div></section>
<section class="sec"><div class="wrap"><div class="sec-h c" data-rv><span class="kick">Questions</span><h2>Common questions</h2></div>{faq_html(s["faq"])}</div></section>
{cta_band("../")}'''
    pages.append(page(s["slug"] + "/", s["title"], s["desc"], body, [
        {"@context": "https://schema.org", "@type": "Service", "name": s["nav"], "serviceType": s["nav"], "description": s["desc"],
         "provider": {"@id": BASE + "#org", "@type": "ProfessionalService", "name": "Linqore", "url": BASE},
         "areaServed": {"@type": "Country", "name": "Pakistan"}, "url": BASE + s["slug"] + "/"},
        faq_ld(s["faq"]), crumbs_ld(trail)], s["slug"]))

# ---------------------------------------------------------------- PROJECTS
cats = []
for p in A["projects"]["items"]:
    if p["cat"] not in cats:
        cats.append(p["cat"])
proj = phero("Projects", "Our work, from the device to the app", A["projects"]["sub"], [("Home", ""), ("Projects", "projects/")], "projects") + f'''
<section class="sec"><div class="wrap">
<h2 class="sr">All projects</h2>
<div class="filters" role="group" aria-label="Filter projects"><button type="button" data-f="all" aria-pressed="true">All</button>{"".join(f'<button type="button" data-f="{e(c)}" aria-pressed="false">{e(c)}</button>' for c in cats)}</div>
<div class="pgrid">{"".join(proj_card(p, "../") for p in A["projects"]["items"])}</div>
</div></section>
{cta_band("../", "Need a system like these?", "We can adapt any of these solutions to your site, budget and timeline.")}'''
pages.append(page("projects/", "Projects: Embedded, IoT and AI Systems | Linqore",
    "Embedded and IoT projects by Linqore: fingerprint attendance, RFID/NFC, smart plug, remote power monitoring, solar fault detection, computer vision and health monitoring.",
    proj, [crumbs_ld([("Home", ""), ("Projects", "projects/")]),
           {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
               {"@type": "ListItem", "position": i + 1, "name": p["t"]} for i, p in enumerate(A["projects"]["items"])]}], "projects"))

# ---------------------------------------------------------------- ABOUT
AB, CM = A["about"], A["comms"]
link_icons = ["wifi", "signal", "bt", "cable"]
story = "".join(f"<p>{e(x)}</p>" for x in AB["story"].strip().split("\n") if x.strip())
about = phero("About", "One team, accountable for the whole system", AB["intro"], [("Home", ""), ("About", "about/")], "about") + f'''
<section class="sec"><div class="wrap split">
<div data-rv><span class="kick">Our story</span><h2 class="h2">Devices, connectivity and software that work as one</h2><div class="prose">{story}</div></div>
<div class="cards one" data-rv>{"".join(f'<div class="card"><div class="ico-b">{ICON[ic]}</div><h3>{e(v["t"])}</h3><p>{e(v["d"])}</p></div>' for v, ic in zip(AB["values"], ["sim", "layers", "doc"]))}</div>
</div></section>
<section class="sec dark"><div class="wrap">
<div class="sec-h" data-rv><span class="kick">Connectivity</span><h2>{e(CM["title"])}</h2><p>{e(CM["sub"])}</p></div>
<div class="cards four">{"".join(f'<div class="card" data-rv><div class="ico-b">{ICON[link_icons[i]]}</div><h3>{e(l["t"])}</h3><p>{e(l["d"])}</p>{tags(l["tags"])}</div>' for i, l in enumerate(CM["links"]))}</div>
</div></section>
<section class="sec"><div class="wrap">
<div class="sec-h" data-rv><span class="kick">Protocols</span><h2>Industry-standard protocols, securely implemented</h2></div>
<div class="proto" data-rv>{"".join(f'<div><b>{e(p["t"])}</b><p>{e(p["d"])}</p></div>' for p in CM["protocols"])}</div>
</div></section>
{cta_band("../")}'''
pages.append(page("about/", "About Linqore: Engineering and Software Company in Islamabad",
    AB["intro"], about, [crumbs_ld([("Home", ""), ("About", "about/")])], "about"))

# ---------------------------------------------------------------- CONTACT
svc_opts = [s["t"] for s in A["services"]["items"]] + [s["nav"] for s in SERVICES if s["nav"] not in [x["t"] for x in A["services"]["items"]]]
faq_items = [(f["q"], f["a"].replace("Send the request form on this page.", "Send the request form above.")) for f in A["faq"]["items"]]
contact = phero("Contact", "Tell us about your project", A["request"]["sub"], [("Home", ""), ("Contact", "contact/")], "contact") + f'''
<section class="sec"><div class="wrap contact-grid">
<form class="form" id="quote" data-endpoint="https://formsubmit.co/ajax/{quote(FORM_TO)}" novalidate>
<div class="fgrid">
<div class="f"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name" maxlength="80" required></div>
<div class="f"><label for="f-contact">Phone or email</label><input id="f-contact" name="contact" autocomplete="email" maxlength="120" required></div>
<div class="f"><label for="f-city">City <small>(optional)</small></label><input id="f-city" name="city" autocomplete="address-level2" maxlength="80"></div>
<div class="f"><label for="f-service">Service</label><select id="f-service" name="service"><option value="">Choose a service</option>{"".join(f'<option>{e(o)}</option>' for o in svc_opts)}<option>Something else</option></select></div>
<div class="f full"><label for="f-budget">Budget <small>(optional)</small></label><input id="f-budget" name="budget" maxlength="80" placeholder="{e(A["request"]["budgetHint"])}"></div>
<div class="f full"><label for="f-details">Project details</label><textarea id="f-details" name="details" maxlength="2000" required placeholder="What should it do? Who will use it? Any deadline?"></textarea></div>
<div class="hp" aria-hidden="true"><label for="f-hp">Leave this empty</label><input id="f-hp" name="_honey" tabindex="-1" autocomplete="off"></div>
</div>
<div class="row"><button class="btn btn-p" type="submit">Send request</button><span class="note">No obligation. Your details are used only to reply to you.</span></div>
<div class="msg" id="form-msg" role="status" aria-live="polite" hidden></div>
</form>
<aside class="side">
<div class="card"><a class="line" href="{WA}" target="_blank" rel="noopener noreferrer"><span class="ico-b">{WAICON}</span><span><small>WhatsApp</small><b>Chat with us</b></span></a></div>
<div class="card"><a class="line" href="tel:{TEL}"><span class="ico-b">{ICON["call"]}</span><span><small>Phone</small><b>{e(PHONE)}</b></span></a></div>
<div class="card"><div class="line"><span class="ico-b">{ICON["pin"]}</span><span><small>Office</small><b>{e(C["city"])}</b><small>Call or message first so we can set a time.</small></span></div></div>
</aside>
</div></section>
<section class="sec alt"><div class="wrap"><div class="sec-h c" data-rv><span class="kick">FAQ</span><h2>{e(A["faq"]["title"])}</h2></div>{faq_html(faq_items)}</div></section>'''
pages.append(page("contact/", "Contact Linqore: Request a Quotation",
    "Request a quotation from Linqore for websites, embedded systems, IoT solutions or mobile apps. Reply by WhatsApp, phone or email.",
    contact, [crumbs_ld([("Home", ""), ("Contact", "contact/")]), faq_ld(faq_items)], "contact"))

# ---------------------------------------------------------------- LEGAL
for d in A["legal"]["docs"]:
    slug = d["id"] + "/"
    secs = "".join(f'<h2>{e(x["t"])}</h2><p>{e(x["b"].replace("in the Contact section", "on our Contact page"))}</p>' for x in d["sections"])
    body = phero("Legal", d["title"], "How this website works and how we handle your information.", [("Home", ""), (d["title"], slug)], "legal") + \
        f'<section class="sec"><div class="wrap legal"><p class="upd">Last updated {e(A["legal"]["updated"])}</p>{secs}</div></section>'
    pages.append(page(slug, f'{d["title"]} | Linqore', f'{d["title"]} for the Linqore website.', body,
                      [crumbs_ld([("Home", ""), (d["title"], slug)])], d["id"]))

# ---------------------------------------------------------------- 404 (served from any depth, so absolute paths)
nf = page("404-tmp/", "Page not found | Linqore", "This page does not exist.",
          f'<section class="phero"><div class="grid-bg"></div><div class="wrap"><div><h1>Page not found</h1><p class="lead">The page you are looking for does not exist or has moved.</p><p class="sec-more"><a class="btn btn-p" href="{BASE}">Back to home {ICON["arr"]}</a></p></div></div></section>')
src = (ROOT / "404-tmp" / "index.html").read_text().replace('href="../', f'href="{BASE}').replace('src="../', f'src="{BASE}')
src = src.replace(f'<link rel="canonical" href="{BASE}404-tmp/">', '<meta name="robots" content="noindex">')
(ROOT / "404.html").write_text(src)
(ROOT / "404-tmp" / "index.html").unlink(); (ROOT / "404-tmp").rmdir()

# ---------------------------------------------------------------- sitemap + robots
pri = {"": "1.0", "services/": "0.9", "contact/": "0.9", "projects/": "0.8", "about/": "0.7", "privacy/": "0.2", "terms/": "0.2"}
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{BASE}{p}</loc><priority>{pri.get(p, '0.8')}</priority></url>\n" for p in pages) + "</urlset>\n")
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /scripts/\nSitemap: {BASE}sitemap.xml\n")
print("built", len(pages), "pages:", ", ".join(p or "/" for p in pages))
