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

# Custom Styling
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    h1 {font-size: 28px !important;}
    h2 {font-size: 22px !important;}
    h3 {font-size: 18px !important;}
    [data-testid="stMetric"] {
        background-color: rgba(128, 128, 128, 0.08);
        padding: 14px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# MEMUAT DATASET
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent
CLEAN_DATA = BASE_DIR / "data" / "day_clean.csv"
RAW_DATA = BASE_DIR / "data" / "day.csv"


@st.cache_data
def load_data():
    if CLEAN_DATA.exists():
        file_path = CLEAN_DATA
    elif RAW_DATA.exists():
        file_path = RAW_DATA
    elif Path("data/day_clean.csv").exists():
        file_path = Path("data/day_clean.csv")
    elif Path("data/day.csv").exists():
        file_path = Path("data/day.csv")
    else:
        raise FileNotFoundError(
            "File day_clean.csv atau day.csv tidak ditemukan di folder data."
        )

    df = pd.read_csv(file_path)

    required_columns = [
        "dteday", "yr", "mnth", "weathersit",
        "casual", "registered", "cnt"
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Kolom berikut tidak ditemukan: {missing_columns}")

    df["dteday"] = pd.to_datetime(df["dteday"], errors="coerce")
    df["yr"] = pd.to_numeric(df["yr"], errors="coerce")
    df["mnth"] = pd.to_numeric(df["mnth"], errors="coerce")
    df["Tahun"] = df["yr"].map({0: 2011, 1: 2012})

    return df


try:
    day_df = load_data()
except Exception as error:
    st.error(f"Dataset gagal dimuat: {error}")
    st.stop()


# Batas tanggal dataset
min_date = day_df["dteday"].min().date()
max_date = day_df["dteday"].max().date()

# Inisialisasi session state untuk filter tanggal
if "start_date" not in st.session_state:
    st.session_state.start_date = min_date
if "end_date" not in st.session_state:
    st.session_state.end_date = max_date

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
    st.markdown("- **ID Dicoding:** DS014B6Y0760")


# Mengambil tanggal aktif dari session state
start_date = st.session_state.start_date
end_date = st.session_state.end_date

# Filter dataframe berdasarkan tanggal yang dipilih
filtered_df = day_df[
    (day_df["dteday"].dt.date >= start_date) &
    (day_df["dteday"].dt.date <= end_date)
]

if filtered_df.empty:
    st.warning("Tidak ada data untuk rentang tanggal yang dipilih.")
    st.stop()


# ==========================================
# PERSIAPAN DATA AGREGASI
# ==========================================
# 1. Tren bulanan
monthly_rentals = (
    filtered_df.groupby(["Tahun", "mnth"], as_index=False)["cnt"]
    .sum()
)

# 2. Perbandingan jenis pengguna
total_casual = int(filtered_df["casual"].sum())
total_registered = int(filtered_df["registered"].sum())
total_all = total_casual + total_registered

user_comparison = pd.DataFrame({
    "Jenis Pengguna": ["Casual", "Registered"],
    "Total Penyewaan": [total_casual, total_registered],
    "Persentase": [
        (total_casual / total_all * 100) if total_all > 0 else 0,
        (total_registered / total_all * 100) if total_all > 0 else 0
    ]
})

# 3. Pengaruh cuaca
weather_labels = {
    1: "Cerah / Sedikit Berawan",
    2: "Berkabut / Berawan",
    3: "Hujan atau Salju Ringan",
    4: "Hujan Lebat / Salju / Kabut"
}

weather_comparison = (
    filtered_df.groupby("weathersit")["cnt"]
    .agg(
        Jumlah_Hari="count",
        Total_Penyewaan="sum",
        Rata_rata_Penyewaan="mean"
    )
    .reindex([1, 2, 3, 4])
    .rename_axis("Kode_Cuaca")
    .reset_index()
)

weather_comparison["Jumlah_Hari"] = weather_comparison["Jumlah_Hari"].fillna(0).astype(int)
weather_comparison["Total_Penyewaan"] = weather_comparison["Total_Penyewaan"].fillna(0)
weather_comparison["Rata_rata_Penyewaan"] = weather_comparison["Rata_rata_Penyewaan"].fillna(0)
weather_comparison["Kondisi Cuaca"] = weather_comparison["Kode_Cuaca"].map(weather_labels)


# ==========================================
# JUDUL DASHBOARD & OVERVIEW KPI
# ==========================================
st.title("🚲 Bike Sharing Dashboard")
st.caption(
    f"Analisis penyewaan sepeda di Washington D.C. | Rentang waktu: **{start_date.strftime('%d %b %Y')}** s.d. **{end_date.strftime('%d %b %Y')}**"
)

st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Penyewaan", f"{int(filtered_df['cnt'].sum()):,}")
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

fig1, ax1 = plt.subplots(figsize=(12, 4))

year_styles = {
    2011: {"color": "#90CAF9", "linestyle": "-"},
    2012: {"color": "#1565C0", "linestyle": "--"}
}

years_present = sorted(monthly_rentals["Tahun"].dropna().unique())
for year in years_present:
    year = int(year)
    data = monthly_rentals[monthly_rentals["Tahun"] == year].sort_values("mnth")
    if not data.empty:
        style = year_styles.get(year, {"color": "#1E88E5", "linestyle": "-"})
        ax1.plot(
            data["mnth"],
            data["cnt"],
            label=str(year),
            color=style["color"],
            linestyle=style["linestyle"],
            marker="o",
            markersize=5,
            linewidth=2
        )

ax1.set_title("Tren Total Penyewaan per Bulan", fontsize=12, pad=10)
ax1.set_xlabel("Bulan", fontsize=10)
ax1.set_ylabel("Total Penyewaan", fontsize=10)
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

    fig2, ax2 = plt.subplots(figsize=(6, 4))

    bars = ax2.bar(
        user_comparison["Jenis Pengguna"],
        user_comparison["Total Penyewaan"],
        color=["#90CAF9", "#1565C0"],
        width=0.5
    )

    ax2.set_ylabel("Total Penyewaan", fontsize=10)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)

    ax2.bar_label(
        bars,
        labels=[f"{int(v):,}" for v in user_comparison["Total Penyewaan"]],
        padding=4,
        fontsize=9
    )

    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    # Tabel ringkasan
    st.dataframe(
        user_comparison.rename(columns={
            "Jenis Pengguna": "Jenis Pengguna",
            "Total Penyewaan": "Total Penyewaan",
            "Persentase": "Persentase (%)"
        }).style.format({
            "Total Penyewaan": "{:,.0f}",
            "Persentase (%)": "{:.2f}%"
        }),
        width="stretch",
        hide_index=True
    )

# Bagian 3: Kondisi Cuaca
with col_weather:
    st.subheader("3. Penyewaan Berdasarkan Kondisi Cuaca")

    fig3, ax3 = plt.subplots(figsize=(6, 4))

    short_labels = [
        "Cerah",
        "Berkabut",
        "Hujan ringan",
        "Cuaca ekstrem"
    ]

    bars = ax3.bar(
        short_labels,
        weather_comparison["Rata_rata_Penyewaan"],
        color=["#1565C0", "#1976D2", "#64B5F6", "#BBDEFB"],
        width=0.55
    )

    ax3.set_ylabel("Rata-rata Penyewaan per Hari", fontsize=10)
    ax3.tick_params(axis="x", labelsize=8.5, rotation=10)
    ax3.grid(axis="y", linestyle="--", alpha=0.3)

    for bar, (_, row) in zip(bars, weather_comparison.iterrows()):
        if row["Jumlah_Hari"] == 0:
            label = "Tidak ada data"
            y_pos = 100
        else:
            label = f"{row['Rata_rata_Penyewaan']:,.0f}"
            y_pos = row["Rata_rata_Penyewaan"] + 60

        ax3.text(
            bar.get_x() + bar.get_width() / 2,
            y_pos,
            label,
            ha="center",
            va="bottom",
            fontsize=8.5
        )

    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

    # Tabel ringkasan cuaca
    st.dataframe(
        weather_comparison[
            [
                "Kode_Cuaca",
                "Kondisi Cuaca",
                "Jumlah_Hari",
                "Total_Penyewaan",
                "Rata_rata_Penyewaan"
            ]
        ].rename(columns={
            "Kode_Cuaca": "Kode Cuaca",
            "Jumlah_Hari": "Jumlah Hari",
            "Total_Penyewaan": "Total Penyewaan",
            "Rata_rata_Penyewaan": "Rata-rata Penyewaan"
        }).style.format({
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
