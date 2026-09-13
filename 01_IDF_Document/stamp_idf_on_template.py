"""
TCDS IDF-B — Template-Faithful PDF Generator
Strategy: Use PyMuPDF to STAMP our content directly onto a copy of the 
original template pages, pixel-perfectly preserving all formatting, 
borders, header, footer, section labels, and TRL table.
We write our content into the blank answer areas identified by coordinate analysis.
"""
import sys
sys.path.insert(0, '/Users/yuvi/Library/Python/3.9/lib/python/site-packages')

import fitz  # PyMuPDF
import os
from PIL import Image as PILImage

TEMPLATE = '/Users/yuvi/Patents/patent1/01_IDF_Document/Invention_Disclosure_Format_B.pdf'
GRAPH_DIR = '/Users/yuvi/Patents/patent1/03_Graphs_and_Visualizations'
OUT      = '/Users/yuvi/Patents/patent1/01_IDF_Document/IDF_B_TCDS_Submitted.pdf'

# ── CONTENT ───────────────────────────────────────────────────────────────────
# Each entry: (x, y, max_width, font, size, text_lines_list)
# x,y = top-left of text in page coords (pt), y increases downward

FONT_BOLD   = 'Times-Bold'
FONT_REG    = 'Times-Roman'
BLACK = (0, 0, 0)
BLUE  = (0.08, 0.18, 0.45)

# We will build a multi-page output:
# Page 1 = template page 1 with content stamped in sections 1-9
# Pages 2-N = inserted graph/detail pages  
# Last page = template page 2 (TRL) with TRL 3 ticked

def get_text_width(text, font, size):
    """Estimate text width using fitz text length."""
    tmp_doc = fitz.open()
    tmp_page = tmp_doc.new_page(width=1000, height=100)
    # Use insert_text and get the rect
    # Approximate: average char width ≈ size * 0.55 for Times, 0.50 for Courier
    factor = 0.52 if 'Bold' in font else 0.50
    tmp_doc.close()
    return len(text) * size * factor

def wrap_text(text, font, size, max_width, doc_ref=None):
    """Wrap text to fit max_width, return list of lines."""
    words = text.split(' ')
    lines = []
    current = ''
    for word in words:
        test = (current + ' ' + word).strip()
        w = get_text_width(test, font, size)
        if w <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines if lines else [text]

def insert_text_block(page, x, y, max_w, font, size, text, color=BLACK, line_height=None):
    """Insert wrapped text block into page. Returns y position after last line."""
    if line_height is None:
        line_height = size * 1.35
    # Use a temporary doc to measure
    tmp = fitz.open()
    tmp.new_page()
    lines = wrap_text(text, font, size, max_w, tmp)
    tmp.close()
    for line in lines:
        page.insert_text((x, y), line, fontname=font, fontsize=size, color=color)
        y += line_height
    return y

def insert_text_lines(page, x, y, max_w, font, size, lines, color=BLACK, line_height=None):
    """Insert pre-split lines."""
    if line_height is None:
        line_height = size * 1.35
    for line in lines:
        if line.startswith('__BOLD__'):
            page.insert_text((x, y), line[8:], fontname=FONT_BOLD, fontsize=size, color=color)
        else:
            page.insert_text((x, y), line, fontname=font, fontsize=size, color=color)
        y += line_height
    return y

def draw_thin_rect(page, x0, y0, x1, y1, color=(0,0,0), width=0.5):
    page.draw_rect(fitz.Rect(x0, y0, x1, y1), color=color, width=width)

def draw_filled_rect(page, x0, y0, x1, y1, fill_color):
    page.draw_rect(fitz.Rect(x0, y0, x1, y1), color=None, fill=fill_color, width=0)

def insert_image_scaled(page, img_path, x0, y0, max_w, max_h=None):
    """Insert image scaled to max_w, preserve aspect ratio."""
    with PILImage.open(img_path) as im:
        iw, ih = im.size
    scale = max_w / iw
    if max_h and ih * scale > max_h:
        scale = max_h / ih
    w = iw * scale
    h = ih * scale
    rect = fitz.Rect(x0, y0, x0 + w, y0 + h)
    page.insert_image(rect, filename=img_path)
    return y0 + h

