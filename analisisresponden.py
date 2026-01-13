import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =========================
# LOAD DATA
# =========================
df = pd.read_excel("Data_survei.xlsx")

# 🔴 FIX 1: bersihkan nama kolom dari spasi aneh
df.columns = df.columns.str.strip()

likert_cols = df.columns[7:26]

# 🔴 FIX 2: pastikan semua kolom Likert numerik
df[likert_cols] = df[likert_cols].apply(
    pd.to_numeric, errors="coerce"
)

# =========================
# HEADER DASHBOARD
# =========================
st.set_page_config(page_title="Dashboard Evaluasi Survei", layout="wide")
st.title("📊 Dashboard Evaluasi Pengguna Sistem")

# =========================
# 1️⃣ HEADER: JUMLAH RESPONDEN & SKOR RATA-RATA
# =========================
total_responden = len(df)
rata_rata_total = df[likert_cols].mean(numeric_only=True).mean()

col1, col2 = st.columns(2)
col1.metric("👥 Jumlah Responden", total_responden)
col2.metric("⭐ Skor Rata-rata", round(rata_rata_total, 2))

st.divider()

# =========================
# 2️⃣ DISTRIBUSI SKOR LIKERT
# =========================
st.subheader("📌 Distribusi Skor Likert")

likert_data = df[likert_cols].values.flatten()
likert_data = likert_data[~np.isnan(likert_data)]

fig, ax = plt.subplots()
ax.hist(likert_data, bins=[1, 2, 3, 4, 5, 6])
ax.set_xlabel("Skor Likert")
ax.set_ylabel("Jumlah Responden")
ax.set_title("Distribusi Skor Likert Keseluruhan")
st.pyplot(fig)

# =========================
# 3️⃣ RATA-RATA PER INDIKATOR
# =========================
st.subheader("📊 Rata-rata Penilaian per Indikator")

mean_scores = df[likert_cols].mean(numeric_only=True).sort_values()

fig, ax = plt.subplots(figsize=(8, 6))
ax.barh(mean_scores.index, mean_scores.values)
ax.set_xlabel("Skor Rata-rata")
ax.set_title("Rata-rata Skor per Indikator")
st.pyplot(fig)

# =========================
# 4️⃣ RADAR CHART KUALITAS SISTEM
# =========================
st.subheader("🕸️ Profil Kualitas Sistem (Radar Chart)")

labels = mean_scores.index.tolist()
scores = mean_scores.values.tolist()
scores += scores[:1]

angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.plot(angles, scores, linewidth=2)
ax.fill(angles, scores, alpha=0.25)
ax.set_thetagrids(np.degrees(angles[:-1]), labels)
ax.set_title("Radar Chart Kualitas Sistem")
st.pyplot(fig)

# =========================
# 5️⃣ BOXPLOT KONSISTENSI PENILAIAN
# =========================
st.subheader("📦 Boxplot Konsistensi Penilaian")

fig, ax = plt.subplots(figsize=(10, 6))
ax.boxplot(df[likert_cols].values, vert=False)
ax.set_yticks(range(1, len(likert_cols) + 1))
ax.set_yticklabels(likert_cols)
ax.set_xlabel("Skor")
ax.set_title("Sebaran dan Konsistensi Penilaian Responden")
st.pyplot(fig)

# =========================
# 6️⃣ PROFIL RESPONDEN
# =========================
st.subheader("👤 Profil Responden")

col3, col4 = st.columns(2)

with col3:
    role_counts = df["Peran/Jabatan"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(role_counts, labels=role_counts.index, autopct="%1.1f%%")
    ax.set_title("Distribusi Peran/Jabatan")
    st.pyplot(fig)

with col4:
    field_counts = df["Bidang Keahlian"].value_counts()
    fig, ax = plt.subplots()
    ax.pie(field_counts, labels=field_counts.index, autopct="%1.1f%%")
    ax.set_title("Distribusi Bidang Keahlian")
    st.pyplot(fig)

# =========================
# 7️⃣ REKOMENDASI PENGGUNA
# =========================
st.subheader("👍 Kesediaan Rekomendasi Pengguna")

col_rekom = "Apakah Anda bersedia merekomendasikan dashboard ini kepada institusi Anda?"

if col_rekom in df.columns:
    rekom = df[col_rekom].dropna().astype(str).value_counts()

    if len(rekom) > 0:
        fig, ax = plt.subplots()
        ax.bar(rekom.index, rekom.values)
        ax.set_xlabel("Jawaban")
        ax.set_ylabel("Jumlah Responden")
        ax.set_title("Kesediaan Rekomendasi Pengguna")
        st.pyplot(fig)
    else:
        st.warning("Data rekomendasi tersedia, namun tidak ada jawaban yang diisi.")
else:
    st.error("Kolom pertanyaan rekomendasi tidak ditemukan dalam data survei.")

# =========================
# 8️⃣ KRITIK & SARAN
# =========================
st.subheader("📝 Kritik dan Saran Pengguna")

feedback = df[
    "Berikan Kritikan dan Saran untuk kemajuan dan perbaikan media yang dibuat"
].dropna()

if len(feedback) > 0:
    for i, text in enumerate(feedback, 1):
        st.write(f"{i}. {text}")
else:
    st.info("Tidak ada kritik dan saran yang diisi responden.")

