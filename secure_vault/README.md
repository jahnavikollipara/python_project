# 🔐 SecureVault — Secure File Vault

A Flask web application that lets users register, log in, and securely upload,
download, and delete files. All files are **encrypted on disk** using Fernet
(AES-128) and **decrypted in-memory** at download time — the plain file is
never written back to disk.

---

## Project Structure

```
secure_vault/
├── app.py                  ← Main Flask application
├── requirements.txt        ← Python dependencies
├── vault.db                ← SQLite database (auto-created)
├── vault.key               ← Encryption key (auto-created, keep secret!)
├── uploads/                ← Encrypted files (auto-created)
├── templates/
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
└── static/
    └── style.css
```

---

## ⚡ Quick Start

### 1. Create a virtual environment (recommended)

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

Open your browser at: **http://127.0.0.1:5000**

---

## 🔒 Security Features

| Feature | How it's done |
|---|---|
| Password storage | SHA-256 hash with random 16-byte salt |
| File encryption | Fernet (AES-128-CBC + HMAC-SHA256) |
| Session security | Flask signed cookies with `secret_key` |
| File isolation | Users can only access their own files |
| No plain storage | Encrypted files only on disk |
| Upload validation | Extension whitelist + 16 MB size cap |

---

## Notes

- `vault.key` is generated once and must be kept safe — losing it means
  encrypted files can no longer be decrypted.
- `debug=True` is set for development. In production, set `debug=False` and
  use a production WSGI server (e.g. gunicorn).
- The secret key is regenerated each restart in this demo. For production,
  set `app.secret_key` to a fixed, stored value so sessions survive restarts.
