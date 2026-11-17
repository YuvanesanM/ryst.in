#!/usr/bin/env python3
"""
Builds the Dreamour Design static site.

    python3 _build/build.py

Edit the data below (contact details, services, projects) and re-run.
Every page is written as plain HTML into the repository root.
"""
import json, os, html as H
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

SITE = "https://design.dreamour.in"
BRAND = "Dreamour Design"
PHONE = "+91 96001 25599"
PHONE_TEL = "+919600125599"
WA = "919600125599"
EMAIL = "info@design.dreamour.in"
STREET = "271/182, Ankur Manor, P.H Road, Kilpauk"
CITY = "Chennai"
PIN = "600010"
ADDRESS = f"{STREET}, {CITY} – {PIN}, India"
MAPS = "https://www.google.com/maps/search/?api=1&query=Ankur+Manor+P.H+Road+Kilpauk+Chennai+600010"
MAP_EMBED = "https://www.google.com/maps?q=Ankur+Manor,+P.H+Road,+Kilpauk,+Chennai+600010&output=embed"
IG = "https://www.instagram.com/design.dreamour.in/"
FB = "https://www.facebook.com/design.dreamour.in/"
TODAY = date.today().isoformat()

def esc(s): return H.escape(str(s), quote=True)

def clip(s, n=158):
    return s if len(s) <= n else s[:s.rfind(" ", 0, n - 1)].rstrip(",.;:") + "…"

# ------------------------------------------------------------------ images
IMG = "assets/img/p"
def sizes_for(name):
    return [w for w in (800, 1600, 2400) if os.path.exists(f"{IMG}/{name}-{w}.webp")]

def dims(name):
    from PIL import Image
    with Image.open(f"{IMG}/{name}-1600.jpg") as im:
        return im.size

def pic(name, alt, sizes="100vw", cls="", eager=False, attrs=""):
    ws = sizes_for(name)
    w, h = dims(name)
    srcset = ", ".join(f"/{IMG}/{name}-{x}.webp {x}w" for x in ws)
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<picture{c}{attrs}><source type="image/webp" srcset="{srcset}" sizes="{sizes}">'
            f'<img src="/{IMG}/{name}-1600.jpg" alt="{esc(alt)}" width="{w}" height="{h}" {load} decoding="async"></picture>')

def full(name):  # largest webp for lightbox
    return f"/{IMG}/{name}-{sizes_for(name)[-1]}.webp"

def og(name): return f"{SITE}/{IMG}/{name}-1600.jpg"

# ------------------------------------------------------------------ content
SERVICES = [
 dict(id="architecture", no="01", name="Architecture Design", img="ryst-day",
      short="Site-sensitive, personalised buildings, from concept sketches to construction drawings.",
      body="We offer site sensitive, personalised architectural design services that include conceptual and schematic design, design development and construction drawings, assisting with contractor bidding and negotiation. Through our architectural design services we commit to create iconic structures.",
      points=["Conceptual & schematic design", "Design development", "Construction drawings", "Contractor bidding & negotiation"],
      projects=["ryst-house", "rasi-home", "h-house", "community-hall"]),
 dict(id="interiors", no="02", name="Interior Design", img="int-living",
      short="Interiors shaped entirely around your requirements, visualised before they're built.",
      body="Interior design solution that we offer is one of its kind in catering to your requirements to the fullest extent possible and providing perfect and the most apt design solution. We bring all the visualization to absolute reality and reality is what we visualize.",
      points=["Requirement-led planning", "Photorealistic visualisation", "Living, kitchen, bedroom & bath", "Home theatres & feature spaces"],
      projects=["cluster-house"]),
 dict(id="landscape", no="03", name="Landscape Design", img="round-aerial",
      short="Gardens, plazas and public landscapes, woven into every project where they belong.",
      body="Landscape design services are offered to all our projects wherever there is a possibility of including them. We also offer specialised landscape design services for projects that have landscaping as their primary objective.",
      points=["Landscape within every project", "Specialised landscape projects", "Public spaces & roundabouts", "Campus & estate landscapes"],
      projects=["roundabout-egmore", "statue-landscape", "mass-estate"]),
 dict(id="product", no="04", name="Product Design", img="int-kitchen",
      short="Custom furniture designed to your taste and built with our own carpenters.",
      body="We can design and customize all possible furniture that comes under our scope of design as per the client's need and taste. We also offer furniture design solutions and work closely with our team of carpenters to make the product as exclusive as possible. We also design furniture for some of the leading furniture stores.",
      points=["Bespoke furniture", "Made with our carpenters", "Kitchens & storage", "Design for furniture stores"],
      projects=["cluster-house"]),
]

