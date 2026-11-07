"""Generate static, crawlable service pages for the Nexwire site."""
import html, json, os, sys

ROOT = sys.argv[1]
BASE = "https://123rahmat.github.io/NX/"
PHONE = "+92 341 2010948"
WA = "https://wa.me/923412010948?text=" + "Hi%20Nexwire%2C%20I%27d%20like%20to%20discuss%20a%20project."
FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap"

P = {
 "fingerprint": ("Smart attendance system", "2025", "Fingerprint attendance on ESP32. Admins enrol and remove people from a mobile app, each scan is time-stamped and sent to the server over HTTP.", ["ESP32", "Fingerprint sensor", "HTTP", "Mobile app"]),
 "rfid": ("RFID and NFC read-write system", "2025", "Reads and writes NFC card data from a mobile app in text and hex form, and copies the contents of one card onto another.", ["RFID", "NFC", "Mobile app"]),
 "plug": ("Smart plug with scheduling", "2025", "Switches a relay on a schedule from an RTC or the network, with a timer mode and direct control from a mobile app.", ["ESP32", "Relay", "RTC", "Wi-Fi"]),
 "power": ("Real-time remote power monitoring", "2025", "Measures voltage and current on an ESP32 and publishes the readings over MQTT for remote monitoring on a mobile screen.", ["ESP32", "MQTT", "Sensors"]),
 "solar": ("Solar fault and damage detection", "2023", "Measures irradiance, temperature, voltage and current, plots the I-V curve in Python, locates a fault and disconnects the faulty panel through a relay.", ["Arduino", "ESP32", "TCP", "Python"]),
 "vision": ("Human detection with computer vision", "2024", "A YOLOv5 model trained in PyTorch on a labelled human dataset for real-time person detection.", ["YOLOv5", "PyTorch", "Python"]),
 "health": ("Smart health monitoring system", "", "Reads heart rate, blood oxygen, body temperature and GPS location on an ESP32 and sends them over GSM to a mobile app.", ["ESP32", "MAX30102", "GPS", "SIM800L"]),
}

