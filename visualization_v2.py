
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_i18n import StreamlitI18n

# Khởi tạo đa ngôn ngữ (giả định đã có i18n được khởi tạo bên app chính)
i18n = StreamlitI18n(languages=["en", "vi", "fr", "es"], translations_path="translations.json")

def display_dashboard(df, audit_results, kpi_df, risk_df):
    df["Audit Result"] = audit_results

    # Bảng kiểm toán
    st.subheader(i18n.t("🧾 Audit Table"))
    styled_df = df.style.applymap(
        lambda v: "background-color: #ffcccc" if "🚫" in str(v) or "🔥" in str(v)
        else "background-color: #fff2cc" if "⏰" in str(v) or "⚠️" in str(v)
        else ""
    )
    st.dataframe(styled_df)

    # Biểu đồ tình trạng tuân thủ
    st.subheader(i18n.t("📈 Overall Compliance Status"))
    pie_data = df["Audit Result"].value_counts().reset_index()
    pie_data.columns = [i18n.t("Status"), i18n.t("Count")]
    fig = px.pie(pie_data, names=i18n.t("Status"), values=i18n.t("Count"),
                 title=i18n.t("Audit Result Distribution"))
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap rủi ro
    st.subheader(i18n.t("🔥 Risk Heatmap"))
    heatmap_data = risk_df.groupby(["Risk Category", "Risk Score"]).size().reset_index(name="Count")
    fig_heatmap = px.density_heatmap(
        heatmap_data,
        x="Risk Category", y="Risk Score", z="Count",
        title=i18n.t("Risk by Category and Score"),
        nbinsx=10, nbinsy=10, color_continuous_scale="OrRd"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    # Xu hướng KPI
    st.subheader(i18n.t("📊 KPI Trends"))
    kpi_trend = kpi_df.melt(id_vars=["KPI ID", "Metric"], value_vars=["Mar-2025", "Apr-2025", "May-2025", "Jun-2025"],
                            var_name="Month", value_name="Actual")
    fig_trend = px.line(kpi_trend, x="Month", y="Actual", color="KPI ID", title=i18n.t("KPI Trend Over Time"))
    st.plotly_chart(fig_trend, use_container_width=True)
