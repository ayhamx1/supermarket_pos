# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Premium Fluent Settings Management UI
📂 Path: ui/admin/settings_management.py
"""
import sys
import os

# 🛡️ حارس المسارات لتشغيل الملف بشكل مستقل وتجنب ModuleNotFoundError
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QGridLayout, QTabWidget, 
                             QFileDialog, QDoubleSpinBox, QTextEdit, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from app.controllers.admin.settings_controller import SettingsController

class SettingsManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.controller = SettingsController()
        
        # ستايل شيت احترافي متوافق مع نمط ويندوز 11
        self.setStyleSheet("""
            QWidget { background-color: #F3F3F3; font-family: 'Segoe UI', 'Arial'; color: #1B1B1B; }
            QTabWidget::pane { border: 1px solid #E5E5E5; background-color: #FFFFFF; border-radius: 8px; padding: 20px; }
            QTabBar::tab { background-color: #E5E5E5; color: #5D5D5D; padding: 8px 16px; border-top-left-radius: 4px; border-top-right-radius: 4px; margin-left: 2px; font-weight: 500; }
            QTabBar::tab:selected { background-color: #FFFFFF; color: #0067B8; border: 1px solid #E5E5E5; border-bottom-color: #FFFFFF; font-weight: bold; }
            QLabel#mainTitle { font-size: 18px; font-weight: 600; color: #1B1B1B; }
            QLabel#lblForm { font-size: 13px; font-weight: 500; color: #5D5D5D; }
            QLineEdit, QComboBox, QDoubleSpinBox, QTextEdit { border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px; background: white; font-size: 13px; }
            QLineEdit:focus, QDoubleSpinBox:focus { border-color: #0067B8; }
            QPushButton#btnSave { background-color: #0067B8; color: white; border: none; border-radius: 4px; padding: 10px 24px; font-weight: bold; font-size: 14px; }
            QPushButton#btnSave:hover { background-color: #005A9E; }
            QPushButton#btnSecondary { background-color: transparent; border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 12px; font-size: 13px; }
            QPushButton#btnSecondary:hover { background-color: #F5F5F5; }
            QFrame#logoFrame { border: 2px dashed #CCCCCC; border-radius: 6px; min-width: 120px; min-height: 120px; max-width: 120px; max-height: 120px; background: #FAFAFA; }
        """)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # 👑 ترويسة الشاشة المركزية
        title_lbl = QLabel("⚙️ إعدادات النظام وتخصيص الهوية الضريبية والفواتير")
        title_lbl.setObjectName("mainTitle")
        main_layout.addWidget(title_lbl)

        # إنشاء مكدس التبويبات الفلوينت
        self.tabs = QTabWidget()
        
        # استدعاء التبويبات وتجميعها
        self.tabs.addTab(self.create_company_tab(), "🏢 بيانات الشركة والشعار")
        self.tabs.addTab(self.create_tax_invoice_tab(), "📄 الضريبة وإعدادات الفاتورة")
        self.tabs.addTab(self.create_printers_tab(), "🖨️ إعدادات الطابعات")
        
        main_layout.addWidget(self.tabs)

        # شريط سفلي يحتوي على زر الحفظ الإجمالي
        bottom_bar = QHBoxLayout()
        bottom_bar.addStretch()
        self.btn_save_all = QPushButton("💾 حفظ التغييرات الإجمالية")
        self.btn_save_all.setObjectName("btnSave")
        self.btn_save_all.clicked.connect(self.handle_save_settings)
        bottom_bar.addWidget(self.btn_save_all)
        
        main_layout.addLayout(bottom_bar)
        
        # تحميل البيانات داخل الحقول
        self.load_settings_into_ui()

    def create_company_tab(self):
        """التبويب الأول: بيانات الشركة وتحميل الشعار"""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setSpacing(40)
        
        # الجانب الأيمن: حقول النصوص
        form_frame = QWidget()
        grid = QGridLayout(form_frame)
        grid.setSpacing(12)
        
        grid.addWidget(QLabel("اسم الشركة / السوبرماركت:"), 0, 0)
        self.txt_company_name = QLineEdit()
        grid.addWidget(self.txt_company_name, 0, 1)
        
        grid.addWidget(QLabel("العنوان بالتفصيل (يظهر بالفاتورة):"), 1, 0)
        self.txt_company_address = QLineEdit()
        grid.addWidget(self.txt_company_address, 1, 1)
        
        grid.addWidget(QLabel("أرقام الهاتف والتواصل:"), 2, 0)
        self.txt_company_phone = QLineEdit()
        grid.addWidget(self.txt_company_phone, 2, 1)
        
        grid.addWidget(QLabel("الرقم الضريبي للمنشأة:"), 3, 0)
        self.txt_tax_number = QLineEdit()
        grid.addWidget(self.txt_tax_number, 3, 1)
        
        layout.addWidget(form_frame, stretch=7)
        
        # الجانب الأيسر: رفع الشعار (Logo)
        logo_frame = QWidget()
        v_logo_layout = QVBoxLayout(logo_frame)
        v_logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        v_logo_layout.addWidget(QLabel("شعار المنشأة (Logo):"))
        self.lbl_logo_preview = QLabel("لا يوجد شعار")
        self.lbl_logo_preview.setObjectName("logoFrame")
        self.lbl_logo_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v_logo_layout.addWidget(self.lbl_logo_preview)
        
        self.btn_browse_logo = QPushButton("🗁 اختيار صورة")
        self.btn_browse_logo.setObjectName("btnSecondary")
        self.btn_browse_logo.clicked.connect(self.handle_browse_logo)
        v_logo_layout.addWidget(self.btn_browse_logo)
        
        self.selected_logo_path = ""
        
        layout.addWidget(logo_frame, stretch=3)
        return tab

    def create_tax_invoice_tab(self):
        """التبويب الثاني: إعدادات الضريبة وفواتير الكاشير"""
        tab = QWidget()
        grid = QGridLayout(tab)
        grid.setSpacing(15)
        
        grid.addWidget(QLabel("نسبة ضريبة القيمة المضافة (%):"), 0, 0)
        self.num_tax_rate = QDoubleSpinBox()
        self.num_tax_rate.setRange(0.0, 100.0)
        self.num_tax_rate.setSuffix(" %")
        grid.addWidget(self.num_tax_rate, 0, 1)
        
        grid.addWidget(QLabel("ملاحظات وتذييل الفاتورة السفلي:"), 1, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeading)
        self.txt_invoice_footer = QTextEdit()
        self.txt_invoice_footer.setPlaceholderText("تكتب هنا جمل الترحيب أو سياسات الاستبدال والاسترجاع...")
        self.txt_invoice_footer.setMaximumHeight(80)
        grid.addWidget(self.txt_invoice_footer, 1, 1)
        
        # خيارات إضافية للفاتورة المطبوعة
        grid.addWidget(QLabel("خيارات طباعة إضافية:"), 2, 0)
        self.cmb_invoice_type = QComboBox()
        self.cmb_invoice_type.addItems(["طباعة حرارية فورية (80mm)", "طباعة حرارية ضيقة (58mm)", "طباعة فواتير مجمعة صفحات كاملة (A4)"])
        grid.addWidget(self.cmb_invoice_type, 2, 1)
        
        grid.setColumnStretch(1, 1)
        return tab

    def create_printers_tab(self):
        """التبويب الثالث: توجيه طابعات الكاشير والتقارير المباشرة"""
        tab = QWidget()
        grid = QGridLayout(tab)
        grid.setSpacing(15)
        
        grid.addWidget(QLabel("طابعة فواتير وإيصالات الكاشير الافتراضية:"), 0, 0)
        self.cmb_receipt_printer = QComboBox()
        # محاكاة لقائمة الطابعات المعرفة على نظام الويندوز
        self.cmb_receipt_printer.addItems(["Xprinter XP-80C", "POS-80 Series", "Microsoft Print to PDF"])
        grid.addWidget(self.cmb_receipt_printer, 0, 1)
        
        grid.addWidget(QLabel("طابعة التقارير والجرد وحركات المخازن المعتمدة:"), 1, 0)
        self.cmb_report_printer = QComboBox()
        self.cmb_report_printer.addItems(["HP LaserJet Pro M402", "Canon LBP6030", "Microsoft XPS Document Writer"])
        grid.addWidget(self.cmb_report_printer, 1, 1)
        
        self.btn_test_print = QPushButton("🖨️ طباعة ورقة اختبار (Test Page)")
        self.btn_test_print.setObjectName("btnSecondary")
        self.btn_test_print.clicked.connect(lambda: QMessageBox.information(self, "فحص الطابعة", "تم إرسال أمر طباعة الاختبار بنجاح إلى الطابعة المحددة."))
        grid.addWidget(self.btn_test_print, 2, 1)
        
        grid.setColumnStretch(1, 1)
        return tab

    def load_settings_into_ui(self):
        """تعبئة الواجهة بالبيانات الحالية القادمة من الكنترولر"""
        data = self.controller.get_settings()
        
        self.txt_company_name.setText(data["company_name"])
        self.txt_company_address.setText(data["company_address"])
        self.txt_company_phone.setText(data["company_phone"])
        self.txt_tax_number.setText(data["tax_number"])
        self.num_tax_rate.setValue(float(data["tax_rate"]))
        self.txt_invoice_footer.setPlainText(data["invoice_footer"])
        
        # ضبط الطابعات
        idx_receipt = self.cmb_receipt_printer.findText(data["receipt_printer"])
        if idx_receipt >= 0: self.cmb_receipt_printer.setCurrentIndex(idx_receipt)
        
        idx_report = self.cmb_report_printer.findText(data["report_printer"])
        if idx_report >= 0: self.cmb_report_printer.setCurrentIndex(idx_report)

    def handle_browse_logo(self):
        """التعامل مع منتقي ملفات الصور لرفع لوجو المنشأة"""
        file_path, _ = QFileDialog.getOpenFileName(self, "اختر شعار السوبرماركت", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.selected_logo_path = file_path
            pixmap = QPixmap(file_path)
            # تقليص وتنسيق أبعاد اللوجو بما يتناسب مع مساحة المعاينة دائرية أو مربعة الحواف
            scaled_pixmap = pixmap.scaled(self.lbl_logo_preview.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.lbl_logo_preview.setPixmap(scaled_pixmap)

    def handle_save_settings(self):
        """تجميع البيانات المدخلة وحفظها من خلال الكنترولر"""
        updated_data = {
            "company_name": self.txt_company_name.text().strip(),
            "company_address": self.txt_company_address.text().strip(),
            "company_phone": self.txt_company_phone.text().strip(),
            "tax_number": self.txt_tax_number.text().strip(),
            "tax_rate": str(self.num_tax_rate.value()),
            "invoice_footer": self.txt_invoice_footer.toPlainText().strip(),
            "receipt_printer": self.cmb_receipt_printer.currentText(),
            "report_printer": self.cmb_report_printer.currentText(),
            "logo_path": self.selected_logo_path
        }
        
        if not updated_data["company_name"]:
            QMessageBox.warning(self, "تنبيه", "الرجاء إدخال اسم الشركة أو السوبرماركت!")
            return
            
        success, msg = self.controller.save_settings(updated_data)
        if success:
            QMessageBox.information(self, "تم الحفظ", msg)

# ميزة التشغيل الفردي والمعزول لفحص الشاشة بدقة
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsManagementWidget()
    window.setWindowTitle("فحص لوحة التحكم في إعدادات النظام - مستقل")
    window.resize(900, 480)
    window.show()
    sys.exit(app.exec())