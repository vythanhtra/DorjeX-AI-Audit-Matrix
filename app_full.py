
import streamlit as st
import os
import json
from modules.load_data import load_all_sheets
from modules.audit_logic import run_audit
from modules.ethics_reflex import ethics_reflex
from modules.visualization import display_dashboard
from report_generator import generate_pdf_report

# Load giao diện tùy chỉnh
with open("style/custom_dark_responsive.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load ngôn ngữ
lang = st.sidebar.selectbox("🌐 Language", ["en", "vi", "fr", "es"])
with open("translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)
T = translations.get(lang, translations["en"])

st.title(T["AI Audit Matrix v2.0"])

# Tải dữ liệu
try:
    data = load_all_sheets("data/ISO_42001_Audit_Matrix.xlsx")
    df_main = data["ISO42001_Mapping"]
    kpi_df = data["KPI_Tracker"]
    risk_df = data["Risk_Register"]
    nc_df = data["NC_CAPA_Log"]

    # Chạy kiểm toán
    audit_results = run_audit(df_main, risk_df, nc_df)
    display_dashboard(df_main, audit_results, kpi_df, risk_df)

    # Phân tích đạo đức
    reflex = ethics_reflex(kpi_df)
    st.subheader(T["Ethical Assessment (DorjeX Reflex)"])
    st.write(T["EIA Assessment: {assessment}"].format(assessment=reflex["eia_assessment"]))
    st.write(T["KPI Assessments: {assessments}"].format(assessments=", ".join(reflex["kpi_assessments"])))
    st.write(T["Similarity Score: {score:.2f}"].format(score=reflex["similarity_score"]))

    # Xuất báo cáo
    if st.button("📄 Xuất báo cáo PDF"):
        pdf_path = generate_pdf_report(df_main, audit_results, reflex)
        with open(pdf_path, "rb") as f:
            st.download_button("Tải xuống báo cáo", f, file_name="audit_report.pdf")

except Exception as e:
    st.error(T["Error loading data: {error}"].format(error=str(e)))
