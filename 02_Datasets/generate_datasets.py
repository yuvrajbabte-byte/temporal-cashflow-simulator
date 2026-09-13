"""
Temporal Cash-Flow Disturbance Simulator (TCDS)
Synthetic Dataset Generator — IDF Support Data
"""
import sys
sys.path.insert(0, '/Users/yuvi/Library/Python/3.9/lib/python/site-packages')

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta

BASE_DIR = '/Users/yuvi/Patents/patent1/02_Datasets'
base_date = datetime(2026, 7, 1)
np.random.seed(42)

# ── 1. SUPPLIERS ──────────────────────────────────────────────────────────────
names = [
    'S01-NexCore Materials','S02-AlphaSteel Ltd','S03-PrimePlast Co',
    'S04-TechMetal Inc','S05-GreenFiber AG','S06-OmegaAlloys',
    'S07-BlueLine Rubber','S08-PrecisionGlass','S09-SwiftFoam',
    'S10-AlloyTech','S11-NanoParts','S12-EcoTex'
]
suppliers = []
for i, name in enumerate(names):
    suppliers.append({
        'supplier_id': f'S{str(i+1).zfill(2)}',
        'name': name,
        'monthly_capacity_units': int(np.random.randint(800, 3000)),
        'reliability_score': round(float(np.random.uniform(0.75, 0.98)), 2),
        'payment_term_days': int(np.random.choice([30, 45, 60])),
        'unit_cost_usd': round(float(np.random.uniform(12, 85)), 2),
        'lead_time_days': int(np.random.randint(7, 21)),
        'country': np.random.choice(['India', 'Germany', 'China', 'USA', 'Vietnam'])
    })
df_sup = pd.DataFrame(suppliers)
df_sup.to_csv(f'{BASE_DIR}/suppliers.csv', index=False)
print(f"Created suppliers.csv ({len(df_sup)} rows)")

# ── 2. PURCHASE ORDERS ────────────────────────────────────────────────────────
orders = []
for i in range(60):
    sid = np.random.choice(df_sup['supplier_id'])
    sup = df_sup[df_sup['supplier_id'] == sid].iloc[0]
    qty = int(np.random.randint(100, 500))
    order_date = base_date + timedelta(days=int(np.random.randint(0, 90)))
    receipt_date = order_date + timedelta(days=int(sup['lead_time_days']))
    total = round(qty * float(sup['unit_cost_usd']), 2)
    orders.append({
        'po_id': f'PO-{str(i+1).zfill(3)}',
        'supplier_id': sid,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'expected_receipt_date': receipt_date.strftime('%Y-%m-%d'),
        'quantity_units': qty,
        'unit_cost_usd': float(sup['unit_cost_usd']),
        'total_value_usd': total,
        'status': np.random.choice(['Open', 'Received', 'Partial'], p=[0.4, 0.5, 0.1])
    })
df_po = pd.DataFrame(orders)
df_po.to_csv(f'{BASE_DIR}/purchase_orders.csv', index=False)
print(f"Created purchase_orders.csv ({len(df_po)} rows)")

# ── 3. INVENTORY RECEIPTS ─────────────────────────────────────────────────────
receipts = []
for idx, row in df_po[df_po['status'].isin(['Received', 'Partial'])].iterrows():
    factor = 1.0 if row['status'] == 'Received' else float(np.random.uniform(0.5, 0.85))
    qty_rec = int(row['quantity_units'] * factor)
    sup_row = df_sup[df_sup['supplier_id'] == row['supplier_id']].iloc[0]
    ap_due = (datetime.strptime(row['expected_receipt_date'], '%Y-%m-%d')
              + timedelta(days=int(sup_row['payment_term_days']))).strftime('%Y-%m-%d')
    receipts.append({
        'receipt_id': f'IR-{str(idx+1).zfill(3)}',
        'po_id': row['po_id'],
        'supplier_id': row['supplier_id'],
        'receipt_date': row['expected_receipt_date'],
        'quantity_received': qty_rec,
        'unit_cost_usd': float(row['unit_cost_usd']),
        'total_value_usd': round(qty_rec * float(row['unit_cost_usd']), 2),
        'ap_created': True,
        'ap_due_date': ap_due
    })
df_ir = pd.DataFrame(receipts)
df_ir.to_csv(f'{BASE_DIR}/inventory_receipts.csv', index=False)
print(f"Created inventory_receipts.csv ({len(df_ir)} rows)")

