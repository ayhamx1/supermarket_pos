from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QLineEdit, QPushButton, QTableWidget, 
                             QHeaderView, QFormLayout, QFrame, QTabWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

FINANCIAL_STYLE = """
    QDialog { background-color: #F8FAFC; }
    QLabel { font-family: 'Segoe UI', 'Cairo'; color: #1E293B; }
    QLineEdit, QComboBox {
        border: 1px solid #CBD5E1; border-radius: 6px; padding: 8px 12px;
        font-size: 14px; background-color: #FFFFFF; color: #334155;
    }
    QLineEdit:focus, QComboBox:focus { border: 2px solid #1E90FF; }
    QTableWidget { background-color: #FFFFFF; border: 1px solid #E2E8F0; font-family: 'Segoe UI'; }
    QHeaderView::section { background-color: #1e5378; color: white; font-weight: bold; padding: 8px; border: none; }
    QTabWidget::pane { border: 1px solid #E2E8F0; background: #FFFFFF; border-radius: 8px; }
    QTabBar::tab { background: #E2E8F0; color: #475569; padding: 10px 20px; font-family: 'Segoe UI'; font-weight: bold; border-top-left-radius: 6px; border-top-right-radius: 6px; }
    QTabBar::tab:selected { background: #1E90FF; color: white; }
"""

class Ui_FinancialManager:
    def setupUi(self, dialog):
        dialog.setFixedSize(900, 650)
        dialog.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        dialog.setStyleSheet(FINANCIAL_STYLE)
        
        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_title = QLabel("💼 النظام المالي المركزي ولوحة تحكم المدير")
        lbl_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color: #1e5378; margin-bottom: 10px;")
        main_layout.addWidget(lbl_title)
        
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # --- تبويب الخزنة ---
        self.tab_treasury = QWidget()
        t_layout = QVBoxLayout(self.tab_treasury)
        
        balance_frame = QFrame()
        balance_frame.setStyleSheet("background-color: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 8px;")
        bf_layout = QHBoxLayout(balance_frame)
        bf_layout.addWidget(QLabel("💵 إجمالي رصيد الخزنة الحالي:"))
        self.lbl_balance = QLabel("0.00 ج.م")
        self.lbl_balance.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.lbl_balance.setStyleSheet("color: #10B981;")
        bf_layout.addWidget(self.lbl_balance)
        bf_layout.addStretch()
        t_layout.addWidget(balance_frame)
        
        form_frame = QFrame()
        form_layout = QFormLayout(form_frame)
        self.cmb_trans_type = QComboBox()
        self.cmb_trans_type.addItems(["إيداع نقدي للمحل (Deposit)", "سحب نقدي / مصاريف (Withdraw)", "تحويل إلى حساب بنكي / خزنة أخرى (Transfer Out)"])
        self.txt_amount = QLineEdit()
        self.txt_amount.setPlaceholderText("أدخل المبلغ المالي...")
        self.txt_desc = QLineEdit()
        self.txt_desc.setPlaceholderText("اكتب تفاصيل الحركة...")
        form_layout.addRow(QLabel("نوع الحركة المالية:"), self.cmb_trans_type)
        form_layout.addRow(QLabel("المبلغ المالي:"), self.txt_amount)
        form_layout.addRow(QLabel("البيان والسبب:"), self.txt_desc)
        
        self.btn_save_trans = QPushButton("تسجيل الحركة في الخزنة")
        self.btn_save_trans.setStyleSheet("QPushButton { background-color: #1E90FF; color: white; font-family: 'Segoe UI'; font-size: 13px; font-weight: bold; border-radius: 6px; padding: 8px 20px; }")
        form_layout.addRow(self.btn_save_trans)
        t_layout.addWidget(form_frame)
        
        self.table_history = QTableWidget()
        self.table_history.setColumnCount(4)
        self.table_history.setHorizontalHeaderLabels(["التاريخ والوقت", "نوع العملية", "المبلغ", "البيان والسبب"])
        self.table_history.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        t_layout.addWidget(QLabel("📋 كشف حركة الخزنة التفصيلي:"))
        t_layout.addWidget(self.table_history)
        self.tabs.addTab(self.tab_treasury, "💵 حركات ورصيد الخزنة")
        
        # --- تبويب الورديات ---
        self.tab_shifts = QWidget()
        s_layout = QVBoxLayout(self.tab_shifts)
        jard_frame = QFrame()
        jard_frame.setStyleSheet("background-color: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px;")
        jard_layout = QFormLayout(jard_frame)
        self.cmb_active_shifts = QComboBox()
        self.txt_actual_cash = QLineEdit()
        jard_layout.addRow(QLabel("الوردية النشطة:"), self.cmb_active_shifts)
        jard_layout.addRow(QLabel("المبلغ الفعلي بالدرج:"), self.txt_actual_cash)
        self.btn_close_shift = QPushButton("🔒 جرد وإغلاق الوردية المحددة")
        self.btn_close_shift.setStyleSheet("QPushButton { background-color: #EF4444; color: white; font-family: 'Segoe UI'; font-weight: bold; border-radius: 6px; padding: 8px 20px; }")
        jard_layout.addRow(self.btn_close_shift)
        s_layout.addWidget(jard_frame)
        
        self.table_shifts = QTableWidget()
        self.table_shifts.setColumnCount(6)
        self.table_shifts.setHorizontalHeaderLabels(["رقم الوردية", "الموظف", "بداية الوردية", "المفترض بالدرج", "الفعلي المستلم", "العجز / الزيادة"])
        self.table_shifts.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        s_layout.addWidget(QLabel("📜 سجل الورديات السابقة ونتائج الجرد:"))
        s_layout.addWidget(self.table_shifts)
        self.tabs.addTab(self.tab_shifts, "📊 جرد الورديات والكاشير")
        
        self.btn_close = QPushButton("إغلاق والعودة للقائمة الإدارية")
        self.btn_close.setStyleSheet("QPushButton { background-color: #64748B; color: white; font-family: 'Segoe UI'; font-weight: bold; border-radius: 6px; padding: 10px; }")
        main_layout.addWidget(self.btn_close)