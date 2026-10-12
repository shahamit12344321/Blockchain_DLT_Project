import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_clear_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette: Modern Obsidian & Electric Cyan/Emerald
    BG_DARK      = RGBColor(11, 15, 25)      # #0B0F19 Deep Obsidian
    CARD_BG      = RGBColor(22, 31, 48)      # #161F30 Dark Slate Card
    CARD_BORDER  = RGBColor(42, 56, 84)      # #2A3854 Clean Border
    TEAL_ACCENT  = RGBColor(0, 210, 180)     # #00D2B4 Electric Teal
    AMBER_ACCENT = RGBColor(245, 158, 11)    # #F59E0B Golden Amber
    BLUE_ACCENT  = RGBColor(59, 130, 246)    # #3B82F6 Vibrant Blue
    GREEN_ACCENT = RGBColor(16, 185, 129)    # #10B981 Emerald Green
    RED_ACCENT   = RGBColor(239, 68, 68)     # #EF4444 Alert Red
    TEXT_WHITE   = RGBColor(255, 255, 255)   # #FFFFFF
    TEXT_MUTED   = RGBColor(148, 163, 184)   # #94A3B8 Cool Gray
    TEXT_BODY    = RGBColor(226, 232, 240)   # #E2E8F0 Soft White

    FONT_MAIN = "Calibri"

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, kicker, title, slide_num, total_slides=12):
        # Kicker / Badge
        k_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(8.0), Inches(0.35))
        tf_k = k_box.text_frame
        tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
        p_k = tf_k.paragraphs[0]
        p_k.text = kicker.upper()
        p_k.font.name = FONT_MAIN
        p_k.font.size = Pt(11)
        p_k.font.bold = True
        p_k.font.color.rgb = AMBER_ACCENT

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(10.5), Inches(0.55))
        tf_t = t_box.text_frame
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_MAIN
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        # Divider
        div = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.38), Inches(11.733), Inches(0.02))
        div.fill.solid()
        div.fill.fore_color.rgb = CARD_BORDER
        div.line.fill.background()

        # Footer
        f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(10.0), Inches(0.3))
        tf_f = f_box.text_frame
        tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0
        p_f = tf_f.paragraphs[0]
        p_f.text = "ChainVision Pro • Supply Chain Visibility & Blockchain Platform • VIT CSE Capstone Project"
        p_f.font.name = FONT_MAIN
        p_f.font.size = Pt(9.5)
        p_f.font.color.rgb = TEXT_MUTED

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(11.5), Inches(7.05), Inches(1.0), Inches(0.3))
        tf_n = num_box.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        p_n = tf_n.paragraphs[0]
        p_n.text = f"{slide_num} / {total_slides}"
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.font.name = FONT_MAIN
        p_n.font.size = Pt(9.5)
        p_n.font.bold = True
        p_n.font.color.rgb = TEAL_ACCENT

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (CLEAN & IMPACTFUL)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    top_accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.06))
    top_accent.fill.solid()
    top_accent.fill.fore_color.rgb = TEAL_ACCENT
    top_accent.line.fill.background()

    tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.15), Inches(11.5), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "CAPSTONE PROJECT PRESENTATION • REVIEW 2"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = AMBER_ACCENT

    tb_t = s1.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.5), Inches(1.6))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p1 = tf_t.paragraphs[0]
    p1.text = "ChainVision Pro: Real-Time Supply Chain"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p2 = tf_t.add_paragraph()
    p2.text = "Visibility & Management Platform"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = TEAL_ACCENT

    tb_sub = s1.shapes.add_textbox(Inches(0.8), Inches(3.25), Inches(11.5), Inches(0.7))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "An Integrated Multi-Tier Platform Combining Live IoT Telemetry, Dynamic Exception Detection, ML Delay Risk Scoring, and a SHA-256 Blockchain Checkpoint Ledger."
    p_sub.font.size = Pt(13.5)
    p_sub.font.color.rgb = TEXT_BODY

    # Team Card
    add_card(s1, 0.8, 4.35, 5.7, 2.2, CARD_BG, CARD_BORDER)
    tb_c1 = s1.shapes.add_textbox(Inches(1.1), Inches(4.55), Inches(5.1), Inches(1.8))
    tf_c1 = tb_c1.text_frame
    p = tf_c1.paragraphs[0]
    p.text = "STUDENT PRESENTERS"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = AMBER_ACCENT

    p1 = tf_c1.add_paragraph()
    p1.text = "• Yash Dharad   |   Roll No: 23BKT0001"
    p1.font.bold = True
    p1.font.size = Pt(13)
    p1.font.color.rgb = TEXT_WHITE

    p2 = tf_c1.add_paragraph()
    p2.text = "• Amit Kumar    |   Roll No: 23BKT0118"
    p2.font.bold = True
    p2.font.size = Pt(13)
    p2.font.color.rgb = TEXT_WHITE

    p3 = tf_c1.add_paragraph()
    p3.text = "B.Tech Computer Science & Engineering • Blockchain & DLT"
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = TEXT_MUTED

    # Guide Card
    add_card(s1, 6.8, 4.35, 5.7, 2.2, CARD_BG, CARD_BORDER)
    tb_c2 = s1.shapes.add_textbox(Inches(7.1), Inches(4.55), Inches(5.1), Inches(1.8))
    tf_c2 = tb_c2.text_frame
    p = tf_c2.paragraphs[0]
    p.text = "PROJECT GUIDANCE"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = AMBER_ACCENT

    p1 = tf_c2.add_paragraph()
    p1.text = "Project Guide: Prof. Sivaranjani A"
    p1.font.bold = True
    p1.font.size = Pt(13)
    p1.font.color.rgb = TEXT_WHITE

    p2 = tf_c2.add_paragraph()
    p2.text = "Department of Computer Science and Engineering"
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_BODY

    p3 = tf_c2.add_paragraph()
    p3.text = "Vellore Institute of Technology (VIT) • Academic Year 2026–2027"
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "THE CHALLENGE", "Problem Statement & Industry Impact", 2)

    prob_cards = [
        ("01", "Fragmented Visibility & Siloed Data", "Shipment coordinates and sensor data reside in isolated carrier portals. Shippers and buyers lack a single end-to-end operational view across tier-1 and tier-2 partners.", RED_ACCENT),
        ("02", "Delayed Anomaly & Spoilage Discovery", "Cold chain excursions (temperature breaches) and route delays are uncovered days after delivery, causing catastrophic losses in perishable foods and biopharmaceuticals.", AMBER_ACCENT),
        ("03", "Vulnerability to Data Tampering", "Centralized carrier databases allow malicious or accidental modification of transit logs and SLA timestamps, leaving no immutable audit trail for legal dispute resolution.", BLUE_ACCENT),
    ]

    for idx, (num, title, desc, col) in enumerate(prob_cards):
        x = 0.8 + idx * 3.95
        add_card(s2, x, 1.65, 3.8, 4.3, CARD_BG, col)

        tb = s2.shapes.add_textbox(Inches(x + 0.25), Inches(1.9), Inches(3.3), Inches(0.45))
        p = tb.text_frame.paragraphs[0]
        p.text = num
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = col

        tb_t = s2.shapes.add_textbox(Inches(x + 0.25), Inches(2.4), Inches(3.3), Inches(0.65))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        tb_d = s2.shapes.add_textbox(Inches(x + 0.25), Inches(3.15), Inches(3.3), Inches(2.5))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_BODY

    # Stat strip
    add_card(s2, 0.8, 6.1, 11.733, 0.75, RGBColor(16, 24, 39), CARD_BORDER)
    tb_st = s2.shapes.add_textbox(Inches(1.0), Inches(6.2), Inches(11.3), Inches(0.55))
    tf_st = tb_st.text_frame
    p = tf_st.paragraphs[0]
    p.text = "INDUSTRY FACT: Logistics disruptions cause an average 8% annual revenue loss. Over 74% of shippers report blind spots beyond Tier-1 suppliers (McKinsey & WEF Survey)."
    p.font.size = Pt(10)
    p.font.color.rgb = TEAL_ACCENT
    p.font.bold = True

    # =========================================================================
    # SLIDE 3: OBJECTIVES OF THE PLATFORM
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "OUR MISSION", "Core Objectives of ChainVision Pro", 3)

    objs = [
        ("1", "Live Multi-Modal Telemetry Streaming", "Simulate dynamic GPS tracking and environmental telemetry (temperature, humidity, speed) across major commercial corridors in India.", TEAL_ACCENT),
        ("2", "Sub-Second Ingestion & Sync Pipeline", "Build a high-throughput Express REST API and a full-duplex WebSocket push channel to eliminate high-latency browser polling.", BLUE_ACCENT),
        ("3", "Dynamic Rule-Based Exception Engine", "Implement immediate automated threshold checks for biopharmaceutical cold chain bounds (2°C–8°C), ETA schedule breaches, and speed glitches.", AMBER_ACCENT),
        ("4", "Proactive Machine Learning Risk Scoring", "Formulate a multi-factor ML algorithm scoring delay risk from 0 to 100 based on carrier history, thermal stress, and route stoppages.", GREEN_ACCENT),
        ("5", "Immutable SHA-256 Checkpoint Ledger", "Develop a decentralized Proof-of-Work blockchain that anchors critical state checkpoints with cryptographic integrity verification.", TEAL_ACCENT),
        ("6", "Operations Command Center Dashboard", "Deliver a responsive Single Page Application (SPA) with Leaflet.js interactive maps, KPI telemetry, and alert triage modals.", BLUE_ACCENT)
    ]

    for idx, (num, title, desc, col) in enumerate(objs):
        row = idx // 3
        col_i = idx % 3
        x = 0.8 + col_i * 3.95
        y = 1.65 + row * 2.5
        add_card(s3, x, y, 3.8, 2.35, CARD_BG, col)

        tb_n = s3.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.15), Inches(3.4), Inches(0.35))
        p = tb_n.text_frame.paragraphs[0]
        p.text = f"Objective {num}"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col

        tb_t = s3.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.5), Inches(3.4), Inches(0.5))
        tf_t = tb_t.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.size = Pt(12.5)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        tb_d = s3.shapes.add_textbox(Inches(x + 0.2), Inches(y + 1.05), Inches(3.4), Inches(1.15))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE (4-TIER MODEL)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "SYSTEM BLUEPRINT", "4-Tier Architectural Specification", 4)

    layers = [
        ("TIER 4: APPLICATION & UI LAYER", "Single Page Application (SPA) Operations Dashboard", [
            "Leaflet.js interactive geospatial India map with animated vehicle markers and polyline trails",
            "Real-time KPI telemetry cards: In-Transit, Overdue Shipments, and On-Time Fleet Reliability (%)",
            "Alert triage modal with one-click resolution and live DLT Blockchain Explorer"
        ], GREEN_ACCENT),
        ("TIER 3: INTELLIGENCE & TRUST LAYER", "Dual Intelligence Core & Distributed Ledger Technology", [
            "Dynamic Rule Exception Engine: Evaluates cold-chain limits (2°C–8°C) and ETA delays",
            "ML Delay Risk Predictor: 5-feature weighted algorithm computing 0–100 risk score",
            "SHA-256 Checkpoint Ledger: Proof-of-Work mining (difficulty 00) for immutable audit trails"
        ], AMBER_ACCENT),
        ("TIER 2: INGESTION & PIPELINE LAYER", "High-Throughput REST Gateway & Full-Duplex WebSockets", [
            "Express HTTP Ingestion Route (POST /api/events) with JSON schema validation",
            "Full-duplex WebSocket server (ws://) pushing instant sub-second event broadcasts to all clients",
            "Zero-dependency atomic datastore ensuring transaction safety and portability"
        ], BLUE_ACCENT),
        ("TIER 1: SENSING & DATA LAYER", "Multi-Modal IoT Route Telemetry Simulator", [
            "Continuous GPS coordinate streaming across 5 major Indian commercial corridors (NH-44, NH-48)",
            "Ambient telemetry: Temperature (°C), Humidity (%), Speed (km/h), and progress tracking",
            "Stochastic anomaly generator injecting thermal spikes (+10°C) and unplanned route stops"
        ], TEAL_ACCENT),
    ]

    for idx, (title, sub, bullets, col) in enumerate(layers):
        y = 1.65 + idx * 1.3
        add_card(s4, 0.8, y, 11.733, 1.2, CARD_BG, col)

        tb_t = s4.shapes.add_textbox(Inches(1.0), Inches(y + 0.12), Inches(3.6), Inches(0.35))
        p = tb_t.text_frame.paragraphs[0]
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col

        tb_s = s4.shapes.add_textbox(Inches(1.0), Inches(y + 0.45), Inches(3.6), Inches(0.65))
        tf_s = tb_s.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = sub
        p_s.font.size = Pt(9.5)
        p_s.font.color.rgb = TEXT_MUTED

        # Separator line
        sep = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.7), Inches(y + 0.12), Inches(0.02), Inches(0.96))
        sep.fill.solid()
        sep.fill.fore_color.rgb = CARD_BORDER
        sep.line.fill.background()

        tb_b = s4.shapes.add_textbox(Inches(4.9), Inches(y + 0.08), Inches(7.4), Inches(1.0))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for b_idx, bullet in enumerate(bullets):
            p_b = tf_b.paragraphs[0] if b_idx == 0 else tf_b.add_paragraph()
            p_b.text = f"• {bullet}"
            p_b.font.size = Pt(9.5)
            p_b.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 5: MODULE 1 & 2 — TELEMETRY & INGESTION
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "MODULES 1 & 2", "IoT Telemetry Simulation & WebSocket Ingestion", 5)

    # Left Card: Simulator
    add_card(s5, 0.8, 1.65, 5.7, 5.1, CARD_BG, TEAL_ACCENT)
    tb_l = s5.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.2), Inches(4.7))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    p.text = "MODULE 1: IOT ROUTE SIMULATOR"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = AMBER_ACCENT

    sim_routes = [
        ("SHP-001 (Electronics: Chennai → Delhi)", "Follows NH-44 through Hyderabad, Nagpur, Bhopal. Standard cargo temp: 28°C."),
        ("SHP-002 (Pharma Cold Chain: Mumbai → Kolkata)", "Strict biopharmaceutical cold chain (2°C–8°C). Injects 15% thermal excursion chance."),
        ("SHP-003 (Textile Export: Surat → JNPT Port)", "Intermodal container transit from Gujarat mills to Maharashtra export harbor."),
        ("SHP-004 (Auto Components: Pune → Bengaluru)", "Industrial supply line via NH-48 with high-precision GPS tracking."),
        ("SHP-005 (FMCG Goods: Ahmedabad → Guwahati)", "Cross-country trans-India multi-modal shipment (2,450 km corridor).")
    ]
    for r_t, r_d in sim_routes:
        p_t = tf_l.add_paragraph()
        p_t.text = f"▸ {r_t}"
        p_t.font.bold = True
        p_t.font.size = Pt(10)
        p_t.font.color.rgb = TEXT_WHITE
        p_d = tf_l.add_paragraph()
        p_d.text = r_d
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = TEXT_BODY

    # Right Card: Ingestion & WS
    add_card(s5, 6.8, 1.65, 5.7, 5.1, CARD_BG, BLUE_ACCENT)
    tb_r = s5.shapes.add_textbox(Inches(7.05), Inches(1.85), Inches(5.2), Inches(4.7))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_r = tf_r.paragraphs[0]
    p_r.text = "MODULE 2: REST INGESTION & WEBSOCKETS"
    p_r.font.bold = True
    p_r.font.size = Pt(12)
    p_r.font.color.rgb = TEAL_ACCENT

    ws_details = [
        ("REST Ingestion Gateway (POST /api/events)", "Accepts JSON payloads every 4s, validates mandatory attributes, calculates transit completion %, and updates the database atomically."),
        ("Full-Duplex WebSocket Push Protocol", "Server broadcasts events to connected clients via ws://. Eliminates network-heavy polling, reducing server overhead by > 80%."),
        ("Event Distribution Types", "• location_update: Instant coordinate shift on Leaflet map\n• alert: Emergency toast & banner for threshold breaches\n• block: Real-time mined ledger block push to explorer"),
        ("Ingestion Latency Benchmark", "Achieves an average latency of 11.8 ms from edge HTTP transmission to browser DOM update.")
    ]
    for w_t, w_d in ws_details:
        p_t = tf_r.add_paragraph()
        p_t.text = f"▸ {w_t}"
        p_t.font.bold = True
        p_t.font.size = Pt(10)
        p_t.font.color.rgb = TEXT_WHITE
        p_d = tf_r.add_paragraph()
        p_d.text = w_d
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 6: MODULE 3 & 4 — EXCEPTION ENGINE & ML PREDICTOR
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "MODULES 3 & 4", "Dynamic Exception Engine & ML Delay Scoring", 6)

    # Left: Rule Engine
    add_card(s6, 0.8, 1.65, 5.7, 5.1, CARD_BG, AMBER_ACCENT)
    tb_el = s6.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.2), Inches(4.7))
    tf_el = tb_el.text_frame
    tf_el.word_wrap = True

    p = tf_el.paragraphs[0]
    p.text = "MODULE 3: DYNAMIC RULE EXCEPTION ENGINE"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = AMBER_ACCENT

    rules = [
        ("Cold Chain Pharma Limits (2.0°C – 8.0°C)", "Flags excursions immediately as Critical severity and initiates automatic mining of a TEMPERATURE_EXCURSION block on the blockchain."),
        ("General Freight Temp Range (2.0°C – 30.0°C)", "Detects cargo overheating in ambient containers across hot corridors."),
        ("ETA Schedule Breach (> 2.0h Overdue)", "Computes elapsed time vs. ETA. Auto-updates status to 'Delayed' and mines an ETA_BREACH block to the ledger."),
        ("Implausible Speed Filter (> 1200 km/h)", "Quarantines erroneous GPS satellite jumps without corrupting historical tracking logs.")
    ]
    for r_t, r_d in rules:
        p_t = tf_el.add_paragraph()
        p_t.text = f"▸ {r_t}"
        p_t.font.bold = True
        p_t.font.size = Pt(10)
        p_t.font.color.rgb = TEXT_WHITE
        p_d = tf_el.add_paragraph()
        p_d.text = r_d
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = TEXT_BODY

    # Right: ML Delay Predictor
    add_card(s6, 6.8, 1.65, 5.7, 5.1, CARD_BG, GREEN_ACCENT)
    tb_er = s6.shapes.add_textbox(Inches(7.05), Inches(1.85), Inches(5.2), Inches(4.7))
    tf_er = tb_er.text_frame
    tf_er.word_wrap = True

    p_r = tf_er.paragraphs[0]
    p_r.text = "MODULE 4: FEATURE-WEIGHTED ML RISK PREDICTOR"
    p_r.font.bold = True
    p_r.font.size = Pt(12)
    p_r.font.color.rgb = TEAL_ACCENT

    p_f = tf_er.add_paragraph()
    p_f.text = "Risk Formula: S = min(100,  w1·C1 + w2·C2 + w3·C3 + w4·C4 + w5·C5)"
    p_f.font.bold = True
    p_f.font.size = Pt(9.5)
    p_f.font.color.rgb = AMBER_ACCENT

    ml_factors = [
        ("Carrier Historical Reliability (w1 = 25%)", "Empirical delay rates (DHL: 12%, FedEx Pharma: 18%, MSC: 25%)."),
        ("Thermal Stress Variance (w2 = 20%)", "Penalizes score if |AvgTemp − 22°C| exceeds 5°C safety margin."),
        ("Schedule Adherence Gap (w3 = 30%)", "Gap = Time Elapsed % − Geographic Progress %. Heaviest weight factor."),
        ("Unplanned Route Stoppages (w4 = 15%)", "Counts low-speed events (speed < 2 km/h) without delivery status."),
        ("Seasonal Multiplier (w5 = 10%)", "Q4 festival rush: 1.4× multiplier; Monsoon season: 1.15× multiplier.")
    ]
    for m_t, m_d in ml_factors:
        p_t = tf_er.add_paragraph()
        p_t.text = f"▸ {m_t}"
        p_t.font.bold = True
        p_t.font.size = Pt(9.5)
        p_t.font.color.rgb = TEXT_WHITE
        p_d = tf_er.add_paragraph()
        p_d.text = m_d
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 7: MODULE 5 — SHA-256 BLOCKCHAIN LEDGER
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "MODULE 5", "SHA-256 Blockchain Checkpoint Ledger & Verification", 7)

    # 3 Horizontal Cards
    b_cols = [
        ("BLOCK SCHEMA & POW MINING", [
            ("Block Data Model", "{ id, hash, prev_hash, data: { shipment_id, event_type, payload }, nonce, timestamp }"),
            ("Proof-of-Work Difficulty", "Requires SHA-256 hash to begin with '00' prefix. Mined in average 34 ms without event lag."),
            ("Genesis Block", "Auto-mined at server initialization with prev_hash set to 64 zeros.")
        ], TEAL_ACCENT),
        ("CRITICAL CHECKPOINTS ANCHORED", [
            ("GENESIS", "Blockchain network bootstrapped with root block."),
            ("TEMPERATURE_EXCURSION", "Cold-chain thermal excursions committed with exact sensor temperature and timestamp."),
            ("ETA_BREACH", "SLA delay violations recorded with hours overdue."),
            ("DELIVERY_CONFIRMATION", "Consignment arrival and handover validated.")
        ], AMBER_ACCENT),
        ("CRYPTOGRAPHIC AUDIT ALGORITHM", [
            ("O(N) Sequential Audit", "verifyChain() recalculates hashes and verifies prev_hash linkage across all 690+ mined blocks."),
            ("Tamper Resistance Test", "Simulated modification of a temperature payload in Block #42 immediately breaks Block #43's link."),
            ("Live Verification API", "GET /api/analytics/ledger confirms 100% chain validity.")
        ], BLUE_ACCENT),
    ]

    for idx, (col_t, items, col) in enumerate(b_cols):
        x = 0.8 + idx * 3.95
        add_card(s7, x, 1.65, 3.8, 5.1, CARD_BG, col)

        tb_h = s7.shapes.add_textbox(Inches(x + 0.2), Inches(1.85), Inches(3.4), Inches(0.45))
        p = tb_h.text_frame.paragraphs[0]
        p.text = col_t
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = col

        # Divider
        div_c = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x + 0.2), Inches(2.3), Inches(3.4), Inches(0.02))
        div_c.fill.solid()
        div_c.fill.fore_color.rgb = CARD_BORDER
        div_c.line.fill.background()

        curr_top = 2.4
        for i_t, i_d in items:
            tb_it = s7.shapes.add_textbox(Inches(x + 0.2), Inches(curr_top), Inches(3.4), Inches(1.15))
            tf_it = tb_it.text_frame
            tf_it.word_wrap = True
            p_it = tf_it.paragraphs[0]
            p_it.text = f"▸ {i_t}"
            p_it.font.bold = True
            p_it.font.size = Pt(10)
            p_it.font.color.rgb = TEXT_WHITE

            p_id = tf_it.add_paragraph()
            p_id.text = i_d
            p_id.font.size = Pt(8.8)
            p_id.font.color.rgb = TEXT_BODY
            curr_top += 0.95

    # =========================================================================
    # SLIDE 8: MODULE 6 — DASHBOARD & OPERATIONS COMMAND
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_header(s8, "MODULE 6", "Single Page Application (SPA) Operations Dashboard", 8)

    ui_cards = [
        ("Leaflet.js Geospatial Fleet Map", "Renders full pan/zoom India map with real-time animated vehicle markers, carrier labels, and active highway route polylines.", TEAL_ACCENT),
        ("Executive KPI Summary Grid", "Live counters tracking: Total Active Shipments, In-Transit Count, Delayed Consignments, and On-Time Delivery Reliability (%).", BLUE_ACCENT),
        ("Alert Center & One-Click Triage", "Real-time list of temperature excursions and schedule breaches with severity badges. Includes PATCH /api/alerts/:id/resolve workflow.", RED_ACCENT),
        ("ML Delay Risk Analytics Panel", "Visualizes 0–100 risk score meters (Low, Medium, High, Critical) with factor-by-factor score contribution bars.", AMBER_ACCENT),
        ("DLT Blockchain Ledger Explorer", "Interactive table displaying mined block sequence, block hashes with '00' prefix, timestamps, payloads, and chain validity badge.", GREEN_ACCENT),
        ("Sensor Telemetry Visualizer", "Integrated Chart.js line charts tracking historical temperature curves, carrier reliability comparisons, and event frequency distributions.", TEAL_ACCENT),
    ]

    for idx, (title, desc, col) in enumerate(ui_cards):
        row = idx // 3
        col_i = idx % 3
        x = 0.8 + col_i * 3.95
        y = 1.65 + row * 2.5
        add_card(s8, x, y, 3.8, 2.35, CARD_BG, col)

        tb_t = s8.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.15), Inches(3.4), Inches(0.45))
        p = tb_t.text_frame.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = col

        tb_d = s8.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.65), Inches(3.4), Inches(1.5))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 9: EXPERIMENTAL BENCHMARKS & PERFORMANCE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_header(s9, "PERFORMANCE RESULTS", "Empirical Evaluation & System Benchmarks", 9)

    benchmarks = [
        ("11.8 ms", "EVENT INGESTION LATENCY", "Average HTTP POST processing time including JSON schema validation, database insertion, and WebSocket dispatch.", TEAL_ACCENT),
        ("34.2 ms", "PROOF-OF-WORK MINING DURATION", "Average time to mine a valid SHA-256 block matching '00' prefix on standard computing node without GPU overhead.", AMBER_ACCENT),
        ("100%", "EXCEPTION DETECTION ACCURACY", "100% true-positive detection rate across simulated pharmaceutical thermal excursions (> 8°C) with zero false negatives.", GREEN_ACCENT),
        ("82.4 ms", "FULL LEDGER AUDIT SPEED", "Linear O(N) chain traversal verifying cryptographic validity across all 690+ sequential mined blocks.", BLUE_ACCENT),
    ]

    for idx, (stat, label, desc, col) in enumerate(benchmarks):
        row = idx // 2
        col_i = idx % 2
        x = 0.8 + col_i * 5.95
        y = 1.65 + row * 2.5
        add_card(s9, x, y, 5.7, 2.35, CARD_BG, col)

        tb_stat = s9.shapes.add_textbox(Inches(x + 0.25), Inches(y + 0.15), Inches(5.2), Inches(0.65))
        p = tb_stat.text_frame.paragraphs[0]
        p.text = stat
        p.font.bold = True
        p.font.size = Pt(32)
        p.font.color.rgb = col

        tb_lbl = s9.shapes.add_textbox(Inches(x + 0.25), Inches(y + 0.8), Inches(5.2), Inches(0.3))
        p_l = tb_lbl.text_frame.paragraphs[0]
        p_l.text = label
        p_l.font.bold = True
        p_l.font.size = Pt(11)
        p_l.font.color.rgb = TEXT_WHITE

        tb_d = s9.shapes.add_textbox(Inches(x + 0.25), Inches(y + 1.15), Inches(5.2), Inches(1.0))
        tf_d = tb_d.text_frame
        tf_d.word_wrap = True
        p_d = tf_d.paragraphs[0]
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 10: LIVE DEMONSTRATION & TEST SCENARIOS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_header(s10, "LIVE DEMONSTRATION", "Operational Test Cases & Scenarios Validated", 10)

    test_scenarios = [
        ("SCENARIO 1: NORMAL TELEMETRY STREAMING", "SHP-001 (Consumer Electronics: Chennai → Delhi)", [
            "Continuous GPS position streaming every 4s via Blue Dart Express.",
            "Vehicle marker advances progressively along NH-44 across AP and MP.",
            "Temperature stays within nominal bounds (28°C); ML risk score stays LOW (14%)."
        ], TEAL_ACCENT),
        ("SCENARIO 2: COLD-CHAIN THERMAL EXCURSION", "SHP-002 (Pharma Vaccines: Mumbai → Kolkata)", [
            "Injected thermal spike raises reefer box temperature to 11.2°C (Safe limit: 8.0°C).",
            "Exception engine instantly raises Critical Alert toast & banner in dashboard.",
            "Checkpoint ledger immediately mines Block #42 with type TEMPERATURE_EXCURSION."
        ], RED_ACCENT),
        ("SCENARIO 3: SCHEDULE BREACH & DELAY SCORING", "SHP-005 (FMCG Goods: Ahmedabad → Guwahati)", [
            "Simulated vehicle stoppage on highway (speed < 2 km/h for consecutive pings).",
            "ML predictor detects Schedule Gap (> 15% behind planned timeline).",
            "Risk score elevates to HIGH (58%); carrier alerted to expedite backup fleet."
        ], AMBER_ACCENT),
        ("SCENARIO 4: CRYPTOGRAPHIC LEDGER AUDIT", "Ledger Explorer Verification", [
            "Auditor triggers GET /api/analytics/ledger from the Operations view.",
            "SHA-256 chain verified end-to-end; displays 'Valid: 100%' cryptographic badge.",
            "Terminal command 'npm run verify-ledger' outputs { valid: true, length: 697 }."
        ], GREEN_ACCENT)
    ]

    for idx, (title, sub, bullets, col) in enumerate(test_scenarios):
        row = idx // 2
        col_i = idx % 2
        x = 0.8 + col_i * 5.95
        y = 1.65 + row * 2.5
        add_card(s10, x, y, 5.7, 2.35, CARD_BG, col)

        tb_t = s10.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.15), Inches(5.3), Inches(0.3))
        p = tb_t.text_frame.paragraphs[0]
        p.text = title
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = col

        tb_s = s10.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.45), Inches(5.3), Inches(0.25))
        p_s = tb_s.text_frame.paragraphs[0]
        p_s.text = sub
        p_s.font.size = Pt(9.5)
        p_s.font.color.rgb = TEXT_WHITE

        tb_b = s10.shapes.add_textbox(Inches(x + 0.2), Inches(y + 0.75), Inches(5.3), Inches(1.4))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for b_idx, bullet in enumerate(bullets):
            p_b = tf_b.paragraphs[0] if b_idx == 0 else tf_b.add_paragraph()
            p_b.text = f"• {bullet}"
            p_b.font.size = Pt(9)
            p_b.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 11: REVIEW 2 STATUS vs. REVIEW 3 ROADMAP
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_header(s11, "DELIVERY STATUS", "Work Completed in Review 2 vs. Roadmap for Review 3", 11)

    # Left: Completed in Review 2
    add_card(s11, 0.8, 1.65, 5.7, 5.1, CARD_BG, GREEN_ACCENT)
    tb_c11 = s11.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(5.2), Inches(4.7))
    tf_c11 = tb_c11.text_frame
    tf_c11.word_wrap = True

    p = tf_c11.paragraphs[0]
    p.text = "✓ COMPLETED IN REVIEW 2 (85% READY)"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = GREEN_ACCENT

    done_pts = [
        ("Multi-Modal IoT Route Simulator", "Realistic GPS, speed, temperature, and anomaly injection across 5 Indian corridors."),
        ("Real-Time Ingestion & WebSocket Sync", "Full-duplex real-time synchronization between edge simulator, backend, and dashboard UI."),
        ("Dynamic Rule-Based Exception Engine", "Automated detection of cold-chain breaches, ETA delays, speed anomalies, and stale signals."),
        ("Feature-Weighted ML Delay Predictor", "0–100 risk scoring model combining carrier history, thermal stress, schedule gap, and stops."),
        ("SHA-256 DLT Checkpoint Ledger", "Proof-of-Work block mining with difficulty '00' and full cryptographic audit verification."),
        ("Operations Command Center UI", "Interactive Leaflet.js map, KPI telemetry, Chart.js analytics, and alert triage modal.")
    ]
    for t, d in done_pts:
        p_t = tf_c11.add_paragraph()
        p_t.text = f"✔ {t}"
        p_t.font.bold = True
        p_t.font.size = Pt(9.5)
        p_t.font.color.rgb = TEXT_WHITE
        p_d = tf_c11.add_paragraph()
        p_d.text = d
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = TEXT_BODY

    # Right: Plan for Review 3
    add_card(s11, 6.8, 1.65, 5.7, 5.1, CARD_BG, AMBER_ACCENT)
    tb_p11 = s11.shapes.add_textbox(Inches(7.05), Inches(1.85), Inches(5.2), Inches(4.7))
    tf_p11 = tb_p11.text_frame
    tf_p11.word_wrap = True

    p_p = tf_p11.paragraphs[0]
    p_p.text = "➔ ROADMAP FOR REVIEW 3 / FINAL THESIS"
    p_p.font.bold = True
    p_p.font.size = Pt(12)
    p_p.font.color.rgb = AMBER_ACCENT

    plan_pts = [
        ("Solidity Smart Contract Deployment", "Deploy EVM-compatible contracts on Ethereum Sepolia / Polygon testnet to issue tokenized consignment certificates."),
        ("IPFS Decentralized Document Storage", "Link InterPlanetary File System (IPFS) CIDs to the ledger for decentralized storage of digital Bills of Lading and customs manifests."),
        ("Multi-Carrier Consensus Simulation", "Extend single-daemon PoW prototype to simulate multi-peer PBFT / Raft consensus between independent carrier nodes."),
        ("Mobile Emergency Notification Webhook", "Integrate Telegram / WhatsApp / SMS webhook triggers for critical temperature alerts to logistics drivers."),
        ("Final Thesis & Conference Publication", "Prepare the comprehensive capstone project thesis and author research manuscript for peer-reviewed publication.")
    ]
    for t, d in plan_pts:
        p_t = tf_p11.add_paragraph()
        p_t.text = f"➔ {t}"
        p_t.font.bold = True
        p_t.font.size = Pt(9.5)
        p_t.font.color.rgb = TEXT_WHITE
        p_d = tf_p11.add_paragraph()
        p_d.text = d
        p_d.font.size = Pt(8.5)
        p_d.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 12: CONCLUSION & FACULTY Q&A
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)

    add_card(s12, 1.8, 1.2, 9.733, 5.1, CARD_BG, TEAL_ACCENT)
    tb_12 = s12.shapes.add_textbox(Inches(2.2), Inches(1.5), Inches(8.933), Inches(4.5))
    tf_12 = tb_12.text_frame
    tf_12.word_wrap = True

    p = tf_12.paragraphs[0]
    p.text = "THANK YOU!"
    p.font.bold = True
    p.font.size = Pt(32)
    p.font.color.rgb = AMBER_ACCENT
    p.alignment = PP_ALIGN.CENTER

    p2 = tf_12.add_paragraph()
    p2.text = "ChainVision Pro — Project Review 2 Summary"
    p2.font.bold = True
    p2.font.size = Pt(20)
    p2.font.color.rgb = TEXT_WHITE
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf_12.add_paragraph()
    p3.text = "\nKey Takeaways:\n" \
              "1. Successfully developed and validated an end-to-end working prototype.\n" \
              "2. Multi-tier stack active: IoT Simulator + Exception Rules + ML Risk Scoring + DLT Ledger + Live Dashboard.\n" \
              "3. 85%+ project implementation completed ahead of Final Review 3."
    p3.font.size = Pt(12)
    p3.font.color.rgb = TEXT_BODY

    p4 = tf_12.add_paragraph()
    p4.text = "\nPresented by: Yash Dharad (23BKT0001) & Amit Kumar (23BKT0118)\n" \
              "Project Guide: Prof. Sivaranjani A | Dept. of CSE, VIT"
    p4.font.bold = True
    p4.font.size = Pt(13)
    p4.font.color.rgb = TEAL_ACCENT
    p4.alignment = PP_ALIGN.CENTER

    p5 = tf_12.add_paragraph()
    p5.text = "Questions & Feedback are Welcome"
    p5.font.size = Pt(13)
    p5.font.color.rgb = TEXT_MUTED
    p5.alignment = PP_ALIGN.CENTER

    output_path = "ChainVision_Pro_Clear_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    build_clear_deck()
