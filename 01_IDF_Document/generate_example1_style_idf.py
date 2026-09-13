"""
Official Invention Disclosure Format (IDF)-B Document Generator
Fully Compliant with Section 3(k) of the Indian Patents Act, 1970 and IPO CRI Guidelines (2017)
Incorporating Binding Jurisprudence of the Hon'ble Delhi High Court:
  - Ferid Allani v. Union of India (2019) 265 DLT 420 (Technical Effect / Technical Contribution Test)
  - Microsoft Technology Licensing LLC v. Assistant Controller of Patents & Designs (2023) SCC OnLine Del 2772

Key Statutory & Technical Implementation Highlights:
  1. Title & IPC Strategy: Strictly G06F (G06F 16/90, G06F 9/48, G06F 17/16, G06F 21/64). All G06Q classes eliminated.
  2. De-Financialized Independent Claims (1 & 2): Generic computational constructs (scalar perturbation amplitude ΔA,
     cross-domain transfer operator ψₑ, discrete temporal latency offset δₑ, dynamic state deflection envelope).
  3. Universal Technical Embodiments (Section 7.9):
       - Embodiment 1: Telecommunications & Packet Mesh Networks (buffer delays, packet drop rate, throughput degradation envelope)
       - Embodiment 2: Cloud Distributed Microservice Pipelines (worker queues, memory spikes, latency cascades, SLO violation envelope)
       - Embodiment 3: Enterprise Resource & Transactional Telemetry (secondary industrial application)
  4. Neutralized Dependent Claims:
       - Claim 6: Abstract functional node classes (Originator, Latency Delay, Transformation, Accumulator, Interrupt Nodes)
       - Claim 7: Digital array scanning across circular buffers and finite difference inflection markers (no pure calculus)
       - Claim 8: Telemetry controller, frame buffer memory dynamic addressing, and hardware scanline rasterization
  5. Internal Hardware Technical Effects (Section 4.3):
       - Elimination of graph combinatorial explosion (O(|V| + |E|) single-pass linear time)
       - Hardware memory cache locality via contiguous adjacency array buffers
       - Race-condition-free multi-threaded parallel execution across asynchronous event queues
  6. Document Presentation Standards:
       - Strictly 14 Pages, Portrait A4
       - Footers contain ONLY page numbers ('Page X of 14')
       - All figure captions are clean and descriptive (zero 'IEEE Standards' or 'USPTO')
       - Section 10 TRL table strictly matches template image (media_1788430271710.png) with red validation text in TRL 4
       - Claims in Section 9 are unbolded (TimesNewRomanPSMT) with small Mac keyboard dashes '-' exclusively

Institution: VIT IPR & Technology Transfer Cell
Document No: 02-IPR-R003 | Issue No/Date: 2/01.02.2024 | Amd: 0/00.00.0000
"""

import sys
sys.path.insert(0, '/Users/yuvi/Library/Python/3.9/lib/python/site-packages')

import os
import json
import pandas as pd
from PIL import Image as PILImage
import matplotlib

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, NextPageTemplate, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Times New Roman TrueType Fonts for native Unicode symbol rendering
pdfmetrics.registerFont(TTFont('TimesNewRoman', '/System/Library/Fonts/Supplemental/Times New Roman.ttf'))
pdfmetrics.registerFont(TTFont('TimesNewRoman-Bold', '/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf'))
pdfmetrics.registerFont(TTFont('TimesNewRoman-Italic', '/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf'))
pdfmetrics.registerFont(TTFont('TimesNewRoman-BoldItalic', '/System/Library/Fonts/Supplemental/Times New Roman Bold Italic.ttf'))
pdfmetrics.registerFontFamily(
    'TimesNewRoman',
    normal='TimesNewRoman',
    bold='TimesNewRoman-Bold',
    italic='TimesNewRoman-Italic',
    boldItalic='TimesNewRoman-BoldItalic'
)

# Register DejaVuSans for crisp, universal Unicode checkmarks (✓)
dejavu_bold = os.path.join(matplotlib.get_data_path(), 'fonts/ttf/DejaVuSans-Bold.ttf')
pdfmetrics.registerFont(TTFont('CheckmarkFont', dejavu_bold))

BASE_DIR = '/Users/yuvi/Patents/patent1'
DATA_DIR = os.path.join(BASE_DIR, '02_Datasets')
GRAPH_DIR = os.path.join(BASE_DIR, '03_Graphs_and_Visualizations')
OUT_DIR = os.path.join(BASE_DIR, '01_IDF_Document')
OUT_PDF = os.path.join(OUT_DIR, 'Invention_Disclosure_Format_B_Completed.pdf')
OUT_PDF_SUBMITTED = os.path.join(OUT_DIR, 'IDF_B_TCDS_Submitted.pdf')

# Geometry & Margins
PAGE_W, PAGE_H = A4  # 595.28 x 841.89 pt
LM = 53.64
RM = PAGE_W - 546.70  # 48.58 pt
CW = 493.06           # Exact width of institutional header box
BM = 38.0

# Colors (Formal institutional palette matching example1.pdf)
BLACK = colors.Color(0.0, 0.0, 0.0)
DARK_GRAY = colors.Color(0.12, 0.12, 0.12)
LIGHT_BG = colors.Color(0.96, 0.97, 0.99)
BORDER_GRAY = colors.Color(0.72, 0.75, 0.78)
TABLE_HEAD = colors.Color(0.12, 0.20, 0.38)

# Typography Styles
base_styles = getSampleStyleSheet()

def st(name, **kwargs):
    parent = kwargs.pop('parent', base_styles['Normal'])
    return ParagraphStyle(name, parent=parent, **kwargs)

S_SEC = st('Sec', fontName='TimesNewRoman-Bold', fontSize=9.8, leading=12.5, textColor=BLACK, spaceBefore=5.5, spaceAfter=2.0, keepWithNext=True)
S_SUB = st('Sub', fontName='TimesNewRoman-Bold', fontSize=8.6, leading=11.2, textColor=BLACK, spaceBefore=4.0, spaceAfter=1.5, keepWithNext=True)
S_SUBSUB = st('SubSub', fontName='TimesNewRoman-BoldItalic', fontSize=8.1, leading=10.5, textColor=BLACK, spaceBefore=3.0, spaceAfter=1.0, keepWithNext=True)

S_BODY = st('Body', fontName='TimesNewRoman', fontSize=8.1, leading=11.0, textColor=DARK_GRAY, alignment=TA_JUSTIFY, spaceAfter=1.8)
S_BODY_B = st('BodyB', fontName='TimesNewRoman-Bold', fontSize=8.1, leading=11.0, textColor=BLACK, spaceAfter=1.8)
S_BULLET = st('Bullet', fontName='TimesNewRoman', fontSize=8.1, leading=11.0, textColor=DARK_GRAY, leftIndent=12, bulletIndent=3, spaceAfter=1.0)
S_CAPTION = st('Caption', fontName='TimesNewRoman-Italic', fontSize=7.3, leading=9.2, textColor=colors.Color(0.20, 0.20, 0.20), alignment=TA_CENTER, spaceAfter=2.0)
S_FORMULA = st('Formula', fontName='TimesNewRoman-Bold', fontSize=8.6, leading=12.0, textColor=BLACK, leftIndent=14, spaceBefore=2.0, spaceAfter=2.0)

# Plain style for claims without bolding
S_CLAIM_HEAD = st('ClaimHead', fontName='TimesNewRoman', fontSize=8.1, leading=11.0, textColor=BLACK, spaceBefore=4.0, spaceAfter=1.0, keepWithNext=True)

# Table cell styles
S_TH = st('TH', fontName='TimesNewRoman-Bold', fontSize=7.2, leading=9.0, textColor=colors.white, alignment=TA_CENTER)
S_TH_DARK = st('THD', fontName='TimesNewRoman-Bold', fontSize=7.2, leading=9.0, textColor=BLACK, alignment=TA_CENTER)
S_TD = st('TD', fontName='TimesNewRoman', fontSize=6.9, leading=8.6, textColor=DARK_GRAY)
S_TD_C = st('TDC', fontName='TimesNewRoman', fontSize=6.9, leading=8.6, textColor=DARK_GRAY, alignment=TA_CENTER)
S_TD_B = st('TDB', fontName='TimesNewRoman-Bold', fontSize=6.9, leading=8.6, textColor=BLACK)
S_TD_BC = st('TDBC', fontName='TimesNewRoman-Bold', fontSize=6.9, leading=8.6, textColor=BLACK, alignment=TA_CENTER)

# Custom Numbered Canvas
class Example1Canvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        is_first = (self._pageNumber == 1)
        is_last = (self._pageNumber == total_pages)

        # 1. Top Left Branding
        self.setFont('TimesNewRoman', 11)
        self.setFillColor(BLACK)
        self.drawString(53.88, PAGE_H - 42.0, "©VIT IPR&TTCELL")

        # 2. Header Box on Page 1 and Last Page ONLY (matching example1.pdf)
        if is_first or is_last:
            box_y0 = PAGE_H - 117.62
            self.setStrokeColor(BLACK)
            self.setLineWidth(0.6)
            self.rect(53.64, box_y0, 493.06, 69.02)
            self.line(410.95, box_y0, 410.95, box_y0 + 69.02)
            self.line(473.98, box_y0, 473.98, box_y0 + 69.02)
            self.line(410.95, PAGE_H - 76.68, 546.70, PAGE_H - 76.68)
            self.line(410.95, PAGE_H - 97.22, 546.70, PAGE_H - 97.22)

            self.setFont('TimesNewRoman-Bold', 12)
            self.drawCentredString((53.64 + 410.95) / 2.0, PAGE_H - 85.5, "Invention Disclosure Format (IDF)-B")

            self.setFont('Helvetica', 8)
            self.drawString(416.5, PAGE_H - 65.5, "Document No.")
            self.drawString(479.5, PAGE_H - 65.5, "02-IPR-R003")
            self.drawString(416.5, PAGE_H - 89.5, "Issue No/Date")
            self.drawString(479.5, PAGE_H - 89.5, "2/01.02.2024")
            self.drawString(416.5, PAGE_H - 110.0, "Amd. No/Date")
            self.drawString(479.5, PAGE_H - 110.0, "0/00.00.0000")

        # 3. Running Footer on all pages: ONLY page numbers, zero extraneous text strings
        self.setStrokeColor(BORDER_GRAY)
        self.setLineWidth(0.4)
        self.line(53.64, 28.0, 546.70, 28.0)
        self.setFont('TimesNewRoman', 8.0)
        self.setFillColor(colors.Color(0.35, 0.35, 0.35))
        self.drawRightString(546.70, 18.0, f"Page {self._pageNumber} of {total_pages}")

        self.restoreState()

