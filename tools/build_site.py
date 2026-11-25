# -*- coding: utf-8 -*-
"""Builds the HD Events site pages from tools/site_content.py.

    python3 tools/build_site.py

Writes:  public/<slug>.html for every service page, the shared header/footer and
structured data into public/index.html, plus sitemap.xml, robots.txt, llms.txt,
_redirects and _headers. Old page files that have moved are removed.
"""
import datetime, html, json, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
from site_content import *  # noqa

ROOT = os.path.join(os.path.dirname(__file__), "..", "public")
TODAY = datetime.date.today().isoformat()
e = html.escape


def url(slug):
    return SITE + ("/" if slug in ("", "index") else "/" + slug)


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, indent=1).replace("</", "<\\/") + "</script>"


ORG_ID = SITE + "/#organization"
ORG = {
    "@type": "Organization", "@id": ORG_ID, "name": "HD Events", "url": SITE + "/",
    "logo": SITE + "/assets/logo.png", "image": SITE + "/assets/concorde-dinner.jpg",
    "description": "HD Events provides corporate audio visual hire and technical event production across London and the UK: sound systems, wireless microphones, presentation and relay screens, lighting and custom digital lecterns, supplied and operated by its own technical team.",
    "telephone": PHONE, "email": EMAIL, "sameAs": [INSTAGRAM],
    "areaServed": [{"@type": "City", "name": "London"}, {"@type": "Country", "name": "United Kingdom"}],
    "knowsAbout": ["Corporate audio visual hire", "Conference AV", "Awards ceremony production", "Gala dinner production",
                   "PA hire", "Wireless microphone hire", "Relay screens", "Event lighting", "Digital lecterns",
                   "Festival sound", "Dry hire", "AV installation"],
    "brand": [{"@type": "Brand", "name": b} for b in BRANDS],
}


# ---------- Shared pieces ----------
def header(active=None):
    items = []
    for label, target in MENU:
        if isinstance(target, list):
            sub = "".join(
                f'<li><a href="{"/" + s if not s.startswith("/") else s}"><b>{e(l)}</b><span>{e(d)}</span></a></li>' for l, s, d in target)
            cur = ' class="current"' if active == label else ""
            items.append(f'<li class="has-sub"><button type="button" aria-expanded="false"{cur}>{e(label)} <span aria-hidden="true">▾</span></button><ul class="sub">{sub}</ul></li>')
        else:
            cur = ' aria-current="page"' if active == label else ""
            items.append(f'<li><a href="/{target}"{cur}>{e(label)}</a></li>')
    return f'''<header class="site-header">
  <a class="brand" href="/" aria-label="HD Events home"><img src="/assets/logo.png" alt="HD Events" width="164" height="77"></a>
  <nav class="main-nav" id="mainNav" aria-label="Main navigation"><ul>{"".join(items)}</ul>
    <a class="button solid nav-cta" href="{QUOTE}" data-enquiry>Request a quote <span>↗</span></a></nav>
  <a class="header-driver" href="/av-delivery-collection#book"><small>Need transport?</small><b>Book a driver <i aria-hidden="true">→</i></b></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mainNav"><span class="bars" aria-hidden="true"></span><span class="label">Menu</span></button>
</header>'''


def footer():
    links = [(l, t) for l, t in MENU if not isinstance(t, list) and t != "events"] + [(l, s) for l, s, _ in MENU[-1][1]]
    svc = "".join(f'<li><a href="{"/" + s if not s.startswith("/") else s}">{e(l)}</a></li>' for l, s in links)
    return f'''<footer class="site-footer">
  <div class="footer-grid">
    <div class="footer-brand"><a class="brand" href="/"><img src="/assets/logo.png" alt="HD Events" width="130" height="65"></a>
      <p>Corporate audio visual hire and event production across London and the UK. Sound, screens, lighting and digital lecterns, supplied and operated by our own technical team.</p></div>
    <div><h2>Services</h2><ul>{svc}</ul></div>
    <div><h2>Contact</h2><ul><li><a href="tel:{PHONE_LINK}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us ↗</a></li><li><a href="{QUOTE}" data-enquiry>Request a quote ↗</a></li></ul></div>
    <div><h2>Follow</h2><ul><li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram ↗</a></li><li><a href="/events">Upcoming events</a></li></ul></div>
  </div>
  <div class="footer-base"><span>© {datetime.date.today().year} HD Events · Corporate audio visual hire · London &amp; nationwide</span><a href="#">Back to top ↑</a></div>
</footer>'''


