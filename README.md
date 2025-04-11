# Final Project - Human Capital Management BI System

## 📊 Deskripsi Proyek

Proyek ini bertujuan untuk membangun sistem Business Intelligence (BI) yang mendukung proses pengambilan keputusan dalam pengelolaan sumber daya manusia (Human Capital Management). Sistem ini akan mengintegrasikan berbagai data terkait SDM dan menyajikannya dalam bentuk dashboard yang informatif dan interaktif.

## 🗂️ Sumber Data

Sistem BI ini menggunakan data dari beberapa sumber utama terkait pengelolaan SDM, yaitu:

- **Recruitment & Selection**  
  Data pelamar kerja, tahapan proses seleksi, dan hasil evaluasi.

- **Data Management & Payroll**  
  Data karyawan aktif, informasi penggajian, tunjangan, serta lembur.

- **Training & Development**  
  Data aktivitas pelatihan, sertifikasi yang diperoleh, dan peningkatan kompetensi karyawan.

- **Performance Management**  
  Data evaluasi kinerja karyawan berdasarkan Key Performance Indicators (KPI) dan penilaian atasan.

## 💼 Business Use Case

Berikut adalah use case utama yang dikembangkan dalam proyek ini:

### 1. Demografi Pekerja
- 📌 Jumlah total pekerja
- 👩‍💼 Jumlah pekerja berdasarkan **jenis kelamin**
- 🎂 Jumlah pekerja berdasarkan **rentang usia**

### 2. Demografi Pelamar Kerja
- 📌 Jumlah total pelamar kerja
- 👨‍💼 Jumlah pelamar berdasarkan **jenis kelamin**
- 🎓 Jumlah pelamar berdasarkan **rentang usia**

### 3. Biaya Sumber Daya Manusia
- 💰 Total biaya **gaji**
- ⏱️ Total biaya **lembur**

## 📁 Struktur Direktori

```
final-project-dw/
├── dags/                      # DAG Airflow
├── etl/                       # Script ETL dan ELT
├── notebooks/                 # Jupyter Notebook dokumentasi
├── sql/                       # Script SQL DWH dan Data Mart
├── docker-compose.yaml        # Docker setup
├── .env                       # Environment variables
└── README.md                  # Dokumentasi proyek
```
## ⚙️ Teknologi yang Digunakan
- Docker
- Apache Airflow
- PostgreSQL (Data Warehouse)
- MariaDB (OLTP Source – Training & Development)
- MongoDB (OLTP Source – Recruitment)
- Python (pandas, SQLAlchemy)
- Google Looker Studio (Dashboard)
- VS Code & GitHub

## 📈 Output Dashboard

Dashboard akan menampilkan informasi dalam bentuk visualisasi grafik dan tabel interaktif untuk mendukung pengambilan keputusan strategis oleh tim HR dan manajemen.

## 🚀 Tujuan Akhir

Menyediakan sistem informasi berbasis data untuk:
- Monitoring performa dan beban biaya SDM
- Melacak efektivitas rekrutmen dan pelatihan
- Menyediakan insight demografis pekerja dan pelamar kerja

---

> Dibuat sebagai bagian dari proyek akhir untuk mendemonstrasikan keahlian dalam bidang Data Engineering & Business Intelligence.
