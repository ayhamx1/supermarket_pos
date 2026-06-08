# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Add Product Dialog
📂 Path: ui/admin/add_product_dialog.py
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
                             QLineEdit, QComboBox, QPushButton, QMessageBox, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from app.controllers.products.product_controller import ProductController

DIALOG_STYLE = """
    QDialog { background-color: #F8FAFC; font-family: 'Segoe UI', 'Arial'; }
    QLabel { font-size: 13px; font-weight: bold; color: #334155; }
    QLineEdit, QComboBox { border: 1px solid #CBD5E1; border-radius: 6px; padding: 8px; background: white; font-size: 13px; }
    QLineEdit:focus, QComboBox:focus { border: 2px solid #2563EB; }
    
    QPushButton#btnSave { background-color: #10B981; color: white; font-weight: bold; border: none; border-radius: 6px; padding: 10px 20px; font-size: 14px; }
    QPushButton#btnSave:hover { background-color: #059669; }
    QPushButton#btnCancel { background-color: #EF4444; color: white; font-weight: bold; border: none; border-radius: 6px; padding: 10px 20px; font-size: 14px; }
    QPushButton#btnCancel:hover { background-color: #DC2626; }
"""

class AddProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.controller = ProductController()
        
        self.setWindowTitle("➕ إضافة صنف جديد للمخزن")
        self.setFixedSize(460, 500)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(DIALOG_STYLE)
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        header_title = QLabel("📝 كارت البيانات الأساسية والمخزنية للمنتج")
        header_title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        header_title.setStyleSheet("color: #2563EB; border-bottom: 2px solid #E2E8F0; padding-bottom: 8px;")
        main_layout.addWidget(header_title)
        
        # شبكة المدخلات لضبط المسافات والمحاذاة التامة للأعمدة السبعة
        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)
        grid_layout.setColumnStretch(1, 1)
        
        # 1. اسم المنتج
        grid_layout.addWidget(QLabel("اسم المنتج *:"), 0, 0)
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("مثال: جبنة عبور لاند 500 جرام")
        grid_layout.addWidget(self.txt_name, 0, 1)
        
        # 2. الباركود
        grid_layout.addWidget(QLabel("باركود الصنف *:"), 1, 0)
        self.txt_barcode = QLineEdit()
        self.txt_barcode.setPlaceholderText("امسح بالليزر أو اكتب الباركود...")
        grid_layout.addWidget(self.txt_barcode, 1, 1)
        
        # 3. القسم
        grid_layout.addWidget(QLabel("القسم التابع له *:"), 2, 0)
        self.cmb_category = QComboBox()
        self.cmb_category.addItems(["ألبان وأجبان", "بقوليات ومواد جافة", "زيوت وسمن", "حلويات وتسالي", "منظفات", "مجمدات"])
        grid_layout.addWidget(self.cmb_category, 2, 1)
        
        # 4. الوحدة
        grid_layout.addWidget(QLabel("وحدة القياس *:"), 3, 0)
        self.cmb_unit = QComboBox()
        self.cmb_unit.addItems(["قطعة (Item)", "علبة (Box)", "كيلو جرام (Kg)", "كرتونة (Carton)", "لتر (Ltr)"])
        grid_layout.addWidget(self.cmb_unit, 3, 1)
        
        # 5. سعر الشراء
        grid_layout.addWidget(QLabel("سعر الشراء (ج.م) *:"), 4, 0)
        self.txt_purchase_price = QLineEdit()
        self.txt_purchase_price.setPlaceholderText("0.00")
        grid_layout.addWidget(self.txt_purchase_price, 4, 1)
        
        # 6. سعر البيع
        grid_layout.addWidget(QLabel("سعر البيع المقترح *:"), 5, 0)
        self.txt_sales_price = QLineEdit()
        self.txt_sales_price.setPlaceholderText("0.00")
        grid_layout.addWidget(self.txt_sales_price, 5, 1)
        
        # 7. الحد الأدنى للمخزون
        grid_layout.addWidget(QLabel("الحد الأدنى للنواقص *:"), 6, 0)
        self.txt_min_stock = QLineEdit()
        self.txt_min_stock.setText("10") 
        grid_layout.addWidget(self.txt_min_stock, 6, 1)
        
        main_layout.addLayout(grid_layout)
        main_layout.addSpacing(10)
        
        # أزرار الحفظ والإلغاء
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        
        self.btn_save = QPushButton("💾 حفظ المنتج الجديد")
        self.btn_save.setObjectName("btnSave")
        self.btn_save.clicked.connect(self.handle_add_product)
        
        self.btn_cancel = QPushButton("❌ إلغاء الأمر")
        self.btn_cancel.setObjectName("btnCancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.btn_save)
        buttons_layout.addWidget(self.btn_cancel)
        main_layout.addLayout(buttons_layout)

    def handle_add_product(self):
        success, msg = self.controller.validate_and_create_product(
            self.txt_barcode.text().strip(),
            self.txt_name.text().strip(),
            self.cmb_category.currentText(),
            self.cmb_unit.currentText(),
            self.txt_purchase_price.text().strip(),
            self.txt_sales_price.text().strip(),
            self.txt_min_stock.text().strip()
        )
        if success:
            QMessageBox.information(self, "نجاح 🎉", msg)
            self.accept()
        else:
            QMessageBox.warning(self, "خطأ مدخلات", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dial = AddProductDialog()
    dial.show()
    sys.exit(app.exec())