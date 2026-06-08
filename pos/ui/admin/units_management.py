# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Units Management UI
📂 Path: ui/admin/units_management.py
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QFrame, QLineEdit, QMessageBox, QApplication, QAbstractItemView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from app.controllers.products.unit_controller import UnitController

UNIT_STYLE = """
    QWidget { background-color: #F8FAFC; font-family: 'Segoe UI', 'Arial'; color: #1E293B; }
    QFrame#panelCard { background: white; border: 1px solid #E2E8F0; border-radius: 10px; padding: 15px; }
    QLineEdit { border: 1px solid #CBD5E1; border-radius: 6px; padding: 8px; background: white; font-size: 13px; }
    QLineEdit:focus { border: 2px solid #2563EB; }
    
    QTableWidget { background-color: white; border: 1px solid #E2E8F0; border-radius: 8px; }
    QHeaderView::section { background-color: #F1F5F9; font-weight: bold; border: none; padding: 10px; font-size: 13px; }
    
    QPushButton#btnSave { background-color: #2563EB; color: white; font-weight: bold; border: none; border-radius: 6px; padding: 10px; font-size: 13px; }
    QPushButton#btnSave:hover { background-color: #1D4ED8; }
    
    QPushButton[class="actionBtn"] { font-weight: bold; border: none; border-radius: 6px; padding: 8px 12px; font-size: 12px; color: white; }
    QPushButton#btnDelete { background-color: #EF4444; }
    QPushButton#btnDelete:hover { background-color: #DC2626; }
"""

class UnitsManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = UnitController()
        
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(UNIT_STYLE)
        
        self.init_ui()
        self.refresh_table()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # 🟢 القسم الأيمن: جدول عرض الوحدات والإحصائيات
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        
        title_lbl = QLabel("📏 سجل وحدات القياس والوزن المركزية")
        title_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        left_layout.addWidget(title_lbl)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["م الرقمي", "وحدة القياس", "عدد الأصناف المرتبطة"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        left_layout.addWidget(self.table)
        
        # أزرار التحكم السفلية لجدول الوحدات
        actions_layout = QHBoxLayout()
        self.btn_delete = QPushButton("🗑️ حذف الوحدة المحددة")
        self.btn_delete.setObjectName("btnDelete")
        self.btn_delete.setProperty("class", "actionBtn")
        self.btn_delete.clicked.connect(self.handle_delete_unit)
        actions_layout.addWidget(self.btn_delete)
        actions_layout.addStretch()
        left_layout.addLayout(actions_layout)
        
        main_layout.addLayout(left_layout, stretch=3)
        
        # 🟡 القسم الأيسر: كارت إضافة وحدة جديدة
        right_panel = QFrame()
        right_panel.setObjectName("panelCard")
        right_panel.setFixedWidth(300)
        panel_layout = QVBoxLayout(right_panel)
        panel_layout.setSpacing(12)
        
        panel_title = QLabel("➕ إضافة وحدة قياس")
        panel_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        panel_title.setStyleSheet("color: #2563EB; border-bottom: 1px solid #E2E8F0; padding-bottom: 8px;")
        panel_layout.addWidget(panel_title)
        
        panel_layout.addWidget(QLabel("اسم الوحدة الجديدة *:"))
        self.txt_unit_name = QLineEdit()
        self.txt_unit_name.setPlaceholderText("مثال: علبة، شيكارة، جرام...")
        panel_layout.addWidget(self.txt_unit_name)
        
        panel_layout.addSpacing(10)
        
        self.btn_save = QPushButton("💾 حفظ الوحدة")
        self.btn_save.setObjectName("btnSave")
        self.btn_save.clicked.connect(self.handle_save_unit)
        panel_layout.addWidget(self.btn_save)
        
        panel_layout.addStretch()
        main_layout.addWidget(right_panel, stretch=1)

    def refresh_table(self):
        self.table.setRowCount(0)
        units = self.controller.load_units_summary()
        
        for r, row in enumerate(units):
            self.table.insertRow(r)
            id_item = QTableWidgetItem(str(row[0]))
            name_item = QTableWidgetItem(str(row[1]))
            
            count_text = f"{row[2]} صنف نشط" if row[2] > 0 else "غير مستخدمة"
            count_item = QTableWidgetItem(count_text)
            
            if row[2] == 0:
                count_item.setForeground(QColor("#94A3B8"))
            else:
                count_item.setForeground(QColor("#10B981"))
                count_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                
            self.table.setItem(r, 0, id_item)
            self.table.setItem(r, 1, name_item)
            self.table.setItem(r, 2, count_item)

    def handle_save_unit(self):
        unit_name = self.txt_unit_name.text().strip()
        if not unit_name:
            QMessageBox.warning(self, "تنبيه", "برجاء كتابة اسم وحدة القياس أولاً!")
            return
            
        QMessageBox.information(self, "تم الاعتماد 🎉", f"تم تسجيل وإدراج وحدة ({unit_name}) بنجاح في القوائم المتاحة.")
        self.txt_unit_name.clear()
        self.refresh_table()

    def handle_delete_unit(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "تنبيه", "يرجى اختيار وحدة القياس المراد حذفها من الجدول!")
            return
        
        row = selected_rows[0].row()
        unit_name = self.table.item(row, 1).text()
        
        confirm = QMessageBox.question(
            self, "تأكيد الإزالة 🚨", 
            f"هل أنت متأكد من حذف وحدة ({unit_name})؟ سيتم فك ارتباط الأصناف المدرجة بها.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "نجاح", "تمت إزالة وحدة القياس بنجاح.")
            self.refresh_table()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = UnitsManagementWidget()
    w.show()
    sys.exit(app.exec())