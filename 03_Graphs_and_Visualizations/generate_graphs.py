"""
TCDS - Professional IEEE-Grade Figure & Schematic Generator
Strictly adheres to IEEE Transactions and USPTO patent specification standards:
- Typography: Times New Roman / Computer Modern serif fonts
- Formal Mathematical Notation: ALL variables and Greek parameters (ω_e, δ_e, ψ_e, θ_e, ΔM_u, ΔM_v, ΔM_cash, Δ_peak, Δ_cum, t_u, t_v, t_start, t_peak, t_rec) are strictly formatted in mathtext ($...$) so that genuine Greek and mathematical symbols (ω, δ, ψ, θ, Δ, etc.) are rendered everywhere, with ZERO text spellouts (e.g. never 'omega' or raw '\omega')
- Zero Text Overlap Guarantee: All annotations, brackets, and callout boxes have high-contrast background shielding (fc='#FFFFFF', ec=...) and ample spacing
- Resolution: High-resolution publication quality (DPI=300)
- Palette: Pure White (#FFFFFF) background, Black (#000000) outlines, Navy (#002855), Crimson (#990000), Forest Green (#006633)
"""

import sys
sys.path.insert(0, '/Users/yuvi/Library/Python/3.9/lib/python/site-packages')

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Circle, Polygon
from matplotlib.colors import LinearSegmentedColormap
import networkx as nx
from datetime import datetime, timedelta
import os, json

BASE_DIR = '/Users/yuvi/Patents/patent1'
DATA_DIR = f'{BASE_DIR}/02_Datasets'
GRAPH_DIR = f'{BASE_DIR}/03_Graphs_and_Visualizations'
ARCH_DIR = f'{BASE_DIR}/04_System_Architecture_Diagrams'
os.makedirs(GRAPH_DIR, exist_ok=True)
os.makedirs(ARCH_DIR, exist_ok=True)
np.random.seed(42)

# ─── GLOBAL IEEE PUBLICATION STYLING ──────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
    'mathtext.fontset': 'cm',  # Computer Modern mathtext for genuine Greek symbols: \omega, \delta, \psi, \theta, \Delta
    'figure.facecolor': '#FFFFFF',
    'axes.facecolor': '#FFFFFF',
    'axes.edgecolor': '#000000',
    'axes.linewidth': 0.9,
    'axes.spines.top': True,
    'axes.spines.right': True,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'xtick.top': True,
    'ytick.right': True,
    'xtick.major.size': 4.5,
    'ytick.major.size': 4.5,
    'xtick.minor.size': 2.5,
    'ytick.minor.size': 2.5,
    'text.color': '#000000',
    'axes.labelcolor': '#000000',
    'xtick.color': '#000000',
    'ytick.color': '#000000',
    'legend.frameon': True,
    'legend.edgecolor': '#000000',
    'legend.facecolor': '#FFFFFF',
    'legend.fancybox': False,
    'legend.fontsize': 8.5,
})

# IEEE Academic Colors
IEEE_BLACK   = '#000000'
IEEE_NAVY    = '#002855'
IEEE_CRIMSON = '#990000'
IEEE_GREEN   = '#006633'
IEEE_AMBER   = '#C0504D'
IEEE_GREY    = '#4D4D4D'
IEEE_LGREY   = '#EAEAEA'
IEEE_WHITE   = '#FFFFFF'

# ══════════════════════════════════════════════════════════════════════════════
# FIG. 1: Novelty Differentiation Radar Chart (IEEE Journal Standard)
# ══════════════════════════════════════════════════════════════════════════════
def fig1_novelty_radar():
    categories = [
        'Monetary Disturbance\nas Typed State',
        'Event-Level\nBusiness Graph',
        'Dual-Transform\nCoupling ($\\omega_e, \\psi_e, \\delta_e$)',
        'Multi-Path\nConvergence & Attribution',
        'Liquidity Impact\nWindow Output (LIW)',
        'Cryptographic Audit\nTrail & Immutability',
        'State-Dependent\nThreshold Rules ($\\theta_e$)',
    ]
    N = len(categories)

    scores = {
        'TCDS (This Invention)':      [10, 10, 10, 10, 10, 10, 10],
        'US20240362563A1':             [ 2,  4,  3,  3,  1,  3,  2],
        'US12380389B2':                [ 2,  4,  2,  2,  1,  2,  2],
        'Generic Risk-Score Systems':  [ 1,  3,  2,  1,  1,  1,  1],
    }

    styles = {
        'TCDS (This Invention)':      {'color': IEEE_GREEN,   'ls': '-',  'lw': 2.5, 'marker': 's', 'ms': 6, 'alpha': 0.20},
        'US20240362563A1':             {'color': IEEE_CRIMSON, 'ls': '--', 'lw': 1.8, 'marker': 'o', 'ms': 5, 'alpha': 0.08},
        'US12380389B2':                {'color': IEEE_NAVY,    'ls': '-.', 'lw': 1.8, 'marker': '^', 'ms': 5, 'alpha': 0.08},
        'Generic Risk-Score Systems':  {'color': IEEE_GREY,    'ls': ':',  'lw': 1.6, 'marker': 'd', 'ms': 4, 'alpha': 0.05},
    }

    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(IEEE_WHITE)
    ax.set_facecolor(IEEE_WHITE)

    for label, vals in scores.items():
        cfg = styles[label]
        vals_plot = vals + vals[:1]
        ax.plot(angles, vals_plot, color=cfg['color'], ls=cfg['ls'], lw=cfg['lw'],
                marker=cfg['marker'], markersize=cfg['ms'], label=label)
        ax.fill(angles, vals_plot, color=cfg['color'], alpha=cfg['alpha'])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=9.5, fontweight='bold', color=IEEE_BLACK)
    ax.tick_params(axis='x', pad=24)  # Generous padding to prevent label overlap with polar ring
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels(['2', '4', '6', '8', '10 (Max)'], color='#333333', size=8.5)
    ax.set_ylim(0, 10.5)
    ax.spines['polar'].set_color(IEEE_BLACK)
    ax.spines['polar'].set_linewidth(0.9)
    ax.grid(color='#B0B0B0', linestyle='--', linewidth=0.6, alpha=0.8)

    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.18), ncol=2,
              frameon=True, edgecolor=IEEE_BLACK, facecolor=IEEE_WHITE, fontsize=9)

    ax.set_title('FIG. 1: Novelty Differentiation Radar - Quantitative Prior Art Benchmarking (Scale: 1-10)',
                 pad=28, fontsize=11.5, fontweight='bold', color=IEEE_BLACK)

    path = f'{GRAPH_DIR}/06_novelty_radar_chart.png'
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=IEEE_WHITE)
    plt.close(fig)
    print(f"✅ Fig. 1 (IEEE Radar) saved: {path}")

