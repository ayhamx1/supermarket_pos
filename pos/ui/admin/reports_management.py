# -*- coding: utf-8 -*-
"""
Supermarket POS - Reports Management UI (Windows 11 Fluent Style)
Path: ui/admin/reports_management.py
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QFrame, QMessageBox, QApplication, QAbstractItemView, QComboBox, QDateEdit)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QColor
from app.controllers.reports.reports_controller import ReportsController

REPORTS_STYLE = """
    QWidget { background-color: #F3F3F3; font-family: 'Segoe UI', 'Arial'; color: #1B1B1B; }
    QFrame#filterBar { background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 4px; padding: 12px; }
    QComboBox, QDateEdit { border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 10px; background: #FFFFFF; font-size: 13px; min-width: 150px; }
    QComboBox:focus, QDateEdit:focus { border: 2px solid #0067B8; }
    
    QTableWidget { background-color: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 4px; }
    QHeaderView::section { background-color: #F9F9F9; font-weight: 600; border: 1px solid #E5E5E5; padding: 8px; font-size: 13px; }
    
    QPushButton { background-color: #0067B8; color: #FFFFFF; border: none; border-radius: 4px; padding: 8px 16px; font-size: 13px; font-weight: 600; }
    QPushButton:hover { background-color: #005A9E; }
    QPushButton#btnPrint { background-color: #FFFFFF; color: #1B1B1B; border: 1px solid #CCCCCC; }
    QPushButton#btnPrint:hover { background-color: #F5F5F5; }
"""

class ReportsManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ReportsController()
        
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(REPORTS_STYLE)
        
        self.init_ui()
        self.handle_report_change() # تحميل أولي لأول تقرير

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        title_lbl = QLabel("مركز التقارير الموحد والتحليلات المالية")
        title_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title_lbl)
        
        # شريط أدوات وفلاتر التقارير
        filter_bar = QFrame()
        filter_bar.setObjectName("filterBar")
        filter_layout = QHBoxLayout(filter_bar)
        filter_layout.setContentsMargins(8, 6, 8, 6)
        filter_layout.setSpacing(16)
        
        filter_layout.addWidget(QLabel("نوع التقرير الاستراتيجي:"))
        self.cmb_report_type = QComboBox()
        self.cmb_report_type.addItems([
            "تقرير المبيعات",
            "تقرير الأرباح الخسائر",
            "تقرير رصيد المخزون الحالي",
            "تقرير الأصناف الراكدة",
            "تقرير المشتريات والشركات",
            "تقرير مديونيات الموردين",
            "تقرير حسابات العملاء الآجل",
            "تقرير حركة نقدية الخزنة"
        ])
        self.cmb_report_type.currentIndexChanged.connect(self.handle_report_change)
        filter_layout.addWidget(self.cmb_report_type)
        
        # أدوات التحكم بالتواريخ
        self.lbl_from = QLabel("من تاريخ:")
        self.txt_start_date = QDateEdit(QDate.currentDate().addDays(-7))
        self.txt_start_date.setCalendarPopup(True)
        
        self.lbl_to = QLabel("إلى تاريخ:")
        self.txt_end_date = QDateEdit(QDate.currentDate())
        self.txt_end_date.setCalendarPopup(True)
        
        filter_layout.addWidget(self.lbl_from)
        filter_layout.addWidget(self.txt_start_date)
        filter_layout.addWidget(self.lbl_to)
        filter_layout.addWidget(self.txt_end_date)
        
        # أزرار الإجراءات
        self.btn_fetch = QPushButton("توليد التقرير")
        self.btn_fetch.clicked.connect(self.fetch_report_data)
        filter_layout.addWidget(self.btn_fetch)
        
        self.btn_print = QPushButton("تصدير وطباعة")
        self.btn_print.setObjectName("btnPrint")
        filter_layout.addWidget(self.btn_print)
        
        filter_layout.addStretch()
        layout.addWidget(filter_bar)
        
        # جدول عرض البيانات الديناميكي
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table)

    def handle_report_change(self):
        """إخفاء وإظهار فلاتر التاريخ حسب التقرير لمنع أخطاء المدخلات الدفترية"""
        idx = self.cmb_report_type.currentIndex()
        # تقارير المخزون، الراكدة، الموردين، والعملاء لا تتطلب تحديد مدى تاريخي (تظهر اللحظة الحالية)
        static_reports = [2, 3, 5, 6]
        is_static = idx in static_reports
        
        self.lbl_from.setVisible(not is_static)
        self.txt_start_date.setVisible(not is_static)
        self.lbl_to.setVisible(not is_static)
        self.txt_end_date.setVisible(not is_static)
        
        self.fetch_report_data()

    def fetch_report_data(self):
        self.table.setRowCount(0)
        idx = self.cmb_report_type.currentIndex()
        
        start = self.txt_start_date.date().toString("yyyy-MM-dd 00:00:00")
        end = self.txt_end_date.date().toString("yyyy-MM-dd 23:59:59")
        
        # الخريطة البرمجية للتقارير
        type_keys = ["sales", "profits", "inventory", "stagnant", "purchases", "suppliers", "customers", "vault"]
        chosen_key = type_keys[idx]
        
        data = self.controller.generate_report(chosen_key, start, end)
        
        # تهيئة رؤوس الأعمدة ديناميكياً حسب نوع التقرير المطلوب
        headers = []
        if chosen_key == "sales":
            headers = ["التاريخ", "عدد الفواتير", "إجمالي المبيعات", "النقدية المحصلة", "الآجل المتبقي"]
        elif chosen_key == "profits":
            headers = ["التاريخ", "حجم المبيعات", "تكلفة البضاعة", "صافي الربح الحقيقي"]
        elif chosen_key == "inventory":
            headers = ["اسم الصنف", "الباركود", "الرصيد", "سعر التكلفة", "سعر البيع", "قيمة التكلفة الإجمالية", "القيمة البيعية المتوقعة"]
        elif chosen_key == "stagnant":
            headers = ["الرقم المرجعي", "الباركود", "اسم الصنف", "الكمية الراكدة بالرف", "السعر"]
        elif chosen_key == "purchases":
            headers = ["التاريخ", "الشركة / المورد", "عدد الفواتير", "إجمالي المشتريات"]
        elif chosen_key == "suppliers":
            headers = ["اسم الشركة", "المندوب المسؤول", "رقم الهاتف", "المديونية المستحقة له"]
        elif chosen_key == "customers":
            headers = ["اسم العميل", "رقم الهاتف", "الحساب الآجل المستحق عليه", "نقاط الولاء"]
        elif chosen_key == "vault":
            headers = ["التاريخ والوقت", "نوع الحركة", "المبلغ", "البيان والملاحظات"]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # تعبئة الخلايا بالبيانات المستخرجة
        for r, row in enumerate(data):
            self.table.insertRow(r)
            for c, val in enumerate(row):
                # تنسيق الأرقام العشرية والمالية تلقائياً لسهولة القراءة الدفترية
                if isinstance(val, (int, float)) and c > 0:
                    item_text = f"{val:,.2f}" if isinstance(val, float) or val > 100 else str(val)
                else:
                    item_text = str(val)
                    
                table_item = QTableWidgetItem(item_text)
                
                # تلوين خاص لصافي الأرباح والإيداعات
                if chosen_key == "profits" and c == 3:
                    table_item.setForeground(QColor("#008A17"))
                    table_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                    
                self.table.setItem(r, c, table_item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ReportsManagementWidget()
    w.show()
    sys.exit(app.exec())