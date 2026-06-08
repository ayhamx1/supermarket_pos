# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - System Audit Logs & Monitoring UI
📂 Path: ui/admin/audit_logs_management.py
"""
import sys
import os

# 🛡️ تهيئة مسار المشروع الرئيسي فوراً ليتعرف بايثون على مجلد app عند التشغيل المباشر
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# استدعاء مكتبات واجهات المستخدم
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

# استدعاء الكنترولر المركزي المسؤول عن جرد السجلات من قاعدة البيانات
from app.controllers.auth.audit_controller import AuditController

class AuditLogsManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.controller = AuditController()
        
        # تطبيق تصميم متناسق مع نمط ويندوز 11 الفلوينت
        self.setStyleSheet("""
            QWidget { background-color: #F3F3F3; font-family: 'Segoe UI', 'Arial'; color: #1B1B1B; }
            QFrame#filterCard { background: white; border: 1px solid #E5E5E5; border-radius: 6px; padding: 12px; }
            QComboBox, QLineEdit { border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px; background: white; min-width: 150px; }
            QPushButton { background-color: #0067B8; color: white; border: none; border-radius: 4px; padding: 7px 16px; font-weight: 500; }
            QPushButton:hover { background-color: #005A9E; }
            QTableWidget { background: white; border: 1px solid #E5E5E5; border-radius: 4px; }
            QHeaderView::section { background-color: #F9F9F9; font-weight: bold; border: 1px solid #E5E5E5; padding: 6px; }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # عنوان الصفحة المركزي
        title_lbl = QLabel("🛡️ سجل العمليات والرقابة والأمان (Audit Log)")
        title_lbl.setStyleSheet("font-size: 16px; font-weight: 600; color: #1B1B1B;")
        layout.addWidget(title_lbl)

        # شريط الفلترة والبحث الذكي للمدير
        filter_card = QFrame()
        filter_card.setObjectName("filterCard")
        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(10, 10, 10, 10)
        filter_layout.setSpacing(15)

        filter_layout.addWidget(QLabel("نوع العملية:"))
        self.cmb_action_type = QComboBox()
        self.cmb_action_type.addItems(["الكل", "إضافة منتج", "تعديل سعر", "حذف فاتورة", "إغلاق وردية"])
        filter_layout.addWidget(self.cmb_action_type)

        filter_layout.addWidget(QLabel("بحث بالموظف:"))
        self.txt_search_user = QLineEdit()
        self.txt_search_user.setPlaceholderText("اكتب اسم الموظف...")
        filter_layout.addWidget(self.txt_search_user)

        btn_refresh = QPushButton("🔄 تحديث السجل")
        btn_refresh.clicked.connect(self.load_logs_into_table)
        filter_layout.addWidget(btn_refresh)
        
        filter_layout.addStretch()
        layout.addWidget(filter_card)

        # جدول عرض الحركات بالتفاصيل والـ IP
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["الموظف المسؤول", "نوع الحركة", "تفاصيل العملية الكاملة", "عنوان الجهاز IP", "التاريخ والوقت"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # جعل عمود التفاصيل يتمدد بالكامل
        
        layout.addWidget(self.table)
        
        # تحميل السجلات تلقائياً فور تشغيل الشاشة
        self.load_logs_into_table()

    def load_logs_into_table(self):
        """جلب البيانات من الكنترولر وتوزيعها على الجدول وتلوين الحركات الحساسة"""
        self.table.setRowCount(0)
        logs_data = self.controller.load_all_logs()
        
        for row_idx, data in enumerate(logs_data):
            self.table.insertRow(row_idx)
            
            user_item = QTableWidgetItem(data[1])
            type_item = QTableWidgetItem(data[2])
            details_item = QTableWidgetItem(data[3])
            ip_item = QTableWidgetItem(data[4])
            date_item = QTableWidgetItem(data[5])
            
            # الرقابة البصرية: تلوين عمليات الحذف أو التحذيرات باللون الأحمر لتنبيه المدير فوراً
            if "حذف" in data[2] or "⚠️" in data[3]:
                type_item.setForeground(QColor("#C42B1C"))
                type_item.setFont(QFont("Segoe UI", -1, QFont.Weight.Bold))
            elif "إغلاق" in data[2]:
                type_item.setForeground(QColor("#107C41")) # تلوين إغلاق الورديات باللون الأخضر المالي
                
            self.table.setItem(row_idx, 0, user_item)
            self.table.setItem(row_idx, 1, type_item)
            self.table.setItem(row_idx, 2, details_item)
            self.table.setItem(row_idx, 3, ip_item)
            self.table.setItem(row_idx, 4, date_item)

# تفعيل ميزة التشغيل التجريبي الفردي للملف الفرعي
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuditLogsManagementWidget()
    window.setWindowTitle("فحص سجل العمليات - تجريبي")
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec())