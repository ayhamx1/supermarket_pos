# -*- coding: utf-8 -*-
"""
Supermarket POS - Users & Permissions UI (Windows 11 Fluent Style)
Path: ui/admin/permissions_management.py
"""
import sys
import os

# =========================================================================
# 🛠️ حل مشكلة الـ ModuleNotFoundError تلقائياً عند التشغيل المنفرد للشاشة
# =========================================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QFrame, QMessageBox, QApplication, QAbstractItemView, QCheckBox, QComboBox, QTabWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from app.controllers.auth.permissions_controller import PermissionsController

PERM_STYLE = """
    QWidget { background-color: #F3F3F3; font-family: 'Segoe UI', 'Arial'; color: #1B1B1B; }
    QTabWidget::panel { border: 1px solid #E5E5E5; background: #FFFFFF; border-radius: 4px; padding: 12px; }
    QTabBar::tab { background: #E9E9E9; border: 1px solid #E5E5E5; padding: 8px 16px; font-size: 13px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
    QTabBar::tab:selected { background: #FFFFFF; border-bottom-color: #FFFFFF; font-weight: 600; color: #0067B8; }
    
    QFrame#matrixCard { background: #F9F9F9; border: 1px solid #E5E5E5; border-radius: 4px; padding: 16px; }
    QComboBox { border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 10px; background: #FFFFFF; font-size: 13px; min-width: 160px; }
    
    QTableWidget { background-color: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 4px; }
    QHeaderView::section { background-color: #F9F9F9; font-weight: 600; border: 1px solid #E5E5E5; padding: 6px; font-size: 13px; }
    
    QCheckBox { font-size: 13px; padding: 4px; }
    QPushButton { background-color: #0067B8; color: #FFFFFF; border: none; border-radius: 4px; padding: 8px 16px; font-size: 13px; font-weight: 600; }
    QPushButton:hover { background-color: #005A9E; }
    QPushButton#btnRefresh { background-color: #FFFFFF; color: #1B1B1B; border: 1px solid #CCCCCC; }
    QPushButton#btnRefresh:hover { background-color: #F5F5F5; }
"""

class PermissionsManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = PermissionsController()
        
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(PERM_STYLE)
        
        self.init_ui()
        self.refresh_users_table()
        self.refresh_audit_logs()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)
        
        title_lbl = QLabel("إدارة المستخدمين، الصلاحيات، وسجل الرقابة والأمان")
        title_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        main_layout.addWidget(title_lbl)
        
        # استخدام نظام التبويب (Tabs) للفصل المنظم لويندوز 11
        self.tabs = QTabWidget()
        
        # 🟢 التبويب الأول: قائمة الموظفين والأدوار
        self.tab_users = QWidget()
        users_layout = QVBoxLayout(self.tab_users)
        self.table_users = QTableWidget()
        self.table_users.setColumnCount(5)
        self.table_users.setHorizontalHeaderLabels(["رقم الموظف", "اسم المستخدم", "الاسم بالكامل", "الدور الوظيفي", "حالة الحساب"])
        self.table_users.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_users.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        users_layout.addWidget(self.table_users)
        self.tabs.addTab(self.tab_users, "قائمة الموظفين والأدوار")
        
        # 🔵 التبويب الثاني: مصفوفة التحكم بالصلاحيات الشاشات والأزرار
        self.tab_matrix = QWidget()
        matrix_layout = QVBoxLayout(self.tab_matrix)
        matrix_layout.setSpacing(16)
        
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("اختر الدور الوظيفي لتعديل صلاحياته الموحدة:"))
        self.cmb_roles = QComboBox()
        self.cmb_roles.addItems(["كاشير", "محاسب", "مدير"])
        self.cmb_roles.currentIndexChanged.connect(self.load_role_permissions_to_ui)
        selector_layout.addWidget(self.cmb_roles)
        selector_layout.addStretch()
        matrix_layout.addLayout(selector_layout)
        
        # كارت الخيارات
        self.matrix_card = QFrame()
        self.matrix_card.setObjectName("matrixCard")
        card_layout = QVBoxLayout(self.matrix_card)
        card_layout.setSpacing(12)
        
        card_layout.addWidget(QLabel("صلاحيات الشاشات الأساسية:"))
        self.chk_screen_pos = QCheckBox("السماح بالدخول إلى شاشة نقطة البيع والـ POS")
        card_layout.addWidget(self.chk_screen_pos)
        
        card_layout.addSpacing(8)
        card_layout.addWidget(QLabel("صلاحيات الأزرار والعمليات الحساسة داخل المبيعات:"))
        self.chk_btn_discount = QCheckBox("السماح للموظف بعمل خصم نقدي أو نسبي على الفاتورة")
        self.chk_btn_price = QCheckBox("السماح للموظف بتعديل السعر الافتراضي للسلعة أثناء البيع")
        self.chk_btn_delete = QCheckBox("السماح للموظف بحذف صنف من سلة المبيعات بعد إدراجه")
        
        card_layout.addWidget(self.chk_btn_discount)
        card_layout.addWidget(self.chk_btn_price)
        card_layout.addWidget(self.chk_btn_delete)
        
        matrix_layout.addWidget(self.matrix_card)
        
        self.btn_save_matrix = QPushButton("حفظ مصفوفة صلاحيات هذا الدور")
        self.btn_save_matrix.clicked.connect(self.handle_save_matrix)
        matrix_layout.addWidget(self.btn_save_matrix)
        matrix_layout.addStretch()
        
        self.tabs.addTab(self.tab_matrix, "مصفوفة صلاحيات الشاشات والأزرار")
        
        # 🔴 التبويب الثالث: سجل العمليات والرقابة الأمنية (Audit Log)
        self.tab_audit = QWidget()
        audit_layout = QVBoxLayout(self.tab_audit)
        audit_layout.setSpacing(8)
        
        audit_top = QHBoxLayout()
        audit_top.addWidget(QLabel("سجل حركة الموظفين والعمليات الحساسة الفورية بالنظام (آخر 100 حركة)"))
        audit_top.addStretch()
        self.btn_refresh_audit = QPushButton("تحديث السجل")
        self.btn_refresh_audit.setObjectName("btnRefresh")
        self.btn_refresh_audit.clicked.connect(self.refresh_audit_logs)
        audit_top.addWidget(self.btn_refresh_audit)
        audit_layout.addLayout(audit_top)
        
        self.table_audit = QTableWidget()
        self.table_audit.setColumnCount(5)
        self.table_audit.setHorizontalHeaderLabels(["التاريخ والوقت", "الموظف المسؤول", "الدور", "نوع الإجراء", "تفصيل البيان المالي / الرقابي"])
        self.table_audit.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_audit.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        audit_layout.addWidget(self.table_audit)
        
        self.tabs.addTab(self.tab_audit, "سجل العمليات والأمان (Audit Log)")
        
        main_layout.addWidget(self.tabs)
        
        # تحميل أولي للبيانات الخاصة بأول دور في القائمة
        self.load_role_permissions_to_ui()

    def refresh_users_table(self):
        try:
            self.table_users.setRowCount(0)
            users = self.controller.load_users_list()
            if not users: return
            for r, row in enumerate(users):
                self.table_users.insertRow(r)
                self.table_users.setItem(r, 0, QTableWidgetItem(str(row[0])))
                self.table_users.setItem(r, 1, QTableWidgetItem(str(row[1])))
                self.table_users.setItem(r, 2, QTableWidgetItem(str(row[2])))
                self.table_users.setItem(r, 3, QTableWidgetItem(str(row[3])))
                
                status_str = "نشط ومصرح له" if row[4] else "موقوف مؤقتاً"
                status_item = QTableWidgetItem(status_str)
                if not row[4]:
                    status_item.setForeground(QColor("#C42B1C"))
                self.table_users.setItem(r, 4, status_item)
        except Exception as e:
            print(f"Error refreshing users table: {e}")

    def load_role_permissions_to_ui(self):
        try:
            role_name = self.cmb_roles.currentText()
            perms = self.controller.get_permissions_for_role(role_name)
            if not perms: return
            
            self.chk_screen_pos.setChecked(perms.get('screen_pos', False))
            self.chk_btn_discount.setChecked(perms.get('button_discount', False))
            self.chk_btn_price.setChecked(perms.get('button_change_price', False))
            self.chk_btn_delete.setChecked(perms.get('button_delete_item', False))
        except Exception as e:
            print(f"Error loading role permissions: {e}")

    def handle_save_matrix(self):
        role_name = self.cmb_roles.currentText()
        success = self.controller.update_role_matrix(
            role_name,
            self.chk_screen_pos.isChecked(),
            self.chk_btn_discount.isChecked(),
            self.chk_btn_price.isChecked(),
            self.chk_btn_delete.isChecked()
        )
        if success:
            QMessageBox.information(self, "أمن النظام", f"تم تحديث مصفوفة الصلاحيات الخاصة بدور ({role_name}) بنجاح، وسيتم تطبيقها تلقائياً عند تسجيل الدخول القادم.")
            self.controller.write_audit(1, "تعديل صلاحيات", f"تعديل صلاحيات المجموعة الوظيفية: {role_name}")
            self.refresh_audit_logs()
        else:
            QMessageBox.warning(self, "خطأ بالخادم", "فشلت عملية حفظ الصلاحيات في قاعدة البيانات.")

    def refresh_audit_logs(self):
        try:
            self.table_audit.setRowCount(0)
            logs = self.controller.load_audit_history()
            if not logs: return
            for r, row in enumerate(logs):
                self.table_audit.insertRow(r)
                self.table_audit.setItem(r, 0, QTableWidgetItem(str(row[0])))
                self.table_audit.setItem(r, 1, QTableWidgetItem(str(row[1])))
                self.table_audit.setItem(r, 2, QTableWidgetItem(str(row[2])))
                self.table_audit.setItem(r, 3, QTableWidgetItem(str(row[3])))
                self.table_audit.setItem(r, 4, QTableWidgetItem(str(row[4])))
        except Exception as e:
            print(f"Error refreshing audit logs: {e}")

# =========================================================================
# 🚀 كود التشغيل المستقل (يضمن توجيه اللغة الصحيح للواجهة العربية)
# =========================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft) # تأمين اتجاه الواجهة العربية
    
    w = PermissionsManagementWidget()
    w.setWindowTitle("فحص معزول - إدارة الصلاحيات والرقابة")
    w.resize(1000, 650)
    w.show()
    sys.exit(app.exec())