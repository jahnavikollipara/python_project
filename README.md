# python_project
Developed a Secure File Vault System using Python and Flask that allows users to upload, store, and manage files with encryption. Implemented user authentication, hashed passwords, and secure file handling to ensure data privacy and access control.
# 🔐 Secure File Vault System

## 📌 Project Overview

The Secure File Vault System is a web-based application built using Python and Flask that allows users to securely upload, store, and manage their files. The system ensures data privacy by using authentication and encryption techniques.

---

## 🚀 Features

* User Registration and Login
* Secure Password Storage (Hashed Passwords)
* File Upload and Storage
* File Encryption before saving
* File Decryption during download
* User-specific file access (privacy)
* Delete files option
* Simple and clean user interface

---

## 🛠️ Technologies Used

* Python
* Flask
* HTML, CSS
* hashlib (for password hashing)
* cryptography (for file encryption)
* JSON / SQLite (for storing user data)

---

## 📂 Project Structure

```
Secure-File-Vault/
│
├── app.py
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│
├── static/
│   └── style.css
│
├── uploads/
├── users.json / users.db
└── README.md
```

---

## ⚙️ Installation & Setup

1. Clone the repository:

```
git clone https://github.com/your-username/secure-file-vault.git
cd secure-file-vault
```

2. Install dependencies:

```
pip install flask cryptography
```

3. Run the application:

```
python app.py
```

4. Open browser and go to:

```
http://127.0.0.1:5000/
```

---

## 🔐 Security Features

* Passwords are stored using hashing (not plain text)
* Files are encrypted before storage
* Only logged-in users can access their files
* Users cannot access other users' data

---

## 📊 How It Works

1. User registers and logs in
2. Uploads a file
3. File gets encrypted and stored
4. User can download (decrypted) or delete the file

---

## 🎯 Future Enhancements

* File size limits
* Password reset feature
* Cloud storage integration
* Two-factor authentication

---

## 🏆 Conclusion

This project demonstrates secure file handling, authentication, and encryption using Python. It is a practical application showcasing real-world security concepts.

---

## 👤 Author

* Your Name
output:
<img width="1339" height="624" alt="image" src="https://github.com/user-attachments/assets/aea0a5cc-1c43-4be7-a0bd-57fb15d67b08" />