WHATSAPP_BUTTON = f'<a class="wa-fixed" href="{WHATSAPP}" aria-label="Message HD Events on WhatsApp" target="_blank" rel="noopener"><svg viewBox="0 0 32 32" aria-hidden="true"><path fill="none" stroke="white" stroke-width="2" d="M5 22a12 12 0 1 1 5 5l-7 2z"/><path fill="white" d="M11 9c-2 0-3 2-2 5 2 5 5 8 10 9 2 0 4-1 4-4l-4-2-2 2c-2-1-4-3-5-5l1-2-1-3z"/></svg><span>Message us</span></a>'
DIALOG = f'<dialog id="enquiry"><div class="dialog-head"><h2>Tell us about your event.</h2><button id="close-enquiry" aria-label="Close enquiry form">×</button></div><p>Share the date, venue and what you need, and we will reply with recommendations and a quote.</p><iframe title="HD Events enquiry form" name="lc_contact_form" width="100%" height="600" src="{QUOTE}" loading="lazy"></iframe><div class="dialog-contact"><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us: {PHONE} ↗</a><a href="tel:{PHONE_LINK}">Call {PHONE}</a><a href="mailto:{EMAIL}">Email {EMAIL} ↗</a></div></dialog>'
LX_SUMMARY = '<section id="lxBuildSummary" hidden><label for="lxSpec">Your lectern build</label><textarea id="lxSpec" readonly rows="5" style="width:100%"></textarea><button type="button" id="lxCopy">Copy build details</button><p id="lxCopyStatus" aria-live="polite">Paste your build into the enquiry details below.</p></section>'
HEAD_COMMON = '''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#050609">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">'''


def social(title, desc, page_url, image):
    return f'''<link rel="canonical" href="{page_url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="HD Events">
<meta property="og:locale" content="en_GB">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{page_url}">
<meta property="og:image" content="{SITE}/assets/{image}">
<meta name="twitter:card" content="summary_large_image">'''


def faq_html(faqs):
    items = "".join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faqs)
    return f'<div class="faq-list">{items}</div>'


def packages_block():
    """Reuse the package cards from the home page so prices stay in one place."""
    src = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    m = re.search(r'<div class="package-grid">.*?\n    </div>\n', src, re.S)
    return m.group(0) if m else ""


def money(n):
    return f"£{n:,.0f}"


def lectern_section():
    L = LECTERN
    inc = "".join(f"<li>{e(x)}</li>" for x in L["included"])
    def opt(u, n, d, pr, mon):
        return (f'<label class="opt"><input type="checkbox" value="{u}" data-price="{"" if pr is None else pr}" data-name="{e(n)}"{" data-monitor" if mon else ""}>'
                f'<span class="opt-box"><b>{e(n)}</b><span>{e(d)}</span></span><span class="opt-price">{"+ " + money(pr) if pr is not None else "Price on request"}</span></label>')
    order = ["Speaker screen (choose one)", "Microphones", "Finish & branding", "Built-in extras", "Protection & transport"]
    groups = sorted({g for *_, g in L["upgrades"]}, key=lambda g: order.index(g) if g in order else 99)
    rows = "\n".join(f'<fieldset class="opt-group"><legend>{e(g)}</legend>' + "".join(opt(*x[:5]) for x in L["upgrades"] if x[5] == g) + '</fieldset>' for g in groups)
    table = "".join(f'<tr><td>{e(n)}</td><td>{e(d)}</td><td>{money(pr) if pr is not None else "On request"}</td></tr>' for u, n, d, pr, mon, g in L["upgrades"])
    lead = f'<li><b>Lead time</b>{e(L["lead_time"])}</li>' if L["lead_time"] else ""
    show = "".join(f'<figure><img src="/assets/{img}" alt="{e(cap)}" loading="lazy"><figcaption>{e(cap)}</figcaption></figure>' for img, cap in L["showcase"])
    showcase = f'<section class="lx-show" aria-labelledby="show-title"><div class="section-intro"><p class="eyebrow"><i></i> SEE IT IN ACTION</p><h2 id="show-title">Built for the<br>moments that matter.</h2></div><div class="lx-show-row">{show}</div></section>'
    return showcase + f'''<section class="lx" id="build" aria-labelledby="build-title">
    <div class="section-intro"><p class="eyebrow"><i></i> BUILD YOUR LECTERN</p><h2 id="build-title">Choose your<br><span>specification.</span></h2>
    <p>Start with our standard digital lectern, add the upgrades you need, and send us your specification. We will confirm a fixed price and build date.</p></div>
    <div class="lx-grid">
      <div class="lx-base"><p class="eyebrow">STANDARD BUILD</p><h3>{e(L["base_name"])}</h3><p class="lx-from">From <b>{money(L["base_price"])}</b> <small>ex VAT</small></p>
        <ul class="lx-inc">{inc}</ul>
        <ul class="lx-facts"><li><b>Buy</b>Built to order, delivered and installed UK-wide</li><li><b>Hire</b>{e(L["hire_note"])}</li>{lead}</ul></div>
      <form class="lx-config" aria-label="Choose upgrades">
        <p class="eyebrow">ADD UPGRADES <small>Tick what you need. The total updates as you go.</small></p>{rows}
        <div class="lx-total" id="lxSend" aria-live="polite"><div><span>Your build from</span><b id="lxTotal" class="lx-total-figure">{money(L["base_price"])}</b><small id="lxNote">ex VAT</small></div>
          <div class="hero-actions"><button class="button solid" id="lxEnquire" type="button">Enquire about this build</button><a class="button" id="lxWhatsApp" href="{WHATSAPP}" target="_blank" rel="noopener">Send spec on WhatsApp <span>↗</span></a><a class="button" id="lxEmail" href="mailto:{EMAIL}">Email my spec <span>↗</span></a></div>
          <p class="hint">No commitment. We reply with a fixed quote and build date.</p></div>
      </form>
    </div>
    <div class="lx-mini" id="lxMini" hidden><span><small id="lxMiniCount">Standard build</small><b id="lxMiniTotal">{money(L["base_price"])}</b></span><a class="button solid small" href="#lxSend">Send my build <span>↓</span></a></div>
    <div class="lx-table-wrap" id="prices"><h3>Price list</h3><table class="lx-table"><thead><tr><th>Item</th><th>What it does</th><th>Price</th></tr></thead>
      <tbody><tr><td><b>{e(L["base_name"])}</b></td><td>Standard build, as above</td><td><b>{money(L["base_price"])}</b></td></tr>{table}
      <tr><td><b>Hire</b></td><td>Per day, on its own or with a full AV package</td><td><b>{money(L["hire_price"])}/day</b> + delivery</td></tr></tbody></table><p class="hint">All prices exclude VAT and delivery. Final price confirmed on quote.</p></div>
    <script type="application/json" id="lxData">{json.dumps({"base": L["base_price"], "name": L["base_name"]})}</script>
  </section>'''