def draw_table(page, x0, y0, col_widths, rows, font=FONT_REG, size=7.5,
               header_fill=(0.18, 0.28, 0.55), row_fills=None, padding=3):
    """Draw a table with text content."""
    if row_fills is None:
        row_fills = [(1,1,1), (0.93,0.95,0.98)]
    
    y = y0
    for ri, row in enumerate(rows):
        # Calculate row height by pre-wrapping all cells
        max_lines = 1
        tmp = fitz.open()
        tmp.new_page()
        cell_lines_list = []
        for ci, cell in enumerate(row):
            cw = col_widths[ci] - 2*padding
            cell_text = cell if isinstance(cell, str) else cell[0]
            is_bold = isinstance(cell, tuple) and cell[1] == 'bold'
            f = FONT_BOLD if (ri == 0 or is_bold) else FONT_REG
            lines = wrap_text(cell_text, f, size, cw, tmp)
            cell_lines_list.append((lines, f))
            max_lines = max(max_lines, len(lines))
        tmp.close()
        
        row_height = max_lines * size * 1.3 + 2 * padding
        
        # Draw cell backgrounds and borders
        x = x0
        for ci, (cell_lines, cf) in enumerate(cell_lines_list):
            cw = col_widths[ci]
            # Fill
            if ri == 0:
                draw_filled_rect(page, x, y, x+cw, y+row_height, header_fill)
            else:
                fill = row_fills[(ri-1) % len(row_fills)]
                draw_filled_rect(page, x, y, x+cw, y+row_height, fill)
            # Border
            draw_thin_rect(page, x, y, x+cw, y+row_height, color=(0.5,0.5,0.5))
            # Text
            ty = y + padding + size
            text_color = (1,1,1) if ri == 0 else BLACK
            for line in cell_lines:
                page.insert_text((x + padding, ty), line,
                                  fontname=cf, fontsize=size, color=text_color)
                ty += size * 1.3
            x += cw
        
        y += row_height
    
    return y  # bottom y of table

