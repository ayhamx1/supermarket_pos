# -*- coding: utf-8 -*-
"""
🚀 Supermarket POS - 3D Premium Login View (No Role ComboBox)
📂 Path: main.py
"""
import sys
import os
import importlib.util

# 1. تحديد مجلد المشروع الأساسي ديناميكياً لتأمين بيئة التشغيل
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def find_file_path(filename, start_dir):
    for root, dirs, files in os.walk(start_dir):
        if filename in files:
            return os.path.join(root, filename)
    return None

cashier_path = find_file_path("cashier_main.py", ROOT_DIR)
admin_path = find_file_path("admin_main.py", ROOT_DIR)

if not cashier_path or not admin_path:
    print("❌ خطأ حرج: تأكد من وجود ملفات السيستم داخل مجلد المشروع.")
    sys.exit(1)

for path_found in [os.path.dirname(cashier_path), os.path.dirname(admin_path), ROOT_DIR]:
    if path_found not in sys.path:
        sys.path.insert(0, path_found)

# تشغيل الموديولات ديناميكياً
spec_cashier = importlib.util.spec_from_file_location("cashier_main", cashier_path)
cashier_main = importlib.util.module_from_spec(spec_cashier)
sys.modules["cashier_main"] = cashier_main
spec_cashier.loader.exec_module(cashier_main)

ExactCashierWindow = cashier_main.ExactCashierWindow
AdminMainWindow = ExactCashierWindow 

try:
    spec_admin = importlib.util.spec_from_file_location("admin_main", admin_path)
    admin_main = importlib.util.module_from_spec(spec_admin)
    sys.modules["admin_main"] = admin_main
    spec_admin.loader.exec_module(admin_main)
    AdminMainWindow = admin_main.AdminMainWindow
except:
    pass

from PyQt6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

# 🎨 ستايل الـ 3D المحدث بمطابقة كاملة لألوان وأشكال أزرار شاشة الكاشير المرفقة
LOGIN_3D_STYLE = """
    QDialog { 
        background-color: transparent; 
    }
    QFrame#panel3D {
        background-color: #F5F5F5; /* نفس خلفية الكاشير المريحة */
        border: 1px solid #D5D5D5;
        border-radius: 16px;
    }
    QLabel { 
        font-family: 'Segoe UI', 'Arial', 'Cairo'; 
        color: #2b2b2b; 
        font-size: 14px;
        font-weight: 500;
    }
    QLabel#mainTitle {
        color: #1e5378; /* نفس درجة لون أزرارك الفاخرة */
        font-size: 18px;
        font-weight: bold;
    }
    QLineEdit {
        border: 1px solid #cccccc;
        border-radius: 8px;
        padding: 10px 12px;
        background-color: #ffffff;
        color: #333333;
        font-size: 14px;
    }
    QLineEdit:focus {
        border: 2px solid #1e5378; /* توهج متناسق مع الأزرار */
    }
    QPushButton#primaryBtn {
        background-color: #1e5378; /* تطابق لون الزر المرفق بالصورة تماماً */
        color: white;
        border: none;
        border-radius: 20px; /* جعل الحواف دائرية بالكامل مثل أزرارك */
        padding: 12px 25px;
        font-family: 'Segoe UI';
        font-size: 15px;
        font-weight: bold;
    }
    QPushButton#primaryBtn:hover {
        background-color: #163f5c; /* تأثير داكن طفيف عند وقوف الماوس */
    }
    QPushButton#primaryBtn:pressed {
        background-color: #0f2d42;
    }
    QPushButton#secondaryBtn {
        background-color: #718096; /* زر الإلغاء القياسي المعتمد في الكاشير */
        color: white;
        border: none;
        border-radius: 20px; /* حواف دائرية متناسقة */
        padding: 12px 25px;
        font-family: 'Segoe UI';
        font-size: 15px;
        font-weight: bold;
    }
    QPushButton#secondaryBtn:hover {
        background-color: #4a5568;
    }
"""

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تسجيل دخول المنظومة")
        self.setFixedSize(460, 350)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        # تفعيل خلفية شفافة لعدم تشويه زوايا الحاوية الدائرية مع تفعيل خاصية الـ 3D
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        
        self.setStyleSheet(LOGIN_3D_STYLE)
        self.init_ui()

    def init_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(15, 15, 15, 15) # مساحة كافية لتأثير تشتت الظل
        
        # 📦 حاوية الـ 3D المستقلة
        self.panel_3d = QFrame()
        self.panel_3d.setObjectName("panel3D")
        
        # ✨ إسقاط تأثير الظل الفاخر لإعطاء العمق الـ 3D
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)                 
        shadow.setXOffset(0)                     
        shadow.setYOffset(8)                     
        shadow.setColor(QColor(0, 0, 0, 75))     
        self.panel_3d.setGraphicsEffect(shadow)
        
        inner_layout = QVBoxLayout(self.panel_3d)
        inner_layout.setContentsMargins(26, 26, 26, 26)
        inner_layout.setSpacing(12)
        
        # الترويسة العليا
        title = QLabel("🔐 بوابة الدخول الذكية للمنظومة")
        title.setObjectName("mainTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inner_layout.addWidget(title)
        inner_layout.addSpacing(10)
        
        # الحقول النصية
        inner_layout.addWidget(QLabel("اسم المستخدم أو رقم الموظف:"))
        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("أدخل اسم المستخدم المعتمد...")
        inner_layout.addWidget(self.txt_username)
        
        inner_layout.addWidget(QLabel("كلمة المرور الآمنة:"))
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setPlaceholderText("••••••••")
        inner_layout.addWidget(self.txt_password)
        
        inner_layout.addSpacing(15)
        
        # أزرار التحكم والتشغيل المودرن المتطابقة مع الكاشير
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        
        self.btn_login = QPushButton("تسجيل الدخول الفوري")
        self.btn_login.setObjectName("primaryBtn")
        self.btn_login.clicked.connect(self.handle_login)
        
        self.btn_close = QPushButton("إلغاء وإغلاق")
        self.btn_close.setObjectName("secondaryBtn")
        self.btn_close.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_close)
        inner_layout.addLayout(btn_layout)
        
        outer_layout.addWidget(self.panel_3d)

    def handle_login(self):
        username = self.txt_username.text().strip()
        password = self.txt_password.text().strip()
        
        SystemMessageBox = cashier_main.SystemMessageBox
        
        if not username or not password:
            SystemMessageBox.show_warning(self, "تنبيه الاعتماد", "يرجى إدخال بيانات الحساب كاملة أولاً!")
            return

        if username == "admin" and password == "123":
            self.accept_data = {"role": "admin", "name": "أحمد"}
            self.accept()
                
        elif username == "cashier" and password == "123":
            self.accept_data = {
                "role": "cashier", 
                "session": {"user_id": 1, "username": username, "pos_id": 1, "pos_name": "نقطة البيع الرئيسية"}
            }
            self.accept()
        else:
            SystemMessageBox.show_critical(self, "فشل الولوج", "بيانات الدخول غير تطابق السجلات، تأكد من صحة الحساب!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    
    login = LoginWindow()
    if login.exec() == QDialog.DialogCode.Accepted:
        if login.accept_data["role"] == "admin":
            main_window = AdminMainWindow(admin_name=login.accept_data["name"])
            main_window.showMaximized()
        else:
            main_window = ExactCashierWindow(session_data=login.accept_data["session"])
            main_window.show()
            
        sys.exit(app.exec())