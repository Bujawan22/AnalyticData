from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ==========================================
# KONFIGURASI HALAMAN STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Custom Styling (Konsisten Tema Biru Modern)
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    h1 {
        font-size: 28px !important;
        color: #0D47A1 !important;
    }
    h2, h3 {
        color: #1565C0 !important;
    }
    [data-testid="stMetric"] {
        background-color: rgba(21, 101, 192, 0.05);
        border: 1px solid rgba(21, 101, 192, 0.15);
        padding: 14px;
        border-radius: 10px;
    }
    [data-testid="stMetricValue"] {
        color: #1565C0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# MEMUAT DATASET DAY_CLEAN.CSV
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DATA = BASE_DIR / "data" / "day_clean.csv"


@st.cache_data
def load_data():
    if CLEAN_DATA.exists():
        file_path = CLEAN_DATA
    elif Path("data/day_clean.csv").exists():
        file_path = Path("data/day_clean.csv")
    else:
        raise FileNotFoundError(
            "File 'day_clean.csv' tidak ditemukan di folder 'data/'. "
            "Pastikan file 'day_clean.csv' tersedia."
        )

    df = pd.read_csv(file_path)

    # Konversi kolom date ke tipe datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df


try:
    day_df = load_data()
except Exception as error:
    st.error(f"❌ Error saat memuat dataset: {error}")
    st.stop()


# Batas rentang tanggal dari dataset
min_date = day_df["date"].min().date()
max_date = day_df["date"].max().date()

# Inisialisasi session state untuk filter tanggal
if "start_date" not in st.session_state:
    st.session_state.start_date = min_date
if "end_date" not in st.session_state:
    st.session_state.end_date = max_date


# ==========================================
# SIDEBAR: FILTER DATA & INFORMASI
# ==========================================
with st.sidebar:
    st.title("🚲 Bike Sharing")
    st.markdown("Dashboard Analisis Penyewaan Sepeda")
    st.divider()

    st.subheader("Filter Rentang Tanggal")
    with st.form(key="filter_form"):
        input_start_date = st.date_input(
            "Tanggal Mulai:",
            value=st.session_state.start_date,
            min_value=min_date,
            max_value=max_date
        )
        input_end_date = st.date_input(
            "Tanggal Akhir:",
            value=st.session_state.end_date,
            min_value=min_date,
            max_value=max_date
        )
        btn_analisis = st.form_submit_button(
            label="🔍 Analisis",
            type="primary"
        )

    if btn_analisis:
        if input_start_date > input_end_date:
            st.error("⚠️ Tanggal Mulai tidak boleh lebih besar dari Tanggal Akhir.")
        else:
            st.session_state.start_date = input_start_date
            st.session_state.end_date = input_end_date

    st.divider()
    st.markdown("**Informasi Proyek:**")
    st.markdown("- **Nama:** I Made Tara Bujawan")
    st.markdown("- **Email:** bujawan.2305551139@student.unud.ac.id")
    st.markdown("- **ID Dicoding:** madetara")


# Mengambil rentang tanggal aktif dari session state
start_date = st.session_state.start_date
end_date = st.session_state.end_date

# Filter data berdasarkan tanggal terpilih
filtered_df = day_df[
    (day_df["date"].dt.date >= start_date) &
    (day_df["date"].dt.date <= end_date)
]

if filtered_df.empty:
    st.warning("⚠️ Tidak ada data untuk rentang tanggal yang dipilih.")
    st.stop()


# ==========================================
# PERSIAPAN DATA AGREGASI
# ==========================================
# 1. Tren penyewaan sepeda bulanan
monthly_rentals = (
    filtered_df.groupby(["year", "month"])["total_rentals"]
    .sum()
    .reset_index()
    .sort_values(["year", "month"])
)

# 2. Perbandingan jenis pengguna
total_casual = int(filtered_df["casual"].sum())
total_registered = int(filtered_df["registered"].sum())
total_all = total_casual + total_registered

user_comparison = pd.DataFrame({
    "Jenis Pengguna": ["Casual", "Registered"],
    "Total Penyewaan": [total_casual, total_registered]
})
user_comparison["Persentase (%)"] = (
    (user_comparison["Total Penyewaan"] / total_all * 100).round(2)
    if total_all > 0 else 0
)

# 3. Penyewaan berdasarkan kondisi cuaca
weather_order = [
    "Cerah / Sedikit Berawan",
    "Berkabut / Berawan",
    "Hujan atau Salju Ringan",
    "Hujan Lebat / Salju / Kabut"
]

weather_comparison = (
    filtered_df.groupby("kondisi_cuaca")["total_rentals"]
    .agg(
        Jumlah_Hari="count",
        Total_Penyewaan="sum",
        Rata_rata_Penyewaan="mean"
    )
    .reindex(weather_order)
    .rename_axis("Kondisi Cuaca")
    .reset_index()
)

weather_comparison = weather_comparison.rename(columns={
    "Jumlah_Hari": "Jumlah Hari",
    "Total_Penyewaan": "Total Penyewaan",
    "Rata_rata_Penyewaan": "Rata-rata Penyewaan"
})

weather_comparison[["Jumlah Hari", "Total Penyewaan", "Rata-rata Penyewaan"]] = (
    weather_comparison[["Jumlah Hari", "Total Penyewaan", "Rata-rata Penyewaan"]].fillna(0)
)
weather_comparison["Jumlah Hari"] = weather_comparison["Jumlah Hari"].astype(int)
weather_comparison["Rata-rata Penyewaan"] = weather_comparison["Rata-rata Penyewaan"].round(2)


# ==========================================
# JUDUL DASHBOARD & OVERVIEW KPI
# ==========================================
st.title("🚲 Bike Sharing Dashboard")
st.caption(
    f"Analisis penyewaan sepeda di Washington D.C. | Rentang waktu: **{start_date.strftime('%d %b %Y')}** s.d. **{end_date.strftime('%d %b %Y')}**"
)

st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Penyewaan", f"{int(filtered_df['total_rentals'].sum()):,}")
col2.metric("Pengguna Casual", f"{total_casual:,}")
col3.metric("Pengguna Registered", f"{total_registered:,}")
col4.metric("Jumlah Hari", f"{len(filtered_df):,}")

st.divider()


# ==========================================
# BAGIAN 1: TREN PENYEWAAN SEPEDA BULANAN
# ==========================================
st.subheader("1. Tren Penyewaan Sepeda Bulanan")

month_names = [
    "Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
    "Jul", "Agu", "Sep", "Okt", "Nov", "Des"
]

fig1, ax1 = plt.subplots(figsize=(10, 4.2))

# Konsisten tema biru: 2011 biru muda (#90CAF9), 2012 biru pekat (#1565C0)
year_palette = {0: "#90CAF9", 1: "#1565C0", 2011: "#90CAF9", 2012: "#1565C0"}
year_labels = {0: "2011", 1: "2012", 2011: "2011", 2012: "2012"}

for yr in sorted(monthly_rentals["year"].unique()):
    df_yr = monthly_rentals[monthly_rentals["year"] == yr].sort_values("month")
    color = year_palette.get(yr, "#1565C0")
    label = year_labels.get(yr, str(yr))
    ax1.plot(
        df_yr["month"],
        df_yr["total_rentals"],
        marker="o",
        linewidth=2.2,
        markersize=6,
        color=color,
        label=label
    )

ax1.set_title("Tren Penyewaan Sepeda Bulanan (2011–2012)", fontsize=11, pad=10, fontweight="bold", color="#0D47A1")
ax1.set_xlabel("Bulan", fontsize=9.5)
ax1.set_ylabel("Total Penyewaan Sepeda", fontsize=9.5)
ax1.set_xticks(range(1, 13))
ax1.set_xticklabels(month_names)
ax1.legend(title="Tahun", frameon=False)
ax1.grid(axis="y", linestyle="--", alpha=0.3)

fig1.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

st.divider()


# ==========================================
# BAGIAN 2 & 3: DUA GRAFIK BERDAMPINGAN
# ==========================================
col_users, col_weather = st.columns(2, gap="large")

# Bagian 2: Jenis Pengguna
with col_users:
    st.subheader("2. Perbandingan Jenis Pengguna")

    fig2, ax2 = plt.subplots(figsize=(6, 4.5))

    # Bar chart: Nilai tertinggi biru pekat (#1565C0), yang lain biru redup (#90CAF9)
    max_user_val = user_comparison["Total Penyewaan"].max()
    user_bar_colors = [
        "#1565C0" if val == max_user_val and val > 0 else "#90CAF9"
        for val in user_comparison["Total Penyewaan"]
    ]

    bars2 = ax2.bar(
        user_comparison["Jenis Pengguna"],
        user_comparison["Total Penyewaan"],
        color=user_bar_colors,
        width=0.45,
        edgecolor="#0D47A1",
        linewidth=0.8
    )

    ax2.set_title("Perbandingan Penyewaan Berdasarkan Jenis Pengguna", fontsize=11, pad=10, fontweight="bold", color="#0D47A1")
    ax2.set_ylabel("Total Penyewaan Sepeda", fontsize=9.5)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)

    # Menampilkan angka di atas setiap batang
    for bar in bars2:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            height + (max_user_val * 0.02 if max_user_val > 0 else 0),
            f"{int(height):,}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold"
        )

    if max_user_val > 0:
        ax2.set_ylim(0, max_user_val * 1.15)

    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    # Tabel ringkasan jenis pengguna
    st.dataframe(
        user_comparison.style.format({
            "Total Penyewaan": "{:,.0f}",
            "Persentase (%)": "{:.2f}%"
        }),
        width="stretch",
        hide_index=True
    )

