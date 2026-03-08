# 🔐 AES-256 Secure File Vault

A robust, local file encryption/decryption system built with **Python**, **PySide6**, and the **Cryptography** library. This tool provides a secure way to store sensitive documents using industry-standard AES-256 encryption.

---

## 🚀 Overview
This application allows you to "lock" any file with a master password. It uses **Authenticated Encryption**, meaning it doesn't just hide your data—it also detects if anyone has tried to modify the encrypted file.

### Key Features
* **AES-256 (Fernet):** High-level symmetric encryption.
* **PBKDF2 Key Derivation:** Transforms your password into a cryptographic key using 100,000 iterations of SHA-256.
* **Random Salting:** Ensures that the same password produces different ciphertexts every time.
* **Integrity Checks:** Automatically verifies that files haven't been tampered with.
* **Modern GUI:** Clean, easy-to-use interface built with PySide6.

---

## 🛠️ How It Works



1.  **Password Processing:** The user enters a password.
2.  **Key Derivation:** The app generates a 16-byte random salt. Using **PBKDF2**, the password and salt are "stretched" into a 32-byte key.
3.  **Encryption:** The `cryptography` library encrypts the file and adds an HMAC (Hash-based Message Authentication Code).
4.  **Storage:** The salt is prepended to the encrypted data, and the file is saved with a `.enc` extension.



---

## 📁 Project Structure

.
├── vault_app.py        # The main Python application
├── README.md           # Documentation
└── requirements.txt    # List of dependencies