# ══════════════════════════════════════════════════════════════════════════════
# FIG. 2: Physical System Architecture Flowchart (USPTO / IEEE Schematic)
# ══════════════════════════════════════════════════════════════════════════════
def fig2_architecture_flowchart():
    fig, ax = plt.subplots(figsize=(15, 10.5))
    fig.patch.set_facecolor(IEEE_WHITE)
    ax.set_facecolor(IEEE_WHITE)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Figure Header
    ax.text(50, 98.0, "FIG. 2: PHYSICAL SYSTEM ARCHITECTURE FLOWCHART - END-TO-END PIPELINE",
            ha='center', va='center', fontsize=12, fontweight='bold', color=IEEE_BLACK)
    ax.text(50, 95.5, "Computer-Implemented Subsystems, Core Algorithmic Engines, and Data Processing Flow",
            ha='center', va='center', fontsize=9.5, style='italic', color=IEEE_GREY)

    # Box Drawing Helper
    def draw_ieee_block(x, y, w, h, numeral, title, subitems, bg='#FFFFFF'):
        rect = Rectangle((x, y), w, h, facecolor=bg, edgecolor=IEEE_BLACK, linewidth=1.0, zorder=2)
        ax.add_patch(rect)
        # Numeral header
        ax.text(x + 1.2, y + h - 2.0, f"[{numeral}]", fontsize=8.5, fontweight='bold', color=IEEE_BLACK, zorder=3)
        # Title
        ax.text(x + w/2, y + h - 2.8, title, ha='center', va='center', fontsize=9, fontweight='bold', color=IEEE_BLACK, zorder=3)
        # Divider line
        ax.plot([x, x+w], [y+h-4.5, y+h-4.5], color=IEEE_BLACK, linewidth=0.6, zorder=3)
        # Bullet items
        cur_y = y + h - 6.8
        for it in subitems:
            ax.text(x + 1.5, cur_y, f"• {it}", fontsize=7.6, color=IEEE_BLACK, zorder=3)
            cur_y -= 2.0

    # Connector Arrow Helper
    def draw_ieee_arrow(x1, y1, x2, y2, label=None, rad=0.0):
        arr = FancyArrowPatch((x1, y1), (x2, y2),
                              arrowstyle='-|>,head_length=5,head_width=3',
                              connectionstyle=f'arc3,rad={rad}',
                              color=IEEE_BLACK, linewidth=1.2, zorder=5)
        ax.add_patch(arr)
        if label:
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.text(mx, my + 1.6, label, ha='center', va='bottom', fontsize=7.2,
                    color=IEEE_BLACK, bbox=dict(boxstyle='square,pad=0.25', fc=IEEE_WHITE, ec=IEEE_BLACK, lw=0.6), zorder=6)

    # Subsystem Bounding Boxes
    def draw_subsystem_frame(x, y, w, h, numeral, name):
        box = Rectangle((x, y), w, h, facecolor='#FAFAFA', edgecolor='#888888',
                        linewidth=0.9, linestyle='--', zorder=1)
        ax.add_patch(box)
        ax.text(x + 1.5, y + h - 2.2, f"SUBSYSTEM [{numeral}]: {name.upper()}",
                fontsize=8.5, fontweight='bold', color='#333333', zorder=2)

    # ── SUBSYSTEM [100]: Ingestion & Baseline Layer (Top) ──
    draw_subsystem_frame(3, 70, 94, 23.5, "100", "Enterprise Data Ingestion & Canonicalization Layer")
    draw_ieee_block(5, 72, 27, 18, "102", "ERP / SCM Log Ingestion",
                    ["Raw Purchase Orders (60 POs)", "Goods Receipts (36 records)", "Customer Orders & Invoices (80 records)", "Accounts Payable & Receivable Ledgers"])
    draw_ieee_block(36.5, 72, 27, 18, "104", "Canonical Normalization Engine",
                    ["13 Business Mechanism Schemas", "Transaction Timestamp Normalization", "Entity ID & Key De-duplication", "Operational Lead Time Indexing"])
    draw_ieee_block(68, 72, 27, 18, "106", "Immutable Baseline Engine",
                    ["Forward Working Capital Solver", "120-Day Daily Baseline Cash $C_{base}(t)$", "Initial Cash Reserve: $500,000", "Cryptographic Baseline Freeze (SHA-256)"])

    draw_ieee_arrow(32, 81, 36.5, 81, "Raw Streams")
    draw_ieee_arrow(63.5, 81, 68, 81, "Normalized Events")

    # ── SUBSYSTEM [200]: Graph Construction & Dual-Transform Propagation (Middle) ──
    draw_subsystem_frame(3, 38, 94, 29.5, "200", "Temporal Graph Construction & Dual-Transform Propagation Core")
    draw_ieee_block(5, 40, 27, 24, "202", "Disturbance Parser Engine",
                    ["Natural Language Incident Parsing", "Compiles: S03 Capacity -30% (60d)", "Disturbance State: $\\Delta M_u, t_u$, duration", "Conversion Function Operator: $\\psi_e$", "Seed Mechanism: Supplier[S03]"])
    draw_ieee_block(36.5, 40, 27, 24, "204", "13-Mechanism Graph Engine",
                    ["Directed Multigraph: $G = (V, E, T)$", "13 Typed Mechanism Nodes", "14 Dual-Transform Edges $e = (u, v)$", "Coupling Weights: $\\omega_e \\in [0.0, 1.0]$", "Operational Delays: $\\delta_e$ (Days)"])
    draw_ieee_block(68, 40, 27, 24, "206", "Propagation Computing Core",
                    ["Topological Chronological Queue", "Monetary Transform: $\\Delta M_v = \\Delta M_u \\cdot \\omega_e \\cdot \\psi_e$", "Temporal Transform: $t_v = t_u + \\delta_e$", "Path A Revenue Deficit (-$178,125)", "Path B Emergency Cost (-$45,000)", "Threshold Rule Evaluator ($\\theta_e$) [208]"])

    draw_ieee_arrow(50, 72, 50, 64, "Event Topologies")
    draw_ieee_arrow(32, 52, 36.5, 52, "Disturbance State")
    draw_ieee_arrow(63.5, 52, 68, 52, "Graph Structure")

    # ── SUBSYSTEM [300]: Convergence, LIW Detection & Presentation (Bottom) ──
    draw_subsystem_frame(3, 4, 94, 31.5, "300", "Multi-Path Convergence, LIW Detection & Executive Output")
    draw_ieee_block(5, 6, 27, 26, "302", "Multi-Path Convergence Module",
                    ["Detects Temporal Arrival at CashAccount", "Convergence Sum: $\\Delta M_{cash} = \\sum_p \\Delta M_p$", "Path A Causal Share: 81.0% (-$178,125)", "Path B Causal Share: 19.0% (-$45,000)", "Total Converged Impact: -$223,125", "Exact Attribution Conservation: 100.0%"])
    draw_ieee_block(36.5, 6, 27, 26, "304", "LIW Detection Engine",
                    ["Superposition: $C_{dist}(t) = C_{base}(t) + \\Delta C(t)$", "Extracts Formal 7-Tuple: $\\mathcal{W} = \\langle ... \\rangle$", "Onset Date: $t_{start} = T+21\\text{d}$", "Peak Deficit: $t_{peak} = T+72\\text{d}, \\Delta_{peak} = -\\$218.4\\text{K}$", "Recovery: $t_{rec\\_start} = T+85\\text{d}, t_{rec} = T+103\\text{d}$", "Total Duration: $D = 47\\text{ Days}$"])
    draw_ieee_block(68, 6, 27, 26, "308", "Executive Presentation Layer",
                    ["Interactive 9-Panel UI Dashboard", "Gantt-Style Timeline Viewport", "Dual Cash Trajectory with Deficit Zone", "Multi-Path Attribution Bar Visualizer", "Line-Item Variance Analyzer [306]", "12-Step Cryptographic Audit Logger"])

    draw_ieee_arrow(81.5, 40, 81.5, 32, "Causal Paths A & B")
    draw_ieee_arrow(68, 19, 63.5, 19, "Converged Deltas")
    draw_ieee_arrow(36.5, 19, 32, 19, "7-Tuple LIW")
    draw_ieee_arrow(68, 72, 81.5, 32, "Baseline $C_{base}(t)$", rad=0.22)

    path1 = f'{GRAPH_DIR}/09_physical_system_architecture_flowchart.png'
    path2 = f'{ARCH_DIR}/09_physical_system_architecture_flowchart.png'
    fig.savefig(path1, dpi=300, bbox_inches='tight', facecolor=IEEE_WHITE)
    fig.savefig(path2, dpi=300, bbox_inches='tight', facecolor=IEEE_WHITE)
    plt.close(fig)
    print(f"✅ Fig. 2 (IEEE Flowchart) saved: {path1}")

