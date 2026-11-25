# -*- coding: utf-8 -*-
"""All page wording for the HD Events site, kept in one place.

Edit text here, then run:  python3 tools/build_site.py
Each page becomes public/<slug>.html and is served at https://www.hd-events.co.uk/<slug>
"""

SITE = "https://www.hd-events.co.uk"
PHONE = "+44 7930 547024"
PHONE_LINK = "+447930547024"
EMAIL = "hello@hd-events.co.uk"
WHATSAPP = "https://wa.me/447930547024"
INSTAGRAM = "https://www.instagram.com/hdeventsuk"
QUOTE = "https://676968.17hats.com/p#/embed/krssknhxgstpsxdddgbvbkxnfgbbfvtz"
BRANDS = ["Sennheiser", "sE Electronics", "Allen & Heath", "Yamaha", "KV2 Audio", "NEXO"]

# Top menu: (label, slug) or (label, [(label, slug, short description)])
MENU = [
    ("Corporate", "corporate-av-hire"),
    ("Awards & Galas", "awards-gala-dinners"),
    ("Entertainment", "live-entertainment"),
    ("Festivals", "festivals-outdoor-events"),
    ("Dry Hire", "dry-hire"),
    ("Digital Lecterns", "digital-lecterns"),
    ("AV Delivery", "av-delivery-collection"),
    ("Events", "events"),
    ("More", [
        ("AV installations", "av-installations", "Permanent sound, screens and lighting for venues"),
        ("Event planning & licensing", "event-planning", "Planning, licensing, risk and compliance"),
        ("AV hire in London", "av-hire-london", "Sound, screens, lecterns and crew for London events"),
        ("Digital lectern buyer's guide", "digital-lectern-guide", "Costs, specs and buy-or-hire advice"),
        ("PA repairs", "pa-repairs", "Fault-finding and repairs for PA equipment"),
        ("Our work", "/#work", "Recent events and venues"),
    ]),
]

PAGES = {}

PAGES["corporate-av-hire"] = dict(
    short="Corporate AV hire",
    title="Corporate AV Hire London & UK | Conference Sound, Screens & Lighting | HD Events",
    description="Corporate AV hire for conferences, AGMs and launches in London and across the UK. Sound, mics, screens, lighting and lecterns with technicians. From £500.",
    nav="Corporate",
    eyebrow="CORPORATE AUDIO VISUAL HIRE · LONDON & NATIONWIDE",
    h1="Corporate events,<br><span>flawlessly delivered.</span>",
    lead="Audio visual hire and technical production for conferences, AGMs, product launches, town halls and internal events. Every presenter clearly heard, every slide clearly seen, and a calm technical team running the show from first rehearsal to final session.",
    hero="corporate-panel-foh.jpg",
    hero_alt="Corporate panel discussion seen from the HD Events sound and video control desk",
    price="Corporate packages from <b>£500</b>",
    intro_title="Technical production that lets your content lead.",
    intro=[
        "Corporate audiences notice when the technology fails and rarely when it works. Our job is to make sure the only thing people remember is your message: a presenter who can be heard at the back of the room, slides that are sharp on every screen, and a programme that runs to time.",
        "We supply, install and operate everything in-house, from a single lectern and microphone for a briefing to a full multi-session conference with stage, relay screens, lighting and a dedicated technical team. Each specification is designed around your venue, audience size and running order.",
    ],
    services_title="What we provide for corporate events",
    services=[
        ("Conference sound", "Speech-optimised sound systems from Allen & Heath, NEXO and KV2 Audio, tuned so every seat hears clearly without the sound ever feeling loud."),
        ("Wireless microphones", "Sennheiser handheld, lapel and headset microphones for presenters, panel discussions and roaming audience Q&A, with spares on hand."),
        ("Presentation & relay screens", "Presentation screens, relay screens for larger rooms, and confidence monitors so presenters can see their slides and notes without turning their back."),
        ("Lighting", "Presenter and stage lighting that keeps speakers well lit for the room and on camera, plus atmosphere lighting that brings your brand colours into the space."),
        ("Lecterns", "Branded and digital lecterns with built-in microphones and screens, from our own custom-built range."),
        ("Show running", "Experienced technicians operating sound, slides and lighting throughout, working to your running order and producer's cues."),
    ],
    events=["Conferences", "AGMs", "Product launches", "Town halls", "Panel discussions", "Training days", "Press events", "Exhibitions", "Internal comms events"],
    gallery=[("corporate-setup.jpg", "Sennheiser wireless receivers, mixing console and presentation control at a hotel conference"),
             ("corporate-panel-stage.jpg", "Panel discussion on stage at a corporate conference"),
             ("wireless-mics.jpg", "Row of Sennheiser wireless microphones ready for presenters")],
    packages=True,
    faqs=[
        ("What AV do I need for a conference?", "Most conferences need a sound system sized to the room, wireless microphones for each presenter and the panel, a presentation screen with a way to play slides and video, and lighting on the stage or lectern. Rooms over around 150 guests usually benefit from relay screens so everyone has a clear view. Send us your venue and running order and we will specify exactly what is needed."),
        ("Do you provide a technician on the day?", "Yes. For conference and AGM packages a technician from our own team operates sound, slides and lighting throughout the event. For smaller briefings we can set up, test and hand over, or stay on site, whichever you prefer."),
        ("Do you cover events outside London?", "Yes. We focus on London but deliver corporate events across the UK, including Wales, the South West, the Midlands and the North."),
        ("How much does corporate AV hire cost?", "Our Speaker Essentials package for smaller rooms starts from £500. Larger conferences and multi-room events are quoted individually, as the cost depends on audience size, screens, lighting and the length of the day. Every quote is itemised."),
        ("Can you work with our venue's in-house AV?", "Yes. We regularly work alongside venue teams, either providing the full technical package or adding to what the venue already has, such as extra microphones, lecterns or relay screens."),
        ("How far in advance should we book?", "As early as possible for busy conference periods, typically spring and autumn. We can often help at shorter notice, so it is always worth asking."),
    ],
    related=["awards-gala-dinners", "digital-lecterns", "av-hire-london"],
    service_type="Corporate audio visual hire",
)

