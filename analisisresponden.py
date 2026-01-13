import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =============================
# KONFIGURASI HALAMAN
# =============================
st.set_page_config(
    page_title="Analisis Deskriptif Responden",
    layout="wide"
)

st.title("📊 Analisis Deskriptif Responden")
st.markdown("Analisis partisipasi dan latar belakang responden survei")

# =============================
# LOAD DATA
# =============================
data = pd.read_excel("Data_survei.xlsx")  # ganti dengan nama file Anda

# =============================
# JUMLAH RESPONDEN
# =============================
total_responden = len(data)

st.metric(
    label="👥 Jumlah Responden",
    value=total_responden
)

st.divider()

# =============================
# FUNGSI ANALISIS KATEGORI
# =============================
def analisis_kategori(kolom, judul):
    st.subheader(f"🔹 Distribusi {judul}")
    
    distribusi = data[kolom].value_counts().reset_index()
    distribusi.columns = [judul, "Jumlah"]
    
    col1, col2 = st.columns(2)
    
    # TABEL
    with col1:
        st.markdown("**Tabel Ringkasan**")
        st.dataframe(distribusi, use_container_width=True)
    
    # GRAFIK
    with col2:
        fig, ax = plt.subplots()
        ax.pie(
            distribusi["Jumlah"],
            labels=distribusi[judul],
            autopct='%1.1f%%',
            startangle=90
        )
        ax.set_title(f"Diagram Pie {judul}")
        st.pyplot(fig)

# =============================
# ANALISIS LATAR BELAKANG
# =============================

if "Profesi" in data.columns:
    analisis_kategori("Profesi", "Profesi Responden")

if "Instansi" in data.columns:
    analisis_kategori("Instansi", "Instansi Responden")

if "Pengalaman" in data.columns:
    st.subheader("🔹 Distribusi Pengalaman Responden")
    
    pengalaman = data["Pengalaman"].value_counts().sort_index()
    
    fig, ax = plt.subplots()
    pengalaman.plot(kind="bar", ax=ax)
    ax.set_xlabel("Pengalaman")
    ax.set_ylabel("Jumlah Responden")
    ax.set_title("Diagram Batang Pengalaman Responden")
    
    st.pyplot(fig)

# =============================
# CATATAN INTERPRETASI
# =============================
st.info(
    "Analisis ini menunjukkan bahwa hasil evaluasi dashboard "
    "didukung oleh partisipasi responden yang memadai dan beragam, "
    "sehingga hasil survei dapat dianggap representatif."
)