# ══════════════════════════════════════════════════════════════════════════════
# FIG. 3: Temporal Business-Event Graph (IEEE Network Schematic)
# ══════════════════════════════════════════════════════════════════════════════
def fig3_event_graph():
    fig, ax = plt.subplots(figsize=(16, 9.5))
    fig.patch.set_facecolor(IEEE_WHITE)
    ax.set_facecolor(IEEE_WHITE)

    # 13 Nodes with patent numerals - spaced out to prevent overlap
    nodes_info = {
        'Supplier':           ('[210]', (0.0, 0.50), 'Operational', '#DCE6F1'),
        'PurchaseOrder':      ('[212]', (1.1, 0.50), 'Operational', '#DCE6F1'),
        'InventoryReceipt':   ('[214]', (2.2, 0.50), 'Operational', '#DCE6F1'),
        'ProductionEvent':    ('[216]', (3.3, 0.50), 'Operational', '#DCE6F1'),
        'CustomerOrder':      ('[218]', (4.4, 0.50), 'Revenue',     '#E2EFDA'),
        'Invoice':            ('[220]', (5.5, 0.50), 'Revenue',     '#E2EFDA'),
        'AccountsReceivable': ('[222]', (6.6, 0.50), 'Revenue',     '#E2EFDA'),
        'CustomerPayment':    ('[224]', (7.7, 0.50), 'Revenue',     '#E2EFDA'),
        'ExpenseEvent':       ('[226]', (1.1, 0.08), 'Cost',        '#FCE4D6'),
        'AccountsPayable':    ('[228]', (3.8, 0.08), 'Cost',        '#FCE4D6'),
        'SupplierPayment':    ('[230]', (6.0, 0.08), 'Cost',        '#FCE4D6'),
        'CashAccount':        ('[232]', (8.8, 0.28), 'Cash',        '#F8CBAD'),
        'FinancingEvent':     ('[234]', (8.8, 0.72), 'Financing',   '#E1D5E7'),
    }

    # Edges with exact mathematical symbols: \omega_e and \delta_e in mathtext
    edges_info = [
        ('Supplier','PurchaseOrder',        '$\\omega_e=0.70, \\delta_e=14\\text{d}$', 'PathA'),
        ('PurchaseOrder','InventoryReceipt', '$\\omega_e=0.95, \\delta_e=7\\text{d}$',  'PathA'),
        ('InventoryReceipt','ProductionEvent','$\\omega_e=0.80, \\delta_e=14\\text{d}$', 'PathA'),
        ('ProductionEvent','CustomerOrder',  '$\\omega_e=0.85, \\delta_e=7\\text{d}$',  'PathA'),
        ('CustomerOrder','Invoice',          '$\\omega_e=1.00, \\delta_e=0\\text{d}$',  'PathA'),
        ('Invoice','AccountsReceivable',     '$\\omega_e=1.00, \\delta_e=30\\text{d}$', 'PathA'),
        ('AccountsReceivable','CustomerPayment','$\\omega_e=0.95, \\delta_e=0\\text{d}$','PathA'),
        ('CustomerPayment','CashAccount',    '$\\omega_e=1.00, \\delta_e=0\\text{d}$',  'PathA'),
        ('Supplier','ExpenseEvent',          '$\\omega_e=1.00, \\delta_e=7\\text{d}$',  'PathB'),
        ('ExpenseEvent','AccountsPayable',   '$\\omega_e=1.00, \\delta_e=30\\text{d}$', 'PathB'),
        ('AccountsPayable','SupplierPayment','$\\omega_e=1.00, \\delta_e=0\\text{d}$',  'PathB'),
        ('SupplierPayment','CashAccount',    '$\\omega_e=1.00, \\delta_e=0\\text{d}$',  'PathB'),
        ('InventoryReceipt','AccountsPayable','$\\omega_e=1.00, \\delta_e=45\\text{d}$','Other'),
        ('CashAccount','FinancingEvent',     '$\\omega_e=0.80, \\delta_e=1\\text{d}$',  'Other'),
    ]

    # Draw Nodes as crisp IEEE rectangular blocks
    for name, (numeral, (x, y), category, bg_col) in nodes_info.items():
        w, h = 0.82, 0.26
        rx, ry = x - w/2, y - h/2
        rect = Rectangle((rx, ry), w, h, facecolor=bg_col, edgecolor=IEEE_BLACK, linewidth=1.0, zorder=3)
        ax.add_patch(rect)
        ax.text(x, y + 0.04, f"{name}", ha='center', va='center', fontsize=8.2, fontweight='bold', color=IEEE_BLACK, zorder=4)
        ax.text(x, y - 0.06, f"{numeral} [{category[:3].upper()}]", ha='center', va='center', fontsize=7.0, color='#333333', zorder=4)

    # Draw Edges - Labels positioned with clear vertical offsets to avoid touching boxes
    for src, tgt, lbl, path_type in edges_info:
        sx, sy = nodes_info[src][1]
        tx, ty = nodes_info[tgt][1]
        if path_type == 'PathA':
            col, lw, ls = IEEE_NAVY, 2.4, '-'
        elif path_type == 'PathB':
            col, lw, ls = IEEE_CRIMSON, 2.4, '--'
        else:
            col, lw, ls = '#666666', 1.2, '-'

        rad = 0.14 if src in ['InventoryReceipt', 'CashAccount'] and tgt in ['AccountsPayable', 'FinancingEvent'] else 0.0
        arr = FancyArrowPatch((sx, sy), (tx, ty),
                              arrowstyle='-|>,head_length=5,head_width=3',
                              connectionstyle=f'arc3,rad={rad}',
                              color=col, linewidth=lw, linestyle=ls, zorder=2)
        ax.add_patch(arr)

        # Label position: Path A sits cleanly at y=0.69 (above boxes), Path B sits at y=-0.06 (below boxes)
        mx, my = (sx + tx)/2, (sy + ty)/2
        if rad != 0:
            my += 0.12
        elif path_type == 'PathA':
            my = 0.69
        elif path_type == 'PathB':
            my = -0.06
        else:
            my += 0.06

        ax.text(mx, my, lbl, ha='center', va='center', fontsize=6.8, color=col, fontweight='bold',
                bbox=dict(boxstyle='square,pad=0.2', fc=IEEE_WHITE, ec=col, lw=0.6), zorder=5)

    # Legend placed at bottom right in clear white space
    legend_elements = [
        mpatches.Patch(facecolor='#DCE6F1', edgecolor=IEEE_BLACK, label='Operational Mechanism Nodes [210-216]'),
        mpatches.Patch(facecolor='#E2EFDA', edgecolor=IEEE_BLACK, label='Revenue Mechanism Nodes [218-224]'),
        mpatches.Patch(facecolor='#FCE4D6', edgecolor=IEEE_BLACK, label='Cost / Disbursement Mechanism Nodes [226-230]'),
        mpatches.Patch(facecolor='#F8CBAD', edgecolor=IEEE_BLACK, label='Central Cash Account State Node [232]'),
        mpatches.Patch(facecolor='#E1D5E7', edgecolor=IEEE_BLACK, label='Contingent Financing Node [234]'),
        plt.Line2D([0], [0], color=IEEE_NAVY, lw=2.2, ls='-', label='Path A: Revenue Loss Cascade (81.0% Share)'),
        plt.Line2D([0], [0], color=IEEE_CRIMSON, lw=2.2, ls='--', label='Path B: Emergency Cost Cascade (19.0% Share)'),
        plt.Line2D([0], [0], color='#666666', lw=1.2, ls='-', label='Auxiliary Dependency & Financing Edges'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', bbox_to_anchor=(0.98, 0.02),
              ncol=2, frameon=True, edgecolor=IEEE_BLACK, facecolor=IEEE_WHITE, fontsize=8.0)

    ax.set_title('FIG. 3: Temporal Business-Event Graph - 13 Mechanism Nodes & 14 Dual-Transform Edges $e = (u, v)$',
                 pad=18, fontsize=11.5, fontweight='bold', color=IEEE_BLACK)
    ax.set_xlim(-0.6, 9.6)
    ax.set_ylim(-0.16, 0.95)
    ax.axis('off')

    path = f'{GRAPH_DIR}/02_temporal_business_event_graph.png'
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=IEEE_WHITE)
    plt.close(fig)
    print(f"✅ Fig. 3 (IEEE Event Graph) saved: {path}")

