import sys
import os
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                               QLineEdit, QLabel, QFileDialog, QMessageBox)
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class CryptoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('AES-256 Secure File Vault (PySide6)')
        self.setMinimumSize(400, 250)
        
        layout = QVBoxLayout()

        self.label = QLabel('Enter Master Password:')
        layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        self.encrypt_btn = QPushButton('🔒 Encrypt File')
        self.encrypt_btn.clicked.connect(self.encrypt_action)
        layout.addWidget(self.encrypt_btn)

        self.decrypt_btn = QPushButton('🔓 Decrypt File')
        self.decrypt_btn.clicked.connect(self.decrypt_action)
        layout.addWidget(self.decrypt_btn)

        self.status_label = QLabel('Status: Ready')
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def derive_key(self, password: str, salt: bytes):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_action(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File to Encrypt")
        password = self.password_input.text()
        
        if not path or not password:
            QMessageBox.warning(self, "Error", "Need both a file and a password!")
            return

        salt = os.urandom(16)
        key = self.derive_key(password, salt)
        fernet = Fernet(key)

        with open(path, 'rb') as f:
            data = f.read()

        encrypted_data = fernet.encrypt(data)
        
        with open(path + ".enc", 'wb') as f:
            f.write(salt + encrypted_data)

        self.status_label.setText(f"Success: {os.path.basename(path)}.enc created.")
        QMessageBox.information(self, "Done", "File encrypted and secured!")

    def decrypt_action(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select .enc File", "", "Encrypted Files (*.enc)")
        password = self.password_input.text()

        if not path or not password:
            return

        with open(path, 'rb') as f:
            file_content = f.read()

        salt = file_content[:16]
        encrypted_payload = file_content[16:]
        
        try:
            key = self.derive_key(password, salt)
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_payload)

            # Creating a 'restored' version of the original file
            original_filename = os.path.basename(path).replace(".enc", "")
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Decrypted File As", original_filename)
            
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(decrypted_data)
                self.status_label.setText("Success: File restored.")
        except Exception:
            QMessageBox.critical(self, "Failed", "Incorrect password or tampered file.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CryptoApp()
    ex.show()
    sys.exit(app.exec())