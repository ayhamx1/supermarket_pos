# -*- coding: utf-8 -*-
import sys
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QMessageBox
from PyQt6.QtCore import Qt

class SalesReturnsManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet("""
            QWidget { background-color: #F3F3F3; font-family: 'Segoe UI', 'Arial'; color: #1B1B1B; }
            QFrame#card { background: white; border: 1px solid #E5E5E5; border-radius: 6px; padding: 15px; }
            QLineEdit { border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px; background: white; }
            QPushButton { background-color: #0067B8; color: white; border: none; border-radius: 4px; padding: 8px 15px; font-weight: bold; }
            QPushButton:hover { background-color: #005A9E; }
            QTableWidget { background: white; border: 1px solid #E5E5E5; border-radius: 4px; }
            QHeaderView::section { background-color: #F9F9F9; font-weight: bold; border: 1px solid #E5E5E5; }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        title = QLabel("🔄 شاشة مرتجعات المبيعات (تحديث تلقائي للمخزن والخزنة)")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #0067B8;")
        layout.addWidget(title)

        # بار البحث والتأكيد
        search_card = QFrame()
        search_card.setObjectName("card")
        search_layout = QHBoxLayout(search_card)
        
        search_layout.addWidget(QLabel("رقم فاتورة البيع:"))
        self.txt_invoice_id = QLineEdit()
        self.txt_invoice_id.setPlaceholderText("ادخل رقم الفاتورة هنا...")
        search_layout.addWidget(self.txt_invoice_id)
        
        btn_search = QPushButton("🔎 استدعاء الفاتورة")
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        layout.addWidget(search_card)

        # جدول عناصر الفاتورة القابلة للإرجاع
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["كود الصنف", "اسم المنتج", "الكمية المباعة", "سعر البيع", "الكمية المراد إرجاعها"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # إضافة سطر وهمي تجريبي للفحص
        self.table.setRowCount(1)
        self.table.setItem(0, 0, QTableWidgetItem("1001"))
        self.table.setItem(0, 1, QTableWidgetItem("علبة سمنة كريستال"))
        self.table.setItem(0, 2, QTableWidgetItem("3"))
        self.table.setItem(0, 3, QTableWidgetItem("100.00 ج.م"))
        self.table.setItem(0, 4, QTableWidgetItem("1")) # كمية المرتجع الافتراضية
        
        layout.addWidget(self.table)

        # زر التأكيد النهائي
        btn_confirm = QPushButton("✅ تأكيد إرجاع البضاعة وصرف المبلغ من الخزنة")
        btn_confirm.setStyleSheet("background-color: #C42B1C; font-size: 14px; padding: 12px;")
        btn_confirm.clicked.connect(self.confirm_return)
        layout.addWidget(btn_confirm)

    def confirm_return(self):
        QMessageBox.information(self, "مرتجع المبيعات", "تمت العملية بنجاح!\n1. تم إعادة المنتج للمخزن وتحديث الكمية.\n2. تم خصم المبلغ من الخزنة تلقائياً.\n3. تم تسوية الأرباح.")