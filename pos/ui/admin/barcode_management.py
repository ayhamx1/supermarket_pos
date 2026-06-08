# -*- coding: utf-8 -*-
"""
🏷️ Supermarket POS - Premium Fluent Barcode & Label Management UI
📂 Path: ui/admin/barcode_management.py
"""
import sys
import os

# 🛡️ حارس المسارات لتشغيل الملف بشكل مستقل وتجنب ModuleNotFoundError
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QGridLayout, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QSpinBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from app.controllers.admin.barcode_controller import BarcodeController

class BarcodeManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.controller = BarcodeController()
        
        # ستايل شيت احترافي متوافق مع معايير Windows 11 Fluent Design
        self.setStyleSheet("""
            QWidget { background-color: #F3F3F3; font-family: 'Segoe UI', 'Arial'; color: #1B1B1B; }
            QFrame#cardFrame { background: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 8px; padding: 15px; }
            QLabel#mainTitle { font-size: 18px; font-weight: 600; color: #1B1B1B; }
            QLabel#sectionTitle { font-size: 14px; font-weight: 600; color: #0067B8; padding-bottom: 5px; }
            QLineEdit, QSpinBox { border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px; background: white; font-size: 13px; }
            QLineEdit:focus, QSpinBox:focus { border-color: #0067B8; }
            QPushButton#btnPrimary { background-color: #0067B8; color: white; border: none; border-radius: 4px; padding: 8px 16px; font-weight: bold; }
            QPushButton#btnPrimary:hover { background-color: #005A9E; }
            QPushButton#btnSecondary { background-color: transparent; border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 12px; font-size: 13px; }
            QPushButton#btnSecondary:hover { background-color: #F5F5F5; }
            QTableWidget { background-color: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 4px; gridline-color: #E5E5E5; }
            QHeaderView::section { background-color: #FAFAFA; font-weight: bold; border: none; border-bottom: 1px solid #E5E5E5; padding: 4px; }
            QFrame#barcodePreview { background-color: #FFFFFF; border: 2px solid #1B1B1B; border-radius: 4px; padding: 10px; }
        """)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # 👑 ترويسة الشاشة المركزية
        title_lbl = QLabel("🏷️ وحدة إنشاء وطباعة الباركود وملصقات الأسعار الذكية")
        title_lbl.setObjectName("mainTitle")
        main_layout.addWidget(title_lbl)

        # تقسيم الشاشة إلى عمودين متجاورين
        body_layout = QHBoxLayout()
        body_layout.setSpacing(16)

        # ------------------------------------------------------------
        # [العمود الأيمن]: إنشاء وتصميم ملصق باركود جديد
        # ------------------------------------------------------------
        design_card = QFrame()
        design_card.setObjectName("cardFrame")
        design_layout = QVBoxLayout(design_card)
        design_layout.setSpacing(12)
        
        lbl_design_title = QLabel("✨ إنشاء وتوليد ملصق جديد")
        lbl_design_title.setObjectName("sectionTitle")
        design_layout.addWidget(lbl_design_title)

        grid = QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(QLabel("اسم الصنف المعبأ:"), 0, 0)
        self.txt_prod_name = QLineEdit()
        self.txt_prod_name.setPlaceholderText("مثال: عدس أصفر معبأ 1ك")
        grid.addWidget(self.txt_prod_name, 0, 1)
        
        grid.addWidget(QLabel("سعر البيع الافتراضي:"), 1, 0)
        self.txt_prod_price = QLineEdit()
        self.txt_prod_price.setPlaceholderText("0.00 ج.م")
        grid.addWidget(self.txt_prod_price, 1, 1)
        
        grid.addWidget(QLabel("رقم الباركود الحالي/المقترح:"), 2, 0)
        h_bar_lay = QHBoxLayout()
        self.txt_barcode_val = QLineEdit()
        h_bar_lay.addWidget(self.txt_barcode_val)
        btn_gen = QPushButton("🔄 توليد تلقائي")
        btn_gen.setObjectName("btnSecondary")
        btn_gen.clicked.connect(self.handle_auto_generate)
        h_bar_lay.addWidget(btn_gen)
        grid.addLayout(h_bar_lay, 2, 1)

        grid.addWidget(QLabel("عدد النسخ المطلوبة:"), 3, 0)
        self.num_copies = QSpinBox()
        self.num_copies.setRange(1, 100)
        self.num_copies.setValue(1)
        grid.addWidget(self.num_copies, 3, 1)

        design_layout.addLayout(grid)
        
        # صندوق محاكاة شكل الملصق المطبوع (Preview)
        design_layout.addWidget(QLabel("👁️ معاينة حية لشكل الملصق (Label Preview):"))
        self.preview_frame = QFrame()
        self.preview_frame.setObjectName("barcodePreview")
        preview_layout = QVBoxLayout(self.preview_frame)
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lbl_preview_name = QLabel("[اسم الصنف سيظهر هنا]")
        self.lbl_preview_name.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.lbl_preview_barcode_visual = QLabel("|| ||| || |||| ||| || ||| ||") # تمثيل عشوائي لخطوط الباركود
        self.lbl_preview_barcode_visual.setFont(QFont("Courier New", 20, QFont.Weight.Bold))
        self.lbl_preview_barcode_num = QLabel("0000000000000")
        self.lbl_preview_price = QLabel("السعر: 0.00 ج.م")
        self.lbl_preview_price.setStyleSheet("font-weight: bold; color: #0067B8; font-size: 14px;")
        
        preview_layout.addWidget(self.lbl_preview_name)
        preview_layout.addWidget(self.lbl_preview_barcode_visual)
        preview_layout.addWidget(self.lbl_preview_barcode_num)
        preview_layout.addWidget(self.lbl_preview_price)
        design_layout.addWidget(self.preview_frame)

        # ربط التحديث المباشر للمعاينة عند الكتابة
        self.txt_prod_name.textChanged.connect(lambda t: self.lbl_preview_name.setText(t if t else "[اسم الصنف سيظهر هنا]"))
        self.txt_prod_price.textChanged.connect(lambda t: self.lbl_preview_price.setText(f"السعر: {t} ج.م" if t else "السعر: 0.00 ج.م"))
        self.txt_barcode_val.textChanged.connect(lambda t: self.lbl_preview_barcode_num.setText(t if t else "0000000000000"))

        self.btn_print_now = QPushButton("🖨️ طباعة الملصق الآن")
        self.btn_print_now.setObjectName("btnPrimary")
        self.btn_print_now.clicked.connect(self.handle_print_label)
        design_layout.addWidget(self.btn_print_now)
        
        design_layout.addStretch()
        body_layout.addWidget(design_card, stretch=5)

        # ------------------------------------------------------------
        # [العمود الأيسر]: سجل الملصقات المطبوعة وإعادة الطباعة الفورية
        # ------------------------------------------------------------
        history_card = QFrame()
        history_card.setObjectName("cardFrame")
        history_layout = QVBoxLayout(history_card)
        
        lbl_hist_title = QLabel("📋 ملصقات تمت طباعتها مؤخراً (إعادة طباعة فورية)")
        lbl_hist_title.setObjectName("sectionTitle")
        history_layout.addWidget(lbl_hist_title)

        self.table_history = QTableWidget()
        self.table_history.setColumnCount(4)
        self.table_history.setHorizontalHeaderLabels(["الباركود", "اسم الصنف", "السعر", "إعادة طباعة"])
        self.table_history.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table_history.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        history_layout.addWidget(self.table_history)

        body_layout.addWidget(history_card, stretch=5)

        main_layout.addLayout(body_layout)
        
        # شحن الجدول بالبيانات التاريخية فور فتح الشاشة
        self.refresh_history_table()

    def handle_auto_generate(self):
        """توليد كود باركود عشوائي للسلعة المحلية"""
        new_code = self.controller.generate_new_barcode()
        self.txt_barcode_val.setText(new_code)

    def refresh_history_table(self):
        """تحديث جدول ملصقات السجل الأخير"""
        history_data = self.controller.get_history()
        self.table_history.setRowCount(len(history_data))
        
        for row_idx, item in enumerate(history_data):
            self.table_history.setItem(row_idx, 0, QTableWidgetItem(item["barcode"]))
            self.table_history.setItem(row_idx, 1, QTableWidgetItem(item["product_name"]))
            self.table_history.setItem(row_idx, 2, QTableWidgetItem(f"{item['price']:.2f} ج.م"))
            
            # إنشاء زر سريع داخل الجدول لإعادة طباعة الملصق بضغطة زر واحدة
            btn_reprint = QPushButton("🔁 إعادة طباعة")
            btn_reprint.setObjectName("btnSecondary")
            btn_reprint.setStyleSheet("padding: 2px 5px; font-size: 11px;")
            # استخدام تقنية الـ Lambda الحذرة لتمرير البيانات المحددة للسطر للطباعة
            btn_reprint.clicked.connect(lambda checked, i=item: self.handle_reprint_action(i))
            self.table_history.setCellWidget(row_idx, 3, btn_reprint)

    def handle_print_label(self):
        """معالجة أمر طباعة الملصق الجديد"""
        name = self.txt_prod_name.text().strip()
        price = self.txt_prod_price.text().strip()
        barcode = self.txt_barcode_val.text().strip()
        qty = self.num_copies.value()

        if not name or not price or not barcode:
            QMessageBox.warning(self, "تنبيه مدخلات", "الرجاء إكمال كافة الحقول (الاسم، السعر، والباركود) لتوليد الملصق!")
            return

        success, msg = self.controller.send_to_printer(barcode, name, price, qty)
        if success:
            QMessageBox.information(self, "نجاح الطباعة", msg)
            self.refresh_history_table()
            # تنظيف الحقول لتهيئتها للصنف التالي
            self.txt_prod_name.clear()
            self.txt_prod_price.clear()
            self.txt_barcode_val.clear()
            self.num_copies.setValue(1)

    def handle_reprint_action(self, item_data):
        """إعادة طباعة الملصق التاريخي مباشرة مع تحديد كمية سريعة"""
        success, msg = self.controller.send_to_printer(
            item_data["barcode"], 
            item_data["product_name"], 
            item_data["price"], 
            qty=1
        )
        if success:
            QMessageBox.information(self, "إعادة الطباعة", f"تمت إعادة طباعة ملصق لـ ({item_data['product_name']}) بنجاح.")

# ميزة التشغيل الفردي والمعزول لفحص الشاشة بدقة
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BarcodeManagementWidget()
    window.setWindowTitle("فحص وحدة إدارة وطباعة الباركود - مستقل")
    window.resize(1100, 520)
    window.show()
    sys.exit(app.exec())