import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

# =========================
# LOAD DATA
# =========================
df = pd.read_excel("Data_survei.xlsx")

likert_cols = df.columns[7:26]

# =========================
# HEADER DASHBOARD
# =========================
st.set_page_config(page_title="Dashboard Evaluasi Survei", layout="wide")
st.title("📊 Dashboard Evaluasi Pengguna Sistem")

# =========================
# 1️⃣ HEADER: JUMLAH RESPONDEN & SKOR RATA-RATA
# =========================
total_responden = len(df)
rata_rata_total = df[likert_cols].mean().mean()

col1, col2 = st.columns(2)
col1.metric("👥 Jumlah Responden", total_responden)
col2.metric("⭐ Skor Rata-rata", round(rata_rata_total, 2))

st.divider()

# =========================
# 2️⃣ DISTRIBUSI SKOR LIKERT
# =========================
st.subheader("📌 Distribusi Skor Likert")

likert_data = df[likert_cols].values.flatten()
likert_series = pd.Series(likert_data)

fig_likert = px.histogram(
    likert_series,
    x=likert_series,
    nbins=5,
    labels={"x": "Skor Likert", "y": "Jumlah Responden"},
    title="Distribusi Skor Likert Keseluruhan"
)
st.plotly_chart(fig_likert, use_container_width=True)

# =========================
# 3️⃣ RATA-RATA PER INDIKATOR
# =========================
st.subheader("📊 Rata-rata Penilaian per Indikator")

mean_scores = df[likert_cols].mean().sort_values()

fig_mean = px.bar(
    mean_scores,
    orientation="h",
    labels={"value": "Skor Rata-rata", "index": "Indikator"},
    title="Rata-rata Skor per Indikator"
)
st.plotly_chart(fig_mean, use_container_width=True)

# =========================
# 4️⃣ RADAR CHART KUALITAS SISTEM
# =========================
st.subheader("🕸️ Profil Kualitas Sistem (Radar Chart)")

radar_df = pd.DataFrame({
    "Indikator": mean_scores.index,
    "Skor": mean_scores.values
})

fig_radar = px.line_polar(
    radar_df,
    r="Skor",
    theta="Indikator",
    line_close=True,
    title="Radar Chart Kualitas Sistem"
)
fig_radar.update_traces(fill="toself")
st.plotly_chart(fig_radar, use_container_width=True)

# =========================
# 5️⃣ BOXPLOT KONSISTENSI PENILAIAN
# =========================
st.subheader("📦 Boxplot Konsistensi Penilaian")

fig_box = px.box(
    df[likert_cols],
    title="Sebaran dan Konsistensi Penilaian Responden"
)
st.plotly_chart(fig_box, use_container_width=True)

# =========================
# 6️⃣ PROFIL RESPONDEN
# =========================
st.subheader("👤 Profil Responden")

col3, col4 = st.columns(2)

with col3:
    fig_role = px.pie(
        df,
        names="  Peran/Jabatan",
        title="Distribusi Peran/Jabatan"
    )
    st.plotly_chart(fig_role, use_container_width=True)

with col4:
    fig_field = px.pie(
        df,
        names="Bidang Keahlian",
        title="Distribusi Bidang Keahlian"
    )
    st.plotly_chart(fig_field, use_container_width=True)

# =========================
# 7️⃣ REKOMENDASI PENGGUNA
# =========================
st.subheader("👍 Kesediaan Rekomendasi Pengguna")

fig_rekom = px.bar(
    df["Apakah Anda bersedia merekomendasikan dashboard ini kepada institusi Anda?"].value_counts(),
    labels={"value": "Jumlah Responden", "index": "Jawaban"},
    title="Kesediaan Rekomendasi"
)
st.plotly_chart(fig_rekom, use_container_width=True)

# =========================
# 8️⃣ KRITIK & SARAN
# =========================
st.subheader("📝 Kritik dan Saran Pengguna")

feedback = df["Berikan Kritikan dan Saran untuk kemajuan dan perbaikan media yang dibuat"].dropna()

if len(feedback) > 0:
    for i, text in enumerate(feedback, 1):
        st.write(f"{i}. {text}")
else:
    st.info("Tidak ada kritik dan saran yang diisi responden.")