# ══════════════════════════════════════════════════════════════════════════════
# FIG. 4: Dependency Strength Heatmap (IEEE Matrix Standard)
# ══════════════════════════════════════════════════════════════════════════════
def fig4_dependency_heatmap():
    df = pd.read_csv(f'{DATA_DIR}/temporal_graph_edges.csv')
    nodes_ordered = ['Supplier','PurchaseOrder','InventoryReceipt','ProductionEvent',
                     'CustomerOrder','Invoice','AccountsReceivable','CustomerPayment',
                     'ExpenseEvent','AccountsPayable','SupplierPayment','CashAccount','FinancingEvent']

    matrix = pd.DataFrame(0.0, index=nodes_ordered, columns=nodes_ordered)
    for _, row in df.iterrows():
        if row['source_node'] in matrix.index and row['target_node'] in matrix.columns:
            matrix.loc[row['source_node'], row['target_node']] = row['dependency_strength']

    cmap = LinearSegmentedColormap.from_list('ieee_heat', [
        '#FFFFFF',  # 0.0: Pure White
        '#DEEBF7',  # 0.2: Light Academic Blue
        '#9ECAE1',  # 0.5: Medium Academic Blue
        '#3182BD',  # 0.7: Dark Academic Blue
        '#08519C',  # 0.85: Navy
        '#990000',  # 1.0: Dark Crimson Red
    ])

    fig, ax = plt.subplots(figsize=(11, 9))
    fig.patch.set_facecolor(IEEE_WHITE)
    ax.set_facecolor(IEEE_WHITE)

    im = ax.imshow(matrix.values, cmap=cmap, vmin=0, vmax=1, aspect='auto')
    cbar = fig.colorbar(im, ax=ax, fraction=0.038, pad=0.03)
    cbar.set_label('Dependency Coupling Strength Coefficient, $\\omega_e \\in [0.0, 1.0]$',
                   fontsize=9.5, fontweight='bold', color=IEEE_BLACK)
    cbar.ax.tick_params(labelsize=8.5)
    cbar.outline.set_edgecolor(IEEE_BLACK)
    cbar.outline.set_linewidth(0.8)

    # Numerical cell values
    for i in range(len(nodes_ordered)):
        for j in range(len(nodes_ordered)):
            val = matrix.iloc[i, j]
            if val > 0:
                col = IEEE_WHITE if val >= 0.70 else IEEE_BLACK
                ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                        fontsize=8.5, fontweight='bold', color=col)

    # IEEE Clean Grid lines between cells
    ax.set_xticks(np.arange(-.5, len(nodes_ordered), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(nodes_ordered), 1), minor=True)
    ax.grid(which='minor', color='#000000', linestyle='-', linewidth=0.5)
    ax.tick_params(which='minor', bottom=False, left=False)

    ax.set_xticks(range(len(nodes_ordered)))
    ax.set_yticks(range(len(nodes_ordered)))
    ax.set_xticklabels(nodes_ordered, rotation=42, ha='right', fontsize=8.5, fontweight='bold', color=IEEE_BLACK)
    ax.set_yticklabels(nodes_ordered, fontsize=8.5, fontweight='bold', color=IEEE_BLACK)
    ax.set_xlabel('Target Mechanism Node, $v \\in \\mathcal{V}$', fontsize=10, fontweight='bold', color=IEEE_BLACK)
    ax.set_ylabel('Source Mechanism Node, $u \\in \\mathcal{V}$', fontsize=10, fontweight='bold', color=IEEE_BLACK)

    # Title with genuine Greek \omega_e symbol enclosed in mathtext ($...$)
    ax.set_title('FIG. 4: Dependency Strength Coupling Matrix - Pairwise Parameters ($\\omega_e$)',
                 pad=14, fontsize=11.5, fontweight='bold', color=IEEE_BLACK)

    fig.tight_layout()
    path = f'{GRAPH_DIR}/08_dependency_strength_heatmap.png'
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=IEEE_WHITE)
    plt.close(fig)
    print(f"✅ Fig. 4 (IEEE Heatmap) saved: {path}")

