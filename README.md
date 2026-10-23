# Bike Sharing Data Analysis

## Deskripsi

Proyek ini merupakan bagian dari kelas **Belajar Fundamental Analisis Data Dicoding**. Analisis menggunakan dataset Bike Sharing `day.csv` yang berisi data penyewaan sepeda harian di Washington, D.C., selama tahun 2011–2012.

Tujuan proyek ini adalah melihat pola penyewaan sepeda berdasarkan waktu, jenis pengguna, dan kondisi cuaca. Hasil analisis disajikan melalui notebook Python dan dashboard interaktif menggunakan Streamlit.

## Pertanyaan Bisnis

1. Bagaimana perubahan jumlah penyewaan sepeda setiap bulan selama 2011–2012?
2. Bagaimana perbandingan penyewaan oleh pengguna *casual* dan *registered*?
3. Bagaimana rata-rata penyewaan sepeda pada setiap kondisi cuaca?

Analisis lanjutan juga menggunakan teknik **binning** dan **manual grouping** untuk mengelompokkan tingkat permintaan berdasarkan jumlah penyewaan, cuaca, dan musim.

## Struktur Proyek

```text
submission/
├── dashboard/
│   └── dashboard.py
├── data/
│   ├── day.csv
│   └── day_clean.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Teknologi

- Python
- Pandas dan NumPy
- Matplotlib dan Seaborn
- Streamlit

## Menjalankan Notebook

1. Instal library yang diperlukan:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Buka `notebook.ipynb` melalui Jupyter Notebook atau editor yang mendukung notebook.
3. Jalankan seluruh cell secara berurutan.

## Menjalankan Dashboard Lokal

Jalankan perintah berikut dari folder utama proyek:

```bash
python -m pip install -r requirements.txt
python -m streamlit run dashboard/dashboard.py
```

Buka alamat lokal yang muncul di terminal, biasanya `http://localhost:8501`.

## Dashboard Online

Dashboard dapat diakses melalui tautan berikut:

**[Bike Sharing Analysis Dashboard](https://bbikesharinganalysis.streamlit.app/)**

## Referensi

Fanaee-T, H., & Gama, J. (2013). Event labeling combining ensemble detectors and background knowledge. *Progress in Artificial Intelligence, 2*, 113–127. https://doi.org/10.1007/s13748-013-0040-3
