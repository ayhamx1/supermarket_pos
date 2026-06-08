# -*- coding: utf-8 -*-
"""
🏪 Supermarket POS - Premium Fluent Shifts & Cashier Management UI
📂 Path: ui/admin/shifts_management.py
"""
import sys
import os

# 🛡️ حارس المسارات لتشغيل الملف بشكل مستقل وتجنب ModuleNotFoundError
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QGridLayout, QComboBox, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from app.controllers.admin.shift_controller import ShiftController

class ShiftsManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.controller = ShiftController()
        
        # ستايل شيت احترافي بنمط ويندوز 11 فلوينت
        self.setStyleSheet("""
            QWidget { background-color: #F3F3F3; font-family: 'Segoe UI', 'Arial'; color: #1B1B1B; }
            QFrame#cardFrame { background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 8px; padding: 15px; }
            QLabel#mainTitle { font-size: 18px; font-weight: 600; color: #1B1B1B; }
            QLabel#sectionTitle { font-size: 14px; font-weight: 600; color: #0067B8; padding-bottom: 5px; }
            QLabel#lblData { font-size: 13px; font-weight: bold; color: #5D5D5D; }
            QLabel#lblValue { font-size: 14px; font-weight: bold; color: #1B1B1B; }
            QLineEdit, QComboBox { border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px; background: white; font-size: 13px; }
            QPushButton#btnOpen { background-color: #107C41; color: white; border: none; border-radius: 4px; padding: 8px 16px; font-weight: bold; }
            QPushButton#btnOpen:hover { background-color: #0B592E; }
            QPushButton#btnClose { background-color: #C42B1C; color: white; border: none; border-radius: 4px; padding: 8px 16px; font-weight: bold; }
            QPushButton#btnClose:hover { background-color: #A32418; }
        """)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # 👑 ترويسة الشاشة المركزية
        title_lbl = QLabel("🏪 إدارة الورديات وجرد الخزينة وتمليك العهدة")
        title_lbl.setObjectName("mainTitle")
        main_layout.addWidget(title_lbl)

        # تصميم الواجهة على عمودين متجاورين (فتح وردية ضد إغلاق وجرد وردية)
        body_layout = QHBoxLayout()
        body_layout.setSpacing(16)

        # ------------------------------------------------------------
        # [العمود الأيمن]: فتح وردية جديدة وتسليم العهدة
        # ------------------------------------------------------------
        open_card = QFrame()
        open_card.setObjectName("cardFrame")
        open_layout = QVBoxLayout(open_card)
        open_layout.setSpacing(12)
        
        lbl_open_title = QLabel("🔑 فتح وردية جديدة وتسليم العهدة")
        lbl_open_title.setObjectName("sectionTitle")
        open_layout.addWidget(lbl_open_title)

        open_layout.addWidget(QLabel("اختيار الموظف / الكاشير المستلم:"))
        self.cmb_cashiers = QComboBox()
        self.cmb_cashiers.addItems(["أحمد محمود (كاشير 1)", "سارة علي (كاشير 2)", "محمد حسن (وردية ليلية)"])
        open_layout.addWidget(self.cmb_cashiers)

        open_layout.addWidget(QLabel("مبلغ عهدة البداية (استلام نقدى للدرج):"))
        self.txt_opening_balance = QLineEdit()
        self.txt_opening_balance.setPlaceholderText("مثال: 500.00 ج.م")
        open_layout.addWidget(self.txt_opening_balance)

        self.btn_open_shift = QPushButton("🚀 فتح الوردية وبدء العمل")
        self.btn_open_shift.setObjectName("btnOpen")
        self.btn_open_shift.clicked.connect(self.handle_open_shift)
        open_layout.addWidget(self.btn_open_shift)
        
        open_layout.addStretch()
        body_layout.addWidget(open_card, stretch=5)

        # ------------------------------------------------------------
        # [العمود الأيسر]: جرد الكاشير وإغلاق الوردية الحالية
        # ------------------------------------------------------------
        close_card = QFrame()
        close_card.setObjectName("cardFrame")
        close_layout = QVBoxLayout(close_card)
        close_layout.setSpacing(10)

        lbl_close_title = QLabel("🔒 جرد وتسليم الخزينة وإغلاق الوردية")
        lbl_close_title.setObjectName("sectionTitle")
        lbl_close_title.setStyleSheet("color: #C42B1C;")
        close_layout.addWidget(lbl_close_title)

        # شبكة لعرض بيانات الوردية النشطة المسجلة بالسيستم
        self.grid_active_info = QGridLayout()
        self.grid_active_info.setSpacing(8)
        close_layout.addLayout(self.grid_active_info)

        close_layout.addWidget(QLabel("المبلغ الفعلي الموجود داخل الدرج حالياً (الجرد اليدوي):"))
        self.txt_actual_cash = QLineEdit()
        self.txt_actual_cash.setPlaceholderText("أدخل المبلغ المالي الفعلي بالخزنة...")
        self.txt_actual_cash.setStyleSheet("font-size: 14px; font-weight: bold; border-color: #0067B8;")
        close_layout.addWidget(self.txt_actual_cash)

        self.btn_close_shift = QPushButton("🏁 إنهاء الجرد وإغلاق الوردية")
        self.btn_close_shift.setObjectName("btnClose")
        self.btn_close_shift.clicked.connect(self.handle_close_shift)
        close_layout.addWidget(self.btn_close_shift)

        close_layout.addStretch()
        body_layout.addWidget(close_card, stretch=5)

        main_layout.addLayout(body_layout)
        
        # شحن بيانات الوردية المفتوحة فور تشغيل الشاشة
        self.refresh_active_shift_ui()

    def refresh_active_shift_ui(self):
        """تحديث بيانات الوردية النشطة في جانب الجرد"""
        # تنظيف الجريد أولاً
        for i in reversed(range(self.grid_active_info.count())): 
            self.grid_active_info.itemAt(i).widget().setParent(None)

        shift = self.controller.get_active_shift_details()
        if shift:
            infos = [
                ("رقم الوردية الحالية:", shift["shift_id"]),
                ("الموظف المسؤول:", shift["cashier_name"]),
                ("تاريخ ووقت الفتح:", shift["open_time"]),
                ("العهدة الافتتاحية:", f"{shift['opening_balance']:.2f} ج.م"),
                ("مبيعات السيستم الإلكترونية:", f"{shift['system_sales']:.2f} ج.م"),
                ("المبلغ المتوقع بالخزنة:", f"{(shift['opening_balance'] + shift['system_sales']):.2f} ج.م")
            ]
            for row, (lbl, val) in enumerate(infos):
                l_lbl = QLabel(lbl); l_lbl.setObjectName("lblData")
                l_val = QLabel(val); l_val.setObjectName("lblValue")
                if "المتوقع" in lbl: l_val.setStyleSheet("color: #0067B8; font-size: 15px;")
                self.grid_active_info.addWidget(l_lbl, row, 0)
                self.grid_active_info.addWidget(l_val, row, 1)
            self.btn_close_shift.setEnabled(True)
            self.txt_actual_cash.setEnabled(True)
        else:
            lbl_empty = QLabel("⚠️ لا توجد وردية مفتوحة نشطة حالياً بالنظام.")
            lbl_empty.setStyleSheet("color: #E17B00; font-weight: bold; font-size: 13px; padding: 10px;")
            self.grid_active_info.addWidget(lbl_empty, 0, 0)
            self.btn_close_shift.setEnabled(False)
            self.txt_actual_cash.setEnabled(False)

    def handle_open_shift(self):
        """التعامل مع زر فتح الوردية واستلام العهدة"""
        cashier = self.cmb_cashiers.currentText()
        balance_text = self.txt_opening_balance.text().strip()
        
        if not balance_text:
            QMessageBox.warning(self, "تنبيه", "الرجاء إدخال مبلغ عهدة الاستلام لبدء الوردية!")
            return
        
        try:
            success, msg = self.controller.open_new_shift(cashier, balance_text)
            if success:
                QMessageBox.information(self, "تم التسليم", msg)
                self.txt_opening_balance.clear()
                self.refresh_active_shift_ui()
        except ValueError:
            QMessageBox.critical(self, "خطأ مدخلات", "الرجاء إدخال رقم مالي صحيح لقيمة العهدة!")

    def handle_close_shift(self):
        """التعامل مع جرد الكاشير وحساب الفروقات المالية المباشرة"""
        actual_text = self.txt_actual_cash.text().strip()
        if not actual_text:
            QMessageBox.warning(self, "تنبيه الجرد", "الرجاء إدخال المبلغ الفعلي الموجود بالدرج لإتمام عملية المطابقة!")
            return
        
        try:
            success, report = self.controller.close_current_shift(actual_text)
            if success:
                # عرض تقرير المطابقة المالية للمدير
                diff = report["difference"]
                if diff == 0:
                    result_msg = "✅ الجرد سليم تماماً والمبلغ الفعلي مطابق تماماً لحسابات النظام المالي."
                elif diff < 0:
                    result_msg = f"🚨 يوجد عجز مالي في الخزنة بقيمة: {abs(diff):.2f} ج.م (يتحملها الموظف المسؤول)."
                else:
                    result_msg = f"📈 توجد زيادة مالية غير مبررة بالخزنة بقيمة: {diff:.2f} ج.م."

                summary = f"📋 تقرير تسليم الوردية رقم: {report['shift_id']}\n\n" \
                          f"• الإجمالي المفترض: {report['expected_total']:.2f} ج.م\n" \
                          f"• الإجمالي الفعلي: {report['actual_cash']:.2f} ج.م\n" \
                          f"• النتيجة: {report['status']}\n\n" \
                          f"{result_msg}"
                
                QMessageBox.information(self, "تقرير نهاية الوردية والجرد", summary)
                self.txt_actual_cash.clear()
                self.refresh_active_shift_ui()
        except ValueError:
            QMessageBox.critical(self, "خطأ مدخلات", "الرجاء إدخال رقم مالي صحيح لقيمة الجرد الفعلي!")

# ميزة التشغيل الفردي والمعزول لفحص الشاشة بدقة
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShiftsManagementWidget()
    window.setWindowTitle("فحص لوحة إدارة الورديات والجرد - نظام مستقل")
    window.resize(1000, 500)
    window.show()
    sys.exit(app.exec())