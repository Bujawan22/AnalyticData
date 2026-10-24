# Bike Sharing Dashboard 

Proyek Analisis Data dan Dashboard Interaktif penyewaan sepeda menggunakan **Bike Sharing Dataset** (Washington D.C., 2011–2012) 

---

## Profil Pengembang
- **Nama:** I Made Tara Bujawan
- **Email:** bujawan.2305551139@student.unud.ac.id
- **ID Dicoding:** madetara

---

## Deskripsi Proyek
Proyek ini bertujuan untuk menganalisis pola penyewaan sepeda berdasarkan faktor waktu (tren bulanan), karakteristik tipe pengguna (*casual* vs *registered*), dan pengaruh kondisi cuaca. Hasil analisis disajikan dalam bentuk eksplorasi mendalam pada Jupyter Notebook (`notebook.ipynb`) dan dashboard interaktif berbasis web menggunakan **Streamlit** (`dashboard/dashboard.py`).

### Pertanyaan Bisnis
1. Bagaimana tren jumlah penyewaan sepeda setiap bulan selama tahun 2011–2012, dan bagaimana perubahannya dari tahun 2011 ke tahun 2012?
2. Bagaimana perbandingan jumlah penyewaan sepeda oleh pengguna kasual (*casual*) dan pengguna terdaftar (*registered*) selama tahun 2011–2012, serta kelompok pengguna mana yang memberikan kontribusi terbesar terhadap total penyewaan?
3. Bagaimana perbedaan rata-rata jumlah penyewaan sepeda berdasarkan kategori kondisi cuaca selama tahun 2011–2012?

---

## Struktur Direktori

```text
submission/
├── dashboard/
│   └── dashboard.py          # Script aplikasi dashboard Streamlit
├── data/
│   ├── day.csv               # Dataset mentah Bike Sharing
│   └── day_clean.csv         # Dataset bersih hasil wrangling & cleaning
├── notebook.ipynb            # Analisis data lengkap (wrangling, EDA, visualisasi)
├── README.md                 # Dokumentasi proyek
├── requirements.txt          # Dependensi library Python yang dibutuhkan
└── url.txt                   # Tautan URL deployment dashboard online
```

---

## Setup Environment - Anaconda

```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

*Atau menggunakan Python venv bawaan:*

```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

---

## Run Streamlit App

Dari direktori utama proyek (`submission`), jalankan:

```bash
streamlit run dashboard/dashboard.py
```

*Atau jika berada di dalam folder `dashboard`:*

```bash
cd dashboard
streamlit run dashboard.py
```

Akses dashboard melalui browser di: `http://localhost:8501`

---

## Dashboard Online (Deployment)

Dashboard Streamlit telah dideploy dan dapat diakses secara online melalui tautan berikut:

👉 **[Bike Sharing Analysis Dashboard](https://bbikesharinganalysis.streamlit.app/)**

---

## Fitur Utama Dashboard
- **Filter Rentang Tanggal Interaktif:** Menggunakan form input dua tanggal terpisah (*Tanggal Mulai* dan *Tanggal Akhir*) dengan tombol eksekusi **🔍 Analisis** dan validasi rentang tanggal otomatis.
- **KPI Metrics Overview:** Ringkasan metrik utama (*Total Penyewaan*, *Pengguna Casual*, *Pengguna Registered*, dan *Jumlah Hari*).
- **Visualisasi Tren Bulanan (Line Chart):** Perbandingan pola musiman dan peningkatan sewa dari tahun 2011 ke tahun 2012 dengan konsistensi palet biru.
- **Visualisasi Perbandingan Pengguna (Bar Chart & Tabel):** Menyorot pengguna *registered* sebagai kontributor terbesar dengan warna biru tebal/pekat (`#1565C0`) dan pengguna *casual* dengan warna biru redup (`#90CAF9`).
- **Visualisasi Pengaruh Cuaca (Bar Chart & Tabel):** Menyorot kondisi cuaca dengan rata-rata penyewaan harian tertinggi (*Cerah / Sedikit Berawan*) dengan warna biru pekat (`#1565C0`) serta kondisi lainnya dengan warna biru redup (`#90CAF9`).
- **Tabel Ringkasan Data Interaktif:** Tabel rincian angka total dan persentase yang rapi serta otomatis menyesuaikan lebar kontainer (`width="stretch"`).

---

## Ringkasan Insight & Temuan
1. **Tren Bulanan:** Terjadi peningkatan penyewaan sepeda yang sangat signifikan pada tahun 2012 dibandingkan tahun 2011 di seluruh bulan. Puncak aktivitas sewa terjadi pada musim panas hingga awal musim gugur (Juni–September).
2. **Karakteristik Pengguna:** Pengguna terdaftar (*registered*) memberikan kontribusi dominan sebesar **81,17%** (2.672.662 penyewaan), sedangkan pengguna kasual (*casual*) menyumbang **18,83%** (620.017 penyewaan).
3. **Pengaruh Cuaca:** Kondisi cuaca *Cerah / Sedikit Berawan* mencatat rata-rata penyewaan harian tertinggi (**4.876,79** unit/hari), diikuti kondisi *Berkabut / Berawan* (**4.035,86** unit/hari), dan menurun drastis saat *Hujan / Salju Ringan* (**1.803,29** unit/hari).
