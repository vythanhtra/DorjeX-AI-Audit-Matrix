from datetime import datetime
import pandas as pd

def check_evidence(row):
    if row.get("Self-Assessment") == "Yes" and not row.get("Evidence Doc ID"):
        return "🚫 Thiếu bằng chứng"
    return ""

def check_due_date(row):
    try:
        due_date = pd.to_datetime(row.get("Due Date"), errors='coerce').date()
        if due_date and due_date < datetime.today().date():
            return "⏰ Quá hạn"
    except:
        return "📅 Lỗi định dạng ngày"
    return ""

def check_mapping(row):
    missing = []
    standards = ["GDPR Article", "ISO 27701 Clause", "US AI BoR Principle", "NIST SP800-53 Control"]
    for std in standards:
        if not row.get(std):
            missing.append(f"🔍 Thiếu Mapping {std}")
    return ", ".join(missing)

def check_risk(row, risk_df):
    doc_id = row.get("Evidence Doc ID", "")
    related_risks = risk_df[risk_df["Mitigation / Control"].astype(str).str.contains(str(doc_id), na=False)]
    alerts = []
    for _, r in related_risks.iterrows():
        if r.get("Risk Score", 0) > 10 and r.get("Risk Status", "") == "Open":
            alerts.append(f"🔥 Rủi ro cao: {r.get('Risk ID')}")
    return ", ".join(alerts)

def check_nc_capa(row, nc_df):
    doc_id = row.get("Evidence Doc ID", "")
    relevant = nc_df[nc_df["Corrective Action"].astype(str).str.contains(str(doc_id), na=False)]
    if any(relevant["Verified (Y/N)"] == "N"):
        return "⚠️ Chưa khắc phục phi chuẩn"
    return ""

def run_audit_diagnostics(df, risk_df, nc_df):
    results = []
    for _, row in df.iterrows():
        checks = [
            check_evidence(row),
            check_due_date(row),
            check_mapping(row),
            check_risk(row, risk_df),
            check_nc_capa(row, nc_df)
        ]
        alerts = [c for c in checks if c]
        score = 100 - len(alerts) * 20  # 5 yếu tố chính, mỗi cái trừ 20%
        results.append({
            "Control ID": row.get("Control ID", ""),
            "Title": row.get("Title", ""),
            "Audit Score": max(score, 0),
            "Alerts": ", ".join(alerts) if alerts else "✅ OK"
        })
    return pd.DataFrame(results)