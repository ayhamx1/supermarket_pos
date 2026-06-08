# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Purchases Management UI
📂 Path: ui/admin/purchases_management.py
"""
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if root_dir not in sys.path: sys.path.append(root_dir)

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLineEdit, QHeaderView, 
                             QFrame, QTabWidget, QFormLayout, QSpinBox, QComboBox, 
                             QDoubleSpinBox, QApplication, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from app.controllers.purchases.purchase_controller import PurchaseController

PURCHASE_STYLE = """
    QWidget { background-color: #F5F5F5; font-family: 'Segoe UI', 'Arial'; color: #333333; }
    QTabWidget::pane { border: 1px solid #cbd5e0; background: #ffffff; border-radius: 8px; }
    QTabBar::tab { background: #e2e8f0; border: 1px solid #cbd5e0; padding: 10px 20px; font-weight: bold; border-top-left-radius: 6px; border-top-right-radius: 6px; }
    QTabBar::tab:selected { background: #ffffff; color: #1E90FF; }
    
    QFrame#panelCard { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; }
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox { border: 1px solid #cbd5e0; border-radius: 6px; padding: 6px 12px; font-size: 14px; }
    QLineEdit:focus { border: 1px solid #1E90FF; }
    
    QTableWidget { background-color: #ffffff; border: none; gridline-color: #edf2f7; }
    QHeaderView::section { background-color: #f7fafc; color: #4a5568; font-weight: bold; padding: 8px; border-bottom: 2px solid #e2e8f0; }
    
    QPushButton#primaryBtn { background-color: #1E90FF; color: white; font-weight: bold; border-radius: 6px; padding: 8px 20px; border: none; }
    QPushButton#primaryBtn:hover { background-color: #1c86ee; }
    QPushButton#dangerBtn { background-color: #e53e3e; color: white; font-weight: bold; border-radius: 6px; padding: 8px 16px; border: none; }
"""

class PurchasesManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = PurchaseController()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(PURCHASE_STYLE)
        
        self.init_ui()
        self.refresh_suppliers_combos()

    def init_ui(self):
        main_layout = QVBoxLayout(self); main_layout.setContentsMargins(20, 20, 20, 20); main_layout.setSpacing(15)
        
        title = QLabel("🧾 إدارة فواتير المشتريات والموردين والارتجاع"); title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        main_layout.addWidget(title)
        
        self.tabs = QTabWidget()
        
        # 1. تبويب الفاتورة الجديدة
        self.tab_invoice = QWidget(); self.init_invoice_tab()
        # 2. تبويب إضافة مورد
        self.tab_supplier = QWidget(); self.init_supplier_tab()
        # 3. تبويب مرتجع المشتريات
        self.tab_return = QWidget(); self.init_return_tab()
        
        self.tabs.addTab(self.tab_invoice, "➕ فاتورة شراء جديدة")
        self.tabs.addTab(self.tab_supplier, "👥 إضافة مورد جديد")
        self.tabs.addTab(self.tab_return, "🔄 مرتجع بضاعة شراء")
        
        main_layout.addWidget(self.tabs)

    # --- ➕ 1. تبويب فاتورة شراء جديدة ---
    def init_invoice_tab(self):
        layout = QHBoxLayout(self.tab_invoice); layout.setContentsMargins(15, 15, 15, 15); layout.setSpacing(15)
        
        # الجانب الأيمن: جدول بضائع الفاتورة
        left_layout = QVBoxLayout()
        
        input_bar = QHBoxLayout()
        self.txt_item_barcode = QLineEdit(); self.txt_item_barcode.setPlaceholderText("باركود الصنف المشتري...")
        self.spn_item_qty = QSpinBox(); self.spn_item_qty.setRange(1, 99999); self.spn_item_qty.setValue(1)
        self.spn_item_cost = QDoubleSpinBox(); self.spn_item_cost.setRange(0, 99999.99); self.spn_item_cost.setSuffix(" ج.م")
        btn_add_row = QPushButton("إضافة للفاتورة"); btn_add_row.setObjectName("primaryBtn"); btn_add_row.clicked.connect(self.add_item_to_table)
        
        input_bar.addWidget(QLabel("الباركود:")); input_bar.addWidget(self.txt_item_barcode)
        input_bar.addWidget(QLabel("الكمية:")); input_bar.addWidget(self.spn_item_qty)
        input_bar.addWidget(QLabel("سعر الشراء:")); input_bar.addWidget(self.spn_item_cost)
        input_bar.addWidget(btn_add_row)
        left_layout.addLayout(input_bar)
        
        self.table_invoice = QTableWidget(); self.table_invoice.setColumnCount(4)
        self.table_invoice.setHorizontalHeaderLabels(["الباركود", "الكمية المشتراة", "سعر الشراء الفردي", "الإجمالي الفرعي"])
        self.table_invoice.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        left_layout.addWidget(self.table_invoice)
        layout.addLayout(left_layout, stretch=3)
        
        # الجانب الأيسر: بيانات وتثبيت الفاتورة بالكامل
        right_panel = QFrame(); right_panel.setObjectName("panelCard"); right_panel.setFixedWidth(320)
        panel_layout = QFormLayout(right_panel); panel_layout.setSpacing(12); panel_layout.setContentsMargins(15, 15, 15, 15)
        
        self.cmb_suppliers_inv = QComboBox()
        self.cmb_pay_type = QComboBox(); self.cmb_pay_type.addItems(["نقداً (CASH)", "آجل (CREDIT)"])
        self.lbl_total = QLabel("0.00 ج.م"); self.lbl_total.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold)); self.lbl_total.setStyleSheet("color: #48bb78;")
        self.txt_inv_notes = QLineEdit()
        
        btn_save_invoice = QPushButton("💾 ترحيل وحفظ الفاتورة للمخازن"); btn_save_invoice.setObjectName("primaryBtn"); btn_save_invoice.clicked.connect(self.submit_purchase_invoice)
        
        panel_layout.addRow(QLabel("🤝 المورد المستلم:") ,self.cmb_suppliers_inv)
        panel_layout.addRow(QLabel("💳 طريقة السداد:"), self.cmb_pay_type)
        panel_layout.addRow(QLabel("📝 ملاحظات:"), self.txt_inv_notes)
        panel_layout.addRow(QLabel("💰 إجمالي الفاتورة:"), self.lbl_total)
        panel_layout.addRow(QLabel(""), btn_save_invoice)
        
        layout.addWidget(right_panel, stretch=1)

    # --- 👥 2. تبويب إضافة مورد جديد ---
    def init_supplier_tab(self):
        layout = QVBoxLayout(self.tab_supplier); layout.setContentsMargins(30, 30, 30, 30); layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        frame = QFrame(); frame.setObjectName("panelCard"); frame.setFixedWidth(500)
        f_layout = QFormLayout(frame); f_layout.setSpacing(15); f_layout.setContentsMargins(20, 20, 20, 20)
        
        self.txt_sup_name = QLineEdit()
        self.txt_sup_company = QLineEdit()
        self.txt_sup_phone = QLineEdit()
        self.txt_sup_address = QLineEdit()
        btn_save_sup = QPushButton("🤝 حفظ بيانات المورد"); btn_save_sup.setObjectName("primaryBtn"); btn_save_sup.clicked.connect(self.submit_supplier)
        
        f_layout.addRow(QLabel("اسم المورد الكريم:"), self.txt_sup_name)
        f_layout.addRow(QLabel("الشركة / المصنع:"), self.txt_sup_company)
        f_layout.addRow(QLabel("رقم الهاتف للتواصل:"), self.txt_sup_phone)
        f_layout.addRow(QLabel("عنوان المورد:"), self.txt_sup_address)
        f_layout.addRow(QLabel(""), btn_save_sup)
        
        layout.addWidget(frame, alignment=Qt.AlignmentFlag.AlignCenter)

    # --- 🔄 3. تبويب مرتجع بضاعة شراء ---
    def init_return_tab(self):
        layout = QVBoxLayout(self.tab_return); layout.setContentsMargins(30, 30, 30, 30); layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        frame = QFrame(); frame.setObjectName("panelCard"); frame.setFixedWidth(500)
        f_layout = QFormLayout(frame); f_layout.setSpacing(15); f_layout.setContentsMargins(20, 20, 20, 20)
        
        self.txt_ret_barcode = QLineEdit()
        self.spn_ret_qty = QSpinBox(); self.spn_ret_qty.setRange(1, 99999)
        self.cmb_suppliers_ret = QComboBox()
        self.txt_ret_reason = QLineEdit(); self.txt_ret_reason.setPlaceholderText("مثال: بضاعة تالفة أو منتهية الصلاحية...")
        btn_save_ret = QPushButton("❌ تأكيد خصم وارتجاع البضاعة"); btn_save_ret.setObjectName("dangerBtn"); btn_save_ret.clicked.connect(self.submit_purchase_return)
        
        f_layout.addRow(QLabel("باركود الصنف المرتجع:"), self.txt_ret_barcode)
        f_layout.addRow(QLabel("الكمية المرتجعة للشركة:"), self.spn_ret_qty)
        f_layout.addRow(QLabel("المورد المستلم لمرتجعه:"), self.cmb_suppliers_ret)
        f_layout.addRow(QLabel("سبب الارتجاع المباشر:"), self.txt_ret_reason)
        f_layout.addRow(QLabel(""), btn_save_ret)
        
        layout.addWidget(frame, alignment=Qt.AlignmentFlag.AlignCenter)

    # --- ⚙️ منطق العمل والعمليات الفورية ---
    def refresh_suppliers_combos(self):
        suppliers = self.controller.load_all_suppliers()
        self.cmb_suppliers_inv.clear()
        self.cmb_suppliers_ret.clear()
        for s_id, s_name, s_comp in suppliers:
            display_text = f"{s_name} ({s_comp})"
            self.cmb_suppliers_inv.addItem(display_text, s_id)
            self.cmb_suppliers_ret.addItem(display_text, s_id)

    def add_item_to_table(self):
        barcode = self.txt_item_barcode.text().strip()
        qty = self.spn_item_qty.value()
        cost = self.spn_item_cost.value()
        
        if not barcode or cost <= 0: return
        
        row_idx = self.table_invoice.rowCount()
        self.table_invoice.insertRow(row_idx)
        self.table_invoice.setItem(row_idx, 0, QTableWidgetItem(barcode))
        self.table_invoice.setItem(row_idx, 1, QTableWidgetItem(str(qty)))
        self.table_invoice.setItem(row_idx, 2, QTableWidgetItem(f"{cost:.2f}"))
        self.table_invoice.setItem(row_idx, 3, QTableWidgetItem(f"{(qty * cost):.2f}"))
        
        self.txt_item_barcode.clear()
        self.spn_item_qty.setValue(1)
        self.spn_item_cost.setValue(0.0)
        self.update_invoice_total_label()

    def update_invoice_total_label(self):
        total = 0.0
        for row in range(self.table_invoice.rowCount()):
            total += float(self.table_invoice.item(row, 3).text())
        self.lbl_total.setText(f"{total:.2f} ج.م")

    def submit_purchase_invoice(self):
        if self.table_invoice.rowCount() == 0: return
        
        supplier_id = self.cmb_suppliers_inv.currentData()
        pay_type = self.cmb_pay_type.currentText()
        notes = self.txt_inv_notes.text().strip()
        
        total = 0.0
        items_list = []
        for row in range(self.table_invoice.rowCount()):
            b = self.table_invoice.item(row, 0).text()
            q = int(self.table_invoice.item(row, 1).text())
            c = float(self.table_invoice.item(row, 2).text())
            total += (q * c)
            items_list.append((b, q, c))
            
        try:
            inv_id = self.controller.process_purchase_invoice(supplier_id, total, 0.0, 0.0, pay_type, notes, items_list)
            QMessageBox.information(self, "نجاح العملية", f"✨ تم حفظ وتثبيت فاتورة الشراء برقم (#{inv_id}) وزيادة المخزون تلقائياً!")
            self.table_invoice.setRowCount(0)
            self.update_invoice_total_label()
            self.txt_inv_notes.clear()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل ترحيل الفاتورة: {e}")

    def submit_supplier(self):
        name = self.txt_sup_name.text().strip()
        company = self.txt_sup_company.text().strip()
        phone = self.txt_sup_phone.text().strip()
        address = self.txt_sup_address.text().strip()
        
        if not name or not company: return
        self.controller.create_supplier(name, phone, company, address)
        QMessageBox.information(self, "تم الحفظ", "🤝 تم تسجيل بيانات المورد وتحديث القوائم المنسدلة تلقائياً.")
        
        self.txt_sup_name.clear(); self.txt_sup_company.clear(); self.txt_sup_phone.clear(); self.txt_sup_address.clear()
        self.refresh_suppliers_combos()

    def submit_purchase_return(self):
        barcode = self.txt_ret_barcode.text().strip()
        qty = self.spn_ret_qty.value()
        supplier_id = self.cmb_suppliers_ret.currentData()
        reason = self.txt_ret_reason.text().strip()
        
        if not barcode or not reason: return
        success, msg = self.controller.process_purchase_return(barcode, qty, supplier_id, reason)
        if success:
            QMessageBox.information(self, "نجاح المرتجع", msg)
            self.txt_ret_barcode.clear(); self.txt_ret_reason.clear(); self.spn_ret_qty.setValue(1)
        else:
            QMessageBox.warning(self, "تحذير من السيستم", msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PurchasesManagementWidget()
    widget.showMaximized()
    sys.exit(app.exec())