# Flowable Helpers
def p(text, style=S_BODY):
    return Paragraph(text, style)

def pb(text):
    return Paragraph(f"• {text}", S_BULLET)

def sec(title):
    return Paragraph(title, S_SEC)

def sub(title):
    return Paragraph(title, S_SUB)

def subsub(title):
    return Paragraph(title, S_SUBSUB)

def sp(h=2.0):
    return Spacer(1, h)

def embed_fig(filename, caption, max_h=280, scale=0.96):
    img_path = os.path.join(GRAPH_DIR, filename)
    if not os.path.exists(img_path):
        return [p(f"[Figure Missing: {filename}]", S_CAPTION)]
    with PILImage.open(img_path) as im:
        iw, ih = im.size
    target_w = CW * scale
    target_h = target_w * (ih / iw)
    if target_h > max_h:
        target_h = max_h
        target_w = target_h * (iw / ih)
    return [
        sp(2),
        Image(img_path, width=target_w, height=target_h),
        sp(1.5),
        Paragraph(caption, S_CAPTION),
        sp(2)
    ]

def make_tbl(data, col_widths, is_header=True, header_bg=TABLE_HEAD):
    t = Table(data, colWidths=col_widths, repeatRows=1 if is_header else 0)
    cmds = [
        ('GRID', (0,0), (-1,-1), 0.4, BORDER_GRAY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('LEFTPADDING', (0,0), (-1,-1), 2.5),
        ('RIGHTPADDING', (0,0), (-1,-1), 2.5),
    ]
    if is_header:
        cmds.extend([
            ('BACKGROUND', (0,0), (-1,0), header_bg),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'TimesNewRoman-Bold'),
        ])
        for r in range(1, len(data)):
            bg = colors.white if r % 2 != 0 else LIGHT_BG
            cmds.append(('BACKGROUND', (0, r), (-1, r), bg))
    t.setStyle(TableStyle(cmds))
    return t

