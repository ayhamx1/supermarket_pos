# -*- coding: utf-8 -*-
"""
Supermarket POS - Inventory Management UI (Windows 11 Fluent Style)
Path: ui/admin/inventory_management.py
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QFrame, QLineEdit, QMessageBox, QApplication, QAbstractItemView, QDialog, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from app.controllers.inventory.inventory_controller import InventoryController

INVENTORY_STYLE = """
    QWidget { background-color: #F3F3F3; font-family: 'Segoe UI', 'Arial'; color: #1B1B1B; }
    QFrame#toolBarFrame { background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 4px; padding: 12px; }
    QLineEdit { border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 10px; background: #FFFFFF; font-size: 13px; }
    QLineEdit:focus { border: 2px solid #0067B8; }
    
    QTableWidget { background-color: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 4px; }
    QHeaderView::section { background-color: #F9F9F9; font-weight: 600; border: 1px solid #E5E5E5; padding: 8px; font-size: 13px; }
    
    QPushButton { background-color: #FFFFFF; border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 12px; font-size: 13px; color: #1B1B1B; }
    QPushButton:hover { background-color: #F5F5F5; }
    
    QPushButton#btnActionBlue { background-color: #0067B8; color: #FFFFFF; border: none; font-weight: 600; }
    QPushButton#btnActionBlue:hover { background-color: #005A9E; }
    
    QCheckBox { font-size: 13px; }
"""

class InventoryManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = InventoryController()
        self.selected_item_id = None
        self.selected_item_name = ""
        
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(INVENTORY_STYLE)
        
        self.init_ui()
        self.refresh_inventory()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        title_lbl = QLabel("إدارة المخزون والرقابة على الأرصدة")
        title_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title_lbl)
        
        # شريط الأدوات العلوي (البحث والتصنيفات)
        toolbar = QFrame()
        toolbar.setObjectName("toolBarFrame")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(8, 4, 8, 4)
        toolbar_layout.setSpacing(12)
        
        toolbar_layout.addWidget(QLabel("البحث عن صنف:"))
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("ادخل اسم الصنف أو الباركود...")
        self.txt_search.textChanged.connect(self.refresh_inventory)
        toolbar_layout.addWidget(self.txt_search)
        
        self.chk_low_stock = QCheckBox("عرض تنبيهات النواقص فقط (تحت حد الطلب)")
        self.chk_low_stock.stateChanged.connect(self.refresh_inventory)
        toolbar_layout.addWidget(self.chk_low_stock)
        
        toolbar_layout.addStretch()
        layout.addWidget(toolbar)
        
        # جدول عرض الأرصدة
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["الرقم", "الباركود", "اسم الصنف", "الرصيد الحالي", "حد الطلب الآمن", "الوحدة"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.itemClicked.connect(self.handle_row_selection)
        layout.addWidget(self.table)
        
        # أزرار الإجراءات السفلية (الجرد والتسويات وحركة الصنف)
        actions_layout = QHBoxLayout()
        
        self.btn_movements = QPushButton("عرض حركة الصنف التفصيلية")
        self.btn_movements.clicked.connect(self.open_movements_log)
        actions_layout.addWidget(self.btn_movements)
        
        self.btn_adjustment = QPushButton("تسوية كمية الصنف (جرد)")
        self.btn_adjustment.setObjectName("btnActionBlue")
        self.btn_adjustment.clicked.connect(self.open_adjustment_dialog)
        actions_layout.addWidget(self.btn_adjustment)
        
        actions_layout.addStretch()
        layout.addLayout(actions_layout)

    def refresh_inventory(self):
        self.table.setRowCount(0)
        search_query = self.txt_search.text().strip()
        low_stock_only = self.chk_low_stock.isChecked()
        
        items_data = self.controller.get_stock_list(search_query, low_stock_only)
        
        for r, row in enumerate(items_data):
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(r, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(r, 2, QTableWidgetItem(str(row[2])))
            
            stock_qty = float(row[3])
            min_level = float(row[4])
            
            qty_item = QTableWidgetItem(f"{stock_qty:,.2f}")
            min_item = QTableWidgetItem(f"{min_level:,.2f}")
            
            # تلوين السطر باللون الأحمر إذا وصل الصنف إلى حد النواقص
            if stock_qty <= min_level:
                qty_item.setForeground(QColor("#C42B1C"))
                qty_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                
            self.table.setItem(r, 3, qty_item)
            self.table.setItem(r, 4, min_item)
            self.table.setItem(r, 5, QTableWidgetItem(str(row[5])))

    def handle_row_selection(self):
        row = self.table.currentRow()
        if row != -1:
            self.selected_item_id = int(self.table.item(row, 0).text())
            self.selected_item_name = self.table.item(row, 2).text()

    def open_movements_log(self):
        if not self.selected_item_id:
            QMessageBox.warning(self, "تنبيه", "يرجى اختيار الصنف من الجدول أولاً")
            return
        dialog = StockMovementsDialog(self.selected_item_id, self.selected_item_name, self.controller)
        dialog.exec()

    def open_adjustment_dialog(self):
        if not self.selected_item_id:
            QMessageBox.warning(self, "تنبيه", "يرجى اختيار الصنف لإجراء التسووية الجردية")
            return
            
        row = self.table.currentRow()
        current_qty = self.table.item(row, 3).text().replace(",", "")
        
        dialog = AdjustmentDialog(self.selected_item_id, self.selected_item_name, current_qty, self.controller)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_inventory()
            self.selected_item_id = None

# ─── شاشة منبثقة تفصيلية لحركة الصنف ───
class StockMovementsDialog(QDialog):
    def __init__(self, item_id, item_name, controller):
        super().__init__()
        self.item_id = item_id
        self.item_name = item_name
        self.controller = controller
        
        self.setWindowTitle(f"سجل حركات المخزون - {self.item_name}")
        self.resize(750, 400)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        title = QLabel(f"تقرير حركة الصنف التاريخي: {self.item_name}")
        title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        layout.addWidget(title)
        
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["التاريخ والوقت", "نوع العملية", "الكمية", "رقم الفاتورة", "ملاحظات التسووية"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        movements = self.controller.get_movements_log(self.item_id)
        table.setRowCount(0)
        
        # ترجمة مصطلحات قاعدة البيانات إلى لغة عربية نصية ونظيفة
        type_mapping = {
            "sale": "فاتورة مبيعات",
            "purchase": "فاتورة مشتريات",
            "adjustment_in": "تسووية زيادة مخزنية",
            "adjustment_out": "تسووية عجز مخزني",
            "return_in": "مرتجع مبيعات",
            "return_out": "مرتجع مشتريات"
        }
        
        for r, row in enumerate(movements):
            table.insertRow(r)
            table.setItem(r, 0, QTableWidgetItem(str(row[0])))
            
            friendly_type = type_mapping.get(row[1], str(row[1]))
            table.setItem(r, 1, QTableWidgetItem(friendly_type))
            
            table.setItem(r, 2, QTableWidgetItem(f"{float(row[2]):,.2f}"))
            table.setItem(r, 3, QTableWidgetItem(str(row[3]) if row[3] else "لا يوجد"))
            table.setItem(r, 4, QTableWidgetItem(str(row[4]) if row[4] else "لا يوجد"))
            
        layout.addWidget(table)
        
        btn_close = QPushButton("إغلاق السجل")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

# ─── شاشة منبثقة لإجراء التسويات المخزنية (الجرد) ───
class AdjustmentDialog(QDialog):
    def __init__(self, item_id, item_name, current_qty, controller):
        super().__init__()
        self.item_id = item_id
        self.item_name = item_name
        self.current_qty = current_qty
        self.controller = controller
        
        self.setWindowTitle("تسووية جردية للصنف")
        self.setFixedWidth(360)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        layout.addWidget(QLabel(f"الصنف المراد تسويته: {self.item_name}"))
        layout.addWidget(QLabel(f"الرصيد الدفتري الحالي بالنظام: {self.current_qty}"))
        
        layout.addWidget(QLabel("الكمية الفعلية الجديدة بعد الجرد المعملي:"))
        self.txt_new_qty = QLineEdit()
        self.txt_new_qty.setPlaceholderText("ادخل الكمية الحقيقية...")
        layout.addWidget(self.txt_new_qty)
        
        layout.addWidget(QLabel("سبب التسووية (ملاحظات الجرد):"))
        self.txt_notes = QLineEdit()
        self.txt_notes.setPlaceholderText("مثال: تالف، عجز جرد سنوي، صنف زائد...")
        layout.addWidget(self.txt_notes)
        
        buttons = QHBoxLayout()
        self.btn_save = QPushButton("اعتماد التسووية")
        self.btn_save.clicked.connect(self.save_adjustment)
        buttons.addWidget(self.btn_save)
        
        self.btn_cancel = QPushButton("إلغاء")
        self.btn_cancel.clicked.connect(self.reject)
        buttons.addWidget(self.btn_cancel)
        layout.addLayout(buttons)

    def save_adjustment(self):
        try:
            new_qty = float(self.txt_new_qty.text().strip())
        except ValueError:
            QMessageBox.warning(self, "خطأ في الإدخال", "يرجى كتابة كمية صحيحة عددياً")
            return
            
        notes = self.txt_notes.text().strip()
        if not notes:
            QMessageBox.warning(self, "خطأ في الإدخال", "يرجى كتابة سبب التسووية المخزنية")
            return
            
        success, msg = self.controller.process_adjustment(self.item_id, new_qty, notes)
        if success:
            QMessageBox.information(self, "نجاح الإجراء", msg)
            self.accept()
        else:
            QMessageBox.warning(self, "فشل الإجراء", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = InventoryManagementWidget()
    w.show()
    sys.exit(app.exec())