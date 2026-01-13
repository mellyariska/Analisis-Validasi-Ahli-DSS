import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os

# ======================
# KONFIGURASI HALAMAN
# ======================
st.set_page_config(
    page_title="Dashboard Analisis Responden",
    page_icon="📊",
    layout="wide"
)

# ======================
# PATH AMAN (ANTI ERROR)
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "Data_survei.xlsx")
IMAGE_PATH = os.path.join(BASE_DIR, "assets", "survey.png")

# ======================
# LOAD DATA
# ======================
df = pd.read_excel(DATA_PATH)

# ======================
# HEADER
# ======================
st.markdown("""
# 📊 Dashboard Analisis Deskriptif Responden
Visualisasi partisipasi dan latar belakang responden survei
""")

# ======================
# GAMBAR (AMAN – TIDAK WAJIB ADA)
# ======================
if os.path.exists(IMAGE_PATH):
    image = Image.open(IMAGE_PATH)
    st.image(image, use_container_width=True)
else:
    st.info("🖼️ Gambar ilustrasi belum tersedia (assets/survey.png)")

st.divider()

# ======================
# KPI SUMMARY
# ======================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Total Responden", len(df))

with col2:
    st.metric("🧑‍💼 Jenis Profesi", df["Profesi"].nunique())

with col3:
    st.metric("🏢 Instansi Terlibat", df["Instansi"].nunique())

with col4:
    tingkat_diversitas = round(
        (df["Profesi"].nunique() / len(df)) * 100, 1
    )
    st.metric("🌍 Indeks Keberagaman (%)", tingkat_diversitas)

st.divider()

# ======================
# PROFIL RESPONDEN
# ======================
st.subheader("📌 Profil Responden")

colA, colB = st.columns(2)

# PIE PROFESI
with colA:
    profesi = df["Profesi"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(
        profesi,
        labels=profesi.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax1.set_title("Distribusi Profesi Responden")
    st.pyplot(fig1)

# BAR INSTANSI
with colB:
    instansi = df["Instansi"].value_counts()
    fig2, ax2 = plt.subplots()
    instansi.plot(kind="bar", ax=ax2)
    ax2.set_title("Distribusi Instansi Responden")
    ax2.set_xlabel("Instansi")
    ax2.set_ylabel("Jumlah")
    st.pyplot(fig2)

# ======================
# PENGALAMAN
# ======================
if "Pengalaman" in df.columns:
    st.subheader("📈 Pengalaman Responden")
    pengalaman = df["Pengalaman"].value_counts().sort_index()
    fig3, ax3 = plt.subplots()
    pengalaman.plot(kind="bar", ax=ax3)
    ax3.set_xlabel("Pengalaman")
    ax3.set_ylabel("Jumlah Responden")
    ax3.set_title("Distribusi Pengalaman Responden")
    st.pyplot(fig3)

# ======================
# INSIGHT OTOMATIS
# ======================
st.divider()
st.subheader("🧠 Insight Utama")

st.success(
    f"Survei ini melibatkan {len(df)} responden dengan latar belakang "
    f"{df['Profesi'].nunique()} jenis profesi dan "
    f"{df['Instansi'].nunique()} instansi berbeda. "
    "Hal ini menunjukkan bahwa hasil evaluasi dashboard "
    "didukung oleh partisipasi yang beragam dan representatif."
)