def buy_or_hire():
    L = LECTERN
    hire_msg = "Hi HD Events, I would like to hire a digital lectern.\n\nEvent date:\nVenue / town:\nHow many lecterns:\nAnything else (mics, screens, sound):"
    from urllib.parse import quote
    return f'''<section class="choose" id="hire" aria-labelledby="choose-title">
    <div class="section-intro"><p class="eyebrow"><i></i> BUY OR HIRE</p><h2 id="choose-title">Two ways to get one.</h2></div>
    <div class="choose-grid">
      <article class="choose-card"><p class="eyebrow">BUY</p><h3>Built for your venue</h3><p class="choose-price">From <b>{money(L["base_price"])}</b> <small>ex VAT</small></p>
        <p>For venues that host speakers often: conference centres, hotels, universities, councils and offices. Choose your options below and see the price as you go.</p>
        <a class="button solid" href="#build">Build &amp; price yours <span>↓</span></a> <a class="text-link" href="#prices">See the full price list</a></article>
      <article class="choose-card"><p class="eyebrow">HIRE</p><h3>For a single event</h3><p class="choose-price">From <b>{money(L["hire_price"])}</b><small>/day + delivery</small></p>
        <p>For a conference, awards night, AGM or launch. Hire a lectern on its own, or with sound, microphones and screens from our corporate AV hire.</p>
        <a class="button solid" href="{WHATSAPP}?text={quote(hire_msg)}" target="_blank" rel="noopener">Check availability on WhatsApp <span>↗</span></a> <a class="text-link" href="{QUOTE}" data-enquiry>Or send an enquiry</a></article>
    </div>
  </section>'''


def facts_strip(facts):
    return '<section class="facts" aria-label="At a glance"><ul>' + "".join(f"<li><b>{e(a)}</b><span>{e(b)}</span></li>" for a, b in facts) + "</ul></section>"


def delivery_quote():
    return f'''<section class="dq" id="book" aria-labelledby="dq-title">
    <div class="dq-wrap">
      <div class="dq-side"><p class="eyebrow"><i></i> BOOK A DRIVER</p><h2 id="dq-title">Tell us the run.<br><span>We’ll confirm a price.</span></h2>
        <p>Send us the details and we’ll come back with a fixed price, usually the same day. Delivery starts from £85 each way.</p>
        <ul class="dq-points"><li>An AV technician, not just a driver</li><li>Set up, crew and same-night collection if you need it</li><li>Nothing is booked until you agree the price</li></ul>
        <p class="dq-alt">Prefer to talk? <a href="tel:{PHONE_LINK}">Call {PHONE}</a></p></div>
      <form class="dq-form" id="dqForm" aria-label="Book a driver" novalidate>
        <fieldset class="dq-step"><legend><b>1</b> Your details</legend>
          <label class="dq-f"><span>Company <em>*</em></span><input name="company" required autocomplete="organization"></label><label class="dq-f"><span>Your name <em>*</em></span><input name="name" required autocomplete="name"></label><label class="dq-f"><span>Phone <em>*</em></span><input name="phone" required type="tel" autocomplete="tel"></label><label class="dq-f"><span>Email <em>*</em></span><input name="email" required type="email" autocomplete="email"></label></fieldset>
        <fieldset class="dq-step"><legend><b>2</b> The run</legend>
          <label class="dq-f"><span>Collection address <em>*</em></span><textarea name="from" rows="2" required placeholder="Address and postcode"></textarea></label><label class="dq-f"><span>Drop-off address <em>*</em></span><textarea name="to" rows="2" required placeholder="Venue and postcode"></textarea></label><label class="dq-f"><span>Date <em>*</em></span><input name="date" required type="date"></label><label class="dq-f"><span>Delivery time</span><input name="time" placeholder="e.g. on site by 2pm"></label>
          <label class="dq-f"><span>Collect back</span><select name="collect"><option>Same night, after the event</option><option>Next day</option><option>Another date</option><option>Delivery only</option></select></label>
          <label class="dq-f"><span>Extra stops</span><select name="stops"><option value="0">None</option><option value="1">1 extra stop</option><option value="2">2 extra stops</option><option value="3">3 or more</option></select></label></fieldset>
        <fieldset class="dq-step"><legend><b>3</b> Equipment and requirements</legend>
          <label class="dq-f wide"><span>What equipment is being moved? <em>*</em></span><textarea name="load" rows="2" required placeholder="e.g. 2 speakers, 2 subs, a desk in a case, 6 cable cases"></textarea></label>
          <div class="dq-chips wide" role="group" aria-label="What do you need from us?"><label><input type="checkbox" name="setup"><span>Set up &amp; test</span></label><label><input type="checkbox" name="crew"><span>Stay on as crew</span></label><label><input type="checkbox" name="other"><span>Another hire company</span></label><label><input type="checkbox" name="handball"><span>Extra hands to load</span></label></div>
          <label class="dq-f wide"><span>Anything else?</span><textarea name="needs" rows="2" placeholder="Access, parking, loading times, stairs or lifts, site contact"></textarea></label></fieldset>
        <div class="dq-send"><a class="button wa" id="dqWhatsApp" href="{WHATSAPP}" target="_blank" rel="noopener">Send on WhatsApp <span>↗</span></a><a class="button" id="dqEmail" href="mailto:{EMAIL}">Send by email <span>↗</span></a>
          <p class="hint" id="dqHint">Fields marked * are needed for a price.</p></div>
      </form>
    </div>
  </section>'''


DEFAULT_STEPS = [
    ("Share your brief", "Venue, date, running order, audience size and anything you already have in place."),
    ("We design the setup", "The right equipment for your venue, with a clear, itemised quote."),
    ("We deliver and operate", "On site before your guests, a technician throughout where needed, and a clean, discreet derig."),
]


def hero_actions(p):
    acts = p.get("hero_actions")
    if not acts:
        return f'<a class="button solid" href="{QUOTE}" data-enquiry>Request a quote <span>↗</span></a><a class="button" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us <span>↗</span></a>'
    out = []
    for i, (label, href, arrow) in enumerate(acts):
        ext = href == "WHATSAPP"
        out.append(f'<a class="button{" solid" if i == 0 else ""}" href="{WHATSAPP if ext else href}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}>{label} <span>{arrow}</span></a>')
    return "".join(out)


