# -*- coding: utf-8 -*-
"""
Supermarket POS - Customers Management UI (Windows 11 Fluent Style)
Path: ui/admin/partners_management.py
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QFrame, QLineEdit, QMessageBox, QApplication, QAbstractItemView, QDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from app.controllers.partners.partner_controller import PartnerController

CUSTOMER_STYLE = """
    QWidget { background-color: #F3F3F3; font-family: 'Segoe UI', 'Arial'; color: #1B1B1B; }
    QFrame#cardPanel { background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 4px; padding: 16px; }
    QLineEdit { border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 10px; background: #FFFFFF; font-size: 13px; }
    QLineEdit:focus { border: 2px solid #0067B8; }
    
    QTableWidget { background-color: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 4px; }
    QHeaderView::section { background-color: #F9F9F9; font-weight: 600; border: 1px solid #E5E5E5; padding: 8px; font-size: 13px; }
    
    QPushButton { background-color: #FFFFFF; border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 12px; font-size: 13px; font-weight: 400; }
    QPushButton:hover { background-color: #F5F5F5; }
    
    QPushButton#btnSave { background-color: #0067B8; color: #FFFFFF; border: none; font-weight: 600; }
    QPushButton#btnSave:hover { background-color: #005A9E; }
    
    QPushButton#btnStatement { background-color: #E9E9E9; color: #1B1B1B; border: 1px solid #CCCCCC; font-weight: 600; }
    QPushButton#btnStatement:hover { background-color: #DFDFDF; }
"""

class PartnersManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = PartnerController()
        self.selected_customer_id = None
        
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(CUSTOMER_STYLE)
        
        self.init_ui()
        self.refresh_data()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # القسم الأيمن: جدول العملاء والديون ونقاط الولاء
        left_layout = QVBoxLayout()
        left_layout.setSpacing(12)
        
        title_lbl = QLabel("إدارة حسابات العملاء والديون الآجلة")
        title_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        left_layout.addWidget(title_lbl)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["رقم الحساب", "اسم العميل", "رقم الهاتف", "المديونية الآجلة", "الحد الائتماني", "نقاط الولاء"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.itemClicked.connect(self.handle_row_selection)
        left_layout.addWidget(self.table)
        
        # أزرار الإجراءات والتحكم
        actions_layout = QHBoxLayout()
        self.btn_statement = QPushButton("عرض كشف الحساب والمسحوبات الآجلة")
        self.btn_statement.setObjectName("btnStatement")
        self.btn_statement.clicked.connect(self.open_customer_statement)
        actions_layout.addWidget(self.btn_statement)
        
        self.btn_clear_selection = QPushButton("عميل جديد")
        self.btn_clear_selection.clicked.connect(self.clear_form)
        actions_layout.addWidget(self.btn_clear_selection)
        actions_layout.addStretch()
        left_layout.addLayout(actions_layout)
        
        main_layout.addLayout(left_layout, stretch=3)
        
        # القسم الأيسر: بطاقة البيانات الفنية (إضافة / تعديل)
        right_panel = QFrame()
        right_panel.setObjectName("cardPanel")
        right_panel.setFixedWidth(320)
        panel_layout = QVBoxLayout(right_panel)
        panel_layout.setSpacing(10)
        
        self.panel_title = QLabel("تسجيل عميل جديد")
        self.panel_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.panel_title.setStyleSheet("color: #0067B8; padding-bottom: 4px;")
        panel_layout.addWidget(self.panel_title)
        
        panel_layout.addWidget(QLabel("اسم العميل الكامل:"))
        self.txt_name = QLineEdit()
        panel_layout.addWidget(self.txt_name)
        
        panel_layout.addWidget(QLabel("رقم الهاتف المحمول:"))
        self.txt_phone = QLineEdit()
        panel_layout.addWidget(self.txt_phone)
        
        panel_layout.addWidget(QLabel("المديونية الآجلة الافتتاحية (عليه):"))
        self.txt_balance = QLineEdit()
        self.txt_balance.setText("0.00")
        panel_layout.addWidget(self.txt_balance)
        
        panel_layout.addWidget(QLabel("الحد الائتماني الأقصى (جنيه):"))
        self.txt_limit = QLineEdit()
        self.txt_limit.setText("1000.00")
        panel_layout.addWidget(self.txt_limit)
        
        panel_layout.addWidget(QLabel("رصيد نقاط الولاء الحالي:"))
        self.txt_points = QLineEdit()
        self.txt_points.setText("0")
        panel_layout.addWidget(self.txt_points)
        
        panel_layout.addSpacing(10)
        
        self.btn_save = QPushButton("حفظ بيانات العميل")
        self.btn_save.setObjectName("btnSave")
        self.btn_save.clicked.connect(self.handle_save)
        panel_layout.addWidget(self.btn_save)
        
        panel_layout.addStretch()
        main_layout.addWidget(right_panel, stretch=1)

    def refresh_data(self):
        self.table.setRowCount(0)
        customers = self.controller.load_all_customers()
        
        for r, row in enumerate(customers):
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(r, 1, QTableWidgetItem(str(row[1])))
            self.table.setItem(r, 2, QTableWidgetItem(str(row[2])))
            
            balance_val = float(row[3])
            limit_val = float(row[4])
            
            balance_item = QTableWidgetItem(f"{balance_val:,.2f} جنيه")
            
            # تمييز العملاء الذين لديهم ديون معلقة أو اقتربوا من تجاوز الحد الائتماني
            if balance_val >= limit_val:
                balance_item.setForeground(QColor("#C42B1C")) # اللون الأحمر الرسمي لويندوز
                balance_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            elif balance_val > 0:
                balance_item.setForeground(QColor("#0067B8"))
                
            self.table.setItem(r, 3, balance_item)
            self.table.setItem(r, 4, QTableWidgetItem(f"{limit_val:,.2f} جنيه"))
            self.table.setItem(r, 5, QTableWidgetItem(str(row[5])))

    def handle_row_selection(self, item):
        row = self.table.currentRow()
        self.selected_customer_id = int(self.table.item(row, 0).text())
        self.txt_name.setText(self.table.item(row, 1).text())
        self.txt_phone.setText(self.table.item(row, 2).text())
        
        balance_raw = self.table.item(row, 3).text().replace(" جنيه", "").replace(",", "")
        self.txt_balance.setText(balance_raw)
        
        limit_raw = self.table.item(row, 4).text().replace(" جنيه", "").replace(",", "")
        self.txt_limit.setText(limit_raw)
        
        self.txt_points.setText(self.table.item(row, 5).text())
        
        self.panel_title.setText("تعديل بيانات العميل الحالي")

    def clear_form(self):
        self.selected_customer_id = None
        self.txt_name.clear()
        self.txt_phone.clear()
        self.txt_balance.setText("0.00")
        self.txt_limit.setText("1000.00")
        self.txt_points.setText("0")
        self.panel_title.setText("تسجيل عميل جديد")
        self.table.clearSelection()

    def handle_save(self):
        name = self.txt_name.text().strip()
        phone = self.txt_phone.text().strip()
        
        try:
            balance = float(self.txt_balance.text().strip())
            limit = float(self.txt_limit.text().strip())
            points = int(self.txt_points.text().strip())
        except ValueError:
            QMessageBox.warning(self, "خطأ في الإدخال", "يرجى كتابة قيم رقمية صحيحة في حقول المديونية، الحد الائتماني، والنقاط")
            return
            
        success, msg = self.controller.save_customer(name, phone, balance, limit, points, self.selected_customer_id)
        
        if success:
            QMessageBox.information(self, "نجاح العملية", msg)
            self.clear_form()
            self.refresh_data()
        else:
            QMessageBox.warning(self, "فشل الإجراء", msg)

    def open_customer_statement(self):
        if self.selected_customer_id is None:
            QMessageBox.warning(self, "تنبيه", "يرجى تحديد العميل من الجدول أولاً لاستعراض كشف الحساب")
            return
            
        dialog = CustomerStatementDialog(self.selected_customer_id, self.txt_name.text(), self.controller)
        dialog.exec()

# ─── شاشة منبثقة تفصيلية لكشف الحساب وعمليات الآجل ───
class CustomerStatementDialog(QDialog):
    def __init__(self, customer_id, customer_name, controller):
        super().__init__()
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.controller = controller
        
        self.setWindowTitle(f"كشف المسحوبات والآجل - {self.customer_name}")
        self.resize(700, 450)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        title = QLabel(f"كشف حساب الفواتير الآجلة للعميل: {self.customer_name}")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["التاريخ والوقت", "نوع المعاملة", "رقم الفاتورة المرجعي", "القيمة المطلوبة"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        statement_data = self.controller.load_statement(self.customer_id)
        table.setRowCount(0)
        
        for r, row in enumerate(statement_data):
            table.insertRow(r)
            table.setItem(r, 0, QTableWidgetItem(str(row[0])))
            table.setItem(r, 1, QTableWidgetItem(str(row[1])))
            table.setItem(r, 2, QTableWidgetItem(str(row[2])))
            
            amount_val = float(row[3])
            table.setItem(r, 3, QTableWidgetItem(f"{amount_val:,.2f} جنيه"))
            
        layout.addWidget(table)
        
        btn_close = QPushButton("إغلاق كشف الحساب")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PartnersManagementWidget()
    w.show()
    sys.exit(app.exec())