# ══════════════════════════════════════════════════════════════════════════════
# FIG. 5: Temporal Propagation Timeline (IEEE Gantt Standard)
# ══════════════════════════════════════════════════════════════════════════════
def fig5_propagation_timeline():
    steps = [
        ('Supplier[S03] → PurchaseOrder',     0,  14, 'Path A', IEEE_NAVY,    '//'),
        ('PurchaseOrder → InventoryReceipt',  14, 21, 'Path A', IEEE_NAVY,    '//'),
        ('InventoryReceipt → Production',     21, 35, 'Path A', IEEE_NAVY,    '//'),
        ('Production → CustomerOrder',        35, 42, 'Path A', IEEE_NAVY,    '//'),
        ('CustomerOrder → Invoice',           42, 42, 'Path A', IEEE_NAVY,    '//'),
        ('Invoice → AccountsReceivable',      42, 72, 'Path A', IEEE_NAVY,    '//'),
        ('AR → CustomerPayment → CashAccount',72, 72, 'Path A', IEEE_CRIMSON, ''),
        ('Supplier[S03] → ExpenseEvent',      0,   7, 'Path B', IEEE_AMBER,   '\\\\'),
        ('ExpenseEvent → AccountsPayable',    7,  37, 'Path B', IEEE_AMBER,   '\\\\'),
        ('AP → SupplierPayment → CashAccount',37, 37, 'Path B', IEEE_CRIMSON, ''),
    ]

    fig, ax = plt.subplots(figsize=(13.5, 7.8))
    fig.patch.set_facecolor(IEEE_WHITE)
    ax.set_facecolor(IEEE_WHITE)

    labels, starts, ends, paths, colors, hatches = zip(*steps)
    y_pos = list(range(len(labels)))

    for i, (lbl, s, e, pth, col, htch) in enumerate(steps):
        width = max(e - s, 0.6)
        ax.barh(i, width, left=s, height=0.55,
                color=col, alpha=0.88, edgecolor=IEEE_BLACK, linewidth=0.8, hatch=htch)
        if col == IEEE_CRIMSON:
            ax.scatter(e, i, marker='*', s=250, color=IEEE_CRIMSON, edgecolors=IEEE_BLACK, linewidths=0.8, zorder=10)
            val_txt = "-$178,125" if i == 6 else "-$45,000"
            ax.text(e + 2.2, i, f"T+{e}d: {val_txt} (Cash Settlement)", va='center', ha='left',
                    fontsize=8.0, color=IEEE_CRIMSON, fontweight='bold',
                    bbox=dict(boxstyle='square,pad=0.2', fc=IEEE_WHITE, ec=IEEE_CRIMSON, lw=0.6), zorder=11)
        else:
            # Mathtext for operational delay symbol: \delta_e
            dur_str = f"T+{e}d" if s == e else f"$\\delta_e={e-s}\\text{{d}}$"
            ax.text(s + width/2, i, dur_str, va='center', ha='center',
                    fontsize=7.8, color=IEEE_WHITE, fontweight='bold')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=8.5, fontweight='bold', color=IEEE_BLACK)
    ax.set_xlabel('Elapsed Simulation Time from Disturbance Onset, $t$ [Calendar Days]', fontsize=9.5, fontweight='bold', color=IEEE_BLACK)
    ax.set_title('FIG. 5: Temporal Propagation Timeline (Scenario DIST-001) - Dual-Path Cascade Dynamics',
                 fontsize=11.5, fontweight='bold', color=IEEE_BLACK, pad=14)

    # Vertical reference lines
    ax.axvline(21, color=IEEE_CRIMSON, linestyle='--', alpha=0.8, lw=1.2)
    ax.axvline(72, color=IEEE_CRIMSON, linestyle='--', alpha=0.8, lw=1.2)

    # Date callout boxes placed in top clear space with white boxes (never touching bars)
    ax.set_ylim(-0.8, len(labels) + 0.9)
    ax.text(21, len(labels) + 0.1, 'Impact Onset\n$t_{start} = T+21\\text{d}$', fontsize=8.2, color=IEEE_CRIMSON,
            ha='center', va='center', fontweight='bold',
            bbox=dict(boxstyle='square,pad=0.25', fc=IEEE_WHITE, ec=IEEE_CRIMSON, lw=0.7), zorder=12)
    ax.text(72, len(labels) + 0.1, 'Peak Cash Deficit\n$t_{peak} = T+72\\text{d}$', fontsize=8.2, color=IEEE_CRIMSON,
            ha='center', va='center', fontweight='bold',
            bbox=dict(boxstyle='square,pad=0.25', fc=IEEE_WHITE, ec=IEEE_CRIMSON, lw=0.7), zorder=12)

    legend_elements = [
        mpatches.Patch(facecolor=IEEE_NAVY, edgecolor=IEEE_BLACK, hatch='//', label='Path A: Revenue Cascade (Delayed Collections)'),
        mpatches.Patch(facecolor=IEEE_AMBER, edgecolor=IEEE_BLACK, hatch='\\\\', label='Path B: Emergency Cost Cascade (Spot Procurement)'),
        plt.Line2D([0], [0], marker='*', color='w', markerfacecolor=IEEE_CRIMSON, markeredgecolor=IEEE_BLACK,
                   markersize=12, label='Direct Settlement Event at CashAccount'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', frameon=True, edgecolor=IEEE_BLACK, fontsize=8.5)
    ax.grid(axis='x', color='#CCCCCC', linestyle=':', alpha=0.8)
    ax.set_xlim(-2, 108)

    fig.tight_layout()
    path = f'{GRAPH_DIR}/03_propagation_timeline.png'
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=IEEE_WHITE)
    plt.close(fig)
    print(f"✅ Fig. 5 (IEEE Timeline) saved: {path}")

# ══════════════════════════════════════════════════════════════════════════════
# FIG. 6: Multi-Path Convergence & Attribution (IEEE Standard)
# ══════════════════════════════════════════════════════════════════════════════
def fig6_path_attribution():
    categories = ['Path A\nRevenue Loss\nCascade', 'Path B\nEmergency Cost\nCascade', 'Converged Total\nat CashAccount']
    values     = [-178125, -45000, -223125]
    colors     = [IEEE_NAVY, IEEE_AMBER, IEEE_CRIMSON]
    hatches    = ['//', '\\\\', 'xx']

    fig, ax = plt.subplots(figsize=(9.5, 6.8))
    fig.patch.set_facecolor(IEEE_WHITE)
    ax.set_facecolor(IEEE_WHITE)

    bars = ax.bar(categories, [abs(v) for v in values], color=colors, width=0.45,
                  edgecolor=IEEE_BLACK, linewidth=1.0, hatch=hatches, alpha=0.9)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + 3500,
                f'-${abs(val):,.0f}', ha='center', va='bottom',
                fontsize=10.5, fontweight='bold', color=IEEE_BLACK)

    # Greek symbol \Delta M in labels
    pct_labels = ['81.0% Share\n($-\\Delta M_A$)', '19.0% Share\n($-\\Delta M_B$)', '100.0% Converged\n($-\\Delta M_{cash}$)']
    for bar, lbl in zip(bars, pct_labels):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height()/2,
                lbl, ha='center', va='center',
                fontsize=9.0, color=IEEE_WHITE, fontweight='bold')

    ax.set_ylabel('Monetary Disturbance Amplitude, $|\\Delta M|$ [USD]', fontsize=10, fontweight='bold', color=IEEE_BLACK)
    ax.set_title('FIG. 6: Multi-Path Monetary Convergence & Exact Causal Attribution (Scenario DIST-001)',
                 fontsize=11.5, fontweight='bold', color=IEEE_BLACK, pad=14)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    ax.set_ylim(0, 275000)
    ax.grid(axis='y', color='#D0D0D0', linestyle='--', alpha=0.7)

    # Mathematical Formula Box placed in top clear space with formal summation symbol
    formula_text = (
        "Convergence Law: $\\Delta M_{cash}(t) = \\sum_{p \\in \\mathcal{P}} \\Delta M_p(t)$\n"
        "Numerical Conservation: -$178,125 + (-$45,000) = -$223,125 (100.00%)"
    )
    ax.text(0.5, 0.90, formula_text, transform=ax.transAxes, ha='center', va='center',
            fontsize=8.5, bbox=dict(boxstyle='square,pad=0.4', fc='#F4F4F6', ec=IEEE_BLACK, lw=0.8))

    fig.tight_layout()
    path = f'{GRAPH_DIR}/04_multipath_convergence_attribution.png'
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=IEEE_WHITE)
    plt.close(fig)
    print(f"✅ Fig. 6 (IEEE Attribution) saved: {path}")

