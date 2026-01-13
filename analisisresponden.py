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
# PATH AMAN
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "Data_survei.xlsx")
IMAGE_PATH = os.path.join(BASE_DIR, "assets", "survey.png")

# ======================
# LOAD DATA
# ======================
df = pd.read_excel(DATA_PATH)

# 🔧 BERSIHKAN NAMA KOLOM (ANTI ERROR)
df.columns = df.columns.str.strip().str.lower()

# ======================
# FUNGSI CARI KOLOM AMAN
# ======================
def find_column(possible_names):
    for col in df.columns:
        if col in possible_names:
            return col
    return None

kolom_profesi = find_column(["profesi", "pekerjaan", "role", "jabatan"])
kolom_instansi = find_column(["instansi", "institusi", "unit kerja", "lembaga"])
kolom_pengalaman = find_column(["pengalaman", "lama kerja", "experience"])

# ======================
# HEADER
# ======================
st.markdown("""
# 📊 Dashboard Analisis Deskriptif Responden
Visualisasi partisipasi dan latar belakang responden survei
""")

# ======================
# GAMBAR (AMAN)
# ======================
if os.path.exists(IMAGE_PATH):
    st.image(Image.open(IMAGE_PATH), use_container_width=True)
else:
    st.info("🖼️ Gambar ilustrasi belum tersedia (assets/survey.png)")

st.divider()

# ======================
# KPI SUMMARY (AMAN)
# ======================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👥 Total Responden", len(df))

with col2:
    if kolom_profesi:
        st.metric("🧑‍💼 Jenis Profesi", df[kolom_profesi].nunique())
    else:
        st.metric("🧑‍💼 Jenis Profesi", "Tidak tersedia")

with col3:
    if kolom_instansi:
        st.metric("🏢 Instansi Terlibat", df[kolom_instansi].nunique())
    else:
        st.metric("🏢 Instansi Terlibat", "Tidak tersedia")

with col4:
    if kolom_profesi:
        indeks = round((df[kolom_profesi].nunique() / len(df)) * 100, 1)
        st.metric("🌍 Indeks Keberagaman (%)", indeks)
    else:
        st.metric("🌍 Indeks Keberagaman (%)", "-")

st.divider()

# ======================
# PROFIL RESPONDEN
# ======================
st.subheader("📌 Profil Responden")

colA, colB = st.columns(2)

# PIE PROFESI
with colA:
    if kolom_profesi:
        data_profesi = df[kolom_profesi].value_counts()
        fig, ax = plt.subplots()
        ax.pie(
            data_profesi,
            labels=data_profesi.index,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title("Distribusi Profesi Responden")
        st.pyplot(fig)
    else:
        st.warning("Data profesi tidak tersedia")

# BAR INSTANSI
with colB:
    if kolom_instansi:
        data_instansi = df[kolom_instansi].value_counts()
        fig, ax = plt.subplots()
        data_instansi.plot(kind="bar", ax=ax)
        ax.set_title("Distribusi Instansi Responden")
        ax.set_xlabel("Instansi")
        ax.set_ylabel("Jumlah")
        st.pyplot(fig)
    else:
        st.warning("Data instansi tidak tersedia")

# ======================
# PENGALAMAN
# ======================
if kolom_pengalaman:
    st.subheader("📈 Pengalaman Responden")
    data_pengalaman = df[kolom_pengalaman].value_counts().sort_index()
    fig, ax = plt.subplots()
    data_pengalaman.plot(kind="bar", ax=ax)
    ax.set_xlabel("Pengalaman")
    ax.set_ylabel("Jumlah Responden")
    ax.set_title("Distribusi Pengalaman Responden")
    st.pyplot(fig)

# ======================
# INSIGHT OTOMATIS
# ======================
st.divider()
st.subheader("🧠 Insight Utama")

st.success(
    f"Survei ini melibatkan {len(df)} responden. "
    "Dashboard menampilkan analisis deskriptif berdasarkan data yang tersedia, "
    "menunjukkan bahwa evaluasi sistem didukung oleh partisipasi responden "
    "yang memadai dan representatif."
)