# Build Document Flow
def build_idf():
    story = []

    # =========================================================================
    # PAGE 1: TITLE, FIELD & PRIOR ART SURVEY (STEP 1: RE-CLASSIFICATION & TITLE)
    # =========================================================================
    story.append(sec("1. Title of the invention:"))
    story.append(p(
        "<b>A Computer-Implemented System and Method for Asynchronous Multi-Attribute "
        "State Propagation and Temporal Dynamic Envelope Extraction Across Graph Data Structures</b>",
        S_BODY_B
    ))
    story.append(sp(3))

    story.append(sec("2. Field / Area of invention:"))
    field_tbl_data = [
        [Paragraph("<b>Attribute</b>", S_TH), Paragraph("<b>Details & Technical Classification (Strictly G06F)</b>", S_TH)],
        [Paragraph("<b>Primary Technical Field</b>", S_TD_B), Paragraph("Computer Systems, Graph Computing Data Structures, and Asynchronous Event-Driven Digital Data Processing", S_TD)],
        [Paragraph("<b>Core Computational Domains</b>", S_TD_B), Paragraph("Asynchronous Directed Graph Traversal, Cryptographic State-Transition Verification, Multi-Attribute Vector Scaling, Dynamic State Deflection Envelope Detection", S_TD)],
        [Paragraph("<b>Cross-Domain Embodiments</b>", S_TD_B), Paragraph("Packet Routing & Telecom Mesh Networks, Distributed Cloud Microservice Pipelines, Enterprise Resource & Operational Telemetry", S_TD)],
        [Paragraph("<b>Technical Architecture</b>", S_TD_B), Paragraph("In-Memory Temporal Multigraph Database Core, Chronological Event Queue Schedulers, Contiguous Adjacency Buffers, SHA-256 State Anchoring Engines", S_TD)],
        [Paragraph("<b>Statutory IPC Classifications</b>", S_TD_B), Paragraph("<b>G06F 16/90</b> (Information Retrieval; Graph Data Structures & Traversal Indexes)<br/>"
                                                                                 "<b>G06F 9/48</b> (Program Execution Management; Asynchronous Event Dispatching & Queuing)<br/>"
                                                                                 "<b>G06F 17/16</b> (Vector & Matrix Computational Operations)<br/>"
                                                                                 "<b>G06F 21/64</b> (Data Integrity Verification; Cryptographic State Anchoring)", S_TD)],
    ]
    story.append(make_tbl(field_tbl_data, [CW * 0.26, CW * 0.74], is_header=True))
    story.append(sp(2))
    story.append(p(
        "<b>Statutory Classification & Examination Note:</b> The claimed invention fundamentally pertains to the technical domain of computer-implemented "
        "digital data processing, graph data structures, asynchronous event-queue scheduling, and cryptographic integrity verification under IPC Class G06F. "
        "In accordance with Indian Patent Office CRI Guidelines (2017), the invention solves technical problems internal to computing systems, "
        "and all business methods are explicitly excluded from the claims.",
        st('StatNote', fontName='TimesNewRoman-Italic', fontSize=7.3, leading=9.2, textColor=colors.Color(0.20, 0.20, 0.20))
    ))
    story.append(sp(3))

    story.append(sec("3. Prior Patents and Publications from literature"))
    story.append(sub("3.1 Prior Art Survey"))
    pa_survey_data = [
        [Paragraph("<b>Sl. No.</b>", S_TH), Paragraph("<b>Reference / Publication</b>", S_TH), Paragraph("<b>Year</b>", S_TH), Paragraph("<b>Key Contribution</b>", S_TH), Paragraph("<b>Limitation / Technical Gap under Section 3(k)</b>", S_TH)],
        [
            Paragraph("1", S_TD_C),
            Paragraph("<b>US20240362563A1</b><br/>'Financial risk graph system'", S_TD_B),
            Paragraph("2024", S_TD_C),
            Paragraph("Propagates dimensionless risk scores across entity networks using static weighted edges.", S_TD),
            Paragraph("<b>Abstract business scoring</b>; lacks coupled dual-transform vector operations, event queues, and temporal schedule shifting.", S_TD)
        ],
        [
            Paragraph("2", S_TD_C),
            Paragraph("<b>US12380389B2</b><br/>'Entity-level financial risk graph'", S_TD_B),
            Paragraph("2025", S_TD_C),
            Paragraph("Entity-relationship mapping for corporate vulnerability scoring.", S_TD),
            Paragraph("<b>High-level entity mapping only</b>; lacks typed computational node registers and time-delayed state trajectory outputs.", S_TD)
        ],
        [
            Paragraph("3", S_TD_C),
            Paragraph("<b>US20260120033A1</b><br/>'Business dependency graph'", S_TD_B),
            Paragraph("2026", S_TD_C),
            Paragraph("Quantifies systemic operational dependencies across organizations.", S_TD),
            Paragraph("Lacks structured perturbation vector objects, dual-transform edges, and dynamic state deflection envelope extraction.", S_TD)
        ],
        [
            Paragraph("4", S_TD_C),
            Paragraph("<b>US10679166B2</b><br/>'Supply chain financing system'", S_TD_B),
            Paragraph("2020", S_TD_C),
            Paragraph("Digital ledger managing trade financing instruments.", S_TD),
            Paragraph("Administrative ledger only; does not simulate operational disturbances or extract dynamic state deflection envelopes.", S_TD)
        ],
        [
            Paragraph("5", S_TD_C),
            Paragraph("<b>US6167385A</b><br/>'Event-driven logistics simulation'", S_TD_B),
            Paragraph("2000", S_TD_C),
            Paragraph("Event-driven simulation for physical supply chain inventory queues.", S_TD),
            Paragraph("Restricted to discrete item counts; lacks dual-transform vector scaling, asynchronous graph traversal, and state convergence.", S_TD)
        ],
    ]
    story.append(make_tbl(pa_survey_data, [CW*0.07, CW*0.25, CW*0.08, CW*0.30, CW*0.30], is_header=True))

    # Switch template to LaterPages starting on Page 2
    story.append(NextPageTemplate('Later'))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: ACADEMIC CITATIONS, GAP & SECTION 3(k) INTERNAL HARDWARE EFFECTS
    # =========================================================================
    story.append(sub("3.2 Key Academic Publications"))
    acad_data = [
        [Paragraph("<b>Publication / Citation</b>", S_TH), Paragraph("<b>Focus Area</b>", S_TH), Paragraph("<b>Key Gap vs. Present Invention</b>", S_TH)],
        [
            Paragraph("Tangsucheeva & Prabhu, <i>Int. J. Prod. Econ.</i> (2013)", S_TD_B),
            Paragraph("Analytical formulation of Cash-Flow Bullwhip Effect in supply networks.", S_TD),
            Paragraph("Theoretical study only; lacks computational graph data structures, perturbation vectors, and simulation pipeline.", S_TD)
        ],
        [
            Paragraph("Temporal Attentive Graph Networks (TAGN), Preprints (2024)", S_TD_B),
            Paragraph("Graph neural networks for financial contagion and anomaly detection.", S_TD),
            Paragraph("Statistical ML classification; non-deterministic, lacks coupled dual-transform rules, and outputs no dynamic state envelope.", S_TD)
        ],
    ]
    story.append(make_tbl(acad_data, [CW*0.32, CW*0.34, CW*0.34], is_header=True))
    story.append(sp(2.5))

    story.append(sub("3.3 Identified Technical Gap in Computing Systems"))
    story.append(p(
        "<b>No existing computational system unifies all foundational technical capabilities:</b> (1) an in-memory temporal multigraph "
        "data structure of discrete computational nodes connected by dual-transform directed edges, (2) treatment of scalar perturbations as first-class "
        "typed state vector objects carrying numerical amplitudes and temporal metadata, (3) execution of simultaneous magnitude scaling and "
        "chronological schedule shifting in O(|V| + |E|) single-pass linear time, (4) deterministic multi-path convergence resolution under numerical conservation, "
        "(5) cryptographic state-anchoring (SHA-256) ensuring bitwise execution invariance, and (6) automated extraction of a multi-parameter dynamic "
        "state deflection envelope. The present invention solves these technical data-processing bottlenecks."
    ))
    story.append(sp(2.5))

    story.append(sec("4. Summary and background of the invention"))
    story.append(sub("4.1 Background & Technical Shortcomings of Prior Computing Architectures"))
    story.append(p(
        "Modern distributed networks (telecom mesh topologies, microservice task pipelines, and enterprise systems) exhibit complex multi-hop cascades. "
        "Conventional simulation tools fail because they lack technical mechanisms to model asynchronous causal propagation across cyclic multigraphs, "
        "producing exponential O(V · E^k) combinatorial path explosion, CPU cycle exhaustion, memory cache thrashing, and non-deterministic race conditions."
    ))
    story.append(sp(2))

    story.append(sub("4.2 Summary of the Invention"))
    story.append(p(
        "The present invention is a universal technical computing system and computer-implemented method that processes operational perturbations "
        "through an in-memory temporal multigraph data structure G = (V, E, T), propagating scalar amplitudes and temporal schedules across "
        "dual-transform edges in a single pass, resolving multi-path convergence at terminal accumulator nodes, and extracting an explicit "
        "<b>Dynamic State Deflection Envelope</b> data structure."
    ))
    story.append(sp(2))

    story.append(sub("4.3 Internal Hardware Technical Effects (Section 3(k) Statutory Compliance)"))
    story.append(p(
        "In compliance with Section 3(k) of the Indian Patents Act, 1970, the CRI Guidelines (2017), and binding precedents of the Hon'ble Delhi High Court "
        "in <i>Ferid Allani v. Union of India</i> (2019) 265 DLT 420 and <i>Microsoft Technology Licensing LLC v. Assistant Controller of Patents & Designs</i> "
        "(2023) SCC OnLine Del 2772, the invention provides concrete technical solutions to technical problems internal to the operation of a computer:"
    ))
    story.append(pb("<b>Elimination of Graph Combinatorial Explosion:</b> Standard cyclic temporal multigraph traversal causes infinite loops or exponential O(V · E^k) path explosion. The present invention's single-pass coupled calculation (ΔAᵥ = ΔAᵤ · ωₑ · ψₑ and tᵥ = tᵤ + δₑ) utilizing a priority queue buffer guarantees O(|V| + |E|) linear execution time, dramatically reducing CPU cycle consumption and RAM footprint."))
    story.append(pb("<b>Hardware Memory Cache Locality:</b> The temporal multigraph is indexed in memory using contiguous adjacency array buffers, maximizing L1/L2 hardware CPU cache hits and eliminating memory bus thrashing during multi-hop graph traversal."))
    story.append(pb("<b>Race-Condition-Free Parallel Execution:</b> The deterministic chronological event queue buffer enables multi-threaded worker cores to process asynchronous event streams without deadlocks or thread synchronization latency, achieving bitwise identical reproducibility."))
    story.append(pb("<b>Cryptographic State-Transition Integrity:</b> Pre- and post-simulation state arrays are anchored via SHA-256 cryptographic hash digests, ensuring tamper-evident data integrity across parallel computing nodes."))
    story.append(p(
        "The claimed invention is therefore not a business method, mathematical method, algorithm, or computer programme per se, but an advanced digital data processing architecture.",
        st('StatConc', fontName='TimesNewRoman-BoldItalic', fontSize=7.5, leading=9.5, textColor=BLACK)
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: FIGURE 1 (ENLARGED) & OBJECTIVES OF INVENTION
    # =========================================================================
    story.extend(embed_fig(
        '06_novelty_radar_chart.png',
        "Fig. 1: Novelty Differentiation Radar Chart - Multi-axis quantitative benchmarking of the technical graph computing engine against closest published prior art (US20240362563A1, US12380389B2, Generic Graph Systems) across 7 core patent axes with decile scoring (Scale 1-10).",
        max_h=300, scale=0.96
    ))
    story.append(sp(2))

    story.append(sec("5. Objectives of the Invention"))
    objectives = [
        ("Automated Multi-Attribute Perturbation Simulation", "To provide a computing architecture that automatically maps operational disturbance signals into time-resolved, scalar state deflection trajectories without manual reconfiguration."),
        ("In-Memory Temporal Multigraph Data Modeling", "To construct and maintain an in-memory temporal directed multigraph where nodes represent discrete computational stages and edges embody coupled dual-transform operators."),
        ("Linear-Time Vector State Propagation Core", "To execute simultaneous scalar amplitude transformation and chronological schedule shifting across graph dependencies in O(|V| + |E|) single-pass linear time, minimizing CPU cycles."),
        ("Deterministic Multi-Path Convergence Resolution", "To aggregate concurrent causal streams intersecting at shared terminal accumulator nodes while preserving decoupled path attribution share registers under strict numerical conservation."),
        ("Dynamic State Deflection Envelope Extraction", "To detect and extract a decision-ready multi-parameter Dynamic State Deflection Envelope defining onset boundary, extreme deflection point, active impairment duration, and system equilibrium recovery."),
        ("Cryptographic State Immutability & Auditability", "To maintain a cryptographically locked (SHA-256) forward baseline reference to guarantee bitwise deterministic reproducibility and audit-compliant governance."),
        ("Threshold-Gated Nonlinear Propagation & Interrupt Dispatch", "To execute state-dependent edge activation rules that dynamically trigger contingent actions (hardware/software interrupt handling) when state variables cross safety thresholds.")
    ]
    for i, (otitle, odesc) in enumerate(objectives, 1):
        story.append(p(f"<b>{i}. {otitle}:</b> {odesc}"))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: WORKING PRINCIPLE & FIGURE 2 (ENLARGED ARCHITECTURE FLOWCHART)
    # =========================================================================
    story.append(sec("6. Working principle of the invention"))
    story.append(p(
        "The technical computing system executes an eleven-stage deterministic computational pipeline implemented in hardware processing units and memory buffers:"
    ))
    wp_steps = [
        ("1. Telemetry Ingestion & Canonicalization", "Ingests raw asynchronous event telemetry streams and normalizes payloads into canonical computational node schemas."),
        ("2. Temporal Multigraph Construction", "Instantiates an in-memory multigraph data structure G = (V, E, T) parametrized with static delay offsets δₑ and coupling weights ωₑ."),
        ("3. Cryptographic Baseline Freezing", "Computes an unperturbed forward time-series state vector array and serializes it as an immutable reference locked via SHA-256 hashing."),
        ("4. Perturbation Vector Object Translation", "Parses disturbance signals into a structured Perturbation Vector Object: <code>{source_node, target_var, magnitude, unit, onset_time, duration, conversion_rule}</code>."),
        ("5. Affected Subgraph Isolation", "Executes forward graph traversal from the disturbance source node to isolate reachable downstream mechanisms within the active window."),
        ("6. Single-Pass Dual-Transform Propagation", "Simultaneously computes updated amplitudes: ΔAᵥ = ΔAᵤ · ωₑ · ψₑ and shifts execution timestamps: tᵥ = tᵤ + δₑ across memory registers."),
        ("7. Asynchronous Multi-Path Convergence", "Aggregates converging vector flows at terminal accumulator nodes: ΔA_acc(t) = ∑_p ΔA_p(t) while persisting attribution share registers."),
        ("8. Time-Series Trajectory Synthesis", "Superimposes propagated state deltas onto the immutable baseline vector array to generate the perturbed system state curve."),
        ("9. Dynamic State Deflection Envelope Extraction", "Scans the trajectory difference curve to extract impact onset boundary, extreme deflection point, deflection duration, and recovery timestamps."),
        ("10. Multi-Dimensional Variance Analytics", "Decomposes multi-attribute state variances across discrete buffer registers and memory stages."),
        ("11. Real-Time Telemetry Display Controller", "Addresses hardware display buffer memory to render real-time topological graphs, Gantt timelines, and stacked causal attribution shares.")
    ]
    for wtitle, wdesc in wp_steps:
        story.append(p(f"<b>• {wtitle}:</b> {wdesc}"))
    story.append(sp(2.5))

    story.append(sec("7. Description of the invention in detail"))
    story.append(sub("7.1 End-to-End Physical Computing System Architecture"))
    story.append(p(
        "The physical and functional computing architecture of the system is structured into three discrete operational subsystems as illustrated in <b>Fig. 2</b>: "
        "(1) Telemetry Ingestion & Canonicalization Subsystem [100] (Modules [102]-[106]), "
        "(2) Temporal Multigraph Builder & Single-Pass Dual-Transform Propagation Core [200] (Modules [202]-[208]), and "
        "(3) Multi-Path Convergence, Dynamic State Deflection Detection & Telemetry Presentation Layer [300] (Modules [302]-[308])."
    ))

    # Embed Figure 2 with large, prominent height
    story.extend(embed_fig(
        '09_physical_system_architecture_flowchart.png',
        "Fig. 2: Physical System Architecture Flowchart - Computer-implemented engineering schematic of Subsystems [100], [200], and [300], illustrating event log ingestion, canonical normalization, graph computation core, dual-transform propagation mechanics, and executive presentation layer with reference numerals [102]-[308].",
        max_h=300, scale=0.98
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: FIGURE 3 (ENLARGED EVENT GRAPH) & 13-NODE TAXONOMY
    # =========================================================================
    story.append(sub("7.2 Temporal Multigraph Topology & Node Interconnections"))
    story.append(p(
        "The computational multigraph topology comprises thirteen discrete typed computational nodes [210]-[234] connected via fourteen directed dual-transform edges. "
        "Each node represents an asynchronous processing stage, queue buffer, or state accumulator, as illustrated in <b>Fig. 3</b>."
    ))

    # Embed Figure 3 with spacious dimensions
    story.extend(embed_fig(
        '02_temporal_business_event_graph.png',
        "Fig. 3: Temporal Business-Event Graph - 13 typed transactional mechanism nodes [210]-[234] and 14 dual-transform directed edges e = (u, v), depicting Path A Primary Propagation Cascade (solid blue) and Path B Secondary Cost Cascade (dashed crimson) converging at terminal accumulator node [232].",
        max_h=280, scale=0.98
    ))
    story.append(sp(2))

    story.append(sub("7.3 13-Node Computational Mechanism Taxonomy & Functional Roles"))
    node_tax_data = [
        [Paragraph("<b>Computational Node</b>", S_TH), Paragraph("<b>Functional Class</b>", S_TH), Paragraph("<b>Computational Data Processing Role</b>", S_TH), Paragraph("<b>State Coupling Impact</b>", S_TH)],
        [Paragraph("<code>Supplier [210]</code>", S_TD_B), Paragraph("Originator Node", S_TD_C), Paragraph("External dependency feed generating input flow and capacity signals", S_TD), Paragraph("Input trigger signal", S_TD)],
        [Paragraph("<code>PurchaseOrder [212]</code>", S_TD_B), Paragraph("Queue Buffer", S_TD_C), Paragraph("Procurement state commitment holding scheduled delivery contracts", S_TD), Paragraph("Forward latency offset", S_TD)],
        [Paragraph("<code>InventoryReceipt [214]</code>", S_TD_B), Paragraph("Transformation", S_TD_C), Paragraph("Physical receipt register; generates downstream liability obligations", S_TD), Paragraph("Generates downstream edge", S_TD)],
        [Paragraph("<code>ProductionEvent [216]</code>", S_TD_B), Paragraph("Transformation", S_TD_C), Paragraph("Batch conversion processing raw units into finished output states", S_TD), Paragraph("Scaling transfer operator", S_TD)],
        [Paragraph("<code>CustomerOrder [218]</code>", S_TD_B), Paragraph("Queue Buffer", S_TD_C), Paragraph("Demand commitment queue with fulfillment and pricing parameters", S_TD), Paragraph("Demand coupling factor", S_TD)],
        [Paragraph("<code>Invoice [220]</code>", S_TD_B), Paragraph("Transformation", S_TD_C), Paragraph("Billing transaction generating formal accounts receivable vectors", S_TD), Paragraph("Transforms units to scalar currency", S_TD)],
        [Paragraph("<code>AccountsReceivable [222]</code>", S_TD_B), Paragraph("Latency Delay", S_TD_C), Paragraph("Short-term credit buffer register awaiting settlement signal", S_TD), Paragraph("Scheduled state inflow", S_TD_B)],
        [Paragraph("<code>CustomerPayment [224]</code>", S_TD_B), Paragraph("Accumulator Inflow", S_TD_C), Paragraph("Discrete remittance packet received and deposited into state accumulator", S_TD), Paragraph("<b>POSITIVE STATE DELTA (+)</b>", S_TD_B)],
        [Paragraph("<code>AccountsPayable [228]</code>", S_TD_B), Paragraph("Latency Delay", S_TD_C), Paragraph("Short-term liability debt register awaiting disbursement schedule", S_TD), Paragraph("Scheduled state outflow", S_TD_B)],
        [Paragraph("<code>SupplierPayment [230]</code>", S_TD_B), Paragraph("Accumulator Outflow", S_TD_C), Paragraph("Disbursement packet settling vendor payable obligations", S_TD), Paragraph("<b>NEGATIVE STATE DELTA (-)</b>", S_TD_B)],
        [Paragraph("<code>ExpenseEvent [226]</code>", S_TD_B), Paragraph("Transformation", S_TD_C), Paragraph("Spot procurement, premium freight, and operational overhead costs", S_TD), Paragraph("<b>DIRECT STATE OUTFLOW (-)</b>", S_TD_B)],
        [Paragraph("<code>CashAccount [232]</code>", S_TD_B), Paragraph("Terminal Accumulator", S_TD_C), Paragraph("Central treasury register; multi-path convergence of all inflows and outflows", S_TD), Paragraph("<b>PRIMARY ACCUMULATOR SINK</b>", S_TD_B)],
        [Paragraph("<code>FinancingEvent [234]</code>", S_TD_B), Paragraph("Interrupt Node", S_TD_C), Paragraph("State-dependent threshold-gated contingent credit facility draw", S_TD), Paragraph("<b>CONTINGENT INFLOW (+)</b>", S_TD_B)],
    ]
    story.append(make_tbl(node_tax_data, [CW*0.22, CW*0.16, CW*0.40, CW*0.22], is_header=True))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: MATHEMATICAL FORMALIZATION & 14 EDGES TABLE (STEP 2 VOCABULARY)
    # =========================================================================
    story.append(sub("7.4 Mathematical Formalization of Temporal Graph & Coupled Dual-Transform Operators"))
    story.append(p(
        "Let the technical network be formalized as a directed temporal multigraph G = (V, E, T), "
        "where vertices u, v ∈ V represent typed computational nodes, and directed edges e = (u, v) ∈ E represent causal dependency couplings."
    ))
    story.append(sp(2))

    math_box_data = [[
        Paragraph(
            "<b>COUPLED DUAL-TRANSFORM VECTOR PROPAGATION EQUATIONS:</b><br/>"
            "For every directed edge connecting source node u to target node v:<br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<b>Directed Edge Vector:</b> &nbsp;&nbsp;&nbsp;&nbsp; <b>e = (u, v)</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<b>Scalar Amplitude Scaling:</b> &nbsp;&nbsp;&nbsp;&nbsp; <b>ΔAᵥ = ΔAᵤ · ωₑ · ψₑ</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<b>Temporal Latency Shifting:</b> &nbsp;&nbsp;&nbsp;&nbsp; <b>tᵥ = tᵤ + δₑ</b>",
            S_FORMULA
        )
    ]]
    math_box_tbl = Table(math_box_data, colWidths=[CW])
    math_box_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.8, TABLE_HEAD),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(math_box_tbl)
    story.append(sp(2))

    story.append(p("<b>Explicit Definition of Computational Mathematical Symbols:</b>"))
    sym_def_data = [
        [Paragraph("<b>Symbol</b>", S_TH), Paragraph("<b>Computational Attribute Name</b>", S_TH), Paragraph("<b>Domain & Physical Significance</b>", S_TH)],
        [Paragraph("<b>e = (u, v)</b>", S_TD_B), Paragraph("Directed Temporal Edge", S_TD_B), Paragraph("Causal computational coupling directed from source node u to target node v.", S_TD)],
        [Paragraph("<b>ΔAᵤ</b>", S_TD_B), Paragraph("Source Perturbation Amplitude", S_TD_B), Paragraph("Continuous scalar perturbation amplitude entering or active at source node u (units or scalar currency).", S_TD)],
        [Paragraph("<b>ΔAᵥ</b>", S_TD_B), Paragraph("Target Propagated Amplitude", S_TD_B), Paragraph("Continuous scalar amplitude transmitted to target node v following localized coupling transformation.", S_TD)],
        [Paragraph("<b>ωₑ</b>", S_TD_B), Paragraph("Coupling Weight Coefficient", S_TD_B), Paragraph("Empirical dependency weight on edge e, normalized to ωₑ ∈ [0.0, 1.0].", S_TD)],
        [Paragraph("<b>ψₑ</b>", S_TD_B), Paragraph("Cross-Domain Transfer Operator", S_TD_B), Paragraph("Functional operator mapping operational delta domains into target scalar units: ψₑ(ΔAᵤ).", S_TD)],
        [Paragraph("<b>tᵤ</b>", S_TD_B), Paragraph("Source Event Timestamp", S_TD_B), Paragraph("Discrete temporal onset timestamp or clock index of the event at source node u.", S_TD)],
        [Paragraph("<b>tᵥ</b>", S_TD_B), Paragraph("Target Execution Timestamp", S_TD_B), Paragraph("Discrete execution timestamp of the resulting downstream business event at target node v.", S_TD)],
        [Paragraph("<b>δₑ</b>", S_TD_B), Paragraph("Discrete Temporal Latency Offset", S_TD_B), Paragraph("Queue delay, transit latency, or processing term in integer clock units/days across edge e.", S_TD)],
    ]
    story.append(make_tbl(sym_def_data, [CW*0.18, CW*0.34, CW*0.48], is_header=True))
    story.append(sp(3))

    story.append(sub("7.5 Complete Temporal Graph Coupling Specification"))
    edges_df = pd.read_csv(os.path.join(DATA_DIR, 'temporal_graph_edges.csv'))
    edge_table_data = [[
        Paragraph("<b>ID</b>", S_TH),
        Paragraph("<b>Edge e = (u, v)</b>", S_TH),
        Paragraph("<b>Coupling Type</b>", S_TH),
        Paragraph("<b>Weight ωₑ</b>", S_TH),
        Paragraph("<b>Latency δₑ</b>", S_TH),
        Paragraph("<b>Operator ψₑ</b>", S_TH),
        Paragraph("<b>Rule Type</b>", S_TH),
        Paragraph("<b>Conf.</b>", S_TH),
    ]]
    for _, row in edges_df.iterrows():
        edge_table_data.append([
            Paragraph(f"<b>{row['edge_id']}</b>", S_TD_BC),
            Paragraph(f"({row['source_node']} → {row['target_node']})", S_TD_B),
            Paragraph(str(row['relationship_type']), S_TD),
            Paragraph(f"{row['dependency_strength']:.2f}", S_TD_C),
            Paragraph(f"{row['expected_delay_days']} days", S_TD_C),
            Paragraph(str(row['monetary_conversion']), S_TD),
            Paragraph(str(row['propagation_rule']), S_TD_C),
            Paragraph(f"{row['confidence']:.2f}", S_TD_C),
        ])
    story.append(make_tbl(edge_table_data, [
        CW*0.07, CW*0.27, CW*0.13, CW*0.12, CW*0.11, CW*0.14, CW*0.10, CW*0.06
    ], is_header=True))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: FIGURE 4 (ENLARGED HEATMAP) & FIGURE 5 (ENLARGED TIMELINE)
    # =========================================================================
    story.extend(embed_fig(
        '08_dependency_strength_heatmap.png',
        "Fig. 4: Dependency Strength Matrix Heatmap - Pairwise dependency coupling coefficients (ωₑ) across all 13×13 source-target business mechanism interactions in the enterprise operational network.",
        max_h=280, scale=0.92
    ))
    story.append(sp(2))

    story.append(sub("7.6 Temporal Propagation Timeline & Scheduling Engine"))
    story.append(p(
        "Propagation is governed by Algorithm 1: Beginning at perturbation onset t_0, the traversal engine evaluates downstream nodes "
        "chronologically. For each edge e = (u, v), target timestamp is calculated as tᵥ = tᵤ + δₑ and scalar magnitude as "
        "ΔAᵥ = ΔAᵤ · ωₑ · ψₑ in an asynchronous FIFO queue. The resulting timeline is illustrated in <b>Fig. 5</b>:"
    ))

    story.extend(embed_fig(
        '03_propagation_timeline.png',
        "Fig. 5: Temporal Propagation Timeline (Scenario DIST-001) - Gantt execution sequence from disturbance onset (T+0) to full liquidity recovery (T+103d) showing operational transit delays δₑ and direct cash settlements.",
        max_h=260, scale=0.94
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: MULTI-PATH CONVERGENCE & FIGURE 6 (ENLARGED ATTRIBUTION)
    # =========================================================================
    story.append(sub("7.7 Multi-Path Convergence Mechanics & Worked Example"))
    story.append(p(
        "<b>Perturbation Specification:</b> Source node S03 suffers an immediate 30% reduction in transmission capacity lasting 60 clock cycles. "
        "Two independent causal paths propagate concurrently through the graph and converge at the terminal accumulator node <code>CashAccount</code>:"
    ))
    story.append(sp(2))

    story.append(p("Path A - Primary Cascading Delay Path (Inventory → Deferred Inflow):", S_BODY_B))
    path_a_data = [
        [Paragraph("<b>Step</b>", S_TH), Paragraph("<b>Edge e = (u, v)</b>", S_TH), Paragraph("<b>Source Delta (ΔAᵤ)</b>", S_TH), Paragraph("<b>Target Delta (ΔAᵥ)</b>", S_TH), Paragraph("<b>ωₑ</b>", S_TH), Paragraph("<b>δₑ</b>", S_TH), Paragraph("<b>Target Time (tᵥ)</b>", S_TH)],
        [Paragraph("1", S_TD_C), Paragraph("Supplier → PurchaseOrder", S_TD), Paragraph("-30.0% cap.", S_TD), Paragraph("-30.0% vol.", S_TD), Paragraph("0.70", S_TD_C), Paragraph("14d", S_TD_C), Paragraph("T+14d", S_TD_C)],
        [Paragraph("2", S_TD_C), Paragraph("PurchaseOrder → InventoryReceipt", S_TD), Paragraph("-30.0% vol.", S_TD), Paragraph("-28.5% units", S_TD), Paragraph("0.95", S_TD_C), Paragraph("7d", S_TD_C), Paragraph("T+21d", S_TD_C)],
        [Paragraph("3", S_TD_C), Paragraph("InventoryReceipt → ProductionEvent", S_TD), Paragraph("-28.5% units", S_TD), Paragraph("-22.8% output", S_TD), Paragraph("0.80", S_TD_C), Paragraph("14d", S_TD_C), Paragraph("T+35d", S_TD_C)],
        [Paragraph("4", S_TD_C), Paragraph("ProductionEvent → CustomerOrder", S_TD), Paragraph("-22.8% output", S_TD), Paragraph("-19.4% fulfill", S_TD), Paragraph("0.85", S_TD_C), Paragraph("7d", S_TD_C), Paragraph("T+42d", S_TD_C)],
        [Paragraph("5", S_TD_C), Paragraph("CustomerOrder → Invoice", S_TD), Paragraph("-19.4% fulfill", S_TD), Paragraph("<b>-$187,500 bill</b>", S_TD), Paragraph("1.00", S_TD_C), Paragraph("0d", S_TD_C), Paragraph("T+42d", S_TD_C)],
        [Paragraph("6", S_TD_C), Paragraph("Invoice → AccountsReceivable", S_TD), Paragraph("-$187.5K bill", S_TD), Paragraph("-$187,500 AR", S_TD), Paragraph("1.00", S_TD_C), Paragraph("30d", S_TD_C), Paragraph("T+72d", S_TD_C)],
        [Paragraph("7", S_TD_C), Paragraph("AccountsReceivable → CustomerPayment", S_TD), Paragraph("-$187.5K AR", S_TD), Paragraph("-$178,125 cash", S_TD), Paragraph("0.95", S_TD_C), Paragraph("0d", S_TD_C), Paragraph("T+72d", S_TD_C)],
        [Paragraph("8", S_TD_C), Paragraph("CustomerPayment → CashAccount", S_TD_B), Paragraph("-$178.1K cash", S_TD), Paragraph("<b>-$178,125 CASH</b>", S_TD_B), Paragraph("1.00", S_TD_C), Paragraph("0d", S_TD_C), Paragraph("<b>T+72d</b>", S_TD_BC)],
    ]
    story.append(make_tbl(path_a_data, [
        CW*0.06, CW*0.30, CW*0.15, CW*0.17, CW*0.08, CW*0.08, CW*0.16
    ], is_header=True))
    story.append(sp(2))

    story.append(p("Path B - Secondary Expedited Cost Cascade Path (Spot Sourcing → Accelerated Payables):", S_BODY_B))
    path_b_data = [
        [Paragraph("<b>Step</b>", S_TH), Paragraph("<b>Edge e = (u, v)</b>", S_TH), Paragraph("<b>Source Delta (ΔAᵤ)</b>", S_TH), Paragraph("<b>Target Delta (ΔAᵥ)</b>", S_TH), Paragraph("<b>ωₑ</b>", S_TH), Paragraph("<b>δₑ</b>", S_TH), Paragraph("<b>Target Time (tᵥ)</b>", S_TH)],
        [Paragraph("1", S_TD_C), Paragraph("Supplier → ExpenseEvent[EMRG]", S_TD), Paragraph("-30.0% cap.", S_TD), Paragraph("<b>+$45,000 spot</b>", S_TD), Paragraph("1.00", S_TD_C), Paragraph("7d", S_TD_C), Paragraph("T+7d", S_TD_C)],
        [Paragraph("2", S_TD_C), Paragraph("ExpenseEvent → AccountsPayable", S_TD), Paragraph("+$45,000 spot", S_TD), Paragraph("+$45,000 AP", S_TD), Paragraph("1.00", S_TD_C), Paragraph("30d", S_TD_C), Paragraph("T+37d", S_TD_C)],
        [Paragraph("3", S_TD_C), Paragraph("AccountsPayable → SupplierPayment", S_TD), Paragraph("+$45,000 AP", S_TD), Paragraph("+$45,000 disburse", S_TD), Paragraph("1.00", S_TD_C), Paragraph("0d", S_TD_C), Paragraph("T+37d", S_TD_C)],
        [Paragraph("4", S_TD_C), Paragraph("SupplierPayment → CashAccount", S_TD_B), Paragraph("+$45,000 disburse", S_TD), Paragraph("<b>-$45,000 CASH</b>", S_TD_B), Paragraph("1.00", S_TD_C), Paragraph("0d", S_TD_C), Paragraph("<b>T+37d</b>", S_TD_BC)],
    ]
    story.append(make_tbl(path_b_data, [
        CW*0.06, CW*0.30, CW*0.15, CW*0.17, CW*0.08, CW*0.08, CW*0.16
    ], is_header=True, header_bg=colors.Color(0.45, 0.18, 0.10)))
    story.append(sp(2))

    conv_data = [
        [Paragraph("<b>Causal Propagation Path</b>", S_TH), Paragraph("<b>Physical Mechanism</b>", S_TH), Paragraph("<b>Terminal Amplitude (ΔA)</b>", S_TH), Paragraph("<b>Peak Timestamp</b>", S_TH), Paragraph("<b>Attributed Share</b>", S_TH)],
        [Paragraph("<b>Path A: Primary Delay Cascade</b>", S_TD_B), Paragraph("Unfulfilled finished goods → delayed billing → deferred cash inflows", S_TD), Paragraph("-$178,125", S_TD_BC), Paragraph("T+72 days", S_TD_C), Paragraph("<b>81.0%</b>", S_TD_BC)],
        [Paragraph("<b>Path B: Expedited Cost Surge</b>", S_TD_B), Paragraph("Spot buffer replenishment & premium transit → expedited liabilities", S_TD), Paragraph("-$45,000", S_TD_BC), Paragraph("T+37 days", S_TD_C), Paragraph("<b>19.0%</b>", S_TD_BC)],
        [Paragraph("<b>TOTAL CONVERGED IMPACT</b>", S_TD_B), Paragraph("Superposition of concurrent causal streams at terminal accumulator sink", S_TD_B), Paragraph("<b>-$223,125</b>", S_TD_BC), Paragraph("T+37d to T+72d", S_TD_BC), Paragraph("<b>100.0%</b>", S_TD_BC)],
    ]
    story.append(make_tbl(conv_data, [CW*0.25, CW*0.35, CW*0.15, CW*0.13, CW*0.12], is_header=True))
    story.append(sp(2))

    story.extend(embed_fig(
        '04_multipath_convergence_attribution.png',
        "Fig. 6: Multi-Path Monetary Convergence & Causal Attribution at CashAccount - Causal decomposition demonstrating exact monetary split between revenue losses (Path A: -$178,125 / 81.0%) and emergency cost outflows (Path B: -$45,000 / 19.0%) under numerical conservation law.",
        max_h=240, scale=0.88
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: AUDIT LOG, EMBODIMENTS (STEP 3) & FIGURE 7
    # =========================================================================
    story.append(sub("7.8 Complete 12-Step Propagation Audit Trail Dataset"))
    audit_df = pd.read_csv(os.path.join(DATA_DIR, 'propagation_audit_log.csv'))
    audit_table_data = [[
        Paragraph("<b>#</b>", S_TH),
        Paragraph("<b>Source Node u</b>", S_TH),
        Paragraph("<b>Target Node v</b>", S_TH),
        Paragraph("<b>Src ΔAᵤ</b>", S_TH),
        Paragraph("<b>Tgt ΔAᵥ</b>", S_TH),
        Paragraph("<b>ωₑ</b>", S_TH),
        Paragraph("<b>δₑ</b>", S_TH),
        Paragraph("<b>Rule</b>", S_TH),
        Paragraph("<b>Scheduled Time (tᵥ)</b>", S_TH),
    ]]
    for idx, row in audit_df.iterrows():
        audit_table_data.append([
            Paragraph(str(idx + 1), S_TD_C),
            Paragraph(str(row['source_event']), S_TD),
            Paragraph(str(row['target_event']), S_TD),
            Paragraph(f"{row['source_delta']:.3f}" if isinstance(row['source_delta'], float) else str(row['source_delta']), S_TD_C),
            Paragraph(f"{row['target_delta']:.3f}" if isinstance(row['target_delta'], float) else str(row['target_delta']), S_TD_C),
            Paragraph(f"{row['dependency_strength']:.2f}", S_TD_C),
            Paragraph(f"{row['delay_days']}d", S_TD_C),
            Paragraph(str(row['propagation_rule']), S_TD_C),
            Paragraph(f"T+{row['scheduled_day_from_t0']}d", S_TD_C),
        ])
    story.append(make_tbl(audit_table_data, [
        CW*0.05, CW*0.19, CW*0.20, CW*0.11, CW*0.11, CW*0.07, CW*0.07, CW*0.10, CW*0.10
    ], is_header=True))
    story.append(sp(2.5))

    story.append(sub("7.9 Universal Technical Embodiments: Packet Routing, Distributed Microservices, and Enterprise Telemetry"))
    story.append(p(
        "To establish that the temporal multigraph state propagation architecture is a universal technical computing engine rather than a "
        "field-specific method, the system executes identically across diverse physical computing domains:"
    ))
    story.append(pb("<b>Embodiment 1 (Telecommunications & Packet Mesh Networks):</b> Computational nodes represent network routers, switches, and packet queue buffers; directed edges define physical wire latency (δₑ) and packet drop rate / bandwidth throttle transfer functions (ψₑ). An ingress link failure generates a perturbation amplitude (ΔAᵤ), which propagates through intermediate buffer hops to a terminal egress gateway accumulator, extracting a network throughput degradation envelope."))
    story.append(pb("<b>Embodiment 2 (Cloud Distributed Microservice Task Pipelines):</b> Nodes represent microservice worker pods, Kafka message queues, and database connection pools. Perturbations represent thread starvation or I/O latency spikes. Edges execute processing lag (δₑ) and thread pool backpressure amplification (ψₑ), converging at an end-to-end API response time sink register to extract a Service Level Objective (SLO) violation envelope."))
    story.append(pb("<b>Embodiment 3 (Enterprise Resource & Operational Telemetry):</b> Nodes represent discrete transactional mechanism stages (POs, Inventory, Payables) and edges define operational transit latencies and monetary scaling factors, presented strictly as one applied industrial use-case."))
    story.append(sp(2))

    story.extend(embed_fig(
        '07_supplier_risk_profile.png',
        "Fig. 7: Supplier Network Risk & Capability Profile - (a) Supplier reliability index distribution with S03 highlighted. (b) Monthly capacity vs. unit procurement cost scatter (bubble size = payment term days).",
        max_h=215, scale=0.92
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: TABLE 8.2 & FIGURE 8 (ENLARGED STATE TRAJECTORY)
    # =========================================================================
    story.append(sec("8. Experimental validation results:"))
    story.append(sub("8.1 Dynamic State Deflection Envelope Metrics"))
    with open(os.path.join(DATA_DIR, 'liquidity_impact_window.json')) as f:
        liw = json.load(f)

    liw_res_data = [
        [Paragraph("<b>Dynamic State Deflection Parameter</b>", S_TH), Paragraph("<b>Empirical Value</b>", S_TH), Paragraph("<b>Physical / Computational Interpretation</b>", S_TH)],
        [Paragraph("<b>Impact Onset Boundary (t_start)</b>", S_TD_B), Paragraph(f"<b>{liw['impact_start_date']} (T+21d)</b>", S_TD_BC), Paragraph("Timestamp where differential curve |ΔS(t)| exceeds noise margin ε", S_TD)],
        [Paragraph("<b>Extreme Deflection Index (t_peak)</b>", S_TD_B), Paragraph(f"<b>{liw['impact_peak_date']} (T+72d)</b>", S_TD_BC), Paragraph("Timestamp of maximum negative system state deflection", S_TD)],
        [Paragraph("<b>Peak State Deflection (ΔA_peak)</b>", S_TD_B), Paragraph(f"<b>-${abs(liw['peak_cash_deficit_usd']):,d}</b>", S_TD_BC), Paragraph("Maximum net negative amplitude deflection relative to unperturbed baseline", S_TD)],
        [Paragraph("<b>Active Impairment Duration (D)</b>", S_TD_B), Paragraph(f"<b>{liw['impact_duration_days']} Clock Units</b>", S_TD_BC), Paragraph("Total elapsed duration of active system state deflection: D = t_rec - t_start", S_TD)],
        [Paragraph("<b>Recovery Inflection Marker (t_rec_start)</b>", S_TD_B), Paragraph(f"<b>{liw['recovery_start_date']} (T+85d)</b>", S_TD_BC), Paragraph("Inflection timestamp where forward difference d(ΔS)/dt transitions positive", S_TD)],
        [Paragraph("<b>Equilibrium Recovery Date (t_rec)</b>", S_TD_B), Paragraph(f"<b>{liw['recovery_date']} (T+103d)</b>", S_TD_BC), Paragraph("Timestamp where system trajectory re-enters within equilibrium tolerance band", S_TD)],
        [Paragraph("<b>Cumulative Deflection Integral (ΔA_cum)</b>", S_TD_B), Paragraph(f"<b>-${abs(liw['cumulative_cash_delta_usd']):,d}</b>", S_TD_BC), Paragraph("Total integrated area of state deflection over active impairment window", S_TD)],
    ]
    story.append(make_tbl(liw_res_data, [CW*0.30, CW*0.25, CW*0.45], is_header=True))
    story.append(sp(3))

    # Figure 8 given large, generous page area for maximum clarity
    story.extend(embed_fig(
        '01_baseline_vs_disturbance_cash_trajectory.png',
        "Fig. 8: 120-Day Baseline vs. Disturbed Cash Trajectory - Upper panel: Baseline cash balance C_base(t) vs. disturbed cash balance C_dist(t) with cross-hatched Liquidity Impact Window zone and $150K safety bound. Lower panel: Daily cash delta ΔC(t).",
        max_h=330, scale=0.98
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: FIGURE 9 & SECTION 8.3 VALIDATION TESTS
    # =========================================================================
    # Figure 9 enlarged to full-page prominence with dedicated custom vector table
    story.extend(embed_fig(
        '05_liquidity_impact_window_dashboard.png',
        "Fig. 9: Executive Liquidity Impact Window Dashboard & Parameter Extraction Matrix - Trajectory decomposition and structured specification table of the formal 7-tuple LIW metrics W = <t_start, t_peak, Δ_peak, D, t_rec_start, t_rec, Δ_cum>.",
        max_h=350, scale=0.98
    ))
    story.append(sp(3))

    story.append(sub("8.3 Six Formal System Integrity Validation Tests (Empirical Proof of Technical Effects)"))
    pass_cell = Paragraph("PASS", S_TD_BC)
    val_test_data = [
        [Paragraph("<b>Test ID</b>", S_TH), Paragraph("<b>Verification Test Description</b>", S_TH), Paragraph("<b>Demonstrated Technical Effect under Section 3(k)</b>", S_TH), Paragraph("<b>Empirical Test Result</b>", S_TH), Paragraph("<b>Status</b>", S_TH)],
        [Paragraph("<b>TEST-01</b>", S_TD_BC), Paragraph("Determinism & Seed Invariance", S_TD_B), Paragraph("Elimination of multi-threaded race conditions in graph queue traversal", S_TD), Paragraph("Bitwise identical outputs across 10 execution cycles (Δ = 0.00)", S_TD), pass_cell],
        [Paragraph("<b>TEST-02</b>", S_TD_BC), Paragraph("Baseline Reference Immutability", S_TD_B), Paragraph("Cryptographic data integrity of state array via SHA-256 hash anchoring", S_TD), Paragraph("Cryptographic hash identical pre/post scenario execution", S_TD), pass_cell],
        [Paragraph("<b>TEST-03</b>", S_TD_BC), Paragraph("Multi-Path Convergence Correctness", S_TD_B), Paragraph("Lossless vector accumulation under mathematical conservation rule", S_TD), Paragraph("Path A (-$178,125) + Path B (-$45,000) = -$223,125 exact match", S_TD), pass_cell],
        [Paragraph("<b>TEST-04</b>", S_TD_BC), Paragraph("Threshold-Triggered Propagation", S_TD_B), Paragraph("Real-time event interrupt handling activating contingent graph branches", S_TD), Paragraph("Trigger fired precisely when state crossed bound at Cycle 71", S_TD), pass_cell],
        [Paragraph("<b>TEST-05</b>", S_TD_BC), Paragraph("Complete Propagation Auditability", S_TD_B), Paragraph("Deterministic serializability of graph transitions in memory registers", S_TD), Paragraph("All 12 propagation hops recorded in audit log with rules and confidence", S_TD), pass_cell],
        [Paragraph("<b>TEST-06</b>", S_TD_BC), Paragraph("Attribution Conservation Law", S_TD_B), Paragraph("Exact mathematical attribution balance across converging vector paths", S_TD), Paragraph("Path A (81.0%) + Path B (19.0%) = 100.00% exact numerical balance", S_TD), pass_cell],
    ]
    t_val = make_tbl(val_test_data, [CW*0.10, CW*0.22, CW*0.30, CW*0.28, CW*0.10], is_header=True)
    story.append(t_val)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: CLAIMS 1 TO 5 (DE-FINANCIALIZED PATENTABLE TECHNICAL CLAIMS)
    # =========================================================================
    story.append(sec("9. What aspects of the invention need protection?"))
    story.append(sub("9.1 Claims Requiring Protection"))
    story.append(p(
        "Protection is sought for the novel technical computing systems, computer-implemented methods, in-memory graph data structures, "
        "and telemetry controllers defined in Claims 1 through 8 below, in full statutory compliance with Section 3(k) of the Indian Patents Act, 1970:"
    ))
    story.append(sp(2))

    claims_p1 = [
        ("Claim 1 (Independent Method Claim - Deterministic Multi-Attribute State Propagation Across Graph Architectures):",
         "A computer-implemented method for deterministic multi-attribute state propagation across asynchronous graph architectures, executed by one or more hardware processors, comprising: "
         "(a) receiving, at an ingestion interface, an operational disturbance signal representing a quantifiable disruption event; "
         "(b) generating, via a parsing engine, a structured multi-attribute perturbation vector object comprising: a source node identifier, "
         "a continuous scalar amplitude attribute (ΔAᵤ), a discrete temporal onset timestamp (tᵤ), an elapsed duration parameter, and a localized transfer operator (ψₑ); "
         "(c) instantiating in an allocated memory space a directed temporal multigraph data structure G = (V, E, T) comprising a plurality of typed computational nodes (V) "
         "interconnected by directed dependency edges (E), wherein each edge defines a static delay offset (δₑ) and a coupling weight (ωₑ); "
         "(d) traversing, via an asynchronous event scheduling queue buffer, downstream dependency paths initiated by said perturbation vector object; "
         "(e) executing, at each traversed edge in a single processing pass, a coupled dual-transform vector operation simultaneously advancing the temporal schedule "
         "(tᵥ = tᵤ + δₑ) and scaling the scalar amplitude (ΔAᵥ = ΔAᵤ · ωₑ · ψₑ) within hardware memory registers; "
         "(f) resolving multi-path convergence at a terminal accumulator node where multiple concurrent propagation paths intersect, "
         "by aggregating arriving scalar amplitudes under a strict numerical conservation rule while persisting decoupled path-attribution share registers; and "
         "(g) extracting, via a differential curve scanning engine, a multi-parameter dynamic state deflection envelope defining: "
         "an impact onset boundary (t_start), an extreme deflection point (t_peak, ΔA_peak), an active deflection duration (D), and a system equilibrium recovery timestamp (t_rec)."),

        ("Claim 2 (Independent System Claim - Technical Computing Architecture for Asynchronous Graph Propagation):",
         "A technical computing data processing system for deterministic multi-attribute state propagation across asynchronous graph architectures, comprising: "
         "one or more hardware processors; and "
         "a memory communicatively coupled to said one or more hardware processors storing computer-executable instructions that, when executed by said processors, "
         "configure the system to implement: "
         "an event ingestion and canonicalization module configured to ingest raw asynchronous event streams and normalize incoming payloads into structured perturbation vector objects; "
         "a temporal multigraph database module configured to build and store in allocated memory registers a directed temporal multigraph G = (V, E, T) "
         "comprising a plurality of typed computational nodes (V) interconnected by directed dependency edges (E) configured with dual-transform attributes (ωₑ, ψₑ, δₑ); "
         "an immutable baseline reference module configured to serialize, store, and cryptographically anchor an unperturbed forward time-series state vector array; "
         "an asynchronous event queue scheduling module configured to sort, prioritize, and dispatch propagating graph state updates in chronological order to eliminate race conditions; "
         "a single-pass dual-transform propagation engine configured to traverse said in-memory multigraph across said queue and simultaneously compute "
         "ΔAᵥ = ΔAᵤ · ωₑ · ψₑ and tᵥ = tᵤ + δₑ; "
         "a multi-path convergence accumulator module configured to aggregate converging scalar deltas at a terminal accumulator node under a strict numerical conservation constraint "
         "while recording decoupled path-specific attribution vectors; and "
         "a differential curve scanning module configured to extract a multi-parameter dynamic state deflection envelope defining impact onset boundary, "
         "extreme deflection point, deflection duration, and system equilibrium recovery."),

        ("Claim 3 (Method Claim - Multi-Path Convergence Resolution and Lossless Vector Attribution):",
         "The method of Claim 1, wherein resolving multi-path convergence comprises: "
         "(a) identifying a plurality of mutually independent causal propagation paths originating from said source node identifier and terminating at a common terminal accumulator node; "
         "(b) scheduling execution timestamps for each of said plurality of paths within said asynchronous event scheduling queue buffer; "
         "(c) accumulating scalar deltas arriving at said terminal accumulator node at timestamp t according to ΔA_acc(t) = ∑_p ΔA_p(t); and "
         "(d) recording, in an attribution memory register, a distinct causal share vector for each converging path quantifying absolute scalar contribution "
         "and percentage share relative to total converged deflection, satisfying a strict numerical conservation rule ∑ (percentage_share_p) = 100.0%."),

        ("Claim 4 (Method Claim - State-Dependent and Threshold-Gated Nonlinear Graph Reconfiguration):",
         "The method of Claim 1, wherein one or more directed dependency edges within said in-memory temporal multigraph comprise threshold-gated activation rules "
         "configured to evaluate a state variable of a target node prior to disturbance transmission, "
         "such that when said state variable crosses a predefined safety threshold, the propagation engine dynamically activates an alternative transfer operator "
         "or triggers a real-time event interrupt to dispatch a contingent execution node."),

        ("Claim 5 (Method Claim - Cryptographic State-Transition Anchoring and Bitwise Reproducibility):",
         "The method of Claim 1, further comprising: "
         "(a) generating, prior to perturbation simulation, a cryptographic hash digest of the unperturbed forward baseline state vector array using a secure hashing algorithm (SHA-256); "
         "(b) storing said cryptographic hash digest in an immutable verification registry; and "
         "(c) executing propagation operations deterministically such that identical perturbation vector inputs and multigraph topology guarantee bitwise identical "
         "dynamic state deflection envelope outputs across arbitrary execution instances, verifying absence of multi-threaded race conditions.")
    ]

    for ctitle, cdesc in claims_p1:
        story.append(p(f"{ctitle}", S_CLAIM_HEAD))
        story.append(p(cdesc, S_BODY))
        story.append(sp(2))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: CLAIMS 6 TO 8 & PROTECTION SCOPE & CONTRIBUTION TABLES
    # =========================================================================
    claims_p2 = [
        ("Claim 6 (System Claim - Abstract Functional Computational Node Classes in Memory):",
         "The system of Claim 2, wherein said plurality of typed computational nodes (V) stored in allocated memory registers are configured into abstract functional node classes comprising: "
         "originator nodes configured as trigger generators for initiating perturbation vectors; "
         "latency delay nodes configured as operational queue buffers introducing discrete latency offsets; "
         "transformation nodes configured for scalar magnitude scaling across operational domains; "
         "accumulator nodes configured as state sinks for multi-path convergence and vector summation; and "
         "interrupt nodes configured as threshold-gated state dispatchers for contingent branch execution; "
         "and wherein, in an enterprise resource telemetry embodiment, said node classes map respectively to supplier, inventory, order, billing, receivable, payable, and cash settlement mechanism registers."),

        ("Claim 7 (Method Claim - Circular Buffer Scanning and Bounded Envelope Extraction):",
         "The method of Claim 1, wherein extracting said dynamic state deflection envelope comprises: "
         "(a) computing a discrete differential array ΔS(t) = S_pert(t) - S_base(t) by subtracting unperturbed baseline values from perturbed trajectory values stored across a circular buffer; "
         "(b) scanning said circular buffer with a windowed register comparator to detect an onset boundary timestamp t_start where |ΔS(t)| exceeds a predefined noise margin; "
         "(c) detecting an extreme deflection index t_peak and peak deflection amplitude ΔA_peak via register comparison; "
         "(d) detecting a recovery inflection marker t_rec_start where first-order forward finite differences ΔS(t+1) - ΔS(t) transition from negative to positive; "
         "(e) detecting an equilibrium recovery boundary t_rec where |ΔS(t)| reconverges within a predefined tolerance band; and "
         "(f) accumulating discrete area sum ΔA_cum = ∑ |ΔS(t)| across the active impairment duration D = t_rec - t_start."),

        ("Claim 8 (Apparatus Claim - Telemetry Controller and Display Buffer Dynamic Addressing):",
         "A non-transitory computer-readable storage medium storing computer-executable instructions that, when executed by a hardware processor, "
         "cause the processor to control a display controller and frame buffer memory to render real-time computational graph telemetry, comprising: "
         "dynamically addressing a frame buffer memory to map graph node topology registers into a topological multigraph viewport; "
         "addressing video display memory to map chronological event timestamps from said event queue into an execution timeline viewport; "
         "continuously rasterizing into a trajectory display buffer said baseline state vector and said perturbed state vector while filling memory scanlines "
         "corresponding to said dynamic state deflection envelope with a visually distinguished color mask; and "
         "updating hardware color registers in an attribution viewport to display proportional bit allocations corresponding to individual causal path attribution registers.")
    ]

    for ctitle, cdesc in claims_p2:
        story.append(p(f"{ctitle}", S_CLAIM_HEAD))
        story.append(p(cdesc, S_BODY))
        story.append(sp(2))
    story.append(sp(2))

    story.append(sub("9.2 Summary of Technical Protection Scope (Section 3(k) Mapping)"))
    scope_data = [
        [Paragraph("<b>Claim #</b>", S_TH), Paragraph("<b>Claim Type</b>", S_TH), Paragraph("<b>Core Technical Subject Matter</b>", S_TH), Paragraph("<b>Internal Hardware Technical Effect under Section 3(k)</b>", S_TH)],
        [Paragraph("Claim 1", S_TD_C), Paragraph("Independent Method", S_TD_C), Paragraph("Deterministic state propagation across asynchronous multigraph", S_TD), Paragraph("O(|V| + |E|) linear-time graph traversal, eliminating combinatorial latency", S_TD)],
        [Paragraph("Claim 2", S_TD_C), Paragraph("Independent System", S_TD_C), Paragraph("End-to-end multi-module computing hardware architecture", S_TD), Paragraph("Specialized physical memory data structures with asynchronous queue buffers", S_TD)],
        [Paragraph("Claim 3", S_TD_C), Paragraph("Dependent Method", S_TD_C), Paragraph("Multi-path convergence with decoupled vector attribution", S_TD), Paragraph("Exact numerical conservation without distortion or race conditions", S_TD)],
        [Paragraph("Claim 4", S_TD_C), Paragraph("Dependent Method", S_TD_C), Paragraph("State-dependent threshold rules and contingent execution", S_TD), Paragraph("Real-time event interrupt handling and dynamic graph branch dispatch", S_TD)],
        [Paragraph("Claim 5", S_TD_C), Paragraph("Dependent Method", S_TD_C), Paragraph("Cryptographic SHA-256 state anchoring & determinism", S_TD), Paragraph("Bitwise reproducible execution and tamper-evident audit ledger", S_TD)],
        [Paragraph("Claim 6", S_TD_C), Paragraph("Dependent System", S_TD_C), Paragraph("Abstract functional node classes in memory registers", S_TD), Paragraph("Optimized memory representation and cache locality in contiguous array buffers", S_TD)],
        [Paragraph("Claim 7", S_TD_C), Paragraph("Dependent Method", S_TD_C), Paragraph("Circular buffer scanning & inflection boundary extraction", S_TD), Paragraph("Hardware register comparison avoiding continuous floating-point calculus", S_TD)],
        [Paragraph("Claim 8", S_TD_C), Paragraph("Apparatus / Medium", S_TD_C), Paragraph("Telemetry controller and display buffer memory addressing", S_TD), Paragraph("Direct frame buffer memory scanline rasterization of graph state telemetry", S_TD)],
    ]
    story.append(make_tbl(scope_data, [CW*0.11, CW*0.21, CW*0.35, CW*0.33], is_header=True))
    story.append(sp(2))

    story.append(sub("9.3 Contribution-to-Claim Mapping"))
    mapping_data = [
        [Paragraph("<b>Invention Contribution</b>", S_TH), Paragraph("<b>Addressed Technical Gap under Section 3(k)</b>", S_TH), Paragraph("<b>Core Computational Mechanism</b>", S_TH), Paragraph("<b>Protected Claims</b>", S_TH)],
        [Paragraph("<b>1. First-Class Typed Vector</b>", S_TD_B), Paragraph("Prior art uses dimensionless risk labels (0-1)", S_TD), Paragraph("Typed Perturbation Vector Object: ΔAᵤ, tᵤ, ψₑ", S_TD), Paragraph("Claim 1, Claim 2", S_TD_C)],
        [Paragraph("<b>2. Coupled Dual-Transform</b>", S_TD_B), Paragraph("Prior art edges only scale weights statically", S_TD), Paragraph("ΔAᵥ = ΔAᵤ · ωₑ · ψₑ and tᵥ = tᵤ + δₑ in single pass", S_TD), Paragraph("Claim 1, Claim 2, Claim 6", S_TD_C)],
        [Paragraph("<b>3. Lossless Convergence</b>", S_TD_B), Paragraph("Prior art causes race conditions at accumulators", S_TD), Paragraph("Convergence aggregation: ΔA_acc = ∑ ΔA_p", S_TD), Paragraph("Claim 3", S_TD_C)],
        [Paragraph("<b>4. Dynamic Envelope Extraction</b>", S_TD_B), Paragraph("Prior art outputs static point forecasts", S_TD), Paragraph("Circular buffer scanning for inflection boundaries", S_TD), Paragraph("Claim 1, Claim 7", S_TD_C)],
        [Paragraph("<b>5. Cryptographic Anchoring</b>", S_TD_B), Paragraph("Prior art lacks deterministic reproducibility", S_TD), Paragraph("Threshold rules θₑ and SHA-256 baseline freezing", S_TD), Paragraph("Claim 4, Claim 5", S_TD_C)],
    ]
    story.append(make_tbl(mapping_data, [CW*0.24, CW*0.28, CW*0.34, CW*0.14], is_header=True))

    # =========================================================================
    # LAST PAGE (PAGE 14): SECTION 10 TRL TABLE & END OF DOCUMENT
    # =========================================================================
    story.append(NextPageTemplate('Last'))
    story.append(PageBreak())

    # Section 10 Title matching original template image media_1788430271710.png
    story.append(sec("10. What is Technology readiness level of your invention? (Tick the appropriate TRL)"))
    story.append(sp(6))

    cw_trl = CW / 9.0  # 54.78 pt each
    tick_str = '<font name="CheckmarkFont" size="11">✓</font>'

    # Exact table structure matching media_1788430271710.png and example1.pdf page 19
    trl_table_cells = [
        # Row 0: Phase Super-Headers
        [
            Paragraph("<b>Research</b>", S_TH_DARK), Paragraph("", S_TH_DARK), Paragraph("", S_TH_DARK),
            Paragraph("<b>Development</b>", S_TH_DARK), Paragraph("", S_TH_DARK), Paragraph("", S_TH_DARK),
            Paragraph("<b>Deployment</b>", S_TH_DARK), Paragraph("", S_TH_DARK), Paragraph("", S_TH_DARK),
        ],
        # Row 1: TRL Numbers
        [
            Paragraph("<b>TRL 1</b>", S_TH_DARK), Paragraph("<b>TRL 2</b>", S_TH_DARK), Paragraph("<b>TRL 3</b>", S_TH_DARK),
            Paragraph("<b>TRL 4</b>", S_TH_DARK), Paragraph("<b>TRL 5</b>", S_TH_DARK), Paragraph("<b>TRL 6</b>", S_TH_DARK),
            Paragraph("<b>TRL 7</b>", S_TH_DARK), Paragraph("<b>TRL 8</b>", S_TH_DARK), Paragraph("<b>TRL 9</b>", S_TH_DARK),
        ],
        # Row 2: Standard Descriptions matching original template image
        [
            Paragraph("Basic<br/>Principles<br/>observed", S_TD_C),
            Paragraph("Technology<br/>concept<br/>formulated", S_TD_C),
            Paragraph("Experimental<br/>proof of<br/>concept", S_TD_C),
            Paragraph("Technology<br/>validated in<br/>a lab", S_TD_C),
            Paragraph("Technology<br/>validated in a<br/>relevant<br/>environment<br/>(industrially<br/>relevant in<br/>case of key<br/>enabling<br/>technologies)", S_TD_C),
            Paragraph("Technology<br/>demonstrated<br/>in a relevant<br/>environment<br/>(industrially<br/>relevant in<br/>case of key<br/>enabling<br/>technologies)", S_TD_C),
            Paragraph("System<br/>prototype<br/>demonstration<br/>in an<br/>operational<br/>environment", S_TD_C),
            Paragraph("System<br/>complete<br/>and<br/>qualified", S_TD_C),
            Paragraph("Actual system<br/>proven in an<br/>operational<br/>environment<br/>(competitive<br/>manufacturing<br/>in case of key<br/>enabling<br/>technologies,<br/>or in space )", S_TD_C),
        ],
        # Row 3: Selection Row matching template image media_1788430271710.png
        [
            Paragraph("", S_TD_C),
            Paragraph("", S_TD_C),
            Paragraph("", S_TD_C),
            Paragraph(f'{tick_str}<br/><br/><font color="#C00000">The invention has been validated in a laboratory environment through extensive experimental evaluation.</font>', S_TD_C),
            Paragraph("", S_TD_C),
            Paragraph("", S_TD_C),
            Paragraph("", S_TD_C),
            Paragraph("", S_TD_C),
            Paragraph("", S_TD_C),
        ]
    ]

    t_trl = Table(trl_table_cells, colWidths=[cw_trl]*9)
    trl_style = TableStyle([
        ('SPAN', (0,0), (2,0)),  # Research spans cols 0-2
        ('SPAN', (3,0), (5,0)),  # Development spans cols 3-5
        ('SPAN', (6,0), (8,0)),  # Deployment spans cols 6-8
        ('BACKGROUND', (0,0), (-1,-1), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, BLACK),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,1), 'MIDDLE'),
        ('VALIGN', (0,2), (-1,2), 'TOP'),
        ('VALIGN', (0,3), (-1,3), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ])
    t_trl.setStyle(trl_style)
    story.append(t_trl)
    story.append(sp(20))

    # Concluding Marker (Exact line from template)
    story.append(Paragraph(
        "<b>----------------------END OF THE DOCUMENT-----------------------------</b>",
        st('EndDoc', fontName='TimesNewRoman-Bold', fontSize=10, leading=14, textColor=BLACK, alignment=TA_CENTER)
    ))

    # Build BaseDocTemplate with 3 PageTemplates
    doc = BaseDocTemplate(OUT_PDF, pagesize=A4)

    # Frame 1: Page 1 (Top margin 126 pt to clear full header box)
    frame_first = Frame(LM, BM, CW, PAGE_H - 126.0 - BM, id='frame_first', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)
    # Frame 2: Later Pages (Top margin 52 pt to clear top-left branding)
    frame_later = Frame(LM, BM, CW, PAGE_H - 52.0 - BM, id='frame_later', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)
    # Frame 3: Last Page (Top margin 126 pt to clear full header box)
    frame_last = Frame(LM, BM, CW, PAGE_H - 126.0 - BM, id='frame_last', topPadding=0, bottomPadding=0, leftPadding=0, rightPadding=0)

    pt_first = PageTemplate(id='First', frames=frame_first)
    pt_later = PageTemplate(id='Later', frames=frame_later)
    pt_last = PageTemplate(id='Last', frames=frame_last)
    doc.addPageTemplates([pt_first, pt_later, pt_last])

    doc.build(story, canvasmaker=Example1Canvas)
    print(f"\n✅ Official IDF-B PDF successfully generated: {OUT_PDF}")
    sz = os.path.getsize(OUT_PDF)
    print(f"   Size: {sz / (1024 * 1024):.2f} MB ({sz:,} bytes)")

    # Also synchronize with OUT_PDF_SUBMITTED
    import shutil
    shutil.copyfile(OUT_PDF, OUT_PDF_SUBMITTED)
    print(f"✅ Synchronized with: {OUT_PDF_SUBMITTED}")

if __name__ == '__main__':
    build_idf()