PAGES["awards-gala-dinners"] = dict(
    short="Awards & gala dinners",
    title="Awards Ceremony & Gala Dinner AV Production | Sound, Screens, Lighting | HD Events",
    description="Sound, screens, lighting and lecterns for awards ceremonies and gala dinners across London and the UK. Walk-up music, winner graphics and technicians.",
    nav="Awards & Galas",
    eyebrow="AWARDS CEREMONIES & GALA DINNERS",
    h1="Big moments<br><span>deserve big nights.</span>",
    lead="Technical production for awards ceremonies, gala dinners and charity balls. From the welcome speech and the winners' walk-up to the after-dinner entertainment and the last dance, we make sure every moment lands.",
    hero="concorde-dinner.jpg",
    hero_alt="Gala dinner set for hundreds of guests beneath Concorde, with HD Events stage, PA and lighting",
    price="Bespoke packages, quoted for your event",
    intro_title="One technical team, from first course to final song.",
    intro=[
        "An awards night moves quickly between very different moments: speeches over dinner, a host on stage, winners walking up to music, sponsor videos, and a band or DJ to finish. We design one system that handles all of it, so the evening flows without changeovers or surprises.",
        "We have produced dinners in hotel ballrooms, historic halls and unusual spaces, including a corporate dinner for several hundred guests beneath Concorde in its hangar.",
    ],
    services_title="What we provide for awards and galas",
    services=[
        ("Sound for speech and music", "One system that is clear for speeches during dinner and powerful enough for the band or DJ afterwards."),
        ("Presenter microphones & lecterns", "Lectern and handheld microphones for hosts and presenters, with branded or digital lecterns available."),
        ("Screens & winner graphics", "Screens for category titles, nominee videos, sponsor content and live camera, with playback run from our control desk."),
        ("Walk-up music & stings", "Walk-up and award music cued on time for every winner, alongside background music through dinner."),
        ("Stage & atmosphere lighting", "Stage lighting for presenters and winners, plus uplighting and atmosphere lighting to transform the room."),
        ("Show calling & operation", "Technicians running sound, video and lighting to your script, working closely with your host and event manager."),
    ],
    events=["Awards ceremonies", "Gala dinners", "Charity balls", "Corporate dinners", "Celebration events", "Sports dinners"],
    gallery=[("concorde-dinner-wide.jpg", "Dinner tables beneath Concorde with stage and PA"),
             ("allen-heath-night.jpg", "Allen & Heath console and Sennheiser wireless during an evening event"),
             ("theatre-stage.jpg", "View from the stage across a large auditorium")],
    packages=False,
    faqs=[
        ("What AV does an awards ceremony need?", "Typically a sound system for speech and music, a lectern and presenter microphones, screens for category titles and nominee content, walk-up music for each winner, and stage lighting so winners look good in photos. We put it all on one cue sheet so the night runs smoothly."),
        ("Can you play our nominee videos and sponsor slides?", "Yes. Send us the content in advance and we build it into the show, then operate it live from the control desk."),
        ("Can you also provide sound for a band or DJ after dinner?", "Yes. We design the system for both speeches and music, so there is no changeover between the formal part of the evening and the entertainment."),
        ("Do you work outside London?", "Yes. We deliver awards and gala dinners across the UK."),
        ("How much does awards night AV cost?", "Every awards night is different, so we quote individually based on guest numbers, screens, lighting and the running order. Send us your brief and we will send an itemised quote."),
    ],
    related=["corporate-av-hire", "live-entertainment", "digital-lecterns"],
    service_type="Awards ceremony and gala dinner production",
)

PAGES["live-entertainment"] = dict(
    short="Live music, theatre & entertainment",
    title="Live Music, Theatre & Entertainment Sound and Lighting | HD Events",
    description="Sound, lighting and visual production for concerts, live music, theatre and entertainment across London and the UK, with experienced engineers.",
    nav="Entertainment",
    eyebrow="LIVE MUSIC, THEATRE & ENTERTAINMENT",
    h1="Sound and light<br><span>for unforgettable shows.</span>",
    lead="Audio, lighting and visual production for concerts, live music, theatre and touring productions. From intimate acoustic sessions in historic venues to large auditoriums, we bring the technical detail that lets performers shine.",
    hero="cathedral-show.jpg",
    hero_alt="Candlelit concert in a cathedral with HD Events sound and lighting",
    price="Production quoted for your show",
    intro_title="Production that serves the performance.",
    intro=[
        "Great live sound is about more than volume. It is about clarity, balance and a system that suits the room, whether that is a cathedral, a theatre or a stadium. We specify and engineer every show to sound natural for the audience and comfortable for the performers.",
        "We also provide production and stage management for theatre and touring work, coordinating venues, schedules and technical requirements so the performance can take centre stage.",
    ],
    services_title="What we provide for live events",
    services=[
        ("Front-of-house sound", "Allen & Heath and Yamaha consoles with KV2 Audio and NEXO systems, engineered for the room and the genre."),
        ("Monitors & stage sound", "Stage monitoring and microphones, including sE Electronics and Sennheiser, so performers hear exactly what they need."),
        ("Stage & atmosphere lighting", "Lighting design and operation for concerts and theatre, from warm acoustic looks to full rock-show lighting."),
        ("Visuals & screens", "Screens and video playback to add content, captions or live camera to the show."),
        ("Production & stage management", "Production management, tour and stage management for theatre and touring productions."),
        ("Experienced engineers", "Engineers who have mixed everything from intimate sessions to festival stages."),
    ],
    events=["Concerts", "Live music", "Theatre", "Touring productions", "Church & cathedral events", "Community events"],
    gallery=[("theatre-stage.jpg", "View from the stage across a large theatre auditorium"),
             ("allen-heath-night.jpg", "Allen & Heath SQ-5 at front of house in a historic venue"),
             ("outdoor-stage.jpg", "Outdoor stage with live band and KV2 Audio PA")],
    packages=False,
    faqs=[
        ("Do you provide sound engineers for concerts?", "Yes. Our engineers mix front of house and monitors, or work alongside an artist's own engineer, using our Allen & Heath and Yamaha consoles."),
        ("Can you provide sound for churches and cathedrals?", "Yes. Historic buildings need careful system design because of their long reverberation. We regularly provide sound for concerts and services in churches and cathedrals."),
        ("Do you provide theatre production and stage management?", "Yes. We provide production, tour and stage management alongside sound and lighting."),
        ("Can I just hire the equipment?", "Yes. If you have your own crew, see our dry hire page for sound and lighting equipment hire."),
    ],
    related=["festivals-outdoor-events", "dry-hire", "event-planning"],
    service_type="Live entertainment sound and lighting production",
)

