# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Users & Permissions Management UI
📂 Path: ui/admin/users_management.py
"""
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if root_dir not in sys.path: sys.path.append(root_dir)

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLineEdit, QHeaderView, 
                             QFrame, QTabWidget, QFormLayout, QComboBox, QCheckBox,
                             QApplication, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from app.controllers.users.user_controller import UserController

USER_STYLE = """
    QWidget { background-color: #F5F5F5; font-family: 'Segoe UI', 'Arial'; color: #333333; }
    QTabWidget::pane { border: 1px solid #cbd5e0; background: #ffffff; border-radius: 8px; }
    QTabBar::tab { background: #e2e8f0; border: 1px solid #cbd5e0; padding: 10px 20px; font-weight: bold; border-top-left-radius: 6px; border-top-right-radius: 6px; }
    QTabBar::tab:selected { background: #ffffff; color: #1E90FF; }
    
    QFrame#cardBox { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; }
    QLineEdit, QComboBox { border: 1px solid #cbd5e0; border-radius: 6px; padding: 6px 12px; font-size: 14px; background-color: white; }
    
    QTableWidget { background-color: #ffffff; border: none; gridline-color: #edf2f7; }
    QHeaderView::section { background-color: #f7fafc; color: #4a5568; font-weight: bold; padding: 8px; border-bottom: 2px solid #e2e8f0; }
    
    QPushButton#primaryBtn { background-color: #1E90FF; color: white; font-weight: bold; border-radius: 6px; padding: 8px 20px; border: none; }
    QPushButton#primaryBtn:hover { background-color: #1c86ee; }
    QCheckBox { spacing: 8px; font-size: 14px; }
    QCheckBox::indicator { width: 18px; height: 18px; }
"""

class UsersManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = UserController()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(USER_STYLE)
        
        # ربط الشاشات البرمجية بأسماء عربية مفهومة للمدير
        self.screen_mapping = {
            "products": "📦 إدارة المنتجات والأصناف",
            "inventory": "📥 جرد وحركات المخزون",
            "purchases": "🧾 فواتير المشتريات والموردين",
            "partners": "👥 حسابات العملاء والديون الآجلة",
            "sales_reports": "📊 تقارير المبيعات والأرباح السنوية",
            "cashier_screen": "🏪 شاشة مبيعات الكاشير الحية"
        }
        
        self.init_ui()
        self.refresh_users_list()
        self.load_role_permissions_matrix()

    def init_ui(self):
        main_layout = QVBoxLayout(self); main_layout.setContentsMargins(20, 20, 20, 20); main_layout.setSpacing(15)
        
        title = QLabel("👥 إدارة صلاحيات أدوار المستخدمين والموظفين"); title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        main_layout.addWidget(title)
        
        self.tabs = QTabWidget()
        
        # 1. تبويب مصفوفة الصلاحيات (الشاشات والأزرار)
        self.tab_matrix = QWidget(); self.init_matrix_tab()
        # 2. تبويب إضافة موظف جديد
        self.tab_accounts = QWidget(); self.init_accounts_tab()
        
        self.tabs.addTab(self.tab_matrix, "🛡️ مصفوفة التحكم في الشاشات والأزرار")
        self.tabs.addTab(self.tab_accounts, "👤 حسابات الموظفين الحالية")
        
        main_layout.addWidget(self.tabs)

    # --- 🛡️ 1. تبويب مصفوفة الصلاحيات ---
    def init_matrix_tab(self):
        layout = QVBoxLayout(self.tab_matrix); layout.setContentsMargins(15, 15, 15, 15); layout.setSpacing(12)
        
        ctrl_bar = QHBoxLayout()
        ctrl_bar.addWidget(QLabel("🎯 اختر الوظيفة/الدور المستهدف لتعديل صلاحياته:"))
        self.cmb_roles_filter = QComboBox()
        self.cmb_roles_filter.addItems(["كاشير (CASHIER)", "محاسب (ACCOUNTANT)", "أمين مخزن (STOCKKEEPER)", "مدير النظام (ADMIN)"])
        self.cmb_roles_filter.currentIndexChanged.connect(self.load_role_permissions_matrix)
        
        btn_save_matrix = QPushButton("💾 حفظ وإرسال مصفوفة الصلاحيات الجديدة للموظفين"); btn_save_matrix.setObjectName("primaryBtn"); btn_save_matrix.clicked.connect(self.submit_permissions_matrix)
        
        ctrl_bar.addWidget(self.cmb_roles_filter)
        ctrl_bar.addStretch()
        ctrl_bar.addWidget(btn_save_matrix)
        layout.addLayout(ctrl_bar)
        
        # جدول عرض Matrix التفاعلي
        self.table_matrix = QTableWidget(); self.table_matrix.setColumnCount(5)
        self.table_matrix.setHorizontalHeaderLabels(["الشاشة المستهدفة", "رؤية ودخول الشاشة (View)", "زر إضافة وحفظ (Add)", "زر تعديل وتسوية (Edit)", "زر حذف وإلغاء (Delete)"])
        self.table_matrix.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_matrix)

    # --- 👤 2. تبويب الموظفين ---
    def init_accounts_tab(self):
        layout = QHBoxLayout(self.tab_accounts); layout.setContentsMargins(15, 15, 15, 15); layout.setSpacing(15)
        
        # يسار: جدول عرض الموظفين الحاليين
        left_layout = QVBoxLayout()
        self.table_users = QTableWidget(); self.table_users.setColumnCount(4)
        self.table_users.setHorizontalHeaderLabels(["ID", "اسم المستخدم (Login)", "الاسم بالكامل", "الوظيفة الحالية"])
        self.table_users.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        left_layout.addWidget(self.table_users)
        layout.addLayout(left_layout, stretch=3)
        
        # يمين: إضافة مستخدم جديد
        right_panel = QFrame(); right_panel.setObjectName("cardBox"); right_panel.setFixedWidth(300)
        p_layout = QFormLayout(right_panel); p_layout.setSpacing(12); p_layout.setContentsMargins(15, 15, 15, 15)
        
        self.txt_u_login = QLineEdit()
        self.txt_u_name = QLineEdit()
        self.txt_u_pass = QLineEdit(); self.txt_u_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.cmb_u_role = QComboBox()
        self.cmb_u_role.addItems(["CASHIER", "ACCOUNTANT", "STOCKKEEPER", "ADMIN"])
        btn_save_user = QPushButton("👤 إنشاء حساب الموظف"); btn_save_user.setObjectName("primaryBtn"); btn_save_user.clicked.connect(self.submit_user_form)
        
        p_layout.addRow(QLabel("اسم المستخدم بالإنجليزية:"), self.txt_u_login)
        p_layout.addRow(QLabel("الاسم الكامل للموظف:"), self.txt_u_name)
        p_layout.addRow(QLabel("كلمة المرور السرية:"), self.txt_u_pass)
        p_layout.addRow(QLabel("الدور الوظيفي:"), self.cmb_u_role)
        p_layout.addRow(QLabel(""), btn_save_user)
        layout.addWidget(right_panel, stretch=1)

    # --- ⚙️ المنطق البرمجي وإدارة الخانات الاختيارية ---
    def refresh_users_list(self):
        try:
            users = self.controller.load_users()
            self.table_users.setRowCount(0)
            if not users: return
            role_ar = {"ADMIN": "مدير النظام", "CASHIER": "كاشير المبيعات", "ACCOUNTANT": "المحاسب المالي", "STOCKKEEPER": "أمين المستودع"}
            for r_idx, row in enumerate(users):
                self.table_users.insertRow(r_idx)
                self.table_users.setItem(r_idx, 0, QTableWidgetItem(str(row[0])))
                self.table_users.setItem(r_idx, 1, QTableWidgetItem(row[1]))
                self.table_users.setItem(r_idx, 2, QTableWidgetItem(row[2]))
                self.table_users.setItem(r_idx, 3, QTableWidgetItem(role_ar.get(row[3], row[3])))
        except Exception as e:
            print(f"Error refreshing users list: {e}")

    def load_role_permissions_matrix(self):
        """بناء خانات الاختيار (Checkboxes) ديناميكياً داخل الجدول بناء على دور الموظف المحدد"""
        try:
            role = self.cmb_roles_filter.currentText().split(" ")[1].replace("(", "").replace(")", "")
        except (IndexError, AttributeError):
            role = "CASHIER"
            
        db_perms = self.controller.load_permissions(role)
        
        if not db_perms or isinstance(db_perms, bool):
            db_perms = []
        
        try:
            perm_dict = {row[0]: (row[1], row[2], row[3], row[4]) for row in db_perms}
        except (IndexError, TypeError):
            perm_dict = {}
        
        self.table_matrix.setRowCount(0)
        for r_idx, (screen_code, screen_title) in enumerate(self.screen_mapping.items()):
            self.table_matrix.insertRow(r_idx)
            self.table_matrix.setItem(r_idx, 0, QTableWidgetItem(screen_title))
            
            v_val, a_val, e_val, d_val = perm_dict.get(screen_code, (False, False, False, False))
            is_admin = (role == 'ADMIN')
            
            for c_idx, checked_state in enumerate([v_val, a_val, e_val, d_val], start=1):
                cb = QCheckBox()
                cb.setChecked(checked_state if not is_admin else True)
                if is_admin: 
                    cb.setEnabled(False)
                
                cell_widget = QWidget()
                cell_layout = QHBoxLayout(cell_widget)
                cell_layout.addWidget(cb)
                cell_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell_layout.setContentsMargins(0, 0, 0, 0)
                
                self.table_matrix.setCellWidget(r_idx, c_idx, cell_widget)
                cb.setProperty("screen_code", screen_code)

    def submit_permissions_matrix(self):
        try:
            role = self.cmb_roles_filter.currentText().split(" ")[1].replace("(", "").replace(")", "")
            if role == 'ADMIN': return
            
            for row in range(self.table_matrix.rowCount()):
                screen_code = list(self.screen_mapping.keys())[row]
                
                v = self.table_matrix.cellWidget(row, 1).findChild(QCheckBox).isChecked()
                a = self.table_matrix.cellWidget(row, 2).findChild(QCheckBox).isChecked()
                e = self.table_matrix.cellWidget(row, 3).findChild(QCheckBox).isChecked()
                d = self.table_matrix.cellWidget(row, 4).findChild(QCheckBox).isChecked()
                
                self.controller.save_permission(role, screen_code, v, a, e, d)
                
            QMessageBox.information(self, "نجاح الحفظ", f"🛡️ تم تحديث مصفوفة الأزرار والشاشات لدور ({role})، وسيتم تطبيق الحظر حياً فور إيقاظ السيستم!")
        except Exception as e:
            QMessageBox.critical(self, "خطأ في الحفظ", f"فشلت عملية حفظ المصفوفة: {e}")

    def submit_user_form(self):
        login = self.txt_u_login.text().strip().lower()
        name = self.txt_u_name.text().strip()
        pwd = self.txt_u_pass.text().strip()
        role = self.cmb_u_role.currentText()
        
        if not login or not name or not pwd: 
            QMessageBox.warning(self, "تنبيه", "يرجى ملء جميع الحقول لإنشاء الحساب!")
            return
        try:
            self.controller.create_user(login, name, role, pwd)
            QMessageBox.information(self, "نجاح الإنشاء", f"👤 تم تسجيل الموظف ({name}) على السيستم كـ {role} بنجاح!")
            self.txt_u_login.clear(); self.txt_u_name.clear(); self.txt_u_pass.clear()
            self.refresh_users_list()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل إنشاء الحساب: {e}")


# =========================================================================
# 🚀 كود التشغيل المستقل المؤطر لضمان فتح الشاشة بالشكل والمقاس الصحيح
# =========================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft) # دعم الاتجاه العربي
    
    widget = UsersManagementWidget()
    widget.setWindowTitle("فحص معزول - مصفوفة تحكم حسابات الموظفين")
    widget.resize(1100, 650)
    widget.show()
    sys.exit(app.exec())