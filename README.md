# NutriDash - Indonesian Food Nutrition Analytics Dashboard

Dashboard analisis nutrisi profesional untuk data makanan Indonesia, dibangun dengan Streamlit. Dashboard ini menyediakan eksplorasi data interaktif, visualisasi komprehensif, model prediksi protein dengan Multiple Linear Regression (OLS), Meal Planner, dan fitur perbandingan makanan.

---

## Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| **Overview** | KPI metrics, distribusi protein per kategori, rekomendasi makanan berdasarkan tujuan (cutting/bulking/balanced) |
| **Data Explorer** | Pencarian & filter data makanan dengan tampilan grid atau tabel |
| **Visualisasi** | Scatter plot, heatmap korelasi, distribusi makronutrien, dan top categories |
| **Model & Koefisien** | Evaluasi model regresi (R2, MAE, RMSE), actual vs predicted plot, dan tabel koefisien |
| **Prediksi Protein** | Kalkulator estimasi protein berdasarkan parameter nutrisi dan kategori |
| **Meal Planner** | Susun kombinasi hidangan dan lihat total nutrisi + macro split |
| **Perbandingan** | Bandingkan profil nutrisi 2 makanan dengan radar chart |

---

## Prerequisites

- Python 3.9 atau lebih baru
- pip atau conda

---

## Instalasi Lokal

### 1. Clone atau Download Project

```bash
# Jika menggunakan git
git clone <url-repository>
cd nutridashboard

# Atau download manual, lalu:
cd path/to/nutridashboard
```

### 2. Buat Virtual Environment (Disarankan)

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Siapkan Data

Pastikan file `Data-Nutrisi.csv` berada di direktori yang sama dengan `app.py`. File ini berisi data nutrisi makanan Indonesia dari FatSecret.

Struktur direktori seharusnya:
```
nutridashboard/
├── app.py
├── requirements.txt
├── Data-Nutrisi.csv
└── README.md
```

### 5. Jalankan Dashboard

```bash
streamlit run app.py
```

Dashboard akan terbuka otomatis di browser pada `http://localhost:8501`.

### 6. Deactivate Virtual Environment

```bash
deactivate
```

---

## Deployment ke Streamlit Cloud (Rekomendasi - Gratis)

Streamlit Cloud adalah cara termudah dan gratis untuk deploy dashboard.

### 1. Persiapkan Repository GitHub

1. Buat repository baru di [GitHub](https://github.com/new)
2. Upload semua file project (`app.py`, `requirements.txt`, `Data-Nutrisi.csv`, `README.md`)
3. Commit dan push:

```bash
git init
git add .
git commit -m "Initial commit - NutriDash dashboard"
git branch -M main
git remote add origin https://github.com/USERNAME/nutridashboard.git
git push -u origin main
```

### 2. Deploy di Streamlit Cloud

1. Kunjungi [share.streamlit.io](https://share.streamlit.io)
2. Login dengan akun GitHub
3. Klik **"New app"**
4. Pilih repository, branch (main), dan file utama (`app.py`)
5. Klik **"Deploy"**

Streamlit Cloud akan otomatis:
- Install dependencies dari `requirements.txt`
- Jalankan aplikasi
- Berikan URL publik (contoh: `https://nutridashboard-xxx.streamlit.app`)

### 3. Auto-Update
Setiap kali kamu push ke GitHub, Streamlit Cloud akan otomatis redeploy.

---

## Deployment ke Heroku

### 1. Persiapkan File Tambahan

Buat file `Procfile` (tanpa ekstensi):
```
web: streamlit run app.py --server.port $PORT --server.headless true
```

Buat file `runtime.txt`:
```
python-3.11.6
```

Buat file `.gitignore`:
```
venv/
__pycache__/
*.pyc
.DS_Store
```

### 2. Install Heroku CLI & Login

```bash
# Install Heroku CLI (https://devcenter.heroku.com/articles/heroku-cli)
heroku login
```

### 3. Create & Deploy

```bash
# Inisialisasi git (jika belum)
git init
git add .
git commit -m "Ready for Heroku deployment"

# Buat app Heroku
heroku create nutridashboard-app

# Push ke Heroku
git push heroku main

# Buka aplikasi
heroku open
```

### 4. Manage

```bash
# Lihat logs
heroku logs --tail

# Restart app
heroku restart
```

---

## Deployment ke VPS (Ubuntu/Debian)

Untuk production deployment dengan kontrol penuh.

### 1. Siapkan Server

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python & pip
sudo apt install -y python3-pip python3-venv nginx git
```

### 2. Clone Project

```bash
cd /var/www
git clone https://github.com/USERNAME/nutridashboard.git
cd nutridashboard
```

### 3. Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Test Run

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Akses via `http://IP_SERVER:8501` untuk testing.

### 5. Setup Systemd Service

Buat file service:
```bash
sudo nano /etc/systemd/system/nutridashboard.service
```

Isi dengan:
```ini
[Unit]
Description=NutriDash Streamlit Dashboard
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/nutridashboard
Environment="PATH=/var/www/nutridashboard/venv/bin"
ExecStart=/var/www/nutridashboard/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Aktifkan service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable nutridashboard
sudo systemctl start nutridashboard
sudo systemctl status nutridashboard
```

### 6. Setup Nginx Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/nutridashboard
```

Isi dengan:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 86400;
    }
}
```

Aktifkan:
```bash
sudo ln -s /etc/nginx/sites-available/nutridashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Setup SSL (HTTPS) dengan Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

---

## Deployment dengan Docker

### 1. Buat Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
```

### 2. Build & Run

```bash
# Build image
docker build -t nutridashboard .

# Run container
docker run -p 8501:8501 nutridashboard
```

Akses di `http://localhost:8501`.

---

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError` | Pastikan semua package di `requirements.txt` sudah terinstall: `pip install -r requirements.txt` |
| File CSV tidak ditemukan | Pastikan `Data-Nutrisi.csv` ada di folder yang sama dengan `app.py` |
| Port 8501 sudah digunakan | Ganti port: `streamlit run app.py --server.port 8502` |
| Streamlit Cloud build gagal | Periksa versi Python dan package di `requirements.txt`, pastikan compatible |
| Nginx 502 Bad Gateway | Periksa status service: `sudo systemctl status nutridashboard`, periksa firewall |

---

## Teknologi

- **Streamlit** - Framework dashboard Python
- **Pandas & NumPy** - Data manipulation
- **Plotly** - Interactive visualizations
- **scikit-learn** - Machine learning (Linear Regression)
- **Google Fonts (Inter)** - Typography

---

## Lisensi

Proyek ini untuk keperluan edukasi dan analisis data nutrisi.