# ── 4. CUSTOMER ORDERS ────────────────────────────────────────────────────────
custs = [f'CUST-{str(i+1).zfill(2)}' for i in range(25)]
corders = []
for i in range(80):
    cid = np.random.choice(custs)
    qty = int(np.random.randint(20, 300))
    price = round(float(np.random.uniform(80, 250)), 2)
    odate = base_date + timedelta(days=int(np.random.randint(0, 90)))
    fdate = odate + timedelta(days=int(np.random.randint(5, 20)))
    pterm = int(np.random.choice([30, 45, 60]))
    corders.append({
        'co_id': f'CO-{str(i+1).zfill(3)}',
        'customer_id': cid,
        'order_date': odate.strftime('%Y-%m-%d'),
        'quantity_units': qty,
        'unit_price_usd': price,
        'total_value_usd': round(qty * price, 2),
        'fulfillment_date': fdate.strftime('%Y-%m-%d'),
        'payment_term_days': pterm,
        'invoice_due_date': (fdate + timedelta(days=pterm)).strftime('%Y-%m-%d')
    })
df_co = pd.DataFrame(corders)
df_co.to_csv(f'{BASE_DIR}/customer_orders.csv', index=False)
print(f"Created customer_orders.csv ({len(df_co)} rows)")

# ── 5. BASELINE + DISTURBANCE CASH FLOW ──────────────────────────────────────
baseline_cash = 500000.0
disturbance_cash = 500000.0
rows = []
for day in range(120):
    d = base_date + timedelta(days=day)
    inflow_b = round(float(np.random.uniform(0, 120000)) if day % 7 in [1, 3, 5]
                     else float(np.random.uniform(0, 30000)), 2)
    outflow_b = round(float(np.random.uniform(0, 95000)) if day % 7 in [2, 4]
                      else float(np.random.uniform(0, 25000)), 2)
    baseline_cash += inflow_b - outflow_b

    inflow_d = inflow_b
    outflow_d = outflow_b
    # Path A: lost revenue from day 49
    if day >= 49:
        revenue_loss = round(inflow_d * 0.25 * min(1.0, (day - 49) / 30.0), 2)
        inflow_d = max(0.0, inflow_d - revenue_loss)
    # Path B: emergency procurement cost days 7–67
    if 7 <= day <= 67:
        emergency_cost = round(float(np.random.uniform(500, 2500)), 2)
        outflow_d += emergency_cost
    disturbance_cash += inflow_d - outflow_d

    rows.append({
        'date': d.strftime('%Y-%m-%d'),
        'day_index': day,
        'baseline_inflow_usd': inflow_b,
        'baseline_outflow_usd': outflow_b,
        'baseline_net_usd': round(inflow_b - outflow_b, 2),
        'baseline_cash_balance_usd': round(baseline_cash, 2),
        'disturbance_inflow_usd': round(inflow_d, 2),
        'disturbance_outflow_usd': round(outflow_d, 2),
        'disturbance_net_usd': round(inflow_d - outflow_d, 2),
        'disturbance_cash_balance_usd': round(disturbance_cash, 2),
        'cash_delta_usd': round(disturbance_cash - baseline_cash, 2),
    })
df_cf = pd.DataFrame(rows)
df_cf.to_csv(f'{BASE_DIR}/baseline_vs_disturbance_cashflow.csv', index=False)
print(f"Created baseline_vs_disturbance_cashflow.csv ({len(df_cf)} rows)")

# ── 6. PROPAGATION AUDIT LOG ──────────────────────────────────────────────────
log_rows = [
    ('DIST-001','Supplier[S03]','PurchaseOrder[PO-012]','capacity_reduction','volume_reduction',-0.30,-0.30,0.70,14,'linear',0.95,0),
    ('DIST-001','PurchaseOrder[PO-012]','InventoryReceipt[IR-009]','volume_reduction','units_received',-0.30,-0.285,0.95,7,'linear',0.92,14),
    ('DIST-001','InventoryReceipt[IR-009]','ProductionEvent[PROD-004]','units_received','output_reduction',-0.285,-0.228,0.80,14,'threshold',0.88,21),
    ('DIST-001','ProductionEvent[PROD-004]','CustomerOrder[CO-031]','output_reduction','fulfillment_shortfall',-0.228,-0.194,0.85,7,'linear',0.85,35),
    ('DIST-001','CustomerOrder[CO-031]','Invoice[INV-031]','fulfillment_shortfall','invoice_value_usd',-0.194,-187500.0,1.0,0,'monetary_conversion',0.90,42),
    ('DIST-001','Invoice[INV-031]','AccountsReceivable[AR-031]','invoice_value_usd','ar_reduction_usd',-187500.0,-187500.0,1.0,30,'linear',0.95,42),
    ('DIST-001','AccountsReceivable[AR-031]','CustomerPayment[CP-031]','ar_reduction_usd','cash_inflow_reduction_usd',-187500.0,-178125.0,0.95,0,'collection_probability',0.90,72),
    ('DIST-001','CustomerPayment[CP-031]','CashAccount','cash_inflow_reduction_usd','cash_balance_reduction_usd',-178125.0,-178125.0,1.0,0,'direct',1.00,72),
    ('DIST-001','Supplier[S03]','ExpenseEvent[EMRG-001]','capacity_reduction','emergency_cost_usd',-0.30,45000.0,1.0,7,'nonlinear',0.80,0),
    ('DIST-001','ExpenseEvent[EMRG-001]','AccountsPayable[AP-EMRG]','emergency_cost_usd','payable_increase_usd',45000.0,45000.0,1.0,30,'linear',0.95,7),
    ('DIST-001','AccountsPayable[AP-EMRG]','SupplierPayment[SP-EMRG]','payable_due_usd','cash_outflow_usd',45000.0,45000.0,1.0,0,'direct',1.00,37),
    ('DIST-001','SupplierPayment[SP-EMRG]','CashAccount','cash_outflow_usd','cash_balance_reduction_usd',45000.0,-45000.0,1.0,0,'direct',1.00,37),
]
cols = ['disturbance_id','source_event','target_event','source_variable','target_variable',
        'source_delta','target_delta','dependency_strength','delay_days',
        'propagation_rule','confidence','scheduled_day_from_t0']