PROJECTS = [
 dict(slug="ryst-house", name="RYST House", type="Beach house", cat="architecture", loc="Cheyyur, Tamil Nadu", area="2,400 sq ft", year="2020",
      hero="ryst-night-front",
      desc="A beach house in the corner plot.",
      more='Today the house welcomes guests as <a href="https://stay.ryst.in/" target="_blank" rel="noopener">RYST 109A</a>, a private beach villa on Pearl Beach, ECR.',
      gallery=[("ryst-night-front", "Front elevation lit up at night"), ("ryst-day", "Street-side view by day"),
               ("ryst-day-back", "Rear corner of the plot"),
               ("ryst-night-back", "Rear elevation at night"), ("ryst-detail", "Facade detail with night lighting")]),
 dict(slug="rasi-home", name="Rasi Home", type="Apartment", cat="architecture", loc="Velachery, Chennai", area="4,600 sq ft", year="2017",
      hero="rasi-night", desc="A four unit apartment.", more="",
      gallery=[("rasi-day", "Rasi Home apartment by day"), ("rasi-night", "Rasi Home apartment at dusk")]),
 dict(slug="h-house", name="H-House", type="Residence", cat="architecture", loc="Kottivakkam, Chennai", area="3,500 sq ft", year="2015",
      hero="h-house", desc="A living for a family of four in ECR.", more="",
      gallery=[("h-house", "H-House exterior")]),
 dict(slug="cluster-house", name="Interiors for Cluster House", type="Residential interiors", cat="interiors", loc="Purasaiwakkam, Chennai", area="4,800 sq ft", year="2019",
      hero="int-living-view",
      desc="Less is more is the key for this project. The house is designed with neutral shades and an elegant look.", more="",
      gallery=[("int-living", "Living room with slatted partition"), ("int-living-view", "Living and dining space"),
               ("int-kitchen", "Kitchen with terrazzo counters"), ("int-master-bed", "Master bedroom"),
               ("int-bedroom", "Bedroom with dark feature wall"), ("int-bath", "Master bathroom"),
               ("int-theatre", "Home theatre")]),
 dict(slug="mass-estate", name="Landscape for Mass Estate", type="Estate landscape", cat="landscape", loc="Gummidipoondi, Tamil Nadu", area="20 acres", year="2019",
      hero="mass-farm",
      desc="Landscape design for a 20-acre estate, covering the entrance plaza, parking courts and the planted grounds beyond.", more="",
      gallery=[("mass-farm", "Aerial view of the planted grounds"), ("mass-entrance", "Entrance sculpture and water feature"),
               ("mass-parking", "Landscaped approach and parking"), ("mass-parking-lot", "Tree-lined parking courts")]),
 dict(slug="roundabout-egmore", name="Roundabout Design", type="Public landscape", cat="landscape", loc="Egmore, Chennai", area="1,300 sq ft", year="2016",
      hero="round-aerial",
      desc="Located in the heart of the city, the roundabout serves the purpose of traffic control and relishes one's eyes.", more="",
      gallery=[("round-aerial", "Aerial view of the roundabout"), ("round-overview", "Planting, water and steps"),
               ("round-plaza", "Statue plaza"), ("round-material", "Materials and water feature"), ("round-walk", "At street level")]),
 dict(slug="statue-landscape", name="Statue Landscape", type="Campus landscape", cat="landscape", loc="Tuticorin, Tamil Nadu", area="2,400 sq ft", year="2015",
      hero="statue-night",
      desc="Spread across a college campus in Tamil Nadu, the statue is the central focus of the ground.", more="",
      gallery=[("statue-day", "Statue landscape by day"), ("statue-night", "Statue landscape lit at night")]),
 dict(slug="community-hall", name="Community Hall", type="Civic building", cat="architecture", loc="Tuticorin, Tamil Nadu", area="2,900 sq ft", year="2019",
      hero="hall-angle",
      desc="Ayya Foundation is a community hall where linearity controls the design, both on layout and facade design.", more="",
      gallery=[("hall-front", "Front facade of the community hall"), ("hall-angle", "Corner view of the community hall")]),
]
P = {p["slug"]: p for p in PROJECTS}
CATS = {"architecture": "Architecture", "interiors": "Interiors", "landscape": "Landscape"}

# ------------------------------------------------------------------ icons
I = {
 "arrow": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12Z"/><circle cx="12" cy="9" r="2.5"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8Z"/></svg>',
 "wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1.3-4A8 8 0 1 1 8 18.7Z"/><path d="M9 9.5c.5 2 2 3.6 4 4.4l1.2-1.1 1.8.8v1.4c-3.6.4-7.6-3.4-7.4-7h1.4l.8 1.8Z"/></svg>',
 "zoom": '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6"/><path d="m20 20-4.5-4.5M11 8v6M8 11h6"/></svg>',
}
LOGO = ('<svg class="dd" viewBox="0 0 120 64" aria-hidden="true">'
        '<path d="M10 12h18a20 20 0 0 1 0 40H10" fill="none" stroke="currentColor" stroke-opacity=".55" stroke-width="9" stroke-linecap="round"/>'
        '<path d="M70 12h18a20 20 0 0 1 0 40H70" fill="none" stroke="#9b6cc4" stroke-width="9" stroke-linecap="round"/></svg>')

NAV = [("/about/", "Studio"), ("/services/", "Services"), ("/works/", "Works"), ("/contact-us/", "Contact")]

# ------------------------------------------------------------------ schema
ORG = {
  "@context": "https://schema.org",
  "@graph": [
    {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": BRAND,
     "inLanguage": "en-IN", "publisher": {"@id": f"{SITE}/#business"}},
    {"@type": ["ProfessionalService", "HomeAndConstructionBusiness"], "@id": f"{SITE}/#business",
     "name": BRAND, "legalName": "Dreamour Multiventures", "slogan": "Your Dream Our Design",
     "description": "Architecture, interior, landscape and furniture design studio in Chennai, founded by architect Ramyaa Yuvanesan.",
     "url": f"{SITE}/", "logo": f"{SITE}/assets/img/logo-dd.png", "image": og("ryst-night-front"),
     "telephone": PHONE_TEL, "email": EMAIL, "priceRange": "₹₹",
     "founder": {"@type": "Person", "name": "Ramyaa Yuvanesan", "jobTitle": "Architect"},
     "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY,
                 "postalCode": PIN, "addressRegion": "Tamil Nadu", "addressCountry": "IN"},
     "areaServed": [{"@type": "City", "name": "Chennai"}, {"@type": "State", "name": "Tamil Nadu"}],
     "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Design services", "itemListElement": [
        {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "description": s["short"]}} for s in SERVICES]},
     "sameAs": [IG, FB]}
  ]}

def ld(obj): return f'\n  <script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'

def crumbs_ld(items):
    return ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]})