PAGES = [
 {"slug": "web-development", "nav": "Web development",
  "title": "Web Development Company in Islamabad | Nexwire",
  "desc": "Nexwire builds fast, secure company websites, customer portals and admin panels in Islamabad. Clear scope and quotation before work starts.",
  "h1": "Web development: websites, portals and admin panels",
  "intro": ["We build company websites, customer portals and admin systems that load fast, stay secure and are easy for your team to manage.",
            "Every project starts with a written scope and quotation, so you know what you get, when, and what it costs before any work begins."],
  "build": [("Company websites", "Fast, mobile-first sites that explain what you do and turn visitors into enquiries."),
            ("Customer portals", "Secure areas where your customers log in, track orders or view their data."),
            ("Admin panels", "Internal tools to manage records, users and content without technical help."),
            ("IoT web dashboards", "Live charts, history and alerts for connected devices and machines.")],
  "tech": ["HTML and CSS", "JavaScript", "REST APIs", "Databases", "HTTPS", "Responsive design"],
  "projects": ["fingerprint", "power"],
  "faq": [("How long does a company website take?", "A typical company website takes two to four weeks, depending on the number of pages and how quickly content is ready. You get a timeline with your quotation."),
          ("Will my website work on mobile phones?", "Yes. Every site we build is designed for phones first and tested on phone, tablet and desktop screens."),
          ("Can you connect my website to devices or machines?", "Yes. We build web dashboards that show live data from sensors and devices and send commands back to them.")]},
 {"slug": "embedded-systems", "nav": "Embedded systems",
  "title": "Embedded Systems and Firmware Development | Nexwire",
  "desc": "Embedded firmware for ESP32, STM32 and Arduino: sensors, motor and relay control, low power and fault handling. Simulation before hardware.",
  "h1": "Embedded systems and firmware development",
  "intro": ["We write the code that runs on the device: reading sensors, controlling motors and relays, saving power and handling faults safely.",
            "Where hardware is involved, we model the system first in MATLAB/Simulink or Proteus, so mistakes show up before any parts are bought."],
  "build": [("Firmware for microcontrollers", "Reliable C and C++ firmware for ESP32, STM32 and Arduino boards."),
            ("Sensor and control systems", "Reading sensors, driving relays and motors, and reacting to faults."),
            ("Low-power devices", "Battery-friendly designs with sleep modes and efficient scheduling."),
            ("Simulation and testing", "Run the firmware against a model of the machine, tank or building before real hardware.")],
  "tech": ["ESP32", "STM32 (ARM Cortex-M)", "Arduino", "Raspberry Pi", "C and C++", "MATLAB/Simulink", "Proteus", "UART, SPI, I2C", "RS-485, CAN"],
  "projects": ["plug", "solar", "health"],
  "faq": [("Which microcontrollers do you work with?", "Mainly ESP32, STM32 (ARM Cortex-M), Arduino and Raspberry Pi. Tell us what you already use and we work with it."),
          ("Do I need hardware before we start?", "No. We can simulate the system first and advise on suitable boards and sensors before you buy anything."),
          ("Can you fix or extend existing firmware?", "Yes. We can review existing code, fix faults and add features.")]},
 {"slug": "iot-solutions", "nav": "IoT solutions",
  "title": "IoT Solutions and Cloud Connectivity | Nexwire",
  "desc": "End-to-end IoT systems: devices, Wi-Fi, GSM and Bluetooth connectivity, MQTT and HTTP cloud, remote control, alerts and over-the-air updates.",
  "h1": "IoT solutions: devices, connectivity and cloud",
  "intro": ["We connect devices securely to a server: data storage, remote commands, alerts and over-the-air updates, all designed as one system.",
            "We choose the link that suits the site, whether Wi-Fi indoors, GSM at remote sites or Bluetooth for setup from a phone, and use the protocol your systems already speak."],
  "build": [("Remote monitoring", "Live readings from sensors, meters and machines, viewable from anywhere."),
            ("Remote control", "Switch relays, change settings and send commands from a dashboard or phone."),
            ("Alerts", "SMS, app or email alerts when a value crosses a limit or a device goes offline."),
            ("Over-the-air updates", "Update device firmware remotely without visiting the site.")],
  "tech": ["Wi-Fi", "GSM and LTE", "Bluetooth (BLE)", "MQTT", "HTTP/HTTPS", "TCP and UDP", "WebSocket", "Modbus", "CoAP", "TLS"],
  "projects": ["power", "fingerprint", "health"],
  "faq": [("What if the site has no Wi-Fi?", "We use GSM or LTE mobile data, or SMS alerts, for remote sites without Wi-Fi."),
          ("Is the data secure?", "Data in transit is encrypted with TLS, and devices authenticate to the server."),
          ("Can you connect to systems we already use?", "Yes. We integrate with existing servers, industrial equipment over Modbus and RS-485, and third-party APIs.")]},
 {"slug": "mobile-apps", "nav": "Mobile apps and dashboards",
  "title": "Mobile App and Dashboard Development | Nexwire",
  "desc": "Android and iOS apps and web dashboards that show live data, send commands and raise alerts, built for the people who use them every day.",
  "h1": "Mobile apps and dashboards",
  "intro": ["We build screens that show what your system is doing, send commands and raise alerts, designed for the people who use them every day.",
            "Apps and dashboards are designed together with the firmware and connection, so the whole system works as one."],
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

CSS = """:root{--bg:#0B1426;--card:#111d35;--line:#1f2d4d;--text:#E6ECF5;--muted:#9fb0cc;--accent:#5B8DEF;--btn:#1D5FD6}
@media (prefers-color-scheme:light){:root{--bg:#f4f5f7;--card:#fff;--line:#dde3ec;--text:#0f1b2e;--muted:#4a5a74;--accent:#1D5FD6}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.65 "IBM Plex Sans",system-ui,sans-serif}
a{color:var(--accent)}.wrap{max-width:1040px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line)}header .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:64px;flex-wrap:wrap}
.brand{display:flex;align-items:center;gap:10px;color:var(--text);text-decoration:none;font-weight:600;font-size:18px}
.brand svg{width:30px;height:30px}nav.top{display:flex;gap:18px;flex-wrap:wrap;font-size:14px}nav.top a{color:var(--muted);text-decoration:none}nav.top a:hover,nav.top a[aria-current]{color:var(--text)}
.crumb{font:13px "IBM Plex Mono",monospace;color:var(--muted);margin:28px 0 0}.crumb a{color:var(--muted)}
h1{font-size:clamp(30px,5vw,46px);line-height:1.15;margin:12px 0 16px;font-weight:600}h2{font-size:24px;margin:48px 0 16px;font-weight:600}h3{font-size:17px;margin:0 0 6px}
.lead{font-size:18px;color:var(--muted);max-width:720px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:20px}.card p{margin:0;color:var(--muted)}
.tags{display:flex;flex-wrap:wrap;gap:8px;padding:0;list-style:none;margin:0}.tags li{font:13px "IBM Plex Mono",monospace;border:1px solid var(--line);border-radius:999px;padding:4px 12px;color:var(--muted)}
.card .tags{margin-top:12px}.yr{font:12px "IBM Plex Mono",monospace;color:var(--muted)}
details{border-bottom:1px solid var(--line);padding:14px 0}summary{cursor:pointer;font-weight:500}details p{color:var(--muted);margin:8px 0 0}
.cta{margin:56px 0;padding:28px;border-radius:12px;background:var(--card);border:1px solid var(--line);display:flex;flex-wrap:wrap;gap:16px;align-items:center;justify-content:space-between}
.cta p{margin:0;font-size:18px;font-weight:500}.btns{display:flex;gap:12px;flex-wrap:wrap}
.btn{display:inline-block;padding:12px 20px;border-radius:8px;text-decoration:none;font-weight:600;background:var(--btn);color:#fff}.btn.wa{background:#25D366}
footer{border-top:1px solid var(--line);padding:28px 0;color:var(--muted);font-size:14px}footer nav{display:flex;flex-wrap:wrap;gap:16px;margin-bottom:10px}footer a{color:var(--muted)}
.wa-fab{position:fixed;right:max(16px,env(safe-area-inset-right));bottom:max(16px,env(safe-area-inset-bottom));z-index:99;width:56px;height:56px;border-radius:50%;background:#25D366;display:grid;place-items:center;box-shadow:0 6px 20px rgba(0,0,0,.28)}
.wa-fab:focus-visible,.btn:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
"""

LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="6" fill="#1D5FD6"/><path d="M9 24V8l14 16V8" fill="none" stroke="#fff" stroke-width="3"/></svg>'
WAICON = '<svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><path fill="#fff" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.7c-2 0-4-.6-5.7-1.6l-.4-.2-3.9 1 1-3.8-.3-.4A10.7 10.7 0 1 1 16 26.7zm5.9-8c-.3-.2-1.9-1-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.8 8.8 0 0 1-4.4-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6 0-.9.4s-1.2 1.1-1.2 2.7 1.2 3.2 1.4 3.4 2.4 3.6 5.7 5c2.1.9 3 1 4 .8.7-.1 1.9-.8 2.2-1.5s.3-1.4.2-1.5-.3-.2-.6-.4z"/></svg>'

e = html.escape
NAVS = [(p["slug"], p["nav"]) for p in PAGES] + [("projects", "Projects")]


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def shell(slug, title, desc, body, schemas):
    url = BASE + slug + "/"
    nav = "".join(f'<a href="../{s}/"{" aria-current=\"page\"" if s == slug else ""}>{e(n)}</a>' for s, n in NAVS)
    fnav = "".join(f'<a href="../{s}/">{e(n)}</a>' for s, n in NAVS)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; base-uri 'none'; form-action 'none'; object-src 'none'">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0B1426">
<meta property="og:type" content="website"><meta property="og:site_name" content="Nexwire">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}og-image.png">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}og-image.png">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='6' fill='%231D5FD6'/%3E%3Cpath d='M9 24V8l14 16V8' fill='none' stroke='white' stroke-width='3'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="../pages.css">
{"".join(ld(s) for s in schemas)}
</head>
<body>
<header><div class="wrap"><a class="brand" href="../">{LOGO}Nexwire</a><nav class="top" aria-label="Services">{nav}</nav></div></header>
<main class="wrap">
{body}
<section class="cta"><p>Tell us what you need. We reply with a scope, timeline and quotation.</p><div class="btns"><a class="btn" href="../#contact">Request a quotation</a><a class="btn wa" href="{WA}" target="_blank" rel="noopener">WhatsApp {e(PHONE)}</a></div></section>
</main>
<footer><div class="wrap"><nav aria-label="Site">{fnav}<a href="../">Home</a></nav>&copy; Nexwire &middot; Islamabad &middot; <a href="tel:{PHONE.replace(" ", "")}">{e(PHONE)}</a></div></footer>
<a class="wa-fab" href="{WA}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">{WAICON}</a>
</body>
</html>
'''


def crumbs(slug, name):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": name, "item": BASE + slug + "/"}]}


ORG = {"@type": "ProfessionalService", "name": "Nexwire", "url": BASE, "telephone": PHONE,
       "address": {"@type": "PostalAddress", "addressLocality": "Islamabad", "addressCountry": "PK"}}


def proj_cards(keys):
    out = []
    for k in keys:
        t, y, d, tags = P[k]
        out.append(f'<article class="card"><h3>{e(t)}</h3>{f"<div class=yr>{y}</div>" if y else ""}<p>{e(d)}</p><ul class="tags">{"".join(f"<li>{e(x)}</li>" for x in tags)}</ul></article>')
    return '<div class="grid">' + "".join(out) + "</div>"


for p in PAGES:
    body = f'''<p class="crumb"><a href="../">Home</a> / {e(p["nav"])}</p>
<h1>{e(p["h1"])}</h1>
{"".join(f'<p class="lead">{e(x)}</p>' for x in p["intro"])}
<h2>What we build</h2>
<div class="grid">{"".join(f'<div class="card"><h3>{e(a)}</h3><p>{e(b)}</p></div>' for a, b in p["build"])}</div>
<h2>Technologies</h2>
<ul class="tags">{"".join(f"<li>{e(x)}</li>" for x in p["tech"])}</ul>
<h2>Related projects</h2>
{proj_cards(p["projects"])}
<p><a href="../projects/">See all projects</a></p>
<h2>Questions</h2>
{"".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])}'''
    schemas = [
        {"@context": "https://schema.org", "@type": "Service", "name": p["nav"], "serviceType": p["nav"], "description": p["desc"],
         "provider": ORG, "areaServed": {"@type": "Country", "name": "Pakistan"}, "url": BASE + p["slug"] + "/"},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
        crumbs(p["slug"], p["nav"])]
    os.makedirs(os.path.join(ROOT, p["slug"]), exist_ok=True)
    open(os.path.join(ROOT, p["slug"], "index.html"), "w").write(shell(p["slug"], p["title"], p["desc"], body, schemas))

body = f'''<p class="crumb"><a href="../">Home</a> / Projects</p>
<h1>Projects: embedded, IoT, power and AI systems</h1>
<p class="lead">Systems we have designed and built, from firmware on the device to the application that controls it.</p>
<h2>All projects</h2>
{proj_cards(list(P))}'''
os.makedirs(os.path.join(ROOT, "projects"), exist_ok=True)
open(os.path.join(ROOT, "projects", "index.html"), "w").write(shell(
    "projects", "Projects: Embedded, IoT and AI Systems | Nexwire",
    "Embedded and IoT projects by Nexwire: fingerprint attendance, RFID/NFC, smart plug, remote power monitoring, solar fault detection and computer vision.",
    body, [crumbs("projects", "Projects")]))
open(os.path.join(ROOT, "pages.css"), "w").write(CSS)

urls = [("", "1.0")] + [(s + "/", "0.8") for s, _ in NAVS]
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{BASE}{u}</loc><priority>{pr}</priority></url>\n" for u, pr in urls) + "</urlset>\n")
print("ok", [s for s, _ in NAVS])