df_log = pd.DataFrame(log_rows, columns=cols)
df_log.to_csv(f'{BASE_DIR}/propagation_audit_log.csv', index=False)
print(f"Created propagation_audit_log.csv ({len(df_log)} rows)")

# ── 7. TEMPORAL GRAPH EDGES CONFIG ────────────────────────────────────────────
edges = [
    ('E001','Supplier','PurchaseOrder','triggers',0.70,14,'volume_fraction','linear',0.95),
    ('E002','PurchaseOrder','InventoryReceipt','creates',0.95,7,'direct','linear',0.92),
    ('E003','InventoryReceipt','ProductionEvent','enables',0.80,14,'production_yield','threshold',0.88),
    ('E004','ProductionEvent','CustomerOrder','fulfills',0.85,7,'fill_rate','linear',0.85),
    ('E005','CustomerOrder','Invoice','triggers',1.00,0,'order_value','linear',0.90),
    ('E006','Invoice','AccountsReceivable','creates',1.00,30,'direct','linear',0.95),
    ('E007','AccountsReceivable','CustomerPayment','settles',0.95,0,'collection_prob','stochastic',0.90),
    ('E008','CustomerPayment','CashAccount','credits',1.00,0,'direct','direct',1.00),
    ('E009','Supplier','ExpenseEvent','triggers_emergency',1.00,7,'emergency_cost','nonlinear',0.80),
    ('E010','ExpenseEvent','AccountsPayable','creates',1.00,30,'direct','linear',0.95),
    ('E011','AccountsPayable','SupplierPayment','settles',1.00,0,'direct','direct',1.00),
    ('E012','SupplierPayment','CashAccount','debits',1.00,0,'direct','direct',1.00),
    ('E013','InventoryReceipt','AccountsPayable','creates_ap',1.00,45,'direct','linear',1.00),
    ('E014','CashAccount','FinancingEvent','triggers_if_below_threshold',0.80,1,'credit_draw','threshold',0.85),
]
df_edges = pd.DataFrame(edges, columns=[
    'edge_id','source_node','target_node','relationship_type',
    'dependency_strength','expected_delay_days','monetary_conversion',
    'propagation_rule','confidence'])
df_edges.to_csv(f'{BASE_DIR}/temporal_graph_edges.csv', index=False)
print(f"Created temporal_graph_edges.csv ({len(df_edges)} rows)")

# ── 8. LIQUIDITY IMPACT WINDOW JSON ───────────────────────────────────────────
liw = {
    "disturbance_id": "DIST-001",
    "disturbance_label": "Supplier S03 (PrimePlast Co) capacity -30%",
    "scenario_created": "2026-09-03T11:30:00+05:30",
    "impact_start_date": "2026-07-22",
    "impact_peak_date": "2026-09-11",
    "peak_cash_deficit_usd": -218400,
    "impact_duration_days": 47,
    "recovery_start_date": "2026-09-24",
    "recovery_date": "2026-10-12",
    "cumulative_cash_delta_usd": -341750,
    "path_contributions": [
        {"path": "PathA_RevenueChain", "monetary_impact_usd": -178125, "percentage": 81},
        {"path": "PathB_EmergencyProcurement", "monetary_impact_usd": -45000, "percentage": 19}
    ],
    "top_contributing_paths": [
        "Supplier→PO→IR→Production→CustomerOrder→Invoice→AR→Payment→Cash (-81%)",
        "Supplier→EmergencyProcurement→AP→SupplierPayment→Cash (-19%)"
    ]
}
with open(f'{BASE_DIR}/liquidity_impact_window.json', 'w') as f:
    json.dump(liw, f, indent=2)
print("Created liquidity_impact_window.json")

print("\n✅ All 8 datasets generated successfully.")
for fname in sorted(os.listdir(BASE_DIR)):
    size = os.path.getsize(f'{BASE_DIR}/{fname}')
    print(f"   {fname:<50} {size:>8} bytes")
