# -*- coding: utf-8 -*-
"""
Supermarket POS - Vault Management UI (Windows 11 Fluent Style)
Path: ui/admin/vault_management.py
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QFrame, QLineEdit, QMessageBox, QApplication, QAbstractItemView, QDialog, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from app.controllers.finance.vault_controller import VaultController

VAULT_STYLE = """
    QWidget { background-color: #F3F3F3; font-family: 'Segoe UI', 'Arial'; color: #1B1B1B; }
    QFrame#statusCard { background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 4px; padding: 16px; }
    QFrame#actionPanel { background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 4px; padding: 16px; }
    
    QLineEdit, QComboBox { border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 10px; background: #FFFFFF; font-size: 13px; }
    QLineEdit:focus, QComboBox:focus { border: 2px solid #0067B8; }
    
    QTableWidget { background-color: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 4px; }
    QHeaderView::section { background-color: #F9F9F9; font-weight: 600; border: 1px solid #E5E5E5; padding: 8px; font-size: 13px; }
    
    QPushButton { background-color: #FFFFFF; border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 12px; font-size: 13px; color: #1B1B1B; }
    QPushButton:hover { background-color: #F5F5F5; }
    
    QPushButton#btnPrimary { background-color: #0067B8; color: #FFFFFF; border: none; font-weight: 600; }
    QPushButton#btnPrimary:hover { background-color: #005A9E; }
    
    QPushButton#btnDanger { background-color: #FFFFFF; border: 1px solid #C42B1C; color: #C42B1C; font-weight: 600; }
    QPushButton#btnDanger:hover { background-color: #FDE7E9; }
"""

class VaultManagementWidget(QWidget):
    def __init__(self, current_user_id=1):
        super().__init__()
        self.controller = VaultController()
        self.user_id = current_user_id
        self.active_shift_id = None
        self.opening_balance = 0.0
        
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(VAULT_STYLE)
        
        self.init_ui()
        self.update_shift_ui_status()
        self.refresh_vault_logs()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        # الطرف الأيمن: إدارة الورديات والحركات النقدية
        left_layout = QVBoxLayout()
        left_layout.setSpacing(12)
        
        # 1. كارت حالة الوردية الحالية
        self.status_card = QFrame()
        self.status_card.setObjectName("statusCard")
        status_layout = QVBoxLayout(self.status_card)
        
        self.lbl_shift_title = QLabel("حالة الوردية الحالية")
        self.lbl_shift_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        status_layout.addWidget(self.lbl_shift_title)
        
        self.lbl_shift_details = QLabel("جاري التحقق من النظام المالي...")
        self.lbl_shift_details.setStyleSheet("color: #5D5D5D; padding: 4px 0px;")
        status_layout.addWidget(self.lbl_shift_details)
        
        self.btn_shift_trigger = QPushButton("فتح وردية جديدة")
        self.btn_shift_trigger.setObjectName("btnPrimary")
        self.btn_shift_trigger.clicked.connect(self.handle_shift_trigger)
        status_layout.addWidget(self.btn_shift_trigger)
        
        left_layout.addWidget(self.status_card)
        
        # 2. كارت عمليات السحب والإيداع السريع
        self.action_card = QFrame()
        self.action_card.setObjectName("actionPanel")
        action_layout = QVBoxLayout(self.action_card)
        
        action_title = QLabel("إجراء حركة نقدية (سحب / إيداع)")
        action_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        action_layout.addWidget(action_title)
        
        action_layout.addWidget(QLabel("نوع العملية المالية:"))
        self.cmb_type = QComboBox()
        self.cmb_type.addItems(["إيداع نقدية بالخزنة", "سحب نقدية من الخزنة"])
        action_layout.addWidget(self.cmb_type)
        
        action_layout.addWidget(QLabel("المبلغ المالي (جنيه):"))
        self.txt_amount = QLineEdit()
        action_layout.addWidget(self.txt_amount)
        
        action_layout.addWidget(QLabel("البيان والملاحظات (السبب):"))
        self.txt_notes = QLineEdit()
        action_layout.addWidget(self.txt_notes)
        
        self.btn_execute_trans = QPushButton("اعتماد الحركة المالية")
        self.btn_execute_trans.clicked.connect(self.handle_cash_transaction)
        action_layout.addWidget(self.btn_execute_trans)
        
        left_layout.addWidget(self.action_card)
        left_layout.addStretch()
        
        main_layout.addLayout(left_layout, stretch=1)
        
        # الطرف الأيسر: جدول جرد وحركات الخزنة العام
        right_layout = QVBoxLayout()
        right_layout.setSpacing(12)
        
        table_title = QLabel("سجل جرد الخزنة - آخر العمليات المالية")
        table_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        right_layout.addWidget(table_title)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["التاريخ والوقت", "نوع الحركة", "القيمة", "البيان والملاحظات"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        right_layout.addWidget(self.table)
        
        main_layout.addLayout(right_layout, stretch=2)

    def update_shift_ui_status(self):
        shift = self.controller.check_shift_status(self.user_id)
        if shift:
            self.active_shift_id = shift[0]
            self.opening_balance = float(shift[1])
            self.lbl_shift_details.setText(f"وردية نشطة بالرقم المرجعي: {self.active_shift_id}\nتاريخ الفتح: {shift[2]}\nالعهدة الافتتاحية: {self.opening_balance:,.2f} جنيه")
            self.btn_shift_trigger.setText("إغلاق الوردية الحالية وطباعة التقرير")
            self.btn_shift_trigger.setObjectName("btnDanger")
            self.action_card.setEnabled(True)
        else:
            self.active_shift_id = None
            self.lbl_shift_details.setText("البرنامج مغلق مالياً حالياً. يرجى فتح وردية جديدة لبدء البيع واستلام العهدة.")
            self.btn_shift_trigger.setText("فتح وردية واستلام العهدة الافتتاحية")
            self.btn_shift_trigger.setObjectName("btnPrimary")
            self.action_card.setEnabled(False)
            
        self.setStyleSheet(VAULT_STYLE)

    def handle_shift_trigger(self):
        if self.active_shift_id is None:
            # فتح وردية جديدة عبر نافذة منبثقة
            dialog = OpenShiftDialog()
            if dialog.exec() == QDialog.DialogCode.Accepted:
                balance = dialog.get_balance()
                success, _ = self.controller.start_new_shift(self.user_id, balance)
                if success:
                    QMessageBox.information(self, "النظام المالي", "تم فتح الوردية بنجاح وتم تفعيل نقطة البيع")
                    self.update_shift_ui_status()
                    self.refresh_vault_logs()
        else:
            # حساب التقرير وإغلاق الوردية
            expected, deposits, withdrawals = self.controller.calculate_shift_report(self.active_shift_id, self.opening_balance)
            dialog = CloseShiftDialog(expected, deposits, withdrawals)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                actual_cash, notes = dialog.get_closing_data()
                success = self.controller.finalize_shift(self.active_shift_id, expected, actual_cash, notes)
                if success:
                    QMessageBox.information(self, "النظام المالي", "تم إغلاق الوردية الحالية بنجاح وتصفية النقدية بالخزنة الدفترية")
                    self.update_shift_ui_status()
                    self.refresh_vault_logs()

    def handle_cash_transaction(self):
        try:
            amount = float(self.txt_amount.text().strip())
        except ValueError:
            QMessageBox.warning(self, "خطأ في الإدخال", "يرجى إدخال قيمة مالية صحيحة عددياً")
            return
            
        notes = self.txt_notes.text().strip()
        trans_type = "deposit" if self.cmb_type.currentIndex() == 0 else "withdrawal"
        
        success, msg = self.controller.execute_cash_operation(self.active_shift_id, trans_type, amount, notes)
        if success:
            QMessageBox.information(self, "حركة نقدية", msg)
            self.txt_amount.clear()
            self.txt_notes.clear()
            self.refresh_vault_logs()
        else:
            QMessageBox.warning(self, "خطأ بالعملية", msg)

    def refresh_vault_logs(self):
        self.table.setRowCount(0)
        logs = self.controller.load_vault_logs()
        
        for r, row in enumerate(logs):
            self.table.insertRow(r)
            self.table.setItem(r, 0, QTableWidgetItem(str(row[0])))
            
            friendly_type = "إيداع نقدي" if row[1] == "deposit" else "سحب نقدي"
            type_item = QTableWidgetItem(friendly_type)
            if row[1] == "deposit":
                type_item.setForeground(QColor("#0067B8"))
            else:
                type_item.setForeground(QColor("#C42B1C"))
                
            self.table.setItem(r, 1, type_item)
            self.table.setItem(r, 2, QTableWidgetItem(f"{float(row[2]):,.2f} جنيه"))
            self.table.setItem(r, 3, QTableWidgetItem(str(row[3])))

# ─── شاشة فتح وردية جديدة ───
class OpenShiftDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("استلام العهدة وفتح الوردية")
        self.setFixedWidth(300)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        layout.addWidget(QLabel("قيمة النقدية المستلمة كعهدة افتتاحية:"))
        self.txt_balance = QLineEdit()
        self.txt_balance.setText("0.00")
        layout.addWidget(self.txt_balance)
        
        btn_ok = QPushButton("تأكيد فتح الوردية")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

    def get_balance(self):
        try:
            return float(self.txt_balance.text().strip())
        except ValueError:
            return 0.0

# ─── شاشة تقرير وإغلاق الوردية ───
class CloseShiftDialog(QDialog):
    def __init__(self, expected, deposits, withdrawals):
        super().__init__()
        self.expected = expected
        self.setWindowTitle("تقرير إغلاق الوردية الحالية")
        self.setFixedWidth(360)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)
        
        layout.addWidget(QLabel("ملخص الحركات المالية للوردية:"))
        layout.addWidget(QLabel(f"إجمالي الإيداعات النقدية: {deposits:,.2f} جنيه"))
        layout.addWidget(QLabel(f"إجمالي المسحوبات النقدية: {withdrawals:,.2f} جنيه"))
        layout.addWidget(QLabel(f"الرصيد الدفتري المتوقع بالخزنة: {expected:,.2f} جنيه"))
        
        layout.addWidget(QLabel("الرصيد الفعلي الموجود بالدرج حالياً (جرد):"))
        self.txt_actual = QLineEdit()
        self.txt_actual.setText(f"{expected:.2f}")
        layout.addWidget(self.txt_actual)
        
        layout.addWidget(QLabel("ملاحظات إغلاق الوردية والتسليم:"))
        self.txt_notes = QLineEdit()
        self.txt_notes.setPlaceholderText("اكتب ملاحظات العجز أو الزيادة إن وجدت...")
        layout.addWidget(self.txt_notes)
        
        btn_confirm = QPushButton("اعتماد التقرير المالي وإغلاق الوردية")
        btn_confirm.clicked.connect(self.accept)
        layout.addWidget(btn_confirm)

    def get_closing_data(self):
        try:
            actual = float(self.txt_actual.text().strip())
        except ValueError:
            actual = self.expected
        return actual, self.txt_notes.text().strip()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = VaultManagementWidget()
    w.show()
    sys.exit(app.exec())