PAGES["festivals-outdoor-events"] = dict(
    short="Festivals & outdoor events",
    title="Festival & Outdoor Event Sound, Stage and Lighting Production | HD Events",
    description="Festival and outdoor event production across the UK: KV2 Audio and NEXO stage sound, lighting, screens and crew, plus licensing and safety support.",
    nav="Festivals",
    eyebrow="FESTIVALS & OUTDOOR EVENTS",
    h1="Outdoor stages,<br><span>festival standard.</span>",
    lead="Sound, lighting and stage production for festivals, outdoor concerts, community events and sports venues. Systems designed for your site, crewed by people who know outdoor events, with planning and licensing support if you need it.",
    hero="festival-stage-night.jpg",
    hero_alt="Festival headline show at night with blue stage lighting",
    price="Production quoted for your site",
    intro_title="Built for the site, the crowd and the weather.",
    intro=[
        "Outdoor events bring challenges indoor shows never face: distance, wind, neighbours, power and the British weather. We design each system for your site and audience, with KV2 Audio and NEXO systems that deliver clear, even coverage without disturbing the neighbourhood.",
        "Because we also provide event planning, licensing and risk assessment support, we can help shape the whole event, not just the stage.",
    ],
    services_title="What we provide for festivals and outdoor events",
    services=[
        ("Stage sound systems", "KV2 Audio and NEXO systems sized for your audience, from community stages to large outdoor crowds."),
        ("Stage lighting", "Stage and effects lighting for evening shows and headline sets."),
        ("Screens & visuals", "Screens for live camera, sponsor content and information."),
        ("Backline & stage management", "Stage management and changeovers that keep the programme running on time."),
        ("Planning, licensing & safety", "Support with event planning, licensing, risk assessments and noise management."),
        ("Crew", "Experienced crew for build, show and derig."),
    ],
    events=["Festivals", "Outdoor concerts", "Community events", "Stadium events", "Sports events", "Fun days"],
    gallery=[("festival-stage-day.jpg", "Outdoor festival stage with flown speaker systems"),
             ("outdoor-stage.jpg", "Outdoor stage with KV2 Audio ES1.0 PA and live band"),
             ("stadium-mic.jpg", "sE Electronics microphone pitchside at the Swansea.com Stadium")],
    packages=False,
    faqs=[
        ("Can you provide the full stage production for a festival?", "Yes. We can provide sound, lighting, screens, stage management and crew, and support the planning, licensing and safety side too."),
        ("Do you help with event licensing and risk assessments?", "Yes. See our event planning and licensing page. We help coordinate licensing, risk assessments and compliance."),
        ("How do you manage noise at outdoor events?", "We design and aim the system for even coverage of the audience area, which keeps sound clear for the crowd while reducing spill to neighbours, and we can monitor levels during the event."),
        ("Do you cover events across the UK?", "Yes. We deliver outdoor events across the UK."),
    ],
    related=["live-entertainment", "event-planning", "dry-hire"],
    service_type="Festival and outdoor event production",
)

PAGES["dry-hire"] = dict(
    short="Dry hire",
    title="Dry Hire: PA, Sound & Lighting Equipment Hire | KV2, NEXO, Allen & Heath | HD Events",
    description="PA, microphone, console and lighting dry hire for crews and production companies. KV2 Audio, NEXO, Allen & Heath, Yamaha and Sennheiser. UK-wide.",
    nav="Dry Hire",
    eyebrow="DRY HIRE · SOUND & LIGHTING EQUIPMENT",
    h1="Professional equipment<br><span>for your own crew.</span>",
    lead="Already have your production team? Hire professionally maintained sound and lighting equipment from the same stock we use on our own events. Send us your equipment list, venue and dates and we will confirm availability.",
    hero="allen-heath-sq5.jpg",
    hero_alt="Allen & Heath SQ-5 digital mixing console with Sennheiser wireless rack",
    price="Hire quoted on your equipment list",
    intro_title="The same equipment we trust on our own shows.",
    intro=[
        "All dry hire equipment comes from our own production stock, tested before every hire and packed in road cases. You get the same brands we use for corporate and live events: KV2 Audio, NEXO, Allen & Heath, Yamaha, Sennheiser and sE Electronics.",
        "Collection or delivery can be arranged, and if you need a hand on the day we can add a technician.",
    ],
    services_title="Equipment available to hire",
    services=[
        ("Speaker systems", "KV2 Audio and NEXO systems, including compact NEXO PS10s for speech and the KV2 ES1.0 system for larger rooms and outdoor stages."),
        ("Mixing consoles", "Allen & Heath and Yamaha digital consoles."),
        ("Wireless microphones", "Sennheiser wireless systems with handheld, lapel and headset options, plus sE Electronics capsules."),
        ("Wired microphones & stands", "Vocal and instrument microphones, stands and cabling."),
        ("Lighting", "Stage and atmosphere lighting fixtures."),
        ("Lecterns", "Digital and branded lecterns from our own range."),
    ],
    events=["Production companies", "Bands & artists", "Venues", "Event organisers", "Schools & colleges", "Churches"],
    gallery=[("kv2-es10.jpg", "KV2 Audio ES1.0 speaker on an outdoor stage"),
             ("nexo-ps10.jpg", "NEXO PS10 speaker"),
             ("wireless-mics.jpg", "Sennheiser wireless microphones")],
    packages=False,
    faqs=[
        ("What is dry hire?", "Dry hire means hiring the equipment only, without our technicians. It suits production companies, venues and bands who have their own crew."),
        ("What brands do you hire?", "KV2 Audio, NEXO, Allen & Heath, Yamaha, Sennheiser and sE Electronics."),
        ("Can you deliver the equipment?", "Yes, delivery and collection can be arranged, or you can collect."),
        ("Can I add a technician to a dry hire?", "Yes. If you need help on the day we can add a technician for setup or the full event."),
        ("How do I check availability?", "Send us your equipment list, venue and dates using the quote form or WhatsApp, and we will confirm availability and price."),
    ],
    related=["live-entertainment", "festivals-outdoor-events", "pa-repairs"],
    service_type="Sound and lighting equipment dry hire",
)