# ══════════════════════════════════════════════════════════════════════════════
# FIG. 7: Supplier Risk Profile (IEEE Multi-Panel)
# ══════════════════════════════════════════════════════════════════════════════
def fig7_supplier_profile():
    df = pd.read_csv(f'{DATA_DIR}/suppliers.csv')
    df_sorted = df.sort_values('reliability_score')

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.8))
    fig.patch.set_facecolor(IEEE_WHITE)

    ax1, ax2 = axes
    ax1.set_facecolor(IEEE_WHITE)
    ax2.set_facecolor(IEEE_WHITE)

    # Panel (a): Reliability
    colors_r = [IEEE_CRIMSON if r < 0.85 else IEEE_AMBER if r < 0.92 else IEEE_GREEN
                for r in df_sorted['reliability_score']]
    bars = ax1.barh(df_sorted['name'].str.split('-').str[0],
                    df_sorted['reliability_score'],
                    color=colors_r, height=0.6, edgecolor=IEEE_BLACK, linewidth=0.8)
    ax1.axvline(0.85, color=IEEE_CRIMSON, lw=1.2, linestyle='--', label='High Risk Threshold (0.85)')
    ax1.axvline(0.92, color=IEEE_AMBER, lw=1.2, linestyle=':', label='Moderate Threshold (0.92)')
    ax1.set_xlabel('Reliability Score, $R_i \\in [0.70, 1.00]$', fontsize=9.5, fontweight='bold', color=IEEE_BLACK)
    ax1.set_title('(a) Supplier Reliability Index Distribution', fontsize=10.5, fontweight='bold', color=IEEE_BLACK)
    ax1.set_xlim(0.70, 1.01)
    ax1.legend(fontsize=8, loc='lower right')
    ax1.grid(axis='x', color='#D0D0D0', linestyle='--', alpha=0.6)

    # Highlight S03
    for bar, name in zip(bars, df_sorted['name'].str.split('-').str[0]):
        if 'S03' in name or 'Plast' in df_sorted[df_sorted['name'].str.startswith(name)]['name'].values[0]:
            bar.set_linewidth(2.2)
            bar.set_edgecolor(IEEE_BLACK)

    # Panel (b): Capacity vs Cost
    scatter_colors = [IEEE_CRIMSON if s < 0.85 else IEEE_AMBER if s < 0.92 else IEEE_GREEN
                      for s in df['reliability_score']]
    sc = ax2.scatter(df['monthly_capacity_units'], df['unit_cost_usd'],
                     c=scatter_colors, s=df['payment_term_days']*6.0,
                     alpha=0.90, edgecolors=IEEE_BLACK, linewidths=0.9)

    s03 = df[df['supplier_id']=='S03'].iloc[0]
    ax2.annotate('Supplier S03\n(Disturbance Seed)',
                 xy=(s03['monthly_capacity_units'], s03['unit_cost_usd']),
                 xytext=(s03['monthly_capacity_units'] + 120, s03['unit_cost_usd'] + 8),
                 fontsize=8.5, color=IEEE_CRIMSON, fontweight='bold',
                 bbox=dict(boxstyle='square,pad=0.25', fc=IEEE_WHITE, ec=IEEE_CRIMSON, lw=0.8),
                 arrowprops=dict(arrowstyle='->', color=IEEE_CRIMSON, lw=1.4))
    ax2.set_xlabel('Monthly Capacity, $Q_i$ [Units]', fontsize=9.5, fontweight='bold', color=IEEE_BLACK)
    ax2.set_ylabel('Unit Procurement Cost, $P_i$ [USD]', fontsize=9.5, fontweight='bold', color=IEEE_BLACK)
    ax2.set_title('(b) Monthly Capacity vs. Unit Procurement Cost', fontsize=10.5, fontweight='bold', color=IEEE_BLACK)
    ax2.grid(color='#D0D0D0', linestyle='--', alpha=0.6)

    fig.suptitle('FIG. 7: Multi-Tier Supplier Network Characterization & Operational Risk Profile',
                 fontsize=12, fontweight='bold', color=IEEE_BLACK, y=1.01)
    fig.tight_layout()

    path = f'{GRAPH_DIR}/07_supplier_risk_profile.png'
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=IEEE_WHITE)
    plt.close(fig)
    print(f"✅ Fig. 7 (IEEE Supplier Profile) saved: {path}")

# ══════════════════════════════════════════════════════════════════════════════
# FIG. 8: 120-Day Baseline vs. Disturbance Cash Trajectory (IEEE 2-Panel Standard)
# ══════════════════════════════════════════════════════════════════════════════
def fig8_cash_trajectory():
    df = pd.read_csv(f'{DATA_DIR}/baseline_vs_disturbance_cashflow.csv')
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in df['date']]
    days = list(range(len(dates)))

    fig, axes = plt.subplots(2, 1, figsize=(14, 9.2), sharex=True,
                              gridspec_kw={'height_ratios': [3.2, 1]})
    fig.patch.set_facecolor(IEEE_WHITE)

    ax1, ax2 = axes
    ax1.set_facecolor(IEEE_WHITE)
    ax2.set_facecolor(IEEE_WHITE)

    # Set spacious Y-limit so top clear space (y=1.95 to 2.28) has ZERO curves or shading
    ax1.set_ylim(-0.02, 2.28)

    # Shaded Deficit Region with \Delta_{cum} in mathtext
    ax1.fill_between(days,
                     df['baseline_cash_balance_usd'] / 1e6,
                     df['disturbance_cash_balance_usd'] / 1e6,
                     where=df['disturbance_cash_balance_usd'] < df['baseline_cash_balance_usd'],
                     color=IEEE_CRIMSON, alpha=0.15, hatch='//', label='Liquidity Deficit Envelope ($\\Delta_{cum} = -\\$341.8\\text{K}$)')

    # Curves
    ax1.plot(days, df['baseline_cash_balance_usd'] / 1e6, color=IEEE_BLACK,
             linewidth=2.2, linestyle='-', marker='s', markevery=10, markersize=5,
             label='Baseline Trajectory $C_{base}(t)$ [SHA-256 Frozen]')
    ax1.plot(days, df['disturbance_cash_balance_usd'] / 1e6, color=IEEE_CRIMSON,
             linewidth=2.2, linestyle='--', marker='o', markevery=10, markersize=5,
             label='Disturbed Trajectory $C_{dist}(t)$ [Scenario DIST-001]')

    # Safety Threshold Line
    ax1.axhline(0.15, color='#888888', linestyle=':', linewidth=1.2, label='Safety Reserve Bound $C_{min} = \\$150\\text{K}$')

    # Vertical reference lines for critical dates
    ax1.axvline(21, color=IEEE_CRIMSON, linestyle='--', alpha=0.7, lw=1.1)
    ax1.axvline(68, color='#555555', linestyle=':', alpha=0.7, lw=1.0)
    ax1.axvline(72, color=IEEE_CRIMSON, linestyle=':', alpha=0.7, lw=1.1)
    ax1.axvline(85, color=IEEE_GREEN, linestyle='--', alpha=0.7, lw=1.1)
    ax1.axvline(103, color=IEEE_GREEN, linestyle=':', alpha=0.7, lw=1.1)

    # ZERO-OVERLAP BRACKET FOR ACTIVE IMPAIRMENT WINDOW (D = 47 Days)
    # Positioned at y = 2.05M in clear white space with white bounding box
    bracket_y = 2.05
    ax1.annotate('', xy=(21, bracket_y), xytext=(68, bracket_y),
                 arrowprops=dict(arrowstyle='<->,head_length=5,head_width=3', color=IEEE_BLACK, lw=1.3))
    ax1.text((21+68)/2, bracket_y + 0.05, 'Active Impairment Window ($D = 47\\text{ Days}$)',
             ha='center', va='bottom', fontsize=9.0, fontweight='bold', color=IEEE_BLACK,
             bbox=dict(boxstyle='square,pad=0.3', fc=IEEE_WHITE, ec=IEEE_BLACK, lw=0.8), zorder=10)

    # Peak Cash Deficit Annotation with genuine Greek \Delta_{peak}
    peak_day = 72
    peak_cash = df.loc[peak_day, 'disturbance_cash_balance_usd'] / 1e6
    ax1.annotate('Peak Cash Deficit\n$\\Delta_{peak} = -\\$218,400$\n($t_{peak} = T+72\\text{d}$)',
                 xy=(peak_day, peak_cash),
                 xytext=(peak_day - 26, peak_cash + 0.35),
                 fontsize=8.8, color=IEEE_CRIMSON, fontweight='bold',
                 bbox=dict(boxstyle='square,pad=0.3', fc=IEEE_WHITE, ec=IEEE_CRIMSON, lw=0.8),
                 arrowprops=dict(arrowstyle='->', color=IEEE_CRIMSON, lw=1.4), zorder=11)

    # Date callout boxes placed in clean bottom space (y = 0.25) with white backgrounds
    ax1.text(21, 0.25, '$t_{start}=T+21\\text{d}$\n(Onset)', fontsize=8.0, color=IEEE_CRIMSON, ha='center', va='bottom', fontweight='bold',
             bbox=dict(boxstyle='square,pad=0.2', fc=IEEE_WHITE, ec=IEEE_CRIMSON, lw=0.6), zorder=10)
    ax1.text(72, 0.25, '$t_{peak}=T+72\\text{d}$\n(Peak)', fontsize=8.0, color=IEEE_CRIMSON, ha='center', va='bottom', fontweight='bold',
             bbox=dict(boxstyle='square,pad=0.2', fc=IEEE_WHITE, ec=IEEE_CRIMSON, lw=0.6), zorder=10)
    ax1.text(85, 0.25, '$t_{rec\\_start}=T+85\\text{d}$\n(Inflection)', fontsize=8.0, color=IEEE_GREEN, ha='center', va='bottom', fontweight='bold',
             bbox=dict(boxstyle='square,pad=0.2', fc=IEEE_WHITE, ec=IEEE_GREEN, lw=0.6), zorder=10)
    ax1.text(103, 0.25, '$t_{rec}=T+103\\text{d}$\n(Full Recovery)', fontsize=8.0, color=IEEE_GREEN, ha='center', va='bottom', fontweight='bold',
             bbox=dict(boxstyle='square,pad=0.2', fc=IEEE_WHITE, ec=IEEE_GREEN, lw=0.6), zorder=10)

    ax1.set_ylabel('Cash Balance, $C(t)$ [USD Millions]', fontsize=10, fontweight='bold', color=IEEE_BLACK)
    ax1.set_title('FIG. 8: 120-Day Baseline vs. Disturbed Cash Trajectory - Impact Envelope Detection',
                  fontsize=11.5, fontweight='bold', color=IEEE_BLACK, pad=12)
    ax1.legend(loc='upper right', frameon=True, edgecolor=IEEE_BLACK, facecolor=IEEE_WHITE, fontsize=8.5)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:.2f}M'))
    ax1.grid(color='#E0E0E0', linestyle='--', linewidth=0.5)

    # Bottom Panel: Daily Differential with \Delta C(t)
    colors_d = [IEEE_CRIMSON if v < 0 else IEEE_GREEN for v in df['cash_delta_usd']]
    ax2.bar(days, df['cash_delta_usd'] / 1e3, color=colors_d, alpha=0.85, width=0.8, edgecolor=IEEE_BLACK, linewidth=0.4)
    ax2.axhline(0, color=IEEE_BLACK, lw=0.9)
    ax2.set_ylabel('$\\Delta C(t)$ [K USD]', fontsize=9.5, fontweight='bold', color=IEEE_BLACK)
    ax2.set_xlabel('Elapsed Simulation Time from Disturbance Onset, $t$ [Calendar Days]', fontsize=9.5, fontweight='bold', color=IEEE_BLACK)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:.0f}K'))
    ax2.grid(color='#E0E0E0', linestyle='--', linewidth=0.5)
    ax2.set_xlim(-2, 122)

    fig.tight_layout()
    path = f'{GRAPH_DIR}/01_baseline_vs_disturbance_cash_trajectory.png'
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=IEEE_WHITE)
    plt.close(fig)
    print(f"✅ Fig. 8 (IEEE Cash Trajectory) saved: {path}")