# ---------- Service page ----------
def service_page(slug, p):
    page_url = url(slug)
    services = "".join(f'<article class="svc-card"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t, d in p["services"])
    chips = "".join(f"<li>{e(x)}</li>" for x in p["events"])
    gallery = "".join(f'<figure><img src="/assets/{img}" alt="{e(alt)}" loading="lazy"></figure>' for img, alt in p["gallery"])
    related = "".join(f'<a href="/{r}"><b>{e(PAGES[r]["short"])}</b><span>{e(PAGES[r]["description"][:90].rsplit(" ", 1)[0])}… ↗</span></a>' for r in p["related"])
    brands = "".join(f"<li>{e(b.upper()).replace('SE ELECTRONICS', 'sE ELECTRONICS')}</li>" for b in BRANDS)
    breadcrumb_label = re.sub("<[^>]+>", " ", p["h1"]).split()[0]
    crumb_name = p["short"]
    packages = ""
    if p.get("packages"):
        packages = f'''<section class="packages" id="packages" aria-labelledby="packages-title">
    <div class="section-intro"><p class="eyebrow"><i></i> CORPORATE PACKAGES</p><h2 id="packages-title">Packages built<br>around your event.</h2>
    <p>Each package is a starting point, tailored to your venue, audience and running order.</p></div>
    {packages_block()}  </section>'''
    lectern_cta = lectern_section() if p.get("lectern") else ""

    # Structured data
    offers = None
    if "£" in p["price"]:
        price = re.search(r"£([\d,]+)", p["price"]).group(1).replace(",", "")
        offers = {"@type": "AggregateOffer", "priceCurrency": "GBP", "lowPrice": price, "offerCount": 1, "availability": "https://schema.org/InStock"}
    graph = [
        {"@type": "WebPage", "@id": page_url + "#webpage", "url": page_url, "name": p["title"], "description": p["description"],
         "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": page_url + "#service"}, "primaryImageOfPage": SITE + "/assets/" + p["hero"],
         "dateModified": TODAY, "inLanguage": "en-GB"},
        {"@type": "Service", "@id": page_url + "#service", "name": crumb_name, "serviceType": p["service_type"], "description": p["description"],
         "provider": {"@id": ORG_ID}, "areaServed": ORG["areaServed"], "url": page_url,
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": p["services_title"],
                             "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}} for t, d in p["services"]]},
         **({"offers": offers} if offers else {})},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": crumb_name, "item": page_url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faqs"]]},
        ORG,
    ]
    if p.get("lectern"):
        graph.append({"@type": "Product", "name": "HD Events custom digital lectern", "brand": {"@type": "Brand", "name": "HD Events"},
                      "manufacturer": {"@id": ORG_ID}, "image": [SITE + "/assets/digital-lecterns.jpg", SITE + "/assets/digital-lecterns-portrait.jpg"],
                      "description": "Custom-built digital lectern with full-height front display, optional comfort monitor, microphone inputs and Kramer CAT6 signal converters. Built to specification in the UK; also available to hire.",
                      "category": "Lecterns", "offers": offers})

    return f'''<!doctype html>
<html lang="en-GB">
<head>
{HEAD_COMMON}
<title>{e(p["title"])}</title>
<meta name="description" content="{e(p["description"])}">
{social(p["title"], p["description"], page_url, p["hero"])}
<link rel="stylesheet" href="/style.css">
<link rel="stylesheet" href="/home.css">
<link rel="stylesheet" href="/site.css">
{jsonld({"@context": "https://schema.org", "@graph": graph})}
</head>
<body class="home page">
<a class="skip" href="#main">Skip to content</a>
{header(p["nav"])}
{WHATSAPP_BUTTON}
<main id="main">
  <section class="page-hero" aria-labelledby="page-title">
    <div class="hero-media" aria-hidden="true"><img src="/assets/{p["hero"]}" alt=""></div>
    <div class="hero-inner">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <span aria-current="page">{e(crumb_name)}</span></nav>
      <p class="eyebrow"><i></i> {e(p["eyebrow"])}</p>
      <h1 id="page-title">{p["h1"]}</h1>
      <p class="hero-sub">{e(p["lead"])}</p>
      <div class="hero-actions">{hero_actions(p)}</div>
      <p class="hero-price">{p["price"]} · London &amp; nationwide</p>
    </div>
  </section>

  {facts_strip(p["facts"]) if p.get("facts") else f'<section class="brands slim" aria-label="Brands we supply"><ul class="brand-row">{brands}</ul></section>'}

  <section class="page-intro">
    <h2>{e(p["intro_title"])}</h2>
    <div>{"".join(f"<p>{e(x)}</p>" for x in p["intro"])}</div>
  </section>
  {buy_or_hire() if p.get("lectern") else ""}

  <section class="svc" aria-labelledby="svc-title">
    <div class="section-intro"><p class="eyebrow"><i></i> {"OPTIONS" if p.get("lectern") else "SERVICES"}</p><h2 id="svc-title">{e(p["services_title"])}</h2></div>
    <div class="svc-grid">{services}</div>
    <ul class="event-types" aria-label="Typical events">{chips}</ul>
  </section>

  <div class="ribbon-divider" data-ribbon="0" aria-hidden="true"><canvas></canvas></div>

  {f'<section class="page-gallery" aria-label="Photos from our events"><div class="gallery-row n{len(p["gallery"])}">{gallery}</div></section>' if p["gallery"] else ""}

  {packages}
  {lectern_cta}
  {delivery_quote() if p.get("delivery_quote") else ""}

  <section class="steps" aria-labelledby="steps-title">
    <div class="section-intro"><p class="eyebrow"><i></i> HOW IT WORKS</p><h2 id="steps-title">From first brief<br>to final applause.</h2></div>
    <ol>{"".join(f"<li><b>{e(t)}</b>{e(d)}</li>" for t, d in p.get("steps", DEFAULT_STEPS))}</ol>
  </section>

  <section class="faq" aria-labelledby="faq-title">
    <div class="section-intro"><p class="eyebrow"><i></i> FREQUENTLY ASKED QUESTIONS</p><h2 id="faq-title">Questions, answered.</h2></div>
    {faq_html(p["faqs"])}
  </section>

  <section class="more-services" aria-labelledby="related-title">
    <div class="section-intro"><p class="eyebrow"><i></i> RELATED SERVICES</p><h2 id="related-title">You may also need.</h2></div>
    <div class="service-cards">{related}</div>
  </section>

  <section class="closing" id="contact">
    <div class="sound-ribbon" data-ribbon="3" aria-hidden="true"><canvas></canvas></div>
    <div class="eyebrow"><i></i> START YOUR EVENT</div>
    <h2>Let’s plan<br><span>your next event.</span></h2>
    <div class="closing-bottom"><p>Share the date, venue and format.<br>We’ll recommend the right setup and send a detailed quote.</p>
      <a class="button solid" href="{QUOTE}" data-enquiry>Request a quote <span>↗</span></a></div>
    <div class="contact-options"><a class="button whatsapp" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us <span>↗</span></a><a class="phone" href="tel:{PHONE_LINK}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL} ↗</a></div>
  </section>
</main>
{footer()}
{DIALOG.replace('<iframe', LX_SUMMARY + '<iframe', 1) if p.get("lectern") else DIALOG}
<script src="/contact.js"></script>
<script src="/nav.js"></script>
<script src="/home.js"></script>
<script src="/ribbons.js"></script>
{'<script src="/lectern.js"></script>' if p.get("lectern") else ""}{'<script src="/delivery.js"></script>' if p.get("delivery_quote") else ""}
</body>
</html>
'''