PAGES["digital-lecterns"] = dict(
    short="Digital lecterns",
    title="Digital Lecterns for Sale & Hire UK | Custom Built with Screens | HD Events",
    description="Custom digital lecterns built in the UK with screens, comfort monitors, mic inputs and Kramer CAT6. Built to spec from £1,465, or available to hire.",
    nav="Digital Lecterns",
    eyebrow="DIGITAL LECTERNS · BUILT TO SPEC · SALE & HIRE",
    h1="Give your speakers<br><span>a stage.</span>",
    lead="Custom digital lecterns with full-height screens for your branding, slides or live content. Designed and built by HD Events to your specification, for permanent installation in your venue or available to hire for a single event.",
    hero="digital-lecterns.jpg",
    hero_alt="Two custom HD Events digital lecterns with built-in screens at the Brangwyn Hall, Swansea",
    price="Buy from <b>£1,465</b> · Hire from <b>£250</b>/day",
    intro_title="A lectern that works as hard as your speaker.",
    intro=[
        "A digital lectern turns the most-photographed spot in the room into a screen for your brand. Show your logo between speakers, sponsor content, speaker names or live slides, and change it in seconds.",
        "Every lectern is built to order around how it will be used: the screen, the microphone, the speaker's monitor and how it connects to your AV system. We recently built a matching pair for the Brangwyn Hall in Swansea.",
    ],
    services_title="Why a digital lectern",
    services=[
        ("Your brand in every photo", "The lectern is in almost every photo and stream of your event. A full-height screen keeps your logo, sponsors or speaker names in shot."),
        ("Change it in seconds", "Switch from a welcome screen to sponsor slides, speaker names or a live feed between speakers. No reprinting, no new banners."),
        ("Confident speakers", "Add a comfort monitor so speakers can see their slides, notes or a timer without turning their back on the audience."),
        ("A tidy stage", "Power, video and microphones connect at one rear panel, with hidden cable management and optional single-cable CAT6 runs."),
        ("Built for your venue", "Choose the screens, microphones, finish and case you need. We build it to order in the UK and install it for you."),
        ("Buy it or hire it", "Buy a lectern for your venue, or hire one for a single conference, awards night or AGM, on its own or with a full AV package."),
    ],
    events=["Conference venues", "Hotels", "Universities & schools", "Councils & civic halls", "Corporate offices", "Places of worship"],
    gallery=[],
    packages=False,
    lectern=True,
    faqs=[
        ("How much does a digital lectern cost?", "Our custom digital lecterns start from £1,465. The final price depends on the screen, comfort monitor, microphone and connectivity options you choose."),
        ("Can I hire a digital lectern?", "Yes. Our digital lecterns are available to hire from £250 per day plus delivery, either on their own or as part of a full AV package."),
        ("What can be shown on the lectern screen?", "Anything you can send to a display: your logo, sponsor slides, speaker names, video or a live feed of the presentation."),
        ("How does the lectern connect to the AV system?", "We can fit Kramer CAT6 converters so video and signals travel over a single network cable, keeping the stage tidy and the connection reliable."),
        ("Do you deliver and install lecterns across the UK?", "Yes. We deliver and set up lecterns across the UK, including London."),
        ("How long does a custom build take?", "Lead times depend on the specification. We will confirm the timescale when we quote."),
        ("Should I buy or hire a digital lectern?", "Buy if your venue hosts speakers regularly, such as a conference centre, hotel, university or council chamber: it pays for itself and stays branded to you. Hire if you need one for a single event or a few events a year."),
        ("Do your prices include VAT and delivery?", "No. All lectern prices are shown excluding VAT, and delivery and installation are quoted separately depending on where you are in the UK."),
    ],
    related=["corporate-av-hire", "digital-lectern-guide", "av-hire-london"],
    service_type="Digital lectern sales and hire",
    hero_actions=[("Build &amp; price yours", "#build", "↓"), ("Hire one for an event", "#hire", "↓")],
)

PAGES["av-installations"] = dict(
    short="AV installations",
    title="AV Installations for Venues | Sound Systems, Screens & Lighting | HD Events",
    description="Permanent AV installations for venues, halls, churches and offices: sound systems, screens, projectors, lighting and digital lecterns, with training.",
    nav="More",
    eyebrow="AV INSTALLATIONS",
    h1="Built for<br><span>your space.</span>",
    lead="Permanent sound systems, screens, projectors and lighting, designed around the way you use your venue. Whether it is a new installation or an upgrade to an existing system, we make technology that is simple for your team to use every day.",
    hero="allen-heath-night.jpg",
    hero_alt="Allen & Heath console and wireless system in a historic venue",
    price="Quoted after a site visit",
    intro_title="Technology your team can actually use.",
    intro=[
        "The best installation is one that works every time someone walks in and switches it on. We design systems around your room, your events and the people who will use them, then train your team so they are confident on their own.",
        "Our experience running live events means we know what works in practice, from speech clarity in reverberant halls to simple, reliable presentation connections.",
    ],
    services_title="What we install",
    services=[
        ("Sound systems", "Speech and music systems designed for the room."),
        ("Microphones", "Wired and wireless microphones for presenters and performers."),
        ("Screens & projectors", "Displays and projection for presentations and video."),
        ("Lighting", "Stage and architectural lighting."),
        ("Digital lecterns", "Custom digital lecterns built for your venue."),
        ("Training & support", "Handover training for your team and ongoing support."),
    ],
    events=["Venues & halls", "Churches", "Schools & colleges", "Hotels", "Offices", "Theatres"],
    gallery=[("church-pa.jpg", "NEXO PS10 speaker and microphones in a church"),
             ("digital-lecterns.jpg", "Digital lecterns installed in a civic hall"),
             ("allen-heath-sq5.jpg", "Allen & Heath digital console")],
    packages=False,
    faqs=[
        ("Do you install sound systems in churches and halls?", "Yes. We design and install sound systems for churches, halls and other venues, with careful attention to speech clarity."),
        ("Can you upgrade our existing system?", "Yes. We can assess what you have and recommend upgrades, reusing equipment where it makes sense."),
        ("Do you provide training?", "Yes. We train your team at handover so they can use the system with confidence."),
    ],
    related=["digital-lecterns", "pa-repairs", "corporate-av-hire"],
    service_type="Audio visual installation",
)

