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
  <a class="button small header-cta" href="{QUOTE}" data-enquiry>Request a quote <span>↗</span></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="mainNav"><span class="bars" aria-hidden="true"></span><span class="label">Menu</span></button>
</header>'''


def footer():
    links = [(l, t) for l, t in MENU if not isinstance(t, list)] + [(l, s) for l, s, _ in MENU[-1][1]]
    svc = "".join(f'<li><a href="{"/" + s if not s.startswith("/") else s}">{e(l)}</a></li>' for l, s in links)
    return f'''<footer class="site-footer">
  <div class="footer-grid">
    <div class="footer-brand"><a class="brand" href="/"><img src="/assets/logo.png" alt="HD Events" width="130" height="65"></a>
      <p>Corporate audio visual hire and event production across London and the UK. Sound, screens, lighting and digital lecterns, supplied and operated by our own technical team.</p></div>
    <div><h2>Services</h2><ul>{svc}</ul></div>
    <div><h2>Contact</h2><ul><li><a href="tel:{PHONE_LINK}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us ↗</a></li><li><a href="{QUOTE}" data-enquiry>Request a quote ↗</a></li></ul></div>
    <div><h2>Follow</h2><ul><li><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram ↗</a></li><li><a href="https://www.hd-events.co.uk/tickets" target="_blank" rel="noopener">Event tickets ↗</a></li></ul></div>
  </div>
  <div class="footer-base"><span>© {datetime.date.today().year} HD Events · Corporate audio visual hire · London &amp; nationwide</span><a href="#">Back to top ↑</a></div>