# ------------------------------------------------------------------ layout
def write(path, html):
    fn = path.lstrip("/") or "index.html"
    if not fn.endswith(".html"):
        fn = os.path.join(fn, "index.html")
    os.makedirs(os.path.dirname(fn) or ".", exist_ok=True)
    with open(fn, "w", encoding="utf-8") as f:
        f.write(html)

def layout(path, title, desc, body, image="ryst-night-front", active="", schema="", preload=None, dark_hero=True, noindex=False):
    canon = SITE + path
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    pre = ""
    if preload:
        ws = sizes_for(preload)
        pre = (f'\n  <link rel="preload" as="image" type="image/webp" fetchpriority="high" '
               f'imagesrcset="{", ".join(f"/{IMG}/{preload}-{x}.webp {x}w" for x in ws)}" imagesizes="100vw">')
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large"
    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <script>document.documentElement.className+=' js'</script>
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{canon}">
  <meta name="theme-color" content="#141216">
  <meta name="geo.region" content="IN-TN">
  <meta name="geo.placename" content="Chennai">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:locale" content="en_IN">
  <meta property="og:url" content="{canon}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:image" content="{og(image)}">
  <meta property="og:image:width" content="1600">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{og(image)}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@300;400;500;600&family=Josefin+Sans:wght@400;600&display=swap">{pre}
  <link rel="stylesheet" href="/assets/css/site.css?v={TODAY}">{schema}
</head>
<body class="{'has-hero' if dark_hero else 'no-hero'}">
<a class="skip" href="#main">Skip to content</a>
<header class="hdr" id="hdr">
  <div class="wrap hdr-in">
    <a class="logo" href="/" aria-label="{BRAND}, home">{LOGO}<span>Dreamour<em>Design</em></span></a>
    <nav class="nav" aria-label="Main">{nav}</nav>
    <a class="btn btn-pill hdr-cta" href="/dream-builder/">Dream Builder</a>
    <button class="burger" aria-expanded="false" aria-controls="overlay" aria-label="Open menu"><span></span><span></span></button>
  </div>
</header>
<div class="overlay" id="overlay" hidden>
  <nav class="ov-nav" aria-label="Mobile">
    <a href="/">Home</a>{"".join(f'<a href="{h}">{t}</a>' for h, t in NAV)}<a href="/dream-builder/">Dream Builder</a>
  </nav>
  <div class="ov-foot">
    <a href="tel:{PHONE_TEL}">{PHONE}</a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <div class="social"><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{I['ig']}</a><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{I['fb']}</a><a href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{I['wa']}</a></div>
  </div>
</div>
<main id="main">
{body}
</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr-cta">
      <p class="kicker">Start a project</p>
      <p class="ftr-big">Let's design<br><em>your dream.</em></p>
      <div class="ftr-links">
        <a class="ftr-link" href="mailto:{EMAIL}">{EMAIL}</a>
        <a class="ftr-link" href="tel:{PHONE_TEL}">{PHONE}</a>
      </div>
    </div>
    <div class="ftr-grid">
      <div>
        <a class="logo" href="/">{LOGO}<span>Dreamour<em>Design</em></span></a>
        <p class="ftr-tag">Architecture, interiors, landscape and furniture design. Founded by architect Ramyaa Yuvanesan in Chennai.</p>
      </div>
      <div>
        <h2 class="ftr-h">Studio</h2>
        <address>{STREET},<br>{CITY} – {PIN}, India</address>
        <a class="u-link" href="{MAPS}" target="_blank" rel="noopener">Get directions</a>
      </div>
      <div>
        <h2 class="ftr-h">Explore</h2>
        <ul class="ftr-nav"><li><a href="/about/">Studio</a></li><li><a href="/services/">Services</a></li><li><a href="/works/">Works</a></li><li><a href="/dream-builder/">Dream Builder</a></li><li><a href="/contact-us/">Contact</a></li></ul>
      </div>
      <div>
        <h2 class="ftr-h">Follow</h2>
        <div class="social"><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{I['ig']}</a><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{I['fb']}</a><a href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp">{I['wa']}</a></div>
      </div>
    </div>
    <div class="ftr-bottom">
      <p>© <span class="yr">{date.today().year}</span> Dreamour Multiventures. All rights reserved.</p>
      <nav aria-label="Legal"><a href="/terms-conditions/">Terms &amp; Conditions</a><a href="/home/privacy-policy/">Privacy Policy</a><a href="/return-and-cancellation/">Return &amp; Cancellation</a></nav>
    </div>
  </div>
</footer>
<a class="wa-fab" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">{I['wa']}</a>
<script src="/assets/js/site.js?v={TODAY}" defer></script>
</body>
</html>
"""

def page_hero(title, kicker, img, alt, lead="", crumbs=None, tall=False):
    cr = ""
    if crumbs:
        parts = ['<a href="/">Home</a>'] + [f'<a href="{u}">{esc(n)}</a>' for n, u in crumbs[:-1]] + [f'<span aria-current="page">{esc(crumbs[-1][0])}</span>']
        cr = f'<nav class="crumbs" aria-label="Breadcrumb">{"<i>/</i>".join(parts)}</nav>'
    return f"""<section class="phero{' phero-tall' if tall else ''}">
  <div class="phero-media" data-parallax="0.25">{pic(img, alt, eager=True)}</div>
  <div class="wrap phero-in">
    {cr}
    <p class="kicker light">{kicker}</p>
    <h1 class="tsplit">{title}</h1>
    {f'<p class="phero-lead">{lead}</p>' if lead else ''}
  </div>
</section>"""

STATS = """<div class="stats">
  <div><span class="stat-n" data-count="60">60</span><span class="stat-p">+</span><p>Projects designed</p></div>
  <div><span class="stat-n" data-count="12">12</span><span class="stat-p">+</span><p>Partner contractors</p></div>
  <div><span class="stat-n" data-count="100">100</span><span class="stat-p">+</span><p>Happy customers</p></div>
