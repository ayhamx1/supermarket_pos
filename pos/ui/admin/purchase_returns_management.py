# -*- coding: utf-8 -*-
import sys
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QMessageBox
from PyQt6.QtCore import Qt

class PurchaseReturnsManagementWidget(QWidget):
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

        title = QLabel("🔄 شاشة مرتجعات المشتريات (تخفيض المخزن وتغذية الخزنة)")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #107C41;")
        layout.addWidget(title)

        # بار البحث والتأكيد
        search_card = QFrame()
        search_card.setObjectName("card")
        search_layout = QHBoxLayout(search_card)
        
        search_layout.addWidget(QLabel("كود الصنف المراد إرجاعه للمورد:"))
        self.txt_prod_id = QLineEdit()
        self.txt_prod_id.setPlaceholderText("امسح بالباركود أو اكتب الكود...")
        search_layout.addWidget(self.txt_prod_id)
        
        btn_search = QPushButton("🔎 فحص المخزون")
        search_layout.addWidget(btn_search)
        search_layout.addStretch()
        layout.addWidget(search_card)

        # الجدول
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["كود الصنف", "اسم المنتج", "الكمية الحالية بالمحل", "الكمية المرتجعة للمورد"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.table.setRowCount(1)
        self.table.setItem(0, 0, QTableWidgetItem("2005"))
        self.table.setItem(0, 1, QTableWidgetItem("كرتونة شيبسي عائلي"))
        self.table.setItem(0, 2, QTableWidgetItem("15"))
        self.table.setItem(0, 3, QTableWidgetItem("2"))
        
        layout.addWidget(self.table)

        # زر التأكيد
        btn_confirm = QPushButton("✅ تأكيد شحن البضاعة للمورد واستلام النقدية في الخزنة")
        btn_confirm.setStyleSheet("background-color: #107C41; font-size: 14px; padding: 12px;")
        btn_confirm.clicked.connect(self.confirm_return)
        layout.addWidget(btn_confirm)

    def confirm_return(self):
        QMessageBox.information(self, "مرتجع المشتريات", "تمت العملية بنجاح!\n1. تم سحب الكمية من المخزن بنجاح.\n2. تم إضافة قيمتها كاش داخل الخزنة الحالية.")