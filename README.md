# Beijing Air Quality Analysis Dashboard

Dashboard interaktif untuk analisis kualitas udara di Beijing menggunakan data dari 12 stasiun monitoring (2013-2017).

## Cara Menjalankan Dashboard

### 1. Setup Environment

Buat dan aktifkan virtual environment terlebih dahulu agar dependency project tidak bentrok dengan environment Python lain di komputer kamu.

**Menggunakan venv (bawaan Python):**

```bash
python -m venv env

# Windows
env\Scripts\activate

# Mac/Linux
source env/bin/activate
```

**Atau menggunakan conda:**

```bash
conda create --name main-ds python=3.9
conda activate main-ds
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Jalankan Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`. Jika tidak terbuka otomatis, buka URL tersebut secara manual.

## Struktur Project

```
submission/
├── dashboard/
│   ├── main_data.csv          # Data bersih untuk dashboard
│   └── dashboard.py           # Aplikasi Streamlit
├── data/                      # Folder data mentah (dari zip)
├── Proyek_Analisis_Data.ipynb  # Notebook analisis data
├── README.md                  # Dokumentasi project
├── requirements.txt           # Daftar dependencies
└── url.txt                    # URL dashboard (jika deployed)
```

## Fitur Dashboard

1. **Filter Data** - Filter berdasarkan rentang tanggal (start date - end date) dan stasiun, termasuk opsi "All Stations" untuk membandingkan seluruh stasiun sekaligus
2. **Metrik Utama** - Rata-rata PM2.5, PM10, Suhu, dan O3
3. **Tren PM2.5** - Grafik tren polusi bulanan sesuai rentang tanggal yang dipilih
4. **Perbandingan Stasiun** - Visualisasi perbandingan antar stasiun (stasiun dengan nilai tertinggi disorot)
5. **Pola Musiman** - Analisis pola polusi per bulan (bulan dengan nilai tertinggi disorot)
6. **Weekday vs Weekend** - Perbandingan polusi hari kerja vs akhir pekan di stasiun Dongsi
7. **Clustering** - Pengelompokan stasiun berdasarkan kategori kualitas udara WHO

## Pertanyaan Bisnis (SMART)

1. Bagaimana tren rata-rata bulanan PM2.5 di Beijing dari tahun 2013 hingga 2016, dan stasiun mana yang memiliki rata-rata PM2.5 tertinggi di atas 75 ug/m3 selama periode tersebut?

2. Berapa persen perbedaan rata-rata PM2.5 di stasiun Dongsi antara hari kerja (weekday) dan akhir pekan (weekend) selama tahun 2015-2016, dan pada rentang jam berapa perbedaan tersebut paling signifikan?

## Teknik Analisis Lanjutan

- **Manual Grouping (Clustering)**: Mengelompokkan stasiun berdasarkan standar WHO Air Quality Guidelines untuk PM2.5