# ---------- Events page ----------
EVENTS_PAGE = dict(
    title="Upcoming Events & Tickets | HD Events",
    description="Events hosted by HD Events: dates, venues and tickets for our upcoming live music, festival and community events in South Wales and beyond.",
    hero="festival-stage-night.jpg",
)


def _when(ev):
    start = datetime.datetime.fromisoformat(ev["start"])
    end = datetime.datetime.fromisoformat(ev["end"]) if ev.get("end") else start.replace(hour=23, minute=59)
    return start, end


def _nice_time(t):
    h, m = t.hour % 12 or 12, t.minute
    return f"{h}{':%02d' % m if m else ''}{'am' if t.hour < 12 else 'pm'}"


def _nice_dates(start, end):
    day = lambda d: d.strftime("%a ") + str(d.day) + d.strftime(" %B %Y")
    if end.date() != start.date():
        return f"{start.strftime('%a ')}{start.day} – {day(end)}"
    has_time = (start.hour, start.minute) != (0, 0)
    return day(start) + (" · " + _nice_time(start) if has_time else "")


def event_card(ev):
    start, end = _when(ev)
    status = (ev.get("status") or "").lower()
    where = ", ".join(x for x in (ev.get("venue"), ev.get("town")) if x)
    poster = (f'<img src="/assets/{e(ev["poster"])}" alt="Poster for {e(ev["title"])}" loading="lazy">' if ev.get("poster")
              else f'<div class="ev-noposter" aria-hidden="true"><span>{e(ev["title"])}</span></div>')
    tag = f'<span class="ev-status">{e(status.title())}</span>' if status else ""
    if status == "cancelled":
        cta = '<span class="button ev-off" aria-disabled="true">Cancelled</span>'
    elif status == "sold out":
        cta = '<span class="button ev-off" aria-disabled="true">Sold out</span>'
    elif ev.get("tickets"):
        cta = f'<a class="button solid ev-tickets" href="{e(ev["tickets"])}" target="_blank" rel="noopener">Buy tickets <span>↗</span></a>'
    else:
        cta = '<span class="button ev-off" aria-disabled="true">Tickets coming soon</span>'
    price = f'<span class="ev-price">{e(ev["price"])}</span>' if ev.get("price") else ""
    return f'''<article class="ev-card" data-end="{end.isoformat()}">
      <figure class="ev-poster">{poster}{tag}</figure>
      <div class="ev-body">
        <p class="ev-date"><time datetime="{start.isoformat()}">{_nice_dates(start, end)}</time></p>
        <h3>{e(ev["title"])}</h3>
        {f'<p class="ev-where">{e(where)}</p>' if where else ""}
        <p class="ev-desc">{e(ev.get("description", ""))}</p>
        <div class="ev-cta">{cta}{price}</div>
      </div>
    </article>'''


def event_jsonld(ev):
    start, end = _when(ev)
    status = (ev.get("status") or "").lower()
    place = {"@type": "Place", "name": ev.get("venue") or ev.get("town") or "", "address": ev.get("address") or ", ".join(x for x in (ev.get("venue"), ev.get("town")) if x)}
    out = {"@type": "Event", "name": ev["title"], "startDate": start.isoformat(), "endDate": end.isoformat(),
           "eventStatus": "https://schema.org/EventCancelled" if status == "cancelled" else "https://schema.org/EventScheduled",
           "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "location": place,
           "description": ev.get("description", ""), "organizer": {"@id": ORG_ID}}
    if ev.get("poster"):
        out["image"] = [SITE + "/assets/" + ev["poster"]]
    if ev.get("tickets"):
        offer = {"@type": "Offer", "url": ev["tickets"], "priceCurrency": "GBP",
                 "availability": "https://schema.org/SoldOut" if status == "sold out" else "https://schema.org/InStock"}
        m = re.search(r"£\s*([\d.,]+)", ev.get("price") or "")
        if m:
            offer["price"] = m.group(1).replace(",", "")
        elif re.search(r"free", ev.get("price") or "", re.I):
            offer["price"] = "0"
        out["offers"] = offer
    return out