</div>"""

def cta_band(img="statue-night"):
    return f"""<section class="band band-cta">
  <div class="band-media" data-parallax="0.3">{pic(img, "", attrs=' aria-hidden="true"')}</div>
  <div class="wrap band-in center">
    <p class="kicker light">Dream Builder</p>
    <h2 class="display light">Give life to <em>your dream</em></h2>
    <p class="band-lead">Take our 2-minute questionnaire, structured to understand your unique taste and design preferences.</p>
    <a class="btn btn-light" href="/dream-builder/">Get started {I['arrow']}</a>
  </div>
</section>"""

def proj_card(p, i=0, sizes="(max-width: 700px) 100vw, (max-width: 1100px) 50vw, 33vw"):
    return f"""<a class="pcard reveal" href="/works/{p['slug']}/" data-cat="{p['cat']}">
  <div class="pcard-img">{pic(p['hero'], f"{p['name']}, {p['loc']}", sizes=sizes)}</div>
  <div class="pcard-body">
    <p class="pcard-meta"><span>{CATS[p['cat']]}</span><span>{p['year']}</span></p>
    <h3>{esc(p['name'])}</h3>
    <p class="pcard-loc">{esc(p['loc'])} · {p['area']}</p>
  </div>
</a>"""

# ================================================================== HOME
feat = ["ryst-house", "cluster-house", "roundabout-egmore", "rasi-home"]
feat_html = ""
for i, slug in enumerate(feat):
    p = P[slug]
    feat_html += f"""
    <article class="feat{' feat-rev' if i % 2 else ''}">
      <a class="feat-media" href="/works/{slug}/" tabindex="-1" aria-hidden="true"><div data-parallax="0.12">{pic(p['hero'], '', sizes='(max-width: 900px) 100vw, 62vw')}</div></a>
      <div class="feat-card reveal">
        <p class="feat-no">0{i+1}</p>
        <p class="kicker">{CATS[p['cat']]} · {p['year']}</p>
        <h3 class="display-sm"><a href="/works/{slug}/">{esc(p['name'])}</a></h3>
        <p class="feat-loc">{esc(p['loc'])} · {p['area']}</p>
        <p>{esc(p['desc'])}</p>
        <a class="u-link" href="/works/{slug}/">View project {I['arrow']}</a>
      </div>
    </article>"""

svc_rows = "".join(f"""
      <a class="svc-row reveal" href="/services/#{s['id']}" data-img="/{IMG}/{s['img']}-800.webp">
        <span class="svc-no">{s['no']}</span>
        <span class="svc-name">{s['name']}</span>
        <span class="svc-short">{s['short']}</span>
        <span class="svc-arrow">{I['arrow']}</span>
      </a>""" for s in SERVICES)

home = f"""<section class="hero">
  <div class="hero-media" data-hero>{pic('ryst-night-front', 'RYST House, a beach house in Cheyyur designed by Dreamour Design, lit up at night', eager=True)}</div>
  <div class="wrap hero-in">
    <p class="kicker light hero-k">Architecture · Interiors · Landscape — Chennai</p>
    <h1 class="hero-title tsplit">Your dream,<br><em>our design.</em></h1>
    <p class="hero-lead">An architecture and interior design studio founded by architect Ramyaa Yuvanesan, creating homes, interiors and landscapes across Tamil Nadu.</p>
    <div class="hero-ctas">
      <a class="btn btn-light" href="/works/">Explore our works {I['arrow']}</a>
      <a class="btn btn-ghost" href="/dream-builder/">Start your Dream Builder</a>
    </div>
  </div>
  <div class="wrap hero-foot">
    <a class="hero-feature" href="/works/ryst-house/"><span>Featured</span>RYST House, Cheyyur</a>
    <span class="scroll-cue" aria-hidden="true"><i></i>Scroll</span>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track">
  {"".join(f"<span>{s['name']}</span><b>✦</b>" for s in SERVICES * 4)}
</div></div>

<section class="sec">
  <div class="wrap intro">
    <p class="kicker">The studio</p>
    <p class="statement fill-text">Where creativity meets functionality. We craft spaces that are both beautiful and functional, with smart, sustainable design that brings together light, space, nature, colour and materials.</p>
    <div class="intro-foot">
      {STATS}
      <a class="btn btn-dark" href="/about/">About the studio {I['arrow']}</a>
    </div>
  </div>
</section>

<section class="sec sec-dark svc-sec">
  <div class="wrap">
    <div class="sec-head">
      <p class="kicker light">What we do</p>
      <h2 class="display light">Four disciplines, <em>one vision</em></h2>
    </div>
    <div class="svc-list">{svc_rows}
    </div>
  </div>
  <div class="svc-float" aria-hidden="true"><img alt=""></div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head row">
      <div><p class="kicker">Selected works</p><h2 class="display">Spaces we've <em>shaped</em></h2></div>
      <a class="u-link" href="/works/">All projects {I['arrow']}</a>
    </div>
    <div class="feats">{feat_html}
    </div>
  </div>
</section>

<section class="band band-quote">
  <div class="band-media" data-parallax="0.3">{pic('int-living-view', '', attrs=' aria-hidden="true"')}</div>
  <div class="wrap band-in">
    <blockquote class="quote">
      <p>“Our goal is to enhance everyday living, improving lives through <em>design and innovation.</em>”</p>
      <footer>— Dreamour philosophy</footer>
    </blockquote>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <p class="kicker">How we work</p>
      <h2 class="display">From a dream <em>to drawings</em></h2>
    </div>
    <ol class="process">
      <li class="reveal"><span>01</span><h3>Dream Builder</h3><p>Share your taste in our 2-minute questionnaire: what you're building, the style you love and how you balance function with aesthetics.</p></li>
      <li class="reveal"><span>02</span><h3>Concept</h3><p>Site-sensitive conceptual and schematic design, shaped around your brief and the character of your plot.</p></li>
      <li class="reveal"><span>03</span><h3>Design development</h3><p>Detailed design, visualisations and complete construction drawings, so you see it before it's built.</p></li>
      <li class="reveal"><span>04</span><h3>Build support</h3><p>We assist with contractor bidding and negotiation, and work with our carpenters on bespoke furniture.</p></li>
    </ol>
  </div>