PAGES["event-planning"] = dict(
    short="Event planning & licensing",
    title="Event Planning, Licensing & Risk Assessments | HD Events",
    description="Event planning, licensing, risk assessments and compliance support for festivals, outdoor events and corporate events across the UK.",
    nav="More",
    eyebrow="EVENT PLANNING & LICENSING",
    h1="The thinking<br><span>behind the experience.</span>",
    lead="From the first idea to show day, we help coordinate the detail: event planning, logistics, licensing, risk assessments and compliance. Tell us what you have in mind and we will help shape the next steps.",
    hero="outdoor-stage.jpg",
    hero_alt="Outdoor community event stage with live band",
    price="Support tailored to your event",
    intro_title="Planning that makes show day simple.",
    intro=[
        "A successful event is decided long before the doors open. We help organisers plan the timeline, the site, the suppliers and the paperwork, so that on the day everyone knows what is happening and why.",
        "We support licensing applications, risk assessments, method statements and safety planning, always prepared for review and sign-off by the responsible person for your event.",
    ],
    services_title="How we help",
    services=[
        ("Event planning", "Timelines, schedules and running orders."),
        ("Site planning", "Site layouts, stage and facility positions, and access routes."),
        ("Licensing", "Support with premises licences and Temporary Event Notices."),
        ("Risk assessments", "Event risk assessments, fire risk assessments and method statements."),
        ("Supplier coordination", "Coordinating suppliers, crew and contractors."),
        ("Show day management", "Production management on the day."),
    ],
    events=["Festivals", "Outdoor events", "Community events", "Corporate events", "Charity events"],
    gallery=[("festival-stage-day.jpg", "Festival stage in daylight"),
             ("cathedral-show.jpg", "Event in a cathedral"),
             ("concorde-dinner-wide.jpg", "Corporate dinner beneath Concorde")],
    packages=False,
    faqs=[
        ("Do you help with Temporary Event Notices?", "Yes. We can help you understand what licence your event needs and support the application."),
        ("Do you write event risk assessments?", "Yes. We prepare risk assessments, fire risk assessments and method statements for review and sign-off by the responsible person."),
    ],
    related=["festivals-outdoor-events", "live-entertainment", "corporate-av-hire"],
    service_type="Event planning and licensing support",
)

PAGES["pa-repairs"] = dict(
    short="PA repairs",
    title="PA Repairs | Speaker, Amplifier & Mixer Repair | HD Events",
    description="Repairs for most PA equipment: speakers, amplifiers, mixers and microphones. Send the make, model and fault and we will advise on next steps.",
    nav="More",
    eyebrow="PA REPAIRS",
    h1="Get your<br><span>sound back.</span>",
    lead="Repairs for most PA-related equipment. Send us the make, model and a description of the fault, and we will tell you whether we can help and what to do next.",
    hero="sennheiser-rack.jpg",
    hero_alt="Rack of Sennheiser wireless receivers",
    price="Assessment quoted per item",
    intro_title="Professional repairs from working engineers.",
    intro=[
        "We maintain our own production equipment to a high standard, and offer the same care to yours. Whether it is a speaker that has started distorting, a crackling cable or a mixer channel that has stopped working, we will help diagnose the problem.",
    ],
    services_title="What we repair",
    services=[
        ("Speakers", "Active and passive loudspeakers."),
        ("Amplifiers", "Power amplifiers and powered speakers."),
        ("Mixers", "Analogue and digital mixing consoles."),
        ("Microphones", "Wired and wireless microphones."),
        ("Cables & connectors", "Cable repairs and re-terminations."),
        ("Fault finding", "Diagnosis of intermittent and system faults."),
    ],
    events=["Venues", "Bands", "Churches", "Schools", "Production companies"],
    gallery=[("allen-heath-sq5.jpg", "Mixing console"), ("nexo-ps10.jpg", "Loudspeaker"), ("wireless-mics.jpg", "Wireless microphones")],
    packages=False,
    faqs=[
        ("What information do you need for a repair?", "The make and model, a description of the fault and when it happens. Photos or a short video help too."),
        ("Can you repair any brand?", "We can help with most PA equipment. Send us the details and we will confirm."),
    ],
    related=["dry-hire", "av-installations", "live-entertainment"],
    service_type="PA equipment repair",
)

