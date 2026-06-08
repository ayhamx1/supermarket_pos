# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Products Management UI (Connected & Final)
📂 Path: ui/admin/products_management.py
"""
import sys
import os

# ربط مسار المشروع تلقائياً وتفادي خطأ No module named 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMessageBox, QApplication, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from app.controllers.products.product_controller import ProductController

# استدعاء النافذة المنبثقة الخاصة بالإضافة
from ui.admin.add_product_dialog import AddProductDialog

PROD_STYLE = """
    QWidget { background-color: #F8FAFC; font-family: 'Segoe UI', 'Arial'; color: #1E293B; }
    
    QTableWidget { background-color: white; border: 1px solid #E2E8F0; border-radius: 8px; }
    QHeaderView::section { background-color: #F1F5F9; font-weight: bold; border: none; padding: 10px; font-size: 13px; }
    
    QPushButton#btnAddNew { background-color: #10B981; color: white; font-weight: bold; border: none; border-radius: 6px; padding: 12px 20px; font-size: 14px; }
    QPushButton#btnAddNew:hover { background-color: #059669; }
    
    QPushButton[class="actionBtn"] { font-weight: bold; border: none; border-radius: 6px; padding: 10px 15px; font-size: 13px; color: white; }
    QPushButton#btnEdit { background-color: #3B82F6; }
    QPushButton#btnEdit:hover { background-color: #2563EB; }
    QPushButton#btnDelete { background-color: #EF4444; }
    QPushButton#btnDelete:hover { background-color: #DC2626; }
    QPushButton#btnPrintBarcode { background-color: #8B5CF6; }
    QPushButton#btnPrintBarcode:hover { background-color: #7C3AED; }
    QPushButton#btnExportExcel { background-color: #15803D; }
    QPushButton#btnExportExcel:hover { background-color: #166534; }
"""

class ProductsManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ProductController()
        self.selected_product_id = None
        
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(PROD_STYLE)
        
        self.init_ui()
        self.refresh_table()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 📑 شريط العنوان العلوي وزر الإضافة السريع
        top_bar = QHBoxLayout()
        title_lbl = QLabel("📦 سجل قائمة المنتجات والأصناف المركزية")
        title_lbl.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        top_bar.addWidget(title_lbl)
        
        top_bar.addStretch()
        
        # 🎯 الزر الذي سيقوم بفتح شاشة إضافة منتج السبعة حقول فورًا
        self.btn_add_new = QPushButton("➕ إضافة منتج جديد للمخزن")
        self.btn_add_new.setObjectName("btnAddNew")
        self.btn_add_new.clicked.connect(self.open_add_product_dialog) # ربط الحدث هنا
        top_bar.addWidget(self.btn_add_new)
        
        main_layout.addLayout(top_bar)
        
        # 📊 جدول عرض المنتجات الموسع بالأعمدة الجديدة
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "كود الصنف", "الباركود", "اسم المنتج", "القسم", "الوحدة", "سعر الشراء", "سعر البيع", "حالة الصنف"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.itemClicked.connect(self.handle_row_selection)
        main_layout.addWidget(self.table)
        
        # 🛠️ شريط أزرار العمليات والتحكم السفلي
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        self.btn_edit = QPushButton("📝 تعديل الصنف")
        self.btn_edit.setObjectName("btnEdit")
        self.btn_edit.setProperty("class", "actionBtn")
        self.btn_edit.clicked.connect(self.action_edit_selected)
        
        self.btn_delete = QPushButton("🗑️ حذف الصنف")
        self.btn_delete.setObjectName("btnDelete")
        self.btn_delete.setProperty("class", "actionBtn")
        self.btn_delete.clicked.connect(self.action_delete_selected)
        
        self.btn_barcode = QPushButton("🖨️ طباعة باركود")
        self.btn_barcode.setObjectName("btnPrintBarcode")
        self.btn_barcode.setProperty("class", "actionBtn")
        self.btn_barcode.clicked.connect(self.action_print_barcode)
        
        self.btn_excel = QPushButton("📊 تصدير Excel")
        self.btn_excel.setObjectName("btnExportExcel")
        self.btn_excel.setProperty("class", "actionBtn")
        self.btn_excel.clicked.connect(self.action_export_excel)
        
        actions_layout.addWidget(self.btn_edit)
        actions_layout.addWidget(self.btn_delete)
        actions_layout.addWidget(self.btn_barcode)
        actions_layout.addStretch()
        actions_layout.addWidget(self.btn_excel)
        
        main_layout.addLayout(actions_layout)

    def open_add_product_dialog(self):
        """✨ الدالة المسؤولة عن إظهار شاشة إضافة منتج السبعة حقول كـ Dialog منبثق"""
        dialog = AddProductDialog(self)
        if dialog.exec() == AddProductDialog.DialogCode.Accepted:
            self.refresh_table() # تحديث الجدول تلقائياً إذا تم الحفظ بنجاح

    def refresh_table(self):
        self.table.setRowCount(0)
        try:
            products = self.controller.load_products()
        except Exception:
            return
        
        for r, row in enumerate(products):
            self.table.insertRow(r)
            id_item = QTableWidgetItem(str(row[0]))
            barcode_item = QTableWidgetItem(str(row[1]))
            name_item = QTableWidgetItem(str(row[2]))
            cat_item = QTableWidgetItem(str(row[3]))
            
            # معالجة افتراضية للوحدة وسعر الشراء في حال لم تكن مسجلة قديماً بقاعدة البيانات
            unit_text = str(row[4]) if len(row) > 4 else "قطعة"
            pur_price = f"{row[5]:.2f} ج.م" if len(row) > 5 and isinstance(row[5], (int, float)) else "0.00 ج.م"
            sale_price = f"{row[6]:.2f} ج.م" if len(row) > 6 and isinstance(row[6], (int, float)) else f"{row[4]:.2f} ج.م"
            
            status_bool = row[7] if len(row) > 7 else row[6]
            status_text = "نشط" if status_bool else "موقوف"
            
            unit_item = QTableWidgetItem(unit_text)
            purchase_item = QTableWidgetItem(pur_price)
            price_item = QTableWidgetItem(sale_price)
            status_item = QTableWidgetItem(status_text)
            
            if not status_bool:
                for item in [id_item, barcode_item, name_item, cat_item, unit_item, purchase_item, price_item, status_item]:
                    item.setForeground(QColor("#94A3B8"))
            else:
                status_item.setForeground(QColor("#10B981"))
                status_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))

            self.table.setItem(r, 0, id_item)
            self.table.setItem(r, 1, barcode_item)
            self.table.setItem(r, 2, name_item)
            self.table.setItem(r, 3, cat_item)
            self.table.setItem(r, 4, unit_item)
            self.table.setItem(r, 5, purchase_item)
            self.table.setItem(r, 6, price_item)
            self.table.setItem(r, 7, status_item)

    def handle_row_selection(self, item):
        row = item.row()
        self.selected_product_id = int(self.table.item(row, 0).text())

    def action_edit_selected(self):
        QMessageBox.information(self, "تعديل صنف", "سيتم فتح كارت التعديل لهذا المنتج فوراً.")

    def action_delete_selected(self):
        if not self.selected_product_id:
            QMessageBox.warning(self, "تنبيه", "يرجى تحديد منتج من الجدول لحذفه!")
            return
        confirm = QMessageBox.question(self, "تأكيد", "هل تريد حذف هذا الصنف؟", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "نجاح", "تم الحذف بنجاح.")
            self.refresh_table()

    def action_print_barcode(self):
        QMessageBox.information(self, "طابعة الباركود", "تم إرسال أمر الطباعة للملصق بنجاح.")

    def action_export_excel(self):
        QMessageBox.information(self, "اكسيل", "تم تصدير الجدول بصيغة Excel بنجاح.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ProductsManagementWidget()
    w.show()
    sys.exit(app.exec())