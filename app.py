
import streamlit as st
import pandas as pd
from modules.load_data import load_all_sheets
from modules.audit_logic import audit_matrix_check
from modules.visualization import display_dashboard
from modules.ethics_reflex import ethics_reflex
import json
from streamlit_i18n import StreamlitI18n

# Load đa ngôn ngữ
with open("translations.json", "r", encoding="utf-8") as f:
    translations = json.load(f)
i18n = StreamlitI18n(translations)

# CSS tùy chỉnh
with open("style/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Tiêu đề
st.set_page_config(page_title="AI Audit Matrix v2.0", layout="wide")
st.title(i18n.t("AI Audit Matrix v2.0"))

# Đăng nhập (có thể bổ sung Streamlit Authenticator và dotenv nếu cần)
with st.sidebar:
    st.write(i18n.t("Please enter your username and password"))
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

if login_button:
    if username == "admin" and password == "admin":
        st.success(i18n.t("Welcome {name}").format(name=username))

        try:
            # Load dữ liệu
            data = load_all_sheets("data/ISO_42001_Audit_Matrix.xlsx")
            df = data["ISO42001_Mapping"]
            kpi_df = data["KPI_Tracker"]
            risk_df = data["Risk_Register"]
            nc_df = data["NC_CAPA_Log"]

            # Kiểm toán
            audit_results = audit_matrix_check(df)

            # Hiển thị bảng + biểu đồ
            display_dashboard(df, audit_results, kpi_df, risk_df)

            # Phân tích đạo đức
            st.subheader(i18n.t("Ethical Assessment (DorjeX Reflex)"))
            reflex = ethics_reflex(kpi_df)
            st.markdown(i18n.t("EIA Assessment: {assessment}").format(assessment=reflex["eia_assessment"]))
            st.markdown(i18n.t("KPI Assessments: {assessments}").format(assessments=", ".join(reflex["kpi_assessments"])))
            st.markdown(i18n.t("Similarity Score: {score:.2f}").format(score=reflex["similarity_score"]))

        except Exception as e:
            st.error(i18n.t("Error loading data: {error}").format(error=str(e)))
    else:
        st.error(i18n.t("Username/password is incorrect"))