# Bagian 3: Kondisi Cuaca
with col_weather:
    st.subheader("3. Penyewaan Berdasarkan Kondisi Cuaca")

    fig3, ax3 = plt.subplots(figsize=(6, 4.5))

    # Bar chart: Nilai tertinggi biru pekat (#1565C0), yang lain biru redup (#90CAF9)
    max_weather_val = weather_comparison["Rata-rata Penyewaan"].max()
    weather_bar_colors = [
        "#1565C0" if val == max_weather_val and val > 0 else "#90CAF9"
        for val in weather_comparison["Rata-rata Penyewaan"]
    ]

    bars3 = ax3.bar(
        weather_comparison["Kondisi Cuaca"],
        weather_comparison["Rata-rata Penyewaan"],
        color=weather_bar_colors,
        width=0.55,
        edgecolor="#0D47A1",
        linewidth=0.8
    )

    ax3.set_title("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca", fontsize=11, pad=10, fontweight="bold", color="#0D47A1")
    ax3.set_ylabel("Rata-rata Penyewaan per Hari", fontsize=9.5)
    ax3.tick_params(axis="x", labelsize=8, rotation=15)
    ax3.grid(axis="y", linestyle="--", alpha=0.3)

    # Menampilkan angka di atas setiap batang
    for bar, val in zip(bars3, weather_comparison["Rata-rata Penyewaan"]):
        label = "0.00" if val == 0 else f"{val:,.2f}"
        ax3.text(
            bar.get_x() + bar.get_width() / 2,
            val + (max_weather_val * 0.02 if max_weather_val > 0 else 50),
            label,
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold"
        )

    if max_weather_val > 0:
        ax3.set_ylim(0, max_weather_val * 1.15)

    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

    # Tabel ringkasan cuaca
    st.dataframe(
        weather_comparison.style.format({
            "Jumlah Hari": "{:,.0f}",
            "Total Penyewaan": "{:,.0f}",
            "Rata-rata Penyewaan": "{:,.2f}"
        }),
        width="stretch",
        hide_index=True
    )

    st.caption(
        "Catatan: Kategori cuaca dengan 0 hari berarti tidak ada observasi pada rentang tanggal terpilih."
    )

# ==========================================
# PENUTUP
# ==========================================
st.divider()
st.caption("Sumber data: Bike Sharing Dataset – Hadi Fanaee-T (2011–2012)")