PAGES["av-delivery-collection"] = dict(
    short="AV delivery & collection",
    title="AV Delivery & Collection | Event Equipment Transport with Technicians | HD Events",
    description="AV delivery and collection from £85 each way, by technicians not just drivers. Set up, stay on as crew, multi-drop runs and same-night collection.",
    nav="AV Delivery",
    eyebrow="AV DELIVERY & COLLECTION · LONDON & NATIONWIDE",
    h1="Delivered by technicians,<br><span>not just drivers.</span>",
    lead="Event equipment delivered and collected by experienced AV technicians. They can set up and test on arrival, stay on as crew, then pack down and take everything away the same night. One booking, no second trip.",
    hero="corporate-setup.jpg",
    hero_alt="Road cases, wireless receivers and mixing console set up by HD Events technicians",
    price="Delivery from <b>£85</b> each way",
    intro_title="One trip. Delivered, crewed and collected.",
    intro=[
        "Most delivery services drop the kit at the door and leave. Ours are delivered by working AV technicians, so the person who arrives with your equipment knows exactly what it is, where it goes and how to make it work. They can unload, set up and test, or simply hand over to your team.",
        "If you need an extra pair of hands, they can stay on as crew for the event. When the night is over, they pack down and load out there and then. No separate collection booking, no van coming back the next morning, and no tired crew trying to find someone to collect after a late finish.",
        "We are a lean business without a central London warehouse, so we do not carry central London overheads. That keeps our rates competitive, while our technicians cover London and the rest of the UK.",
    ],
    services_title="What the service covers",
    services=[
        ("Delivery & collection", "Careful transport of sound, lighting, video and staging equipment to and from your venue, loaded and secured by people who handle AV every day."),
        ("Set up & test", "On arrival our technician can rig, connect and test the equipment, or hand over to your crew if you prefer."),
        ("Stay on as crew", "Need a hand during the show? The same technician can stay on as crew for the event, at an hourly or day rate."),
        ("Same-night pack down", "At the end of the event they pack down, load out and collect, saving a second trip and an early-morning collection."),
        ("Multi-drop & cross-hire runs", "Several pick-ups and drop-offs in one trip for a small extra charge, including collecting and returning kit from other hire companies. Far cheaper than booking separate deliveries."),
        ("Venue & production support", "Ideal for production companies, venues and event managers who need reliable logistics with technical know-how."),
    ],
    events=["Production companies", "Event managers", "Venues & hotels", "Hire companies", "Corporate events", "Festivals", "Weddings & parties"],
    gallery=[("allen-heath-sq5.jpg", "Mixing console in its road case, ready to load"),
             ("kv2-es10.jpg", "KV2 Audio speaker delivered and rigged on an outdoor stage"),
             ("festival-stage-day.jpg", "Outdoor stage equipment delivered and rigged for a festival")],
    packages=False,
    steps=[
        ("Tell us the run", "Pick-up and drop-off addresses, times, what is being moved and whether you need a technician on site."),
        ("We confirm a price", "A clear quote from £85 each way, with any multi-drop stops, set up or crew time itemised."),
        ("Delivered, crewed, collected", "We deliver and set up, stay on as crew if needed, then pack down and collect at the end of the night."),
    ],
    faqs=[
        ("How is this different from a normal courier?", "Your equipment is delivered by experienced AV technicians rather than general drivers. They can set up and test on arrival, stay on as crew, and pack down and collect at the end, so one booking covers everything."),
        ("Can the driver stay on and help during the event?", "Yes. Our technician can stay on as crew during the event and then collect everything at the end of the night. This is charged as additional crew time."),
        ("Can you collect at the end of the night instead of the next morning?", "Yes. Same-night collection is one of the main benefits. It saves a second trip, avoids next-morning venue access problems and means your own crew can go home after a late finish."),
        ("Do you only deliver your own equipment?", "No. We can deliver and collect equipment from other hire companies, venues or production stores, as well as our own."),
        ("Do you cover London?", "Yes. We cover London and the rest of the UK. Because we do not run a central London warehouse, our rates are competitive."),
        ("How much does AV delivery and collection cost?", "Delivery starts from £85 each way. The final price depends on distance, the size of the load and how long you need the technician on site. Send us the pick-up and delivery addresses, times and what is being moved, and we will send a clear quote."),
        ("Can you do several pick-ups or drop-offs in one trip?", "Yes. Multi-drop runs let us collect from or deliver to several locations in a single trip for a small additional charge, which costs far less than booking separate deliveries."),
    ],
    related=["dry-hire", "corporate-av-hire", "festivals-outdoor-events"],
    service_type="AV equipment delivery, collection and technical crew",
    hero_actions=[("Book a driver", "#book", "↓"), ("WhatsApp us", "WHATSAPP", "↗")],
    facts=[("From £85", "each way"), ("Technician driver", "not just a courier"), ("Same-night collection", "no second trip"), ("Multi-drop runs", "several stops, one trip")],
    delivery_quote=True,
)