def events_page():
    P = EVENTS_PAGE
    page_url = url("events")
    evs = sorted(EVENTS, key=lambda ev: ev["start"])
    cards = "\n    ".join(event_card(ev) for ev in evs)
    graph = [
        {"@type": "WebPage", "@id": page_url + "#webpage", "url": page_url, "name": P["title"], "description": P["description"],
         "isPartOf": {"@id": SITE + "/#website"}, "dateModified": TODAY, "inLanguage": "en-GB"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Events", "item": page_url}]},
        ORG,
    ] + [event_jsonld(ev) for ev in evs]
    return f'''<!doctype html>
<html lang="en-GB">
<head>
{HEAD_COMMON}
<title>{e(P["title"])}</title>
<meta name="description" content="{e(P["description"])}">
{social(P["title"], P["description"], page_url, P["hero"])}
<link rel="stylesheet" href="/style.css">
<link rel="stylesheet" href="/home.css">
<link rel="stylesheet" href="/site.css">
{jsonld({"@context": "https://schema.org", "@graph": graph})}
</head>
<body class="home page events-page">
<a class="skip" href="#main">Skip to content</a>
{header("Events")}
{WHATSAPP_BUTTON}
<main id="main">
  <section class="page-hero short" aria-labelledby="page-title">
    <div class="hero-media" aria-hidden="true"><img src="/assets/{P["hero"]}" alt=""></div>
    <div class="hero-inner">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> <span aria-hidden="true">/</span> <span aria-current="page">Events</span></nav>
      <p class="eyebrow"><i></i> EVENTS BY HD EVENTS</p>
      <h1 id="page-title">What’s on.<br><span>Get your tickets.</span></h1>
      <p class="hero-sub">The events we are hosting this year. Choose an event to find out more and buy tickets.</p>
    </div>
  </section>

  <section class="events" aria-labelledby="upcoming-title">
    <div class="section-intro"><p class="eyebrow"><i></i> UPCOMING</p><h2 id="upcoming-title">Upcoming events</h2></div>
    <div class="ev-grid" id="evUpcoming">
    {cards}
    </div>
    <div class="ev-empty" id="evEmpty"{"" if not evs else " hidden"}>
      <h3>New dates coming soon.</h3>
      <p>We announce our events here and on Instagram first.</p>
      <a class="button" href="{INSTAGRAM}" target="_blank" rel="noopener">Follow us on Instagram <span>↗</span></a>
    </div>
  </section>

  <section class="events past" id="evPastWrap" aria-labelledby="past-title" hidden>
    <div class="section-intro"><p class="eyebrow"><i></i> PAST EVENTS</p><h2 id="past-title">Thanks for coming.</h2></div>
    <div class="ev-grid" id="evPast"></div>
  </section>

  <section class="closing" id="contact">
    <div class="sound-ribbon" data-ribbon="3" aria-hidden="true"><canvas></canvas></div>
    <div class="eyebrow"><i></i> RUNNING YOUR OWN EVENT?</div>
    <h2>We can help<br><span>make it happen.</span></h2>
    <div class="closing-bottom"><p>Sound, lighting, staging, planning and licensing<br>for festivals, concerts and community events.</p>
      <a class="button solid" href="{QUOTE}" data-enquiry>Request a quote <span>↗</span></a></div>
    <div class="contact-options"><a class="button whatsapp" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us <span>↗</span></a><a class="phone" href="tel:{PHONE_LINK}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL} ↗</a></div>
  </section>
</main>
{footer()}
{DIALOG}
<script src="/contact.js"></script>
<script src="/nav.js"></script>
<script src="/home.js"></script>
<script src="/ribbons.js"></script>
<script src="/events.js"></script>
</body>
</html>
'''


# ---------- Home page: shared header, footer and site-wide structured data ----------
def update_home():
    path = os.path.join(ROOT, "index.html")
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<header.*?</header>", lambda m: header(None), s, count=1, flags=re.S)
    s = re.sub(r"<footer.*?</footer>", lambda m: footer(), s, count=1, flags=re.S)
    s = re.sub(r'<script type="application/ld\+json">.*?</script>\n', "", s, flags=re.S)
    home_graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "HD Events", "publisher": {"@id": ORG_ID}, "inLanguage": "en-GB"},
        {**ORG, "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Audio visual services",
                                    "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": PAGES[k]["service_type"], "url": url(k)}} for k in PAGES]}},
    ]}
    s = s.replace("</head>", jsonld(home_graph) + "\n</head>", 1)
    for tag in ['<link rel="icon" href="/favicon.ico" sizes="48x48">', '<link rel="icon" href="/favicon.png" type="image/png">', '<link rel="apple-touch-icon" href="/apple-touch-icon.png">', '<meta property="og:site_name" content="HD Events">', '<meta property="og:locale" content="en_GB">', '<meta property="og:url" content="' + SITE + '/">', '<meta name="twitter:card" content="summary_large_image">']:
        if tag not in s:
            s = s.replace("<link rel=\"stylesheet\" href=\"style.css\">", tag + "\n<link rel=\"stylesheet\" href=\"style.css\">", 1)
    # Absolute paths so the home page works from any URL
    for a in ("style.css", "home.css", "contact.js", "home.js", "ribbons.js", "flair.js"):
        s = s.replace(f'href="{a}"', f'href="/{a}"').replace(f'src="{a}"', f'src="/{a}"')
    if '/site.css' not in s:
        s = s.replace('<link rel="stylesheet" href="/home.css">', '<link rel="stylesheet" href="/home.css">\n<link rel="stylesheet" href="/site.css">', 1)
    if '/nav.js' not in s:
        s = s.replace('<script src="/contact.js"></script>', '<script src="/contact.js"></script>\n<script src="/nav.js"></script>', 1)
    s = s.replace('src="assets/', 'src="/assets/')
    open(path, "w", encoding="utf-8").write(s)