</section>

{cta_band()}
"""
write("/", layout("/", "Architects & Interior Designers in Chennai | Dreamour Design",
     "Chennai architecture, interior and landscape design studio founded by architect Ramyaa Yuvanesan. Homes, interiors and landscapes across Tamil Nadu.",
     home, active="", schema=ld(ORG), preload="ryst-night-front"))

# ================================================================== ABOUT
about = f"""{page_hero("The <em>studio</em>", "About Dreamour", "rasi-night", "Rasi Home apartment in Velachery at dusk",
   "Where creativity meets functionality.", crumbs=[("Studio", "/about/")])}

<section class="sec">
  <div class="wrap split">
    <div class="split-l"><p class="kicker">Our story</p><h2 class="display">Designing to <em>enhance everyday living</em></h2></div>
    <div class="split-r prose-lg">
      <p class="dropcap">Welcome to Dreamour Multiventures, where creativity meets functionality. Established by the visionary architect <strong>Ramyaa Yuvanesan</strong>, we began our journey as a premier provider of architectural solutions. Over the years, our passion for design and innovation has led us to expand into diverse fields, creating a unique blend of expertise and excellence.</p>
      <p>At our core, we remain dedicated to transforming spaces through exceptional architectural, interior design and landscape services. Our mission is to enhance the quality of life by crafting environments that are both beautiful and functional. We believe in smart, sustainable design, integrating elements like light, space, nature, colour and materials to create harmonious and inspiring spaces.</p>
    </div>
  </div>
  <div class="wrap">{STATS}</div>
</section>

<section class="band band-short">
  <div class="band-media" data-parallax="0.3">{pic('ryst-day', '', attrs=' aria-hidden="true"')}</div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head"><p class="kicker">Our ventures</p><h2 class="display">One family, <em>three ventures</em></h2></div>
    <div class="ventures">
      <article class="venture reveal">
        <div class="venture-mark v-dd">{LOGO}</div>
        <h3>Architectural solutions</h3>
        <p>Architecture, interior design and landscape services that transform spaces, from homes and apartments to campuses and public landscapes.</p>
        <a class="u-link" href="/services/">Our services {I['arrow']}</a>
      </article>
      <article class="venture reveal">
        <div class="venture-mark"><img src="/assets/img/amazon.png" alt="Available at Amazon" width="300" height="145" loading="lazy"></div>
        <h3>Premium cookware &amp; appliances</h3>
        <p>A proud premium seller on Amazon India, offering a curated selection of high-quality cookware and appliances that bring elegance and efficiency to your kitchen.</p>
      </article>
      <article class="venture reveal">
        <div class="venture-mark"><img src="/assets/img/ryst-toys.png" alt="RYST Toys" width="400" height="200" loading="lazy"></div>
        <h3>RYST wooden educational toys</h3>
        <p>Toys crafted to inspire young minds, promoting creativity and learning through play. Safe, durable and thoughtfully designed to foster educational development.</p>
        <a class="u-link" href="https://toys.ryst.in/" target="_blank" rel="noopener">Visit RYST Toys {I['arrow']}</a>
      </article>
    </div>
  </div>
</section>

<section class="sec sec-tint">
  <div class="wrap two">
    <div class="reveal"><p class="kicker">Our philosophy</p><p class="lead-serif">Though our fields of expertise may seem diverse, they are all connected by a common thread: our dedication to improving lives through design and innovation.</p></div>
    <div class="reveal"><p class="kicker">Our team</p><p class="lead-serif">A passionate, multidisciplinary team of architects, designers, engineers and craftsmen, delivering personalised and innovative solutions to the highest standards.</p></div>
  </div>
</section>
{cta_band("hall-front")}
"""
write("/about/", layout("/about/", "About Architect Ramyaa Yuvanesan & Studio | Dreamour Design",
     "Founded by architect Ramyaa Yuvanesan in Chennai: architecture, interiors and landscape, plus premium cookware and RYST wooden educational toys.",
     about, image="rasi-night", active="/about/", schema=crumbs_ld([("Home", "/"), ("Studio", "/about/")]), preload="rasi-night"))

# ================================================================== SERVICES
svc_sections = ""
for i, s in enumerate(SERVICES):
    rel = "".join(f'<a href="/works/{slug}/">{esc(P[slug]["name"])}</a>' for slug in s["projects"])
    svc_sections += f"""
  <article class="svc-block{' rev' if i % 2 else ''}" id="{s['id']}">
    <div class="svc-media"><div data-parallax="0.1">{pic(s['img'], s['name'] + ' by Dreamour Design', sizes='(max-width: 900px) 100vw, 55vw')}</div></div>
    <div class="svc-text reveal">
      <p class="svc-big-no">{s['no']}</p>
      <h2 class="display-sm">{s['name']}</h2>
      <p>{s['body']}</p>
      <ul class="ticks">{''.join(f'<li>{x}</li>' for x in s['points'])}</ul>
      <p class="rel"><span>Related work</span>{rel}</p>
    </div>
  </article>"""
services = f"""{page_hero("Our <em>services</em>", "What we do", "round-overview", "Roundabout landscape design in Egmore, Chennai",
   "From the first sketch to the last piece of furniture.", crumbs=[("Services", "/services/")])}