PAGES["av-hire-london"] = dict(
    short="AV hire in London",
    title="AV Hire London | Event Sound, Screens, Lecterns & Technicians | HD Events",
    description="AV hire in London for conferences, awards, launches and parties: sound, mics, screens, lighting and digital lecterns, delivered and run by our technicians. From £500.",
    nav=None,
    eyebrow="AV HIRE · LONDON",
    h1="AV hire in London,<br><span>delivered by technicians.</span>",
    lead="Sound systems, wireless microphones, screens, lighting and digital lecterns for London events, delivered, set up and run by our own technicians. Event packages from £500, AV delivery from £85 each way, and clear itemised quotes.",
    hero="concorde-dinner-wide.jpg",
    hero_alt="Corporate dinner beneath Concorde with sound, microphones and screens by HD Events",
    price="London event packages from <b>£500</b>",
    intro_title="London events, without London overheads.",
    intro=[
        "HD Events supplies and runs audio visual equipment for conferences, AGMs, awards dinners, product launches, parties and live music across London. The same team plans the kit, delivers it, sets it up and stays to run it, so there is one point of contact from quote to pack-down.",
        "We do not run a central London warehouse, so we do not pass central London overheads on to you. Our technicians travel in with the equipment for each job, which keeps our rates competitive for London venues of every size.",
        "London venues come with their own rules: booked loading bays, goods lifts, tight access windows and late finishes. We plan the delivery and the load-out around them, and can collect the same night so nobody has to come back in the morning.",
    ],
    services_title="What we supply for London events",
    services=[
        ("Event sound & microphones", "Speech and music sound systems from NEXO, KV2 Audio, Allen & Heath and Yamaha, with Sennheiser handheld, lapel and headset microphones."),
        ("Screens & presentation", "Presentation and relay screens, confidence monitors and slide playback, so every guest sees clearly and presenters stay on track."),
        ("Digital lecterns", "Our own custom-built digital lecterns with full-height screens for your branding, available to hire in London from £250 a day plus delivery."),
        ("Lighting", "Stage, presenter and atmosphere lighting that looks good in the room and on camera."),
        ("AV delivery by technicians", "Delivery and collection from £85 each way by working AV technicians, who can set up, stay on as crew and collect the same night."),
        ("Dry hire for London crews", "PA, mixing desks, microphones and lighting for production companies and venues that have their own operators."),
    ],
    events=["Conferences & AGMs", "Awards dinners", "Product launches", "Corporate parties", "Charity galas", "Live music", "Hotels & venues", "Production companies"],
    gallery=[("corporate-panel-stage.jpg", "Panel discussion on stage at a corporate conference"),
             ("lectern-in-use.jpg", "HD Events digital lectern in use at an event"),
             ("allen-heath-night.jpg", "Allen & Heath SQ-5 and Sennheiser wireless at front of house during an evening event")],
    packages=True,
    facts=[("From £500", "London event packages"), ("From £85", "AV delivery each way"), ("Own technicians", "set up and run it"), ("Same-night", "pack down and collection")],
    faqs=[
        ("Do you supply AV hire in London?", "Yes. We supply sound, microphones, screens, lighting and digital lecterns for events across London, delivered, set up and run by our own technicians."),
        ("How much does AV hire cost in London?", "Our Speaker Essentials package starts from £500 and covers a lectern with microphone, two Sennheiser wireless microphones, a compact PA, a laptop audio connection, and delivery, setup and collection for up to 150 guests. Larger events are quoted individually with every item listed. Prices exclude VAT."),
        ("Can you deliver AV equipment to a London venue and collect it the same night?", "Yes. Delivery and collection starts from £85 each way. Our drivers are AV technicians, so they can set up, stay on as crew and pack down at the end of the night."),
        ("Can I hire a digital lectern in London?", "Yes. Our custom digital lecterns can be hired from £250 per day plus delivery, on their own or as part of a full AV package."),
        ("Do you work with London venues' in-house AV teams?", "Yes. We can provide the full technical package or add to what the venue already has, such as extra microphones, a digital lectern or relay screens."),
        ("Why are your London prices competitive?", "We do not run a central London warehouse, so we do not carry central London overheads. Our technicians bring the equipment in for each job."),
        ("How do I book AV for a London event?", "Send us the date, venue, number of guests and what is happening on the day, by the enquiry form, WhatsApp or phone. We reply with a recommended setup and an itemised quote."),
    ],
    related=["corporate-av-hire", "digital-lecterns", "av-delivery-collection"],
    service_type="Audio visual equipment hire in London",
    area="London",
    hero_actions=[("Get a London quote", "QUOTE", "↗"), ("WhatsApp us", "WHATSAPP", "↗")],
)

PAGES["digital-lectern-guide"] = dict(
    short="Digital lectern guide",
    title="Digital Lectern Buyer's Guide: Costs, Screens & Buy vs Hire | HD Events",
    description="What a digital lectern is, what it costs in the UK, the screen, microphone and connection options, and whether to buy or hire. A practical guide from a UK lectern builder.",
    nav=None,
    eyebrow="GUIDE · DIGITAL LECTERNS",
    h1="Digital lecterns:<br><span>a buyer's guide.</span>",
    lead="A plain-English guide to digital lecterns from the team that designs and builds them in the UK: what they are, what goes inside, what they cost, and how to decide between buying and hiring.",
    hero="lectern-screen-detail.jpg",
    hero_alt="Close-up of the screen on an HD Events custom digital lectern",
    price="Built to spec from <b>£1,465</b> · Hire from <b>£250</b>/day",
    intro_title="What is a digital lectern?",
    intro=[
        "A digital lectern is a speaker's lectern with a screen built into the front, and often a second screen on top for the speaker. The front screen shows your logo, sponsor slides, speaker names or live video to the audience and cameras. The top screen, called a comfort monitor, lets the speaker see their slides, notes or a timer without turning round.",
        "Because the lectern appears in almost every photo and livestream of an event, the front screen is one of the most valuable pieces of branding in the room. Unlike a printed panel, it can change between speakers in seconds.",
        "A well-built digital lectern also tidies up the stage. Power, video and microphone connections come together at one rear panel, and with network-cable video extenders such as Kramer CAT6, a single cable can carry the picture from the control desk.",
        "Cost: HD Events digital lecterns are built to order from £1,465 excluding VAT. The price depends on the screen size, whether you add a comfort monitor, the microphone, and how the lectern connects to your AV. Hire starts from £250 per day plus delivery.",
    ],
    services_title="What to look for in a digital lectern",
    services=[
        ("Front screen", "Size and brightness matter most. It should be bright enough for a lit stage and look sharp on camera. Portrait screens suit logos and speaker names."),
        ("Comfort monitor", "A screen on the top surface for the speaker's slides, notes or a countdown. It makes speakers more confident and keeps them facing the audience."),
        ("Microphone", "A gooseneck microphone suits most speeches. Make sure it connects cleanly to the venue's sound system and that a wireless mic can be used alongside it."),
        ("Connections", "Look for a single rear panel with clearly labelled power, video and audio inputs. CAT6 video extenders let you run one long network cable instead of fragile HDMI."),
        ("Build & transport", "A lectern that travels needs a strong frame, protected screens and a flight case. One that stays in a venue can focus on finish and cable management."),
        ("Support", "Check who builds it, who installs it and who to call if something stops working. Buying from the builder makes repairs and upgrades simpler."),
    ],
    events=["Conference centres", "Hotels", "Universities", "Councils & civic halls", "Awards ceremonies", "AGMs", "Places of worship"],
    gallery=[("lectern-rear-panel.jpg", "Rear connection panel on an HD Events digital lectern"),
             ("lectern-top-monitor.jpg", "Comfort monitor on the top of a digital lectern"),
             ("digital-lecterns-portrait.jpg", "A pair of HD Events digital lecterns at the Brangwyn Hall, Swansea")],
    packages=False,
    steps=[
        ("Tell us how it will be used", "The venue, how often it will be used, what should be on the screens and how it connects to your AV."),
        ("We specify and quote", "Screen, comfort monitor, microphone, connections and finish, with a clear price excluding VAT."),
        ("Built, delivered, installed", "We build it in the UK, deliver it and set it up with your team, or bring it for your event if you hire."),
    ],
    faqs=[
        ("What is a digital lectern?", "A digital lectern is a speaker's lectern with a built-in screen on the front, and often a comfort monitor on top. The front screen shows branding, sponsor slides, speaker names or live video, and the top screen shows the speaker their slides or notes."),
        ("How much does a digital lectern cost in the UK?", "HD Events custom digital lecterns are built to order from £1,465 excluding VAT. The final price depends on the screens, microphone and connection options. Hiring one costs from £250 per day plus delivery."),
        ("Should I buy or hire a digital lectern?", "Buy if your venue hosts speakers regularly, such as a hotel, conference centre, university or council chamber. Hire if you need one for a single event or a few events a year."),
        ("What is a comfort monitor on a lectern?", "A comfort monitor is a screen on the top of the lectern, facing the speaker. It shows their slides, notes, a timer or the next slide, so they can present without turning to look at the main screen."),
        ("How does a digital lectern connect to the AV system?", "Usually through a rear panel with power, video and microphone connections. CAT6 video extenders such as Kramer let one network cable carry the picture from the control desk, keeping the stage tidy."),
        ("Who makes custom digital lecterns in the UK?", "HD Events designs and builds custom digital lecterns in the UK, including a matching pair for the Brangwyn Hall in Swansea, and delivers and installs them across the UK, including London."),
        ("Can a digital lectern be branded?", "Yes. The front screen can show your logo, colours, sponsors or event artwork, and change between speakers. The body and finish can also be specified when the lectern is built."),
    ],
    related=["digital-lecterns", "corporate-av-hire", "av-installations"],
    service_type="Digital lectern design, build and hire",
    article=True,
    hero_actions=[("Price a lectern", "/digital-lecterns#build", "→"), ("Hire one", "/digital-lecterns#hire", "→")],
)