</footer>'''


WHATSAPP_BUTTON = f'<a class="wa-fixed" href="{WHATSAPP}" aria-label="Message HD Events on WhatsApp" target="_blank" rel="noopener"><svg viewBox="0 0 32 32" aria-hidden="true"><path fill="none" stroke="white" stroke-width="2" d="M5 22a12 12 0 1 1 5 5l-7 2z"/><path fill="white" d="M11 9c-2 0-3 2-2 5 2 5 5 8 10 9 2 0 4-1 4-4l-4-2-2 2c-2-1-4-3-5-5l1-2-1-3z"/></svg><span>Message us</span></a>'
DIALOG = f'<dialog id="enquiry"><div class="dialog-head"><h2>Tell us about your event.</h2><button id="close-enquiry" aria-label="Close enquiry form">×</button></div><p>Share the date, venue and what you need, and we will reply with recommendations and a quote.</p><iframe title="HD Events enquiry form" name="lc_contact_form" width="100%" height="600" src="{QUOTE}" loading="lazy"></iframe><div class="dialog-contact"><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us: {PHONE} ↗</a><a href="tel:{PHONE_LINK}">Call {PHONE}</a><a href="mailto:{EMAIL}">Email {EMAIL} ↗</a></div></dialog>'
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
    rows = "".join(
        f'<label class="opt"><input type="checkbox" value="{u}" data-price="{"" if pr is None else pr}" data-name="{e(n)}">'
        f'<span class="opt-box"><b>{e(n)}</b><span>{e(d)}</span></span><span class="opt-price">{"+ " + money(pr) if pr is not None else "Price on request"}</span></label>'
        for u, n, d, pr in L["upgrades"])
    table = "".join(f'<tr><td>{e(n)}</td><td>{e(d)}</td><td>{"+ " + money(pr) if pr is not None else "On request"}</td></tr>' for u, n, d, pr in L["upgrades"])
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
        <p class="eyebrow">UPGRADES</p>{rows}
        <div class="lx-total" aria-live="polite"><div><span>Your build from</span><b id="lxTotal">{money(L["base_price"])}</b><small id="lxNote">ex VAT</small></div>
          <div class="hero-actions"><a class="button solid" id="lxWhatsApp" href="{WHATSAPP}" target="_blank" rel="noopener">Send spec on WhatsApp <span>↗</span></a><a class="button" id="lxEmail" href="mailto:{EMAIL}">Email my spec <span>↗</span></a></div>
          <p class="hint">No commitment. We reply with a fixed quote and build date.</p></div>
      </form>
    </div>
    <div class="lx-table-wrap"><h3>Price list</h3><table class="lx-table"><thead><tr><th>Item</th><th>What it does</th><th>Price</th></tr></thead>
      <tbody><tr><td><b>{e(L["base_name"])}</b></td><td>Standard build, as above</td><td><b>{money(L["base_price"])}</b></td></tr>{table}
      <tr><td><b>Hire</b></td><td>Per day, on its own or with a full AV package</td><td><b>{money(L["hire_price"])}/day</b> + delivery</td></tr></tbody></table><p class="hint">All prices exclude VAT and delivery. Final price confirmed on quote.</p></div>
    <script type="application/json" id="lxData">{json.dumps({"base": L["base_price"], "name": L["base_name"]})}</script>
  </section>'''


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
      <div class="hero-actions">{'<a class="button solid" href="#build">Build your lectern <span>↓</span></a><a class="button" href="#build">See price list <span>↓</span></a>' if p.get("lectern") else f'<a class="button solid" href="{QUOTE}" data-enquiry>Request a quote <span>↗</span></a><a class="button" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp us <span>↗</span></a>'}</div>
      <p class="hero-price">{p["price"]} · London &amp; nationwide</p>
    </div>
  </section>

  <section class="brands slim" aria-label="Brands we supply"><ul class="brand-row">{brands}</ul></section>

  <section class="page-intro">
    <h2>{e(p["intro_title"])}</h2>
    <div>{"".join(f"<p>{e(x)}</p>" for x in p["intro"])}</div>
  </section>

  <section class="svc" aria-labelledby="svc-title">
    <div class="section-intro"><p class="eyebrow"><i></i> {"OPTIONS" if p.get("lectern") else "SERVICES"}</p><h2 id="svc-title">{e(p["services_title"])}</h2></div>
    <div class="svc-grid">{services}</div>
    <ul class="event-types" aria-label="Typical events">{chips}</ul>
  </section>

  <div class="ribbon-divider" data-ribbon="0" aria-hidden="true"><canvas></canvas></div>

  {f'<section class="page-gallery" aria-label="Photos from our events"><div class="gallery-row n{len(p["gallery"])}">{gallery}</div></section>' if p["gallery"] else ""}

  {packages}
  {lectern_cta}

  <section class="steps" aria-labelledby="steps-title">
    <div class="section-intro"><p class="eyebrow"><i></i> HOW IT WORKS</p><h2 id="steps-title">From first brief<br>to final applause.</h2></div>
    <ol>
      <li><b>Share your brief</b>Venue, date, running order, audience size and anything you already have in place.</li>
      <li><b>We design the setup</b>The right equipment for your venue, with a clear, itemised quote.</li>
      <li><b>We deliver and operate</b>On site before your guests, a technician throughout where needed, and a clean, discreet derig.</li>
    </ol>
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
{DIALOG}
<script src="/contact.js"></script>
<script src="/nav.js"></script>
<script src="/home.js"></script>
<script src="/ribbons.js"></script>
{'<script src="/lectern.js"></script>' if p.get("lectern") else ""}
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


def main():
    update_home()
    for slug, p in PAGES.items():
        write(slug + ".html", service_page(slug, p))
    # Remove page files that have moved (the redirects send visitors to the new pages)
    for old in REDIRECTS:
        if old.endswith(".html") and os.path.exists(os.path.join(ROOT, old[1:])):
            os.remove(os.path.join(ROOT, old[1:]))
    write("_redirects", "".join(f"{a} {b} 301\n" for a, b in REDIRECTS.items()))
    write("_headers", "/assets/*\n  Cache-Control: public, max-age=2592000\n/*.css\n  Cache-Control: public, max-age=86400\n/*.js\n  Cache-Control: public, max-age=86400\n")
    urls = [("", "1.0")] + [(s, "0.9" if PAGES[s]["nav"] != "More" else "0.6") for s in PAGES]
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
            "- Custom digital lecterns built to specification from £1,466, or hire from £250 per day plus delivery.\n",
            "- Recent work includes a corporate dinner beneath Concorde, custom digital lecterns for the Brangwyn Hall in Swansea, concerts in cathedrals and theatres, and stadium and festival events.\n",
            f"- Contact: {PHONE} · {EMAIL} · WhatsApp {WHATSAPP}\n",
            "\n## Services\n"]
    for slug, p in PAGES.items():
        llms.append(f"- [{p['title'].split(' | ')[0]}]({url(slug)}): {p['description']}\n")
    write("llms.txt", "".join(llms))


if __name__ == "__main__":
    main()
    print("Built", len(PAGES), "service pages + home page")