<nav class="subnav" aria-label="Services"><div class="wrap">{''.join(f'<a href="#{s["id"]}">{s["name"]}</a>' for s in SERVICES)}</div></nav>
<section class="sec svc-page"><div class="wrap">{svc_sections}
</div></section>
{cta_band()}
"""
svc_ld = {"@context": "https://schema.org", "@graph": [
    {"@type": "Service", "name": s["name"], "description": s["body"], "serviceType": s["name"],
     "provider": {"@id": f"{SITE}/#business"}, "areaServed": "Tamil Nadu", "url": f"{SITE}/services/#{s['id']}"} for s in SERVICES]}
write("/services/", layout("/services/", "Architecture & Interior Design Services, Chennai | Dreamour",
     "Architecture, interior, landscape and bespoke furniture design in Chennai: concept design, construction drawings, visualisation and contractor support.",
     services, image="round-overview", active="/services/", schema=crumbs_ld([("Home", "/"), ("Services", "/services/")]) + ld(svc_ld), preload="round-overview"))

# ================================================================== WORKS
counts = {c: sum(1 for p in PROJECTS if p["cat"] == c) for c in CATS}
works = f"""{page_hero("Our <em>works</em>", "Portfolio", "mass-farm", "Landscape design for a 20-acre estate in Gummidipoondi",
   "Homes, interiors and landscapes across Chennai and Tamil Nadu.", crumbs=[("Works", "/works/")])}
<section class="sec">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter projects">
      <button class="chip on" data-f="all" aria-pressed="true">All <sup>{len(PROJECTS)}</sup></button>
      {''.join(f'<button class="chip" data-f="{c}" aria-pressed="false">{n} <sup>{counts[c]}</sup></button>' for c, n in CATS.items())}
    </div>
    <div class="pgrid">{''.join(proj_card(p, i) for i, p in enumerate(PROJECTS))}</div>
  </div>
</section>
{cta_band()}
"""
works_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Our Works", "url": f"{SITE}/works/",
            "mainEntity": {"@type": "ItemList", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/works/{p['slug']}/", "name": p["name"]} for i, p in enumerate(PROJECTS)]}}
write("/works/", layout("/works/", "Our Works – Architecture & Interior Projects | Dreamour Design",
     "Projects by Dreamour Design: RYST House in Cheyyur, Rasi Home in Velachery, H-House, Cluster House interiors, the Egmore roundabout and more.",
     works, image="mass-farm", active="/works/", schema=crumbs_ld([("Home", "/"), ("Works", "/works/")]) + ld(works_ld), preload="mass-farm"))

# ================================================================== PROJECT PAGES
for idx, p in enumerate(PROJECTS):
    prev_p = PROJECTS[idx - 1]
    next_p = PROJECTS[(idx + 1) % len(PROJECTS)]
    gal = "".join(f"""<a class="g-item reveal" href="{full(n)}" data-lb="g" data-cap="{esc(c)}">{pic(n, f"{p['name']}: {c}", sizes='(max-width: 700px) 100vw, 50vw')}<span class="g-zoom">{I['zoom']}</span></a>""" for n, c in p["gallery"])
    related = [q for q in PROJECTS if q["cat"] == p["cat"] and q["slug"] != p["slug"]][:3]
    body = f"""{page_hero(esc(p['name']), f"{CATS[p['cat']]} · {p['type']}", p['hero'], f"{p['name']}, {p['loc']}",
        crumbs=[("Works", "/works/"), (p["name"], f"/works/{p['slug']}/")], tall=True)}
<section class="sec">
  <div class="wrap">
    <dl class="facts reveal">
      <div><dt>Location</dt><dd>{esc(p['loc'])}</dd></div>
      <div><dt>Area</dt><dd>{p['area']}</dd></div>
      <div><dt>Year</dt><dd>{p['year']}</dd></div>
      <div><dt>Discipline</dt><dd>{CATS[p['cat']]}</dd></div>
    </dl>
    <div class="proj-intro">
      <p class="lead-serif reveal">{esc(p['desc'])}</p>
      {f'<p class="proj-more reveal">{p["more"]}</p>' if p['more'] else ''}
    </div>
    <div class="gallery g-{min(len(p['gallery']), 3)}">{gal}</div>
  </div>
</section>
<nav class="pnav" aria-label="More projects">
  <a class="pnav-l" href="/works/{prev_p['slug']}/"><span>Previous</span>{esc(prev_p['name'])}</a>
  <a class="pnav-all" href="/works/" aria-label="All projects"><i></i><i></i><i></i><i></i></a>
  <a class="pnav-r" href="/works/{next_p['slug']}/"><span>Next</span>{esc(next_p['name'])}</a>
</nav>
{f'''<section class="sec sec-tint"><div class="wrap"><div class="sec-head row"><div><p class="kicker">More {CATS[p['cat']].lower()}</p><h2 class="display">Related <em>projects</em></h2></div><a class="u-link" href="/works/">All projects {I['arrow']}</a></div><div class="pgrid">{''.join(proj_card(q) for q in related)}</div></div></section>''' if related else ''}
{cta_band()}
<dialog class="lb" aria-label="Photo viewer">
  <button class="lb-x" aria-label="Close">×</button>
  <button class="lb-prev" aria-label="Previous photo">‹</button>
  <figure><img alt=""><figcaption></figcaption></figure>
  <button class="lb-next" aria-label="Next photo">›</button>
</dialog>
"""
    cw = {"@context": "https://schema.org", "@type": "CreativeWork", "name": p["name"], "description": p["desc"],
          "genre": CATS[p["cat"]], "dateCreated": p["year"], "url": f"{SITE}/works/{p['slug']}/",
          "image": [og(n) for n, _ in p["gallery"]], "creator": {"@id": f"{SITE}/#business"},
          "locationCreated": {"@type": "Place", "name": p["loc"]}}
    write(f"/works/{p['slug']}/", layout(f"/works/{p['slug']}/",
        f"{p['name']}, {p['loc'].split(',')[0]} | Dreamour Design",
        clip(f"{p['name']} by Dreamour Design: {p['area']} {p['type'].lower()} in {p['loc']}, {p['year']}. {p['desc']}"),
        body, image=p["hero"], active="/works/", preload=p["hero"],
        schema=crumbs_ld([("Home", "/"), ("Works", "/works/"), (p["name"], f"/works/{p['slug']}/")]) + ld(cw)))

# ================================================================== CONTACT
contact = f"""{page_hero("Let's <em>talk</em>", "Contact", "h-house", "H-House residence in Kottivakkam, Chennai",
   "Tell us about your plot, your home or your idea. We'll take it from there.", crumbs=[("Contact", "/contact-us/")])}
<section class="sec">
  <div class="wrap contact">
    <div class="c-info">
      <div class="c-item reveal"><span class="c-ic">{I['pin']}</span><div><h2>Studio</h2><address>{STREET},<br>{CITY} – {PIN}, India</address><a class="u-link" href="{MAPS}" target="_blank" rel="noopener">Get directions {I['arrow']}</a></div></div>
      <div class="c-item reveal"><span class="c-ic">{I['phone']}</span><div><h2>Phone</h2><p><a href="tel:{PHONE_TEL}">{PHONE}</a></p><a class="u-link" href="https://wa.me/{WA}" target="_blank" rel="noopener">Chat on WhatsApp {I['arrow']}</a></div></div>
      <div class="c-item reveal"><span class="c-ic">{I['mail']}</span><div><h2>Email</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div>
      <div class="c-item reveal"><span class="c-ic">{I['ig']}</span><div><h2>Follow</h2><p><a href="{IG}" target="_blank" rel="noopener">@design.dreamour.in</a></p></div></div>
    </div>
    <form class="form" id="contact-form" data-subject="Enquiry from design.dreamour.in" novalidate>
      <h2 class="display-sm">Leave us a <em>message</em></h2>
      <div class="f-row">
        <div class="field"><input id="cf-name" name="Name" autocomplete="name" placeholder=" " required><label for="cf-name">Your name *</label></div>
        <div class="field"><input id="cf-phone" name="Phone" type="tel" inputmode="tel" autocomplete="tel" placeholder=" " required><label for="cf-phone">Phone *</label></div>
      </div>
      <div class="field"><input id="cf-email" name="Email" type="email" autocomplete="email" placeholder=" "><label for="cf-email">Email</label></div>
      <div class="field"><select id="cf-type" name="Interested in"><option>Architecture design</option><option>Interior design</option><option>Landscape design</option><option>Product / furniture design</option><option>Something else</option></select><label for="cf-type" class="static">Interested in</label></div>
      <div class="field"><textarea id="cf-msg" name="Message" rows="4" placeholder=" " required></textarea><label for="cf-msg">Tell us about your project *</label></div>
      <div class="f-send">
        <button class="btn btn-dark" type="submit" value="whatsapp">{I['wa']} Send on WhatsApp</button>
        <button class="btn btn-line" type="submit" value="email">{I['mail']} Send by email</button>
      </div>
      <p class="f-note" role="status" aria-live="polite"></p>
    </form>
  </div>
  <div class="wrap"><iframe class="map" title="Map: Dreamour Design studio, Kilpauk, Chennai" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</section>
"""
contact_ld = {"@context": "https://schema.org", "@type": "ContactPage", "url": f"{SITE}/contact-us/", "about": {"@id": f"{SITE}/#business"}}
write("/contact-us/", layout("/contact-us/", "Contact Dreamour Design – Architects in Kilpauk, Chennai",
     f"Visit our Kilpauk, Chennai studio, call or WhatsApp {PHONE}, or email {EMAIL} to start your architecture or interior project.",
     contact, image="h-house", active="/contact-us/", preload="h-house",
     schema=crumbs_ld([("Home", "/"), ("Contact", "/contact-us/")]) + ld(contact_ld)))

# ================================================================== DREAM BUILDER
def chips(name, opts, kind="radio", img=False):
    out = ""
    for o in opts:
        im = f'<img src="/assets/img/shape-{o.lower()}.jpg" alt="" width="120" height="120" loading="lazy">' if img else ""
        out += f'<label class="opt{" opt-img" if img else ""}"><input type="{kind}" name="{name}" value="{o}">{im}<span>{o}</span></label>'
    return out

STEPS = [
 ("About you", f"""<div class="f-row">
    <div class="field"><input id="db-name" name="Name" autocomplete="name" placeholder=" " required><label for="db-name">Your name *</label></div>
    <div class="field"><input id="db-phone" name="Phone" type="tel" inputmode="tel" autocomplete="tel" placeholder=" " required><label for="db-phone">Phone *</label></div>
  </div>
  <div class="field"><input id="db-email" name="Email" type="email" autocomplete="email" placeholder=" " required><label for="db-email">Email *</label></div>
  <p class="hint">We'll use these only to follow up on your dream.</p>""", ["Name", "Phone", "Email"]),
 ("I am building a…", f'<div class="opts big" data-req="Building">{chips("Building", ["Dream house", "Work space", "Other"])}</div>', ["Building"]),
 ("Design requirement", f'<p class="hint">Choose all that apply.</p><div class="opts big" data-req="Requirement">{chips("Requirement", ["Layout", "Interiors", "Landscape", "Product"], "checkbox")}</div>', ["Requirement"]),
 ("I want my dream building to be…", f'<div class="opts big" data-req="Style">{chips("Style", ["Lavish", "Compact", "Ergonomic"])}</div>', ["Style"]),
 ("What's your preferred shape?", f'<div class="opts" data-req="Shape">{chips("Shape", ["Circular", "Squarish", "Pointed"], img=True)}</div>', ["Shape"]),
 ("Function vs aesthetics", """<p class="hint">Slide your balance between design functionality and aesthetics.</p>
  <div class="range"><span>Function</span><input type="range" name="Balance" min="-5" max="5" step="1" value="0" aria-label="Balance between function (−5) and aesthetics (5)"><span>Aesthetics</span></div>
  <p class="range-out">Selected value <output>0</output></p>""", []),
 ("Anything else?", '<div class="field"><textarea id="db-other" name="Other preferences" rows="5" placeholder=" "></textarea><label for="db-other">Location, plot size, budget, timeline, styles you love…</label></div>', []),
]
steps_html = "".join(f"""
    <fieldset class="step" data-step="{i}" data-need="{','.join(need)}">
      <legend><span class="step-no">{i+1:02d}<i>/ {len(STEPS):02d}</i></span>{t}</legend>
      {c}
    </fieldset>""" for i, (t, c, need) in enumerate(STEPS))
builder = f"""{page_hero("Dream <em>Builder</em>", "2-minute questionnaire", "ryst-day-back", "RYST House beach house in Cheyyur",
   "Give life to your dream. Tell us your taste and preferences before we meet.", crumbs=[("Dream Builder", "/dream-builder/")])}
<section class="sec">
  <div class="wrap narrow">
    <form class="form wizard" id="builder-form" data-subject="Dream Builder questionnaire" novalidate>
      <div class="w-progress" aria-hidden="true"><i></i></div>
      {steps_html}
      <div class="w-nav">
        <button class="btn btn-line w-back" type="button">Back</button>
        <button class="btn btn-dark w-next" type="button">Next {I['arrow']}</button>
      </div>
      <div class="f-send w-send">
        <button class="btn btn-dark" type="submit" value="whatsapp">{I['wa']} Send on WhatsApp</button>
        <button class="btn btn-line" type="submit" value="email">{I['mail']} Send by email</button>
      </div>
      <p class="f-note" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>
"""
write("/dream-builder/", layout("/dream-builder/", "Dream Builder – Tell Us Your Design Taste | Dreamour Design",
     "Take Dreamour Design's 2-minute Dream Builder questionnaire: what you're building, your style, preferred shapes and the balance of function and aesthetics.",
     builder, image="ryst-day-back", preload="ryst-day-back", schema=crumbs_ld([("Home", "/"), ("Dream Builder", "/dream-builder/")])))

# ================================================================== LEGAL
LEGAL = os.path.join(ROOT, "_build", "legal")
for slug, title, desc in [
    ("terms-conditions", "Terms &amp; Conditions", "Terms and conditions for using the Dreamour Design website and services."),
    ("home/privacy-policy", "Privacy Policy", "How Dreamour Design collects and uses information when you visit design.dreamour.in."),
    ("return-and-cancellation", "Return &amp; Cancellation Policy", "Return and cancellation policy for Dreamour Design architectural services and products."),
]:
    with open(os.path.join(LEGAL, slug.replace("/", "_") + ".html"), encoding="utf-8") as f:
        prose = f.read()
    body = f"""<section class="lhero"><div class="wrap narrow"><nav class="crumbs dark" aria-label="Breadcrumb"><a href="/">Home</a><i>/</i><span aria-current="page">{title}</span></nav><h1 class="display">{title}</h1></div></section>
<section class="sec sec-top0"><div class="wrap narrow prose">{prose}</div></section>"""
    write(f"/{slug}/", layout(f"/{slug}/", f"{H.unescape(title)} | Dreamour Design", desc, body, dark_hero=False))

# ================================================================== 404
nf = f"""<section class="nf">
  <div class="nf-media">{pic('statue-night', '', attrs=' aria-hidden="true"')}</div>
  <div class="wrap nf-in center">
    <p class="nf-code">404</p>
    <h1 class="display light">This space hasn't been <em>designed yet</em></h1>
    <p class="band-lead">The page you're looking for doesn't exist or has moved.</p>
    <div class="hero-ctas center-row"><a class="btn btn-light" href="/">Back to home</a><a class="btn btn-ghost" href="/works/">See our works</a></div>
  </div>
</section>"""
write("/404.html", layout("/404.html", "Page not found | Dreamour Design", "This page could not be found.", nf, noindex=True))

# ================================================================== SITEMAP etc.
urls = [("/", 1.0, ["ryst-night-front"]), ("/about/", .8, ["rasi-night"]), ("/services/", .9, [s["img"] for s in SERVICES]),
        ("/works/", .9, ["mass-farm"])] + [(f"/works/{p['slug']}/", .8, [n for n, _ in p["gallery"]]) for p in PROJECTS] + \
       [("/contact-us/", .8, ["h-house"]), ("/dream-builder/", .7, []), ("/terms-conditions/", .2, []),
        ("/home/privacy-policy/", .2, []), ("/return-and-cancellation/", .2, [])]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
for u, pr, imgs in urls:
    sm.append(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority>" +
              "".join(f"<image:image><image:loc>{og(n)}</image:loc></image:image>" for n in imgs) + "</url>")
sm.append("</urlset>\n")
open("sitemap.xml", "w").write("\n".join(sm))
open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {SITE}/sitemap.xml\n")
open("site.webmanifest", "w").write(json.dumps({"name": BRAND, "short_name": "Dreamour", "start_url": "/", "display": "standalone",
    "background_color": "#141216", "theme_color": "#141216",
    "icons": [{"src": "/assets/img/logo-dd.png", "sizes": "512x512", "type": "image/png"}]}, indent=2))
open("CNAME", "w").write("design.dreamour.in\n")
open(".nojekyll", "w").write("")
print("built", len(PROJECTS) + 10, "pages")
