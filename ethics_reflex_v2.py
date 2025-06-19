
import pandas as pd
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def ethics_reflex(kpi_df, eia_doc_id="EIA_v1.0"):
    """
    Phân tích đạo đức từ KPI Tracker và nội dung EIA.
    :param kpi_df: DataFrame chứa KPI_Tracker
    :param eia_doc_id: ID tài liệu đánh giá đạo đức
    :return: dict gồm đánh giá từng KPI, EIA và điểm tương đồng
    """
    # Khởi tạo mô hình NLP
    classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

    # Ghép văn bản từ KPI_Tracker
    kpi_text = []
    for _, row in kpi_df.iterrows():
        kpi_status = f"KPI {row['KPI ID']}: {row['Metric']} is {row['Actual']} vs target {row['Target']}. Status: {row['Status']}"
        kpi_text.append(kpi_status)

    # Văn bản giả định từ EIA
    eia_text = f"Ethical Impact Assessment ({eia_doc_id}): Evaluates bias, fairness, and sustainability impacts."

    # Đánh giá từng đoạn văn
    results = []
    for text in kpi_text + [eia_text]:
        try:
            prediction = classifier(text)[0]
            label = prediction["label"]
            score = prediction["score"]
            if label == "POSITIVE" and score > 0.7:
                results.append("✅ Low Bias Risk")
            elif label == "NEGATIVE" and score > 0.7:
                results.append("🚨 Ethical Violation")
            else:
                results.append("⚠️ Review Required")
        except Exception:
            results.append("❌ Model Error")

    # Tính điểm tương đồng
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(kpi_text + [eia_text])
    similarity = cosine_similarity(vectors[-1], vectors[:-1]).mean()

    return {
        "kpi_assessments": results[:-1],
        "eia_assessment": results[-1],
        "similarity_score": similarity
    }