# Old addresses that should send visitors (and search engines) to the new pages.
REDIRECTS = {
    "/pa-hire.html": "/dry-hire",
    "/pa-hire": "/dry-hire",
    "/lecterns.html": "/digital-lecterns",
    "/lecterns": "/digital-lecterns",
    "/live-av.html": "/live-entertainment",
    "/live-av": "/live-entertainment",
    "/theatre-production.html": "/live-entertainment",
    "/theatre-production": "/live-entertainment",
    "/installations.html": "/av-installations",
    "/installations": "/av-installations",
    "/repairs.html": "/pa-repairs",
    "/repairs": "/pa-repairs",
    "/tickets": "/events",
}

# ---------- Digital lectern price list ----------
# price: a number in pounds (shown as "+ £X"), or None to show "Price on request".
# Fill these in and run tools/build_site.py; the configurator and price table update automatically.
LECTERN = dict(
    base_price=1465,
    base_name="HD Events Digital Lectern",
    included=[
        "Full-height front display for logos, slides and video",
        "Solid, stage-ready black cabinet",
        "Rear connection panel with HDMI and powerCON power",
        "Hidden cable management",
        "Designed and built to order in the UK",
    ],
    upgrades=[
        # (id, name, description, price, monitor, group) -- monitor=True: only one monitor option can be ticked
        ("branding", "Custom branding", "Your logo or a branded finish on the cabinet.", 399, False, "Finish & branding"),
        ("comfort", "Comfort monitor (non-touch)", "A built-in presenter screen for slides, notes or a timer.", 300, True, "Speaker screen (choose one)"),
        ("multi-touch", "Multi-touch presenter monitor", "The touchscreen alternative to the non-touch comfort monitor.", 450, True, "Speaker screen (choose one)"),
        ("mic-inputs", "Built-in microphone inputs", "Add microphone connections to the lectern.", 125, False, "Microphones"),
        ("gooseneck", "Two gooseneck microphones", "Pair of gooseneck microphones. Built-in lectern inputs are a separate option.", 495, False, "Microphones"),
        ("padded-case", "Padded case", "Padded protection for the lectern.", 280, False, "Protection & transport"),
        ("case", "Flight case", "Road case for transport and storage.", 995, False, "Protection & transport"),
        ("shelf", "Pull-out laptop shelf", "A sliding shelf inside the lectern for the presenter's laptop, out of sight.", None, False, "Built-in extras"),
        ("steel", "Brushed steel finish", "A premium stainless steel finish in place of the standard black.", None, False, "Finish & branding"),
        ("kramer", "Kramer CAT6 converters", "Video and signal over a single network cable to your AV system: tidy, reliable long runs.", None, False, "Built-in extras"),
        ("player", "Built-in media player", "Show logos and content on the front screen without a laptop.", None, False, "Built-in extras"),
    ],
    showcase=[
        ("lectern-steel-awards.jpg", "Brushed steel finish, branded for the 2026 Player Awards at the Brangwyn Hall"),
        ("lectern-screen-detail.jpg", "Full-height front display with conference welcome screen"),
        ("lectern-top-monitor.jpg", "Built-in comfort monitor, gooseneck mic and pull-out laptop shelf"),
        ("lectern-in-use.jpg", "In use at the British Nuclear Medicine Society Autumn Meeting 2026"),
        ("lectern-rear-panel.jpg", "Rear panel: HDMI, powerCON power and XLR microphone connections"),
    ],
    hire_note="Available to hire for single events from £250 per day plus delivery, on its own or as part of a full AV package.",
    hire_price=250,
    lead_time=None,  # e.g. "4 to 6 weeks"
)


# ---------- Events we are hosting ----------
# Add one dict() per event, then run tools/build_site.py. Events are listed by date, and once an
# event's end time has passed it moves to "Past events" on its own (no rebuild needed).
#   title        Event name
#   start / end  "YYYY-MM-DDTHH:MM" (end is optional; it defaults to the end of the start day)
#   venue, town  Where it is.  address: full address for Google (optional but recommended)
#   poster       Image in public/assets/events/, e.g. "events/beach-fest-2027.jpg" (portrait works best)
#   description  Two or three sentences: what it is, who is on, who it is for
#   tickets      Link to the ticket page.  Leave "" for "Tickets coming soon"
#   price        Optional, e.g. "From £15" or "Free entry"
#   status       Optional: "sold out" or "cancelled"
EVENTS = [
]
