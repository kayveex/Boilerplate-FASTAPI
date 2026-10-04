# FastAPI + SQLAlchemy + Alembic (Ponytail Architecture)

Boilerplate FastAPI dengan arsitektur bersih, modular (*separation of concerns* ala prinsip **Ponytail** / Clean Layered), terintegrasi penuh dengan **Alembic** untuk migrasi database, serta mendukung multi-database: **SQLite (Default), MySQL lokal, PostgreSQL, dan Supabase**.

---

## 📁 Struktur Direktori

```text
myfirst-api/
├── alembic/                      # Konfigurasi & histori file migrasi (Auto-generated)
│   ├── versions/                 # File migrasi database (mirip database/migrations di Laravel)
│   └── env.py                    # Bridge antara Alembic, Settings (.env), & SQLAlchemy Models
├── app/
│   ├── api/                      # Layer Delivery / HTTP API
│   │   └── v1/
│   │       ├── endpoints/        # Route controllers (misal: items.py)
│   │       └── router.py         # Router agregator v1
│   ├── core/                     # Fondasi aplikasi
│   │   ├── config.py             # Pydantic Settings (Membaca file .env)
│   │   └── database.py           # Engine SQLAlchemy, SessionLocal, get_db dependency
│   ├── models/                   # Definisi Tabel Database (SQLAlchemy ORM)
│   │   ├── __init__.py           # Export semua model untuk deteksi Alembic
│   │   └── item.py
│   ├── repositories/             # Layer Akses Data (Query & Manipulasi DB)
│   │   └── item_repository.py
│   ├── schemas/                  # Validasi Data & Serialisasi (Pydantic DTO)
│   │   └── item.py
│   └── services/                 # Layer Business Logic
│       └── item_service.py
├── .env                          # Environment variabel lokal
├── .env.example                  # Template environment
├── alembic.ini                   # File konfigurasi utama Alembic CLI
├── main.py                       # Entrypoint FastAPI Application
├── requirements.txt              # Daftar dependensi Python
└── README.md
```

---

## 🔌 Konfigurasi Database (.env)

Kamu cukup mengubah nilai `DATABASE_URL` di file [.env](file:///g:/ProjectFD/PythonFASTAPI/myfirst-api/.env):

### 1. SQLite (Default - Langsung Jalan)
```env
DATABASE_URL=sqlite:///./app.db
```

### 2. MySQL Lokal (Laragon / XAMPP / Docker)
```env
DATABASE_URL=mysql+pymysql://root:@localhost:3306/nama_database_kamu
```

### 3. PostgreSQL Lokal / Docker
```env
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/nama_database_kamu
```

### 4. Supabase (PostgreSQL Cloud)
Buka Dashboard Supabase: **Project Settings** -> **Database** -> **Connection string** (URI).  
Gunakan driver `postgresql+psycopg2://`:
```env
DATABASE_URL=postgresql+psycopg2://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres?sslmode=require
```

---

## 🛠️ Perintah Migrasi Database (Alembic)

Sama seperti alur Artisan di Laravel:

| Perintah Laravel | Perintah Alembic di FastAPI | Keterangan |
|---|---|---|
| `php artisan make:migration ...` | `alembic revision --autogenerate -m "nama_migrasi"` | Membuat file migrasi baru otomatis dari model |
| `php artisan migrate` | `alembic upgrade head` | Menjalankan seluruh migrasi yang belum dieksekusi |
| `php artisan migrate:rollback` | `alembic downgrade -1` | Rollback migrasi terakhir |
| `php artisan migrate:status` | `alembic current` atau `alembic history` | Melihat status versi migrasi aktif |

---

## 🚀 Menjalankan Server

```bash
uvicorn main:app --reload
```

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📬 Menguji di Bruno

### 1. Create Item (POST)
- **URL**: `http://127.0.0.1:8000/api/v1/items`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body (JSON)**:
  ```json
  {
    "title": "Macbook Pro M3",
    "description": "Laptop untuk coding FastAPI"
  }
  ```

### 2. Get All Items (GET)
- **URL**: `http://127.0.0.1:8000/api/v1/items`
- **Method**: `GET`

### 3. Get Item by ID (GET)
- **URL**: `http://127.0.0.1:8000/api/v1/items/1`
- **Method**: `GET`