# ── BUILD THE PDF ──────────────────────────────────────────────────────────────
def build():
    src = fitz.open(TEMPLATE)
    out = fitz.open()

    # ── PAGE 1: Template page 1 with sections 1-9 filled ─────────────────────
    # Clone template page 1
    out.insert_pdf(src, from_page=0, to_page=0)
    p1 = out[0]

    LX = 54.0   # left x for content
    RX = 547.0  # right x boundary  
    TW = RX - LX  # text width ≈ 493

    FS  = 8.5   # main content font size
    LH  = 11.5  # line height
    SFS = 7.5   # small font size
    SLH = 10.5

    # ── Section 1: Title (y≈161, next section at 213)
    y = 174.0
    insert_text_lines(p1, LX, y, TW, FONT_BOLD, FS,
        ['Temporal Cash-Flow Disturbance Simulator (TCDS): A System and Method for',
         'Propagating Quantified Monetary Disturbances Through a Temporal Business-Event',
         'Graph to Compute a Liquidity Impact Window with Multi-Path Attribution'],
        color=BLACK, line_height=LH)

    # ── Section 2: Field (y≈213, next at 278)
    y = 226.0
    fields = [
        'Business Analytics & Financial Technology (FinTech)',
        'Temporal Graph Computing & Working Capital Management',
        'Supply Chain Finance & Operational Risk Simulation',
        'Decision Support Systems for Enterprise Financial Operations',
    ]
    for f in fields:
        p1.insert_text((LX, y), f'\u2022 {f}', fontname=FONT_REG, fontsize=FS, color=BLACK)
        y += LH

    # ── Section 3: Prior Art Table (y≈278, next at 370)
    y = 293.0
    prior_art_rows = [
        ['Patent / Publication', 'Description', 'Relevance / Gap from this Invention'],
        ['US20240362563A1\n(pub. 2024)', 'Financial risk graph; seed-node risk propagation; exposure scoring; subgraph visualization',
         'Propagates dimensionless risk scores — NOT monetary amounts. No cash scheduling, no Liquidity Impact Window.'],
        ['US12380389B2\n(granted 2025)', 'Graph-based financial risk propagation; entity-level relationship graph; exposure metrics',
         'Entity-level graph (companies as nodes). No business-mechanism events as nodes; no time-aware cash scheduling.'],
        ['US20260120033A1\n(pub. 2026)', 'Business dependency graph for systemic risk; graph traversal from seed events',
         'Risk-score centric. No monetary disturbance object; no cash trajectory; no Liquidity Impact Window.'],
        ['US6167385A', 'Event-driven supply chain simulation for inventory/logistics optimization',
         'Logistics focused. No monetary disturbance propagation through a financial-event graph; no liquidity window.'],
        ['Tangsucheeva & Prabhu\n(PSU, 2013)', 'Academic study of Cash-Flow Bullwhip Effect — working-capital variance amplification in supply chains',
         'Analytical/theoretical only. No computational system, no temporal graph, no disturbance-to-window pipeline.'],
        ['Temporal Attentive Graph\nNetworks (2024)', 'Temporal graph neural network for financial contagion/anomaly detection; outputs risk scores',
         'Statistical learning → anomaly score output. No cash-event scheduling; no multi-path convergence; no LIW.'],
    ]
    col_w = [TW*0.23, TW*0.35, TW*0.42]
    draw_table(p1, LX, y, col_w, prior_art_rows, size=7.0,
               header_fill=(0.15, 0.25, 0.50), row_fills=[(1,1,1),(0.94,0.96,0.99)])

    # ── Section 4: Summary (y≈370, next at 442)
    y = 382.0
    s4_lines = [
        '__BOLD__Problem: Modern businesses operate complex networks of operational and financial events.',
        'A single disturbance (e.g., supplier capacity -30%) cascades through purchase orders,',
        'inventory, production, invoicing, and receivables — ultimately impacting cash days later.',
        'No existing system translates "Supplier S17 capacity -30%" into a time-resolved, multi-path',
        'cash impact analysis with a Liquidity Impact Window (LIW: start/peak/deficit/recovery).',
        '__BOLD__Gap vs Prior Art: US20240362563A1/US12380389B2 propagate dimensionless risk scores',
        '(not USD amounts). ERP what-if tools use aggregate line items, not business-event graphs.',
        '__BOLD__Novelty: TCDS uniquely combines: (1) monetary disturbance as first-class typed state,',
        '(2) event-level temporal graph (POs/Invoices/AR/AP/Cash as nodes), (3) dual-transform',
        'edges (amount + time), (4) multi-path convergence with per-path attribution, and',
        '(5) Liquidity Impact Window as primary structured output. No prior art found unifying all five.',
    ]
    insert_text_lines(p1, LX, y, TW, FONT_REG, FS, s4_lines, color=BLACK, line_height=LH)

    # ── Section 5: Objectives (y≈442, next at 519)
    y = 454.0
    obj_lines = [
        '1. Enable managers to input a natural-language disturbance and receive time-resolved cash impact.',
        '2. Model business operations as an event-level temporal directed graph of settlement mechanisms.',
        '3. Propagate a quantified monetary disturbance preserving both magnitude and timing at each step.',
        '4. Detect multi-path convergence and attribute each path\'s monetary contribution individually.',
        '5. Compute a structured Liquidity Impact Window: {start, peak, deficit, duration, recovery}.',
        '6. Maintain an immutable baseline for auditable, governance-compliant scenario comparison.',
        '7. Support state-dependent nonlinear propagation rules (e.g., threshold-triggered financing).',
    ]
    insert_text_lines(p1, LX, y, TW, FONT_REG, FS, obj_lines, color=BLACK, line_height=LH)

    # ── Section 6: Working Principle (y≈519, next at 596)
    y = 530.0
    s6_lines = [
        'The TCDS operates as an 11-stage deterministic pipeline: (1) Ingest business data (POs,',
        'invoices, receipts, payments). (2) Build a temporal directed graph: nodes = 13 typed business',
        'events; edges = {dependency_strength, expected_delay, monetary_conversion, propagation_rule}.',
        '(3) Freeze an immutable baseline cash-flow timeline. (4) Translate user disturbance into a',
        'structured Disturbance Object: {magnitude, unit, effective_time, duration, conversion_rule}.',
        '(5) Identify affected temporal subgraph. (6) Propagate: target_delta = source_delta x dep_strength;',
        'target_time = source_time + delay. (7) Converge multiple paths at shared cash events, preserving',
        'per-path attribution. (8) Compute disturbance cash trajectory. (9) Detect Liquidity Impact Window.',
        '(10) Compare baseline vs disturbance. (11) Render auditable explanation on 9-panel dashboard.',
    ]
    insert_text_lines(p1, LX, y, TW, FONT_REG, FS, s6_lines, color=BLACK, line_height=LH)

    # ── Section 7: Description (y≈596, next at 677) — brief + pointer to appended pages
    y = 608.0
    s7_lines = [
        '__BOLD__7.1 System Architecture: 11-module pipeline — Ingestion → Temporal Graph Builder →',
        'Baseline Freeze → Disturbance Translator → Affected Subgraph Selector → Temporal Monetary',
        'Propagation Engine → Multi-Path Convergence → Cash-Flow Trajectory → LIW Detector →',
        'Baseline vs Disturbance Comparison → 9-Panel Dashboard. See Figure 2 (appended page).',
        '__BOLD__7.2 Core Propagation Rule: target_delta = source_delta x dependency_strength x',
        'monetary_conversion(source_delta); target_time = source_time + expected_delay.',
        '__BOLD__7.3 Multi-Path Convergence (DIST-001): Path A (Revenue): Supplier[-30%] \u2192 PO \u2192 IR',
        '\u2192 Production \u2192 Invoice \u2192 AR \u2192 Cash: -$178,125 at T+72d (81%). Path B (Emergency):',
        'Supplier \u2192 ExpenseEvent \u2192 AP \u2192 Cash: -$45,000 at T+37d (19%). Combined: -$223,125.',
        '__BOLD__Full technical detail, all figures, and datasets appended on supporting pages.',
    ]
    insert_text_lines(p1, LX, y, TW, FONT_REG, FS, s7_lines, color=BLACK, line_height=LH)

    # ── Section 8: Experimental Validation (y≈677, next at 748)
    y = 688.0
    s8_lines = [
        '__BOLD__Dataset: 12 suppliers, 60 purchase orders, 80 customer orders, 120-day horizon,',
        'starting cash $500K. Disturbance DIST-001: Supplier S03 capacity -30% (60 days).',
        '__BOLD__Results: Impact start T+21d | Peak deficit date T+72d | Peak cash deficit -$218,400',
        'vs baseline | Impact duration 47 days | Recovery start T+85d | Recovery date T+103d |',
        'Cumulative cash delta -$341,750 | Path A: 81% (-$178,125) | Path B: 19% (-$45,000).',
        '__BOLD__Tests passed: Determinism (2 identical runs), Baseline immutability, Multi-path',
        'convergence with attribution, Threshold propagation (FinancingEvent), Audit log (12 steps).',
    ]
    insert_text_lines(p1, LX, y, TW, FONT_REG, FS, s8_lines, color=BLACK, line_height=LH)

    # ── Section 9: Protection (y≈748, bottom ≈ 820)
    y = 760.0
    s9_lines = [
        'A: Method — Quantified monetary disturbance as first-class typed state (not risk score).',
        'B: System — Event-level temporal business-event graph with dual-transform edges (amount+time).',
        'C: Method — Multi-path monetary convergence with per-path attribution at shared cash events.',
        'D: Method — Liquidity Impact Window: {start, peak_date, peak_deficit, duration, recovery}.',
        'E: System — End-to-end disturbance-to-LIW pipeline with immutable baseline & audit log.',
        'F: Method — State-dependent, threshold-based nonlinear propagation rules on graph edges.',
    ]
    insert_text_lines(p1, LX, y, TW, FONT_REG, FS, s9_lines, color=BLACK, line_height=LH)

    # ── APPENDED DETAIL PAGES ─────────────────────────────────────────────────
    # Each page uses the template header/footer by cloning page 1's decorative elements
    # We'll create plain content pages that match the template header style

    def new_content_page(out_doc, title_line=''):
        """Add a new page matching template style."""
        np = out_doc.new_page(width=595.32, height=841.92)
        # White background
        np.draw_rect(fitz.Rect(0, 0, 595.32, 841.92), color=None, fill=(1,1,1), width=0)
        # Header line 1 — VIT branding
        np.insert_text((53.9, 36.1), '©VIT IPR&TTCELL',
                        fontname=FONT_REG, fontsize=11, color=BLACK)
        # Title centered
        np.insert_text((88, 81.5), '                                 Invention Disclosure Format (IDF)-B',
                        fontname=FONT_BOLD, fontsize=12, color=BLACK)
        # Top-right info box — draw borders
        bx = 410.0
        np.draw_rect(fitz.Rect(bx, 48, 547.5, 116), color=BLACK, width=0.5)
        np.draw_line(fitz.Point(bx, 69), fitz.Point(547.5, 69), color=BLACK, width=0.4)
        np.draw_line(fitz.Point(bx, 90), fitz.Point(547.5, 90), color=BLACK, width=0.4)
        np.draw_line(fitz.Point(475, 48), fitz.Point(475, 116), color=BLACK, width=0.4)
        # Info text
        for (lbl, val, yy) in [
            ('Document No.', '02-IPR-R003', 58.4),
            ('Issue No/Date', '2/01.02.2024', 82.6),
            ('Amd. No/Date', '0/00.00.0000', 103.1),
        ]:
            np.insert_text((416.5, yy), lbl, fontname='Helvetica', fontsize=8, color=BLACK)
            np.insert_text((479.5, yy), val, fontname='Helvetica', fontsize=8, color=BLACK)
        # Horizontal separator under header
        np.draw_line(fitz.Point(54, 120), fitz.Point(547, 120), color=BLACK, width=0.5)
        # Section label if provided
        if title_line:
            np.insert_text((54, 140), title_line, fontname=FONT_BOLD, fontsize=9, color=BLACK)
        return np

    # ── Appended Page A: Temporal Business-Event Graph ──────────────────────
    pA = new_content_page(out, 'APPENDIX A — Temporal Business-Event Graph (Figure 2)')
    y_a = 155.0
    desc_a = [
        'The TCDS models business operations as a temporal directed graph where nodes represent',
        'individual business events and settlement mechanisms — not merely companies or entities.',
        'This is a critical novelty: prior art (US20240362563A1) uses entity-level nodes. TCDS uses',
        '13 typed event nodes: Supplier, PurchaseOrder, InventoryReceipt, ProductionEvent,',
        'CustomerOrder, Invoice, AccountsReceivable, CustomerPayment, AccountsPayable,',
        'SupplierPayment, ExpenseEvent, CashAccount, FinancingEvent.',
        'Each edge carries 10 typed attributes: relationship_type, dependency_strength,',
        'expected_delay, delay_distribution, monetary_conversion, probability, effective_start,',
        'effective_end, confidence, propagation_rule. Edges transform BOTH monetary magnitude',
        'AND scheduled settlement time — the dual-transform property absent in all prior art.',
    ]
    y_a = insert_text_lines(pA, LX, y_a, TW, FONT_REG, FS, desc_a, line_height=LH)
    y_a += 6
    # Insert business event graph image
    gpath = f'{GRAPH_DIR}/02_temporal_business_event_graph.png'
    y_a = insert_image_scaled(pA, gpath, LX, y_a, max_w=TW, max_h=260)
    y_a += 4
    pA.insert_text((LX, y_a),
        'Figure 2: Temporal Business-Event Graph — 13 node types, 14 dual-transform directed edges.',
        fontname=FONT_REG, fontsize=8, color=(0.35,0.35,0.35))
    y_a += 14

    # Node table
    pA.insert_text((LX, y_a), 'Table 1: Node Taxonomy',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_a += 13
    node_rows = [
        ['Node Type', 'Category', 'Cash Effect'],
        ['Supplier', 'Operational', 'Indirect'],
        ['PurchaseOrder', 'Operational', 'Indirect'],
        ['InventoryReceipt', 'Operational', 'Triggers AP/outflow'],
        ['ProductionEvent', 'Operational', 'COGS timing'],
        ['CustomerOrder', 'Revenue', 'Indirect'],
        ['Invoice', 'Revenue', 'Initiates AR chain'],
        ['AccountsReceivable', 'Revenue', 'Future cash inflow'],
        ['CustomerPayment', 'Revenue', 'Direct cash inflow'],
        ['AccountsPayable', 'Cost', 'Future cash outflow'],
        ['SupplierPayment', 'Cost', 'Direct cash outflow'],
        ['ExpenseEvent', 'Cost', 'Direct cash outflow'],
        ['CashAccount', 'Cash', 'State convergence node'],
        ['FinancingEvent', 'Financing', 'Threshold-triggered inflow'],
    ]
    draw_table(pA, LX, y_a, [TW*0.35, TW*0.30, TW*0.35], node_rows,
               size=7.5, header_fill=(0.15, 0.25, 0.50))

    # ── Appended Page B: Propagation Timeline ───────────────────────────────
    pB = new_content_page(out, 'APPENDIX B — Propagation Algorithm & Timeline (Figure 3, 4)')
    y_b = 155.0
    algo_lines = [
        '__BOLD__Core Propagation Algorithm:',
        'For each activated edge (src_node -> tgt_node) in affected subgraph:',
        '  tgt_delta    = src_delta x edge.dependency_strength x edge.monetary_conversion(src_delta)',
        '  tgt_schedule = src_schedule + edge.expected_delay',
        '  If edge.propagation_rule == "threshold":',
        '      Activate only if current_state(tgt_node) crosses configured threshold',
        '  Log: {src_event, tgt_event, src_delta, tgt_delta, dep_strength, schedule, rule, confidence}',
        '',
        '__BOLD__DIST-001 Worked Example — Two Paths Converging at CashAccount:',
    ]
    y_b = insert_text_lines(pB, LX, y_b, TW, FONT_REG, FS, algo_lines, line_height=LH)

    # Path tables
    path_a_rows = [
        ['Step', 'Source Event', 'Target Event', 'Source Delta', 'Target Delta', 'Dep.Str.', 'Delay', 'Scheduled'],
        ['1', 'Supplier[S03]', 'PurchaseOrder', '-30%', '-30%', '0.70', '14d', 'T+14'],
        ['2', 'PurchaseOrder', 'InventoryReceipt', '-30%', '-28.5%', '0.95', '7d', 'T+21'],
        ['3', 'InventoryReceipt', 'ProductionEvent', '-28.5%', '-22.8%', '0.80', '14d', 'T+35'],
        ['4', 'ProductionEvent', 'CustomerOrder', '-22.8%', '-19.4%', '0.85', '7d', 'T+42'],
        ['5', 'CustomerOrder', 'Invoice', '-19.4%', '-$187,500', '1.00', '0d', 'T+42'],
        ['6', 'Invoice', 'AccountsReceivable', '-$187,500', '-$187,500', '1.00', '30d', 'T+72'],
        ['7', 'AR', 'CustomerPayment', '-$187,500', '-$178,125', '0.95', '0d', 'T+72'],
        ['8', 'CustomerPayment', 'CashAccount', '-$178,125', '-$178,125', '1.00', '0d', 'T+72'],
    ]
    pB.insert_text((LX, y_b), 'Table 2: Path A — Revenue Loss Chain (81% of total impact)',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_b += 12
    cw_p = [TW*0.05, TW*0.16, TW*0.16, TW*0.12, TW*0.13, TW*0.10, TW*0.08, TW*0.10]
    # Trim to fit 8 columns
    y_b = draw_table(pB, LX, y_b, cw_p, path_a_rows, size=7.0,
                     header_fill=(0.15, 0.25, 0.50))
    y_b += 8

    path_b_rows = [
        ['Step', 'Source Event', 'Target Event', 'Source Delta', 'Target Delta', 'Dep.Str.', 'Delay', 'Scheduled'],
        ['1', 'Supplier[S03]', 'ExpenseEvent[EMRG]', '-30%', '+$45,000', '1.00', '7d', 'T+7'],
        ['2', 'ExpenseEvent', 'AccountsPayable', '$45,000', '$45,000', '1.00', '30d', 'T+37'],
        ['3', 'AccountsPayable', 'SupplierPayment', '$45,000', '$45,000', '1.00', '0d', 'T+37'],
        ['4', 'SupplierPayment', 'CashAccount', '$45,000', '-$45,000', '1.00', '0d', 'T+37'],
    ]
    pB.insert_text((LX, y_b), 'Table 3: Path B — Emergency Procurement Chain (19% of total impact)',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_b += 12
    y_b = draw_table(pB, LX, y_b, cw_p, path_b_rows, size=7.0,
                     header_fill=(0.18, 0.12, 0.45))
    y_b += 8

    # Convergence summary
    conv_rows = [
        ['Path', 'Monetary Impact (USD)', 'Scheduled Date', 'Share of Total'],
        ['Path A — Revenue Loss Chain', '-$178,125', 'T+72 days', '81%'],
        ['Path B — Emergency Procurement', '-$45,000', 'T+37 days', '19%'],
        ['COMBINED at CashAccount', '-$223,125', 'T+37d to T+72d', '100%'],
    ]
    pB.insert_text((LX, y_b), 'Table 4: Multi-Path Convergence at CashAccount',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_b += 12
    y_b = draw_table(pB, LX, y_b, [TW*0.36, TW*0.22, TW*0.22, TW*0.20], conv_rows,
                     size=7.5, header_fill=(0.15, 0.25, 0.50))
    y_b += 10

    # Propagation timeline image
    pB.insert_text((LX, y_b), 'Figure 3: Propagation Timeline — DIST-001 (T+0 to T+103 days)',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_b += 12
    gpath3 = f'{GRAPH_DIR}/03_propagation_timeline.png'
    y_b = insert_image_scaled(pB, gpath3, LX, y_b, max_w=TW, max_h=190)
    y_b += 4
    pB.insert_text((LX, y_b),
        'Stars mark cash impact events. Path A (blue) peaks at T+72d; Path B (orange) peaks at T+37d.',
        fontname=FONT_REG, fontsize=8, color=(0.35,0.35,0.35))

    # ── Appended Page C: Cash Trajectory + LIW Dashboard ───────────────────
    pC = new_content_page(out, 'APPENDIX C — Cash-Flow Trajectory & Liquidity Impact Window (Figure 4, 5)')
    y_c = 155.0

    # LIW metrics table
    liw_rows = [
        ['Liquidity Impact Window Metric', 'Value for DIST-001'],
        ['Impact Start Date', 'T+21 days (2026-07-22)'],
        ['Impact Peak Date', 'T+72 days (2026-09-11)'],
        ['Peak Cash Deficit (vs baseline)', '-$218,400'],
        ['Impact Duration', '47 days'],
        ['Recovery Start Date', 'T+85 days (2026-09-24)'],
        ['Recovery Date (full)', 'T+103 days (2026-10-12)'],
        ['Cumulative Cash Delta', '-$341,750 over 47-day window'],
        ['Path A Contribution', '-$178,125 (81%) — Revenue Loss Chain'],
        ['Path B Contribution', '-$45,000 (19%) — Emergency Procurement Chain'],
        ['Propagation Audit Log Entries', '12 fully logged steps (source → target → cash)'],
    ]
    pC.insert_text((LX, y_c), 'Table 5: Liquidity Impact Window — DIST-001 Results',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_c += 12
    y_c = draw_table(pC, LX, y_c, [TW*0.46, TW*0.54], liw_rows,
                     size=8.0, header_fill=(0.15, 0.25, 0.50))
    y_c += 10

    # Cash trajectory
    pC.insert_text((LX, y_c), 'Figure 4: Baseline vs. Disturbance Cash Trajectory (120 days)',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_c += 12
    gpath1 = f'{GRAPH_DIR}/01_baseline_vs_disturbance_cash_trajectory.png'
    y_c = insert_image_scaled(pC, gpath1, LX, y_c, max_w=TW, max_h=215)
    y_c += 4
    pC.insert_text((LX, y_c),
        'Blue = baseline cash; Orange dashed = disturbance scenario; Red shading = Liquidity Impact Window.',
        fontname=FONT_REG, fontsize=8, color=(0.35,0.35,0.35))
    y_c += 15

    # LIW dashboard
    pC.insert_text((LX, y_c), 'Figure 5: Liquidity Impact Window Executive Dashboard',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_c += 12
    gpath5 = f'{GRAPH_DIR}/05_liquidity_impact_window_dashboard.png'
    y_c = insert_image_scaled(pC, gpath5, LX, y_c, max_w=TW, max_h=210)
    y_c += 4
    pC.insert_text((LX, y_c),
        'Dashboard panels: impact_start, peak_date, peak_deficit, duration, recovery_start, recovery_date, cumulative_delta.',
        fontname=FONT_REG, fontsize=8, color=(0.35,0.35,0.35))

    # ── Appended Page D: Multi-Path Attribution + Novelty Radar ─────────────
    pD = new_content_page(out, 'APPENDIX D — Multi-Path Attribution & Novelty Differentiation (Figure 6, 7)')
    y_d = 155.0

    desc_d = [
        '__BOLD__Multi-Path Convergence (Novel — No prior art found):',
        'When multiple independent causal paths arrive at the same future cash event (CashAccount),',
        'TCDS aggregates their monetary contributions AND preserves per-path attribution records.',
        'This enables management to see exactly how much each business chain contributed to the deficit.',
    ]
    y_d = insert_text_lines(pD, LX, y_d, TW, FONT_REG, FS, desc_d, line_height=LH)
    y_d += 6

    # Attribution chart
    pD.insert_text((LX, y_d), 'Figure 6: Multi-Path Convergence & Attribution at CashAccount',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_d += 12
    gpath4 = f'{GRAPH_DIR}/04_multipath_convergence_attribution.png'
    y_d = insert_image_scaled(pD, gpath4, LX, y_d, max_w=TW*0.65, max_h=200)
    y_d += 4
    pD.insert_text((LX, y_d),
        'Path A (Revenue Loss): -$178,125 (81%). Path B (Emergency Cost): -$45,000 (19%). Combined: -$223,125.',
        fontname=FONT_REG, fontsize=8, color=(0.35,0.35,0.35))
    y_d += 18

    # Novelty radar
    pD.insert_text((LX, y_d), 'Figure 7: Novelty Differentiation Radar — TCDS vs. Closest Prior Art',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_d += 12
    gpath6 = f'{GRAPH_DIR}/06_novelty_radar_chart.png'
    y_d = insert_image_scaled(pD, gpath6, LX, y_d, max_w=TW*0.65, max_h=225)
    y_d += 4
    pD.insert_text((LX, y_d),
        'TCDS (green) scores 10/10 on all 5 novel axes. Prior art scores 1-4/10 on each axis.',
        fontname=FONT_REG, fontsize=8, color=(0.35,0.35,0.35))
    y_d += 18

    # Claims protection table
    claims_rows = [
        ['Claim', 'Type', 'Novel Element Protected'],
        ['A', 'Method', 'Monetary disturbance as first-class typed state (not risk score)'],
        ['B', 'System', 'Event-level temporal graph with dual-transform edges (amount + time)'],
        ['C', 'Method', 'Multi-path monetary convergence with per-path attribution at cash events'],
        ['D', 'Method', 'Liquidity Impact Window: {start, peak, deficit, duration, recovery}'],
        ['E', 'System', 'End-to-end disturbance-to-LIW pipeline with immutable baseline & audit log'],
        ['F', 'Method', 'State-dependent, threshold-based nonlinear propagation rules on graph edges'],
        ['G', 'System', 'Deterministic reproducibility — identical inputs always produce identical LIW'],
        ['H', 'UI', 'Attribution dashboard: propagation timeline + path contribution + LIW markers'],
    ]
    pD.insert_text((LX, y_d), 'Table 6: Claims for IP Protection — Summary',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_d += 12
    draw_table(pD, LX, y_d, [TW*0.07, TW*0.10, TW*0.83], claims_rows,
               size=7.5, header_fill=(0.15, 0.25, 0.50))

    # ── Appended Page E: Supplier Profile + Dependency Heatmap ──────────────
    pE = new_content_page(out, 'APPENDIX E — Dataset Validation: Supplier Profile & Dependency Matrix (Figure 8, 9)')
    y_e = 155.0

    dataset_rows = [
        ['Dataset File', 'Contents', 'Rows'],
        ['suppliers.csv', '12 synthetic suppliers: capacity, reliability (0.75-0.98), payment terms, lead time, cost', '12'],
        ['purchase_orders.csv', '60 purchase orders linked to suppliers with quantity, value, status, dates', '60'],
        ['inventory_receipts.csv', '36 receipts (received/partial) with AP due dates', '36'],
        ['customer_orders.csv', '80 orders across 25 customers; price $80-$250; payment terms 30-60d', '80'],
        ['baseline_vs_disturbance_cashflow.csv', '120-day baseline + DIST-001 cash flows: inflows, outflows, net, balance, delta', '120'],
        ['propagation_audit_log.csv', '12-step full audit trail: source event, target event, deltas, dep_strength, schedule, rule', '12'],
        ['temporal_graph_edges.csv', '14 graph edges with all 10 typed attributes', '14'],
        ['liquidity_impact_window.json', 'LIW output object for DIST-001 with all 7 metrics and path attributions', '1'],
    ]
    pE.insert_text((LX, y_e), 'Table 7: Synthetic Validation Datasets',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_e += 12
    y_e = draw_table(pE, LX, y_e, [TW*0.30, TW*0.58, TW*0.12], dataset_rows,
                     size=7.0, header_fill=(0.15, 0.25, 0.50))
    y_e += 10

    pE.insert_text((LX, y_e), 'Figure 8: Supplier Risk Profile — 12 synthetic suppliers',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_e += 12
    gpath7 = f'{GRAPH_DIR}/07_supplier_risk_profile.png'
    y_e = insert_image_scaled(pE, gpath7, LX, y_e, max_w=TW, max_h=185)
    y_e += 4
    pE.insert_text((LX, y_e),
        'Left: Reliability scores (S03 highlighted as DIST-001 source). Right: Capacity vs. cost scatter.',
        fontname=FONT_REG, fontsize=8, color=(0.35,0.35,0.35))
    y_e += 15

    pE.insert_text((LX, y_e), 'Figure 9: Dependency Strength Heatmap — 13x13 node-pair matrix',
                   fontname=FONT_BOLD, fontsize=8.5, color=BLACK)
    y_e += 12
    gpath8 = f'{GRAPH_DIR}/08_dependency_strength_heatmap.png'
    y_e = insert_image_scaled(pE, gpath8, LX, y_e, max_w=TW, max_h=230)
    y_e += 4
    pE.insert_text((LX, y_e),
        'Each cell shows the dependency_strength value on the edge from source (row) to target (column).',
        fontname=FONT_REG, fontsize=8, color=(0.35,0.35,0.35))

    # ── PAGE LAST: Template page 2 with TRL 3 ticked ─────────────────────────
    out.insert_pdf(src, from_page=1, to_page=1)
    p_last = out[-1]

    # Tick TRL 3 — coordinates from analysis: TRL3 header at x≈173.7, y≈187.7
    # Draw a checkmark box overlay at TRL 3 position
    # TRL cells are evenly spaced from x≈54 to x≈547, 9 columns
    # TRL 3 is col index 2 (0-based) on the TRL row
    # From analysis: TRL3 at x≈173.7
    # Draw tick mark in TRL 3 cell
    tx, ty = 176.0, 356.0   # approximate y of the tick-mark area below TRL descriptions
    # Draw filled green box
    p_last.draw_rect(fitz.Rect(161, 348, 222, 370),
                     color=(0.0, 0.5, 0.2), fill=(0.85, 0.95, 0.85), width=1.5)
    p_last.insert_text((163, 362), '\u2713 CURRENT',
                        fontname=FONT_BOLD, fontsize=7.5, color=(0.0, 0.4, 0.15))

    # Add note above END OF DOCUMENT
    p_last.insert_text((54, 410),
        'TRL 3: Experimental proof of concept validated. Synthetic dataset simulation (12 suppliers,',
        fontname=FONT_REG, fontsize=8.5, color=BLACK)
    p_last.insert_text((54, 422),
        '60 POs, 80 customer orders, 120-day horizon) completed. All 6 validation tests passed.',
        fontname=FONT_REG, fontsize=8.5, color=BLACK)

    # Save
    out.save(OUT, garbage=4, deflate=True)
    print(f'\n✅ PDF saved: {OUT}')
    import os as _os
    sz = _os.path.getsize(OUT)
    print(f'   Pages: {len(out)}')
    print(f'   Size:  {sz/1024:.1f} KB')

if __name__ == '__main__':
    build()
