import streamlit as st
import json
import os
from modules.load_data import load_matrix, load_all_sheets
from modules.audit_logic import audit_matrix_check
from modules.visualization import display_dashboard
from modules.ethics_reflex import ethics_reflex
from dotenv import load_dotenv

# Tải biến môi trường từ .env
load_dotenv()

# Đọc ngôn ngữ
lang = st.sidebar.selectbox("Language", ["en", "vi", "fr", "es"])
with open("translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)
_ = translations.get(lang, {})

# Giao diện người dùng
st.set_page_config(page_title=_["AI Audit Matrix v2.0"], layout="wide")
st.markdown(f"<style>{open('style/custom.css').read()}</style>", unsafe_allow_html=True)

# Xác thực đơn giản
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if username != os.getenv("USERNAME") or password != os.getenv("PASSWORD"):
    st.warning(_["Username/password is incorrect"])
    st.stop()

st.title(_["AI Audit Matrix v2.0"])
st.write(_["Welcome {name}"].format(name=username))

# Tải dữ liệu
try:
    data = load_all_sheets("data/ISO_42001_Audit_Matrix.xlsx")
    df_main = data["ISO42001_Mapping"]
    kpi_df = data["KPI_Tracker"]
    risk_df = data["Risk_Register"]
    nc_df = data["NC_CAPA_Log"]
except Exception as e:
    st.error(_["Error loading data: {error}"].format(error=str(e)))
    st.stop()

# Chạy kiểm toán
audit_results = audit_matrix_check(df_main, risk_df, nc_df)
display_dashboard(df_main, audit_results, kpi_df, risk_df)

# Đánh giá đạo đức
st.subheader(_["Ethical Assessment (DorjeX Reflex)"])
ethics = ethics_reflex(kpi_df)
st.write(_["EIA Assessment: {assessment}"].format(assessment=ethics["eia_assessment"]))
st.write(_["KPI Assessments: {assessments}"].format(assessments=", ".join(ethics["kpi_assessments"])))
st.write(_["Similarity Score: {score:.2f}"].format(score=ethics["similarity_score"]))