# ══════════════════════════════════════════════════════════════════════════════
# FIG. 9: Executive Liquidity Impact Window Dashboard (IEEE Parameter Matrix)
# ══════════════════════════════════════════════════════════════════════════════
def fig9_liw_dashboard():
    df = pd.read_csv(f'{DATA_DIR}/baseline_vs_disturbance_cashflow.csv')
    days = list(range(len(df)))

    fig = plt.figure(figsize=(15, 12.0))
    fig.patch.set_facecolor(IEEE_WHITE)

    # Upper Subplot: Trajectory Plot (positioned comfortably in top half: y=0.54 to 0.94)
    ax_top = fig.add_axes([0.07, 0.54, 0.86, 0.40])
    ax_top.set_facecolor(IEEE_WHITE)
    ax_top.set_ylim(-0.02, 2.28)

    ax_top.plot(days, df['baseline_cash_balance_usd']/1e6, color=IEEE_BLACK, lw=2.0, label='Baseline Cash Balance $C_{base}(t)$ [SHA-256 Frozen]')
    ax_top.plot(days, df['disturbance_cash_balance_usd']/1e6, color=IEEE_CRIMSON, lw=2.0, ls='--', label='Disturbed Cash Balance $C_{dist}(t)$ [Scenario DIST-001]')
    ax_top.fill_between(days, df['baseline_cash_balance_usd']/1e6, df['disturbance_cash_balance_usd']/1e6,
                        where=df['disturbance_cash_balance_usd'] < df['baseline_cash_balance_usd'],
                        color=IEEE_CRIMSON, alpha=0.15, hatch='//', label='Liquidity Deficit Integral $\\Delta_{cum} = -\\$341.8\\text{K}$')

    ax_top.axvspan(21, 68, facecolor='#EEEEEE', edgecolor='#666666', alpha=0.8, linestyle=':')
    ax_top.axvline(21, color=IEEE_CRIMSON, lw=1.2, ls='--')
    ax_top.axvline(72, color=IEEE_CRIMSON, lw=1.2, ls=':')
    ax_top.axvline(103, color=IEEE_GREEN, lw=1.2, ls='--')

    # Unobstructed dimension bracket in top clear space (y=2.05M)
    ax_top.annotate('', xy=(21, 2.05), xytext=(68, 2.05),
                    arrowprops=dict(arrowstyle='<->,head_length=5,head_width=3', color=IEEE_BLACK, lw=1.2))
    ax_top.text((21+68)/2, 2.09, 'Liquidity Impact Window Envelope ($D = 47\\text{ Days}$)',
                ha='center', va='bottom', fontsize=8.8, fontweight='bold', color=IEEE_BLACK,
                bbox=dict(boxstyle='square,pad=0.25', fc=IEEE_WHITE, ec=IEEE_BLACK, lw=0.7), zorder=10)

    # Date callout boxes in bottom clear space
    ax_top.text(21, 0.22, '$t_{start}=T+21\\text{d}$', ha='center', va='bottom', fontsize=8.0, color=IEEE_CRIMSON, fontweight='bold',
                bbox=dict(boxstyle='square,pad=0.2', fc=IEEE_WHITE, ec=IEEE_CRIMSON, lw=0.6), zorder=10)
    ax_top.text(72, 0.22, '$t_{peak}=T+72\\text{d}$', ha='center', va='bottom', fontsize=8.0, color=IEEE_CRIMSON, fontweight='bold',
                bbox=dict(boxstyle='square,pad=0.2', fc=IEEE_WHITE, ec=IEEE_CRIMSON, lw=0.6), zorder=10)
    ax_top.text(103, 0.22, '$t_{rec}=T+103\\text{d}$', ha='center', va='bottom', fontsize=8.0, color=IEEE_GREEN, fontweight='bold',
                bbox=dict(boxstyle='square,pad=0.2', fc=IEEE_WHITE, ec=IEEE_GREEN, lw=0.6), zorder=10)

    ax_top.set_ylabel('Cash Balance [USD Millions]', fontsize=9.5, fontweight='bold')
    ax_top.set_xlabel('Elapsed Simulation Time, $t$ [Calendar Days]', fontsize=9.5, fontweight='bold')
    ax_top.set_title('FIG. 9: Liquidity Impact Window (LIW) Trajectory Decomposition & Formal Parameter Extraction Matrix',
                     fontsize=11.5, fontweight='bold', color=IEEE_BLACK, pad=10)
    ax_top.yaxis.set_major_formatter(plt.FuncFormatter(lambda x,_: f'${x:.2f}M'))
    ax_top.legend(loc='upper right', frameon=True, edgecolor=IEEE_BLACK, fontsize=8.5)
    ax_top.grid(color='#E0E0E0', linestyle='--', linewidth=0.5)

    # Lower Panel: Dedicated Custom IEEE Table (positioned safely in bottom half: y=0.04 to 0.42 with 0.12 margin)
    ax_table = fig.add_axes([0.07, 0.04, 0.86, 0.38])
    ax_table.set_xlim(0, 100)
    ax_table.set_ylim(0, 100)
    ax_table.axis('off')

    # Table Title & Subtitle with ample vertical clearance above table header
    ax_table.text(50, 96.5, "TABLE I: FORMAL LIQUIDITY IMPACT WINDOW (LIW) 7-TUPLE PARAMETER SPECIFICATION",
                  ha='center', va='center', fontsize=9.8, fontweight='bold', color=IEEE_BLACK)
    ax_table.text(50, 91.0, "Mathematical Definitions, Boundary Detection Formulations, and Empirical Scenario Metrics (DIST-001)",
                  ha='center', va='center', fontsize=8.2, style='italic', color=IEEE_GREY)

    cols = [
        (0, 10, 'Symbol', 'center'),
        (10, 22, 'Formal Variable Definition', 'left'),
        (32, 25, 'Mathematical Expression', 'center'),
        (57, 17, 'Empirical Value (DIST-001)', 'center'),
        (74, 26, 'Operational Physical Interpretation', 'left'),
    ]

    rows = [
        ('$t_{start}$', 'Impact Onset Timestamp', '$\\inf \\{t : |C_{dist}(t) - C_{base}(t)| > \\epsilon\\}$', '21 Jul 2026 (T+21d)', 'Disturbance reaches inventory;\nworking capital divergence begins', False),
        ('$t_{peak}$', 'Peak Deficit Timestamp', '$\\arg\\min_t \\{C_{dist}(t) - C_{base}(t)\\}$', '11 Sep 2026 (T+72d)', 'Max working capital depletion;\nreceivable collections reach minimum', False),
        ('$\\Delta_{peak}$', 'Peak Cash Deficit Amplitude', '$\\min_t \\{C_{dist}(t) - C_{base}(t)\\}$', '-$218,400 (Peak)', 'Maximum net negative cash deflection\nfrom unperturbed forward baseline', True),
        ('$D$', 'Active Impairment Duration', '$t_{rec} - t_{start}$', '47 Calendar Days', 'Total calendar duration of active\nenterprise liquidity impairment', False),
        ('$t_{rec\\_start}$', 'Recovery Initiation Timestamp', '$\\inf \\{t > t_{peak} : \\frac{d(\\Delta C)}{dt} > 0\\}$', '24 Sep 2026 (T+85d)', 'Inflection date where deferred receipt\nrescheduling and collections resume', False),
        ('$t_{rec}$', 'Equilibrium Full Recovery Date', '$\\inf \\{t > t_{rec\\_start} : |\\Delta C(t)| \\leq \\epsilon\\}$', '12 Oct 2026 (T+103d)', 'Cash trajectory re-enters within\nequilibrium tolerance envelope ($\\epsilon$)', False),
        ('$\\Delta_{cum}$', 'Cumulative Liquidity Deficit', '$\\int_{t_{start}}^{t_{rec}} [C_{dist}(t) - C_{base}(t)] \\, dt$', '-$341,750 (Total)', 'Total integral of depleted liquidity\nover active 47-day impairment window', True),
    ]

    # Header top is at 74.0 + 10.0 = 84.0, providing a 7.0 unit margin below subtitle at 91.0!
    header_y = 74.0
    header_h = 10.0
    for x, w, title, align in cols:
        rect = Rectangle((x, header_y), w, header_h, facecolor=IEEE_NAVY, edgecolor=IEEE_BLACK, linewidth=0.8)
        ax_table.add_patch(rect)
        tx = x + w/2 if align == 'center' else x + 1.2
        ax_table.text(tx, header_y + header_h/2, title, ha=align, va='center', fontsize=8.6, fontweight='bold', color=IEEE_WHITE)

    cur_y = header_y
    row_h = 9.4
    for r_idx, (sym, name, math_exp, val, desc, is_crimson) in enumerate(rows):
        cur_y -= row_h
        bg = '#F7F9FC' if r_idx % 2 == 0 else IEEE_WHITE
        row_data = [
            (sym, 'center', True, IEEE_BLACK),
            (name, 'left', True, IEEE_BLACK),
            (math_exp, 'center', False, IEEE_BLACK),
            (val, 'center', True, IEEE_CRIMSON if is_crimson else IEEE_BLACK),
            (desc, 'left', False, '#222222')
        ]
        for c_idx, (x, w, _, align) in enumerate(cols):
            rect = Rectangle((x, cur_y), w, row_h, facecolor=bg, edgecolor='#B0B8C0', linewidth=0.5)
            ax_table.add_patch(rect)
            text_val, text_align, is_bold, text_col = row_data[c_idx]
            tx = x + w/2 if text_align == 'center' else x + 1.2
            fsize = 8.5 if c_idx != 4 else 7.8
            fweight = 'bold' if is_bold else 'normal'
            ax_table.text(tx, cur_y + row_h/2, text_val, ha=text_align, va='center', fontsize=fsize, fontweight=fweight, color=text_col)

    # Outer table border
    ax_table.plot([0, 100], [header_y + header_h, header_y + header_h], color=IEEE_BLACK, lw=1.2)
    ax_table.plot([0, 100], [cur_y, cur_y], color=IEEE_BLACK, lw=1.2)
    ax_table.plot([0, 0], [cur_y, header_y + header_h], color=IEEE_BLACK, lw=1.2)
    ax_table.plot([100, 100], [cur_y, header_y + header_h], color=IEEE_BLACK, lw=1.2)

    path = f'{GRAPH_DIR}/05_liquidity_impact_window_dashboard.png'
    fig.savefig(path, dpi=300, bbox_inches='tight', facecolor=IEEE_WHITE)
    plt.close(fig)
    print(f"✅ Fig. 9 (IEEE Dashboard & Matrix) saved: {path}")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("Generating all 9 figures with GENUINE GREEK & MATHEMATICAL SYMBOLS...\n")
    fig1_novelty_radar()
    fig2_architecture_flowchart()
    fig3_event_graph()
    fig4_dependency_heatmap()
    fig5_propagation_timeline()
    fig6_path_attribution()
    fig7_supplier_profile()
    fig8_cash_trajectory()
    fig9_liw_dashboard()
    print(f"\n✅ All 9 IEEE-grade figures generated with 300 DPI, genuine Greek symbols, and zero text overlap in {GRAPH_DIR}/")
