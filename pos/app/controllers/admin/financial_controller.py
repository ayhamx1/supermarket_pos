import sys
import psycopg2
from datetime import datetime
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QComboBox, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QFormLayout, QFrame, 
                             QTabWidget, QMessageBox, QWidget) 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

# إعدادات قاعدة البيانات الخاصة بمشروعك
DB_PARAMS = {
    "dbname": "supermarket_db",
    "user": "postgres",
    "password": "123456",  
    "host": "localhost",
    "port": "5432"
}

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
    QPushButton { font-family: 'Segoe UI', 'Cairo'; font-weight: bold; border: none; }
"""

class FinancialController(QDialog):
    def __init__(self, admin_id=1, parent=None):
        super().__init__(parent)
        self.admin_id = admin_id
        self.setWindowTitle("الإدارة المالية - جرد الورديات وحركات الخزنة")
        self.setFixedSize(900, 650)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(FINANCIAL_STYLE)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        lbl_title = QLabel("💼 النظام المالي المركزي ولوحة تحكم المدير")
        lbl_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        lbl_title.setStyleSheet("color: #1e5378; margin-bottom: 10px;")
        main_layout.addWidget(lbl_title)
        
        self.tabs = QTabWidget()
        self.init_treasury_tab()  
        self.init_shifts_tab()    
        main_layout.addWidget(self.tabs)
        
        self.btn_close = QPushButton("إغلاق والعودة للقائمة الإدارية")
        self.btn_close.setStyleSheet("QPushButton { background-color: #64748B; color: white; font-size: 14px; border-radius: 6px; padding: 10px; } QPushButton:hover { background-color: #475569; }")
        self.btn_close.clicked.connect(self.accept)
        main_layout.addWidget(self.btn_close)
        
        self.load_treasury_data()
        self.load_shifts_data()

    def init_treasury_tab(self):
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        
        balance_frame = QFrame()
        balance_frame.setStyleSheet("background-color: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 8px;")
        bf_layout = QHBoxLayout(balance_frame)
        lbl_bal_txt = QLabel("💵 إجمالي رصيد الخزنة الحالي:")
        lbl_bal_txt.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.lbl_balance = QLabel("0.00 ج.م")
        self.lbl_balance.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.lbl_balance.setStyleSheet("color: #10B981;")
        bf_layout.addWidget(lbl_bal_txt)
        bf_layout.addWidget(self.lbl_balance)
        bf_layout.addStretch()
        layout.addWidget(balance_frame)
        
        form_frame = QFrame()
        form_layout = QFormLayout(form_frame)
        
        self.cmb_trans_type = QComboBox()
        self.cmb_trans_type.addItems([
            "إيداع نقدي للمحل (Deposit)", 
            "سحب نقدي / مصاريف (Withdraw)", 
            "تحويل إلى حساب بنكي / خزنة أخرى (Transfer Out)"
        ])
        
        self.txt_amount = QLineEdit()
        self.txt_amount.setPlaceholderText("أدخل المبلغ المالي...")
        
        self.txt_desc = QLineEdit()
        self.txt_desc.setPlaceholderText("اكتب تفاصيل الحركة...")
        
        form_layout.addRow(QLabel("نوع الحركة المالية:"), self.cmb_trans_type)
        form_layout.addRow(QLabel("المبلغ المالي:"), self.txt_amount)
        form_layout.addRow(QLabel("البيان والسبب:"), self.txt_desc)
        
        self.btn_save_trans = QPushButton("تسجيل الحركة في الخزنة")
        self.btn_save_trans.setStyleSheet("QPushButton { background-color: #1E90FF; color: white; font-size: 13px; border-radius: 6px; padding: 8px 20px; } QPushButton:hover { background-color: #1c82ec; }")
        self.btn_save_trans.clicked.connect(self.process_treasury_transaction)
        form_layout.addRow(self.btn_save_trans)
        layout.addWidget(form_frame)
        
        layout.addWidget(QLabel("📋 كشف حركة الخزنة التفصيلي:"))
        self.table_history = QTableWidget()
        self.table_history.setColumnCount(4)
        self.table_history.setHorizontalHeaderLabels(["التاريخ والوقت", "نوع العملية", "المبلغ", "البيان والسبب"])
        self.table_history.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_history)
        
        self.tabs.addTab(tab_widget, "💵 حركات ورصيد الخزنة")

    def init_shifts_tab(self):
        tab_widget = QWidget()
        layout = QVBoxLayout(tab_widget)
        
        jard_frame = QFrame()
        jard_frame.setStyleSheet("background-color: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px;")
        jard_layout = QFormLayout(jard_frame)
        jard_layout.setContentsMargins(12, 12, 12, 12)
        
        title_jard = QLabel("🔍 جرد وإغلاق وردية كاشير نشطة")
        title_jard.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        jard_layout.addRow(title_jard)
        
        self.cmb_active_shifts = QComboBox()
        self.txt_actual_cash = QLineEdit()
        self.txt_actual_cash.setPlaceholderText("المبلغ الفعلي المستلم من درج الكاشير...")
        
        jard_layout.addRow(QLabel("الوردية النشطة:"), self.cmb_active_shifts)
        jard_layout.addRow(QLabel("المبلغ الفعلي بالدرج:"), self.txt_actual_cash)
        
        self.btn_close_shift = QPushButton("🔒 جرد وإغلاق الوردية المحددة")
        self.btn_close_shift.setStyleSheet("QPushButton { background-color: #EF4444; color: white; font-size: 13px; border-radius: 6px; padding: 8px 20px; } QPushButton:hover { background-color: #dc2626; }")
        self.btn_close_shift.clicked.connect(self.process_shift_closure)
        jard_layout.addRow(self.btn_close_shift)
        layout.addWidget(jard_frame)
        
        layout.addWidget(QLabel("📜 سجل الورديات السابقة ونتائج الجرد الإداري:"))
        self.table_shifts = QTableWidget()
        self.table_shifts.setColumnCount(6)
        self.table_shifts.setHorizontalHeaderLabels(["رقم الوردية", "الموظف", "بداية الوردية", "المفترض بالدرج", "الفعلي المستلم", "العجز / الزيادة"])
        self.table_shifts.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table_shifts)
        
        self.tabs.addTab(tab_widget, "📊 جرد الورديات والكاشير")

    def load_treasury_data(self):
        try:
            conn = psycopg2.connect(**DB_PARAMS); cursor = conn.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(
                    CASE 
                        WHEN transaction_type IN ('deposit', 'transfer_in') THEN amount 
                        WHEN transaction_type IN ('withdraw', 'transfer_out') THEN -amount 
                        ELSE 0 
                    END
                ), 0) FROM treasury_transactions;
            """)
            balance = cursor.fetchone()[0]
            self.lbl_balance.setText(f"{float(balance):.2f} ج.م")
            
            cursor.execute("SELECT transaction_date, transaction_type, amount, description FROM treasury_transactions ORDER BY transaction_date DESC;")
            rows = cursor.fetchall()
            self.table_history.setRowCount(0)
            
            type_mapping = {
                'deposit': 'إيداع نقدي يدوياً',
                'withdraw': 'سحب مصاريف / يدوياً',
                'transfer_out': 'تحويل خارجي / بنكي',
                'transfer_in': 'مبيعات الكاشير آلياً'
            }
            
            for r_idx, r_data in enumerate(rows):
                self.table_history.insertRow(r_idx)
                self.table_history.setItem(r_idx, 0, QTableWidgetItem(r_data[0].strftime("%Y-%m-%d %H:%M")))
                
                t_type = type_mapping.get(r_data[1], r_data[1])
                type_item = QTableWidgetItem(t_type)
                if r_data[1] in ['deposit', 'transfer_in']:
                    type_item.setForeground(QColor("#10B981"))  
                else:
                    type_item.setForeground(QColor("#EF4444"))  
                    
                self.table_history.setItem(r_idx, 1, type_item)
                self.table_history.setItem(r_idx, 2, QTableWidgetItem(f"{float(r_data[2]):.2f}"))
                self.table_history.setItem(r_idx, 3, QTableWidgetItem(str(r_data[3])))
                
            cursor.close(); conn.close()
        except Exception as e:
            print(f"Error loading treasury data: {e}")

    def process_treasury_transaction(self):
        amount_txt = self.txt_amount.text().strip()
        desc = self.txt_desc.text().strip()
        idx = self.cmb_trans_type.currentIndex()
        
        if not amount_txt or not desc:
            QMessageBox.warning(self, "تنبيه", "يرجى ملء خانة المبلغ والبيان أولاً!")
            return
            
        try:
            amount = float(amount_txt)
            if amount <= 0: raise ValueError
        except ValueError:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال رقم مالي صحيح أكبر من الصفر.")
            return
            
        t_type = 'deposit' if idx == 0 else 'withdraw' if idx == 1 else 'transfer_out'
        
        try:
            conn = psycopg2.connect(**DB_PARAMS); cursor = conn.cursor()
            cursor.execute("INSERT INTO treasury_transactions (transaction_type, amount, description, user_id) VALUES (%s, %s, %s, %s);",
                           (t_type, amount, desc, self.admin_id))
            conn.commit(); cursor.close(); conn.close()
            
            self.txt_amount.clear(); self.txt_desc.clear()
            self.load_treasury_data()
            QMessageBox.information(self, "نجاح", "تم تسجيل الحركة المالية بنجاح!")
        except Exception as e:
            QMessageBox.critical(self, "خطأ في قاعدة البيانات", str(e))

    def load_shifts_data(self):
        try:
            conn = psycopg2.connect(**DB_PARAMS); cursor = conn.cursor()
            self.cmb_active_shifts.clear()
            cursor.execute("SELECT s.id, u.username FROM cashier_shifts s JOIN users u ON s.user_id = u.id WHERE s.status = 'open';")
            for s_id, u_name in cursor.fetchall():
                self.cmb_active_shifts.addItem(f"وردية رقم {s_id} - الكاشير: {u_name}", s_id)
                
            cursor.execute("""
                SELECT s.id, u.username, s.start_time, s.expected_cash, s.actual_cash, s.difference 
                FROM cashier_shifts s 
                JOIN users u ON s.user_id = u.id 
                WHERE s.status = 'closed' 
                ORDER BY s.end_time DESC;
            """)
            shifts_rows = cursor.fetchall()
            self.table_shifts.setRowCount(0)
            
            for r_idx, r_data in enumerate(shifts_rows):
                self.table_shifts.insertRow(r_idx)
                self.table_shifts.setItem(r_idx, 0, QTableWidgetItem(str(r_data[0])))
                self.table_shifts.setItem(r_idx, 1, QTableWidgetItem(str(r_data[1])))
                self.table_shifts.setItem(r_idx, 2, QTableWidgetItem(r_data[2].strftime("%Y-%m-%d %H:%M")))
                self.table_shifts.setItem(r_idx, 3, QTableWidgetItem(f"{float(r_data[3]):.2f}"))
                self.table_shifts.setItem(r_idx, 4, QTableWidgetItem(f"{float(r_data[4]):.2f}"))
                
                diff = float(r_data[5])
                diff_item = QTableWidgetItem()
                if diff < 0:
                    diff_item.setForeground(QColor("#EF4444"))
                    diff_item.setText(f"عجز: {abs(diff):.2f}")
                elif diff > 0:
                    diff_item.setForeground(QColor("#10B981"))
                    diff_item.setText(f"زيادة: {diff:.2f}")
                else:
                    diff_item.setForeground(QColor("#475569"))
                    diff_item.setText("متطابق (0.00)")
                    
                self.table_shifts.setItem(r_idx, 5, diff_item)
                
            cursor.close(); conn.close()
        except Exception as e:
            print(f"Error loading shifts data: {e}")

    def process_shift_closure(self):
        if self.cmb_active_shifts.currentIndex() == -1:
            QMessageBox.warning(self, "تنبيه", "لا توجد ورديات مفتوحة حالياً لجردها.")
            return
            
        shift_id = self.cmb_active_shifts.currentData()
        actual_cash_txt = self.txt_actual_cash.text().strip()
        
        if not actual_cash_txt:
            QMessageBox.warning(self, "تنبيه", "يرجى إدخال المبلغ المالي الفعلي المستلم لإتمام الجرد!")
            return
            
        try:
            actual_cash = float(actual_cash_txt)
            if actual_cash < 0: raise ValueError
        except ValueError:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال مبلغ مالي صحيح.")
            return
            
        try:
            conn = psycopg2.connect(**DB_PARAMS); cursor = conn.cursor()
            cursor.execute("SELECT expected_cash FROM cashier_shifts WHERE id = %s;", (shift_id,))
            expected_cash = float(cursor.fetchone()[0])
            
            difference = actual_cash - expected_cash
            
            cursor.execute("""
                UPDATE cashier_shifts 
                SET end_time = NOW(), actual_cash = %s, difference = %s, status = 'closed' 
                WHERE id = %s;
            """, (actual_cash, difference, shift_id))
            
            conn.commit(); cursor.close(); conn.close()
            
            self.txt_actual_cash.clear()
            self.load_shifts_data()
            self.load_treasury_data()
            
            if difference == 0:
                QMessageBox.information(self, "تم الجرد", "عملية الجرد مطابقة وممتازة، الوردية سليمة 100%.")
            elif difference < 0:
                QMessageBox.warning(self, "تم الجرد - يوجد عجز", f"انتبه: تم تسجيل عجز مالي قدره ({abs(difference):.2f} ج.م) في عهدة هذه الوردية.")
            else:
                QMessageBox.information(self, "تم الجرد - توجد زيادة", f"تم التسجيل: توجد زيادة مالية غير متوقعة بالدرج قدرها ({difference:.2f} ج.م).")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    manager = FinancialController(admin_id=1)
    manager.show()
    sys.exit(app.exec())