def write(name, text):
    open(os.path.join(ROOT, name), "w", encoding="utf-8").write(text)


def stamp_assets():
    """Add ?v=<content hash> to every CSS/JS link so visitors always get the latest styles."""
    import hashlib
    ver = {f: hashlib.sha1(open(os.path.join(ROOT, f), "rb").read()).hexdigest()[:8]
           for f in os.listdir(ROOT) if f.endswith((".css", ".js"))}
    for f in os.listdir(ROOT):
        if f.endswith(".html"):
            path = os.path.join(ROOT, f)
            s = open(path, encoding="utf-8").read()
            s2 = re.sub(r'(href|src)="/([\w-]+\.(?:css|js))(?:\?v=\w+)?"', lambda m: f'{m.group(1)}="/{m.group(2)}?v={ver[m.group(2)]}"' if m.group(2) in ver else m.group(0), s)
            if s2 != s:
                open(path, "w", encoding="utf-8").write(s2)


def main():
    update_home()
    for slug, p in PAGES.items():
        write(slug + ".html", service_page(slug, p))
    write("events.html", events_page())
    # Remove page files that have moved (the redirects send visitors to the new pages)
    for old in REDIRECTS:
        if old.endswith(".html") and os.path.exists(os.path.join(ROOT, old[1:])):
            os.remove(os.path.join(ROOT, old[1:]))
    stamp_assets()
    write("_redirects", "".join(f"{a} {b} 301\n" for a, b in REDIRECTS.items()))
    write("_headers", "/assets/*\n  Cache-Control: public, max-age=2592000\n/*.css\n  Cache-Control: public, max-age=86400\n/*.js\n  Cache-Control: public, max-age=86400\n")
    urls = [("", "1.0")] + [(s, "0.9" if PAGES[s]["nav"] != "More" else "0.6") for s in PAGES] + [("events", "0.8")]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"  <url><loc>{url(s)}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for s, pr in urls) + "</urlset>\n")
    bots = ["Googlebot", "Bingbot", "Google-Extended", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "Claude-User", "PerplexityBot", "Perplexity-User", "Applebot", "Applebot-Extended", "DuckDuckBot"]
    write("robots.txt", "# HD Events welcomes search engines and AI assistants.\nUser-agent: *\nAllow: /\n\n" +
          "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {SITE}/sitemap.xml\n")
    llms = [f"# HD Events\n\n> Corporate audio visual hire and technical event production across London and the UK. HD Events supplies, installs and operates sound systems, wireless microphones, presentation and relay screens, lighting and custom-built digital lecterns for conferences, AGMs, awards ceremonies, gala dinners, live entertainment and festivals.\n",
            "\n## Key facts\n",
            "- Coverage: London-focused, delivering events nationwide across the UK.\n",
            "- Equipment brands: " + ", ".join(BRANDS) + ".\n",
            "- Corporate packages from £500 (Speaker Essentials: lectern with microphone, two Sennheiser wireless mics, compact PA, laptop audio connection, delivery, setup and collection; up to 150 guests).\n",
            "- Custom digital lecterns built to specification from £1,465, or hire from £250 per day plus delivery.\n",
            "- Recent work includes a corporate dinner beneath Concorde, custom digital lecterns for the Brangwyn Hall in Swansea, concerts in cathedrals and theatres, and stadium and festival events.\n",
            f"- Contact: {PHONE} · {EMAIL} · WhatsApp {WHATSAPP}\n",
            "\n## Services\n"]
    for slug, p in PAGES.items():
        llms.append(f"- [{p['title'].split(' | ')[0]}]({url(slug)}): {p['description']}\n")
    llms.append(f"- [Upcoming events and tickets]({url('events')}): {EVENTS_PAGE['description']}\n")
    write("llms.txt", "".join(llms))


if __name__ == "__main__":
    main()
    print("Built", len(PAGES), "service pages + home page")
