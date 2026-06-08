# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Backup Management UI
📂 Path: ui/admin/backup_management.py
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFileDialog, QMessageBox, QFrame, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from app.controllers.system.backup_controller import BackupController

BACKUP_UI_STYLE = """
    QWidget { background-color: #F8FAFC; font-family: 'Segoe UI', 'Arial'; color: #1E293B; }
    QFrame#mainCard { background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 25px; }
    QFrame#statusBanner { background-color: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 15px; }
    
    QPushButton#btnBackup { background-color: #2563EB; color: white; font-weight: bold; border: none; border-radius: 6px; padding: 12px 20px; font-size: 14px; }
    QPushButton#btnBackup:hover { background-color: #1D4ED8; }
    
    QPushButton#btnRestore { background-color: #DC2626; color: white; font-weight: bold; border: none; border-radius: 6px; padding: 12px 20px; font-size: 14px; }
    QPushButton#btnRestore:hover { background-color: #B91C1C; }
"""

class BackupManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = BackupController()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(BACKUP_UI_STYLE)
        
        self.init_ui()
        
        # ⚡ تشغيل ميزة النسخ الاحتياطي التلقائي فور تحميل الموديول دون تجميد الواجهة
        self.perform_auto_backup()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)
        
        # العنوان الرئيسي
        title_lbl = QLabel("🛡️ مركز إدارة النسخ الاحتياطي والأمان السحابي")
        title_lbl.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        main_layout.addWidget(title_lbl)
        
        # كرت الحاوية الكبيرة
        main_card = QFrame()
        main_card.setObjectName("mainCard")
        card_layout = QVBoxLayout(main_card)
        card_layout.setSpacing(15)
        
        # بانر حالة النظام
        banner = QFrame()
        banner.setObjectName("statusBanner")
        banner_layout = QVBoxLayout(banner)
        self.lbl_status = QLabel("🔄 جاري فحص حالة قاعدة البيانات وحفظ النسخة التلقائية المجدولة...")
        self.lbl_status.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.lbl_status.setStyleSheet("color: #1E40AF;")
        banner_layout.addWidget(self.lbl_status)
        card_layout.addWidget(banner)
        
        # نص توضيحي
        info_text = QLabel(
            "يقوم نظام السوبرماركت الذكي بحفظ نسخة دورية تلقائية من كافة حساباتك، مبيعاتك، "
            "ومخزونك داخل مجلد المشروع لحمايتك. يمكنك أيضاً إنشاء نسخة يدوية وحفظها على فلاشة "
            "أو هارد خارجي لزيادة الأمان، أو استعادة السستم في حال حدوث أي تلف أو تغيير للجهاز."
        )
        info_text.setWordWrap(True)
        info_text.setFont(QFont("Segoe UI", 11))
        info_text.setStyleSheet("color: #475569; line-height: 1.6;")
        card_layout.addWidget(info_text)
        card_layout.addSpacing(15)
        
        # أزرار التحكم والعمليات
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.btn_manual_backup = QPushButton("📦 إنشاء نسخة احتياطية يدوية الآن")
        self.btn_manual_backup.setObjectName("btnBackup")
        self.btn_manual_backup.clicked.connect(self.handle_manual_backup)
        
        self.btn_manual_restore = QPushButton("🔄 استعادة قاعدة بيانات سابقة")
        self.btn_manual_restore.setObjectName("btnRestore")
        self.btn_manual_restore.clicked.connect(self.handle_restore)
        
        buttons_layout.addWidget(self.btn_manual_backup)
        buttons_layout.addWidget(self.btn_manual_restore)
        card_layout.addLayout(buttons_layout)
        
        main_layout.addWidget(main_card)
        main_layout.addStretch()

    def perform_auto_backup(self):
        """تنفيذ النسخ التلقائي الهادئ عند فتح الشاشة"""
        success, path = self.controller.run_auto_backup()
        if success:
            filename = os.path.basename(path)
            self.lbl_status.setText(f"🟢 حالة الأمان: ممتاز. تم حفظ نسخة احتياطية تلقائية بنجاح باسم ({filename})")
            self.lbl_status.setStyleSheet("color: #065F46;")
            # تغيير لون خلفية البانر لتصبح خضراء مريحة
            self.lbl_status.parent().setStyleSheet("background-color: #D1FAE5; border: 1px solid #A7F3D0; border-radius: 8px; padding: 15px;")
        else:
            self.lbl_status.setText("🔴 تنبيه أمني: فشل محرك النسخ التلقائي! يرجى مراجعة صلاحيات النظام أو أدوات الـ Postgres.")
            self.lbl_status.setStyleSheet("color: #991B1B;")
            self.lbl_status.parent().setStyleSheet("background-color: #FEE2E2; border: 1px solid #FCA5A5; border-radius: 8px; padding: 15px;")

    def handle_manual_backup(self):
        """طلب مسار يدوي من المستخدم وحفظ الملف"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "حفظ النسخة الاحتياطية للسوبرماركت", 
            "supermarket_pos_backup.backup", "Backup Files (*.backup)"
        )
        if not file_path:
            return
            
        self.btn_manual_backup.setEnabled(False)
        self.btn_manual_backup.setText("⌛ جاري استخراج البيانات...")
        QApplication.processEvents() # تحديث الرسوم لكي لا تتجمد الشاشة
        
        success, msg = self.controller.create_manual_backup(file_path)
        
        self.btn_manual_backup.setEnabled(True)
        self.btn_manual_backup.setText("📦 إنشاء نسخة احتياطية يدوية الآن")
        
        if success:
            QMessageBox.information(self, "نجاح العملية 🎉", f"تم استخراج قاعدة البيانات وتأمينها بنجاح كامل في المسار المحدد:\n{file_path}")
        else:
            QMessageBox.critical(self, "خطأ في النظام", msg)

    def handle_restore(self):
        """عملية استعادة قاعدة البيانات الخطيرة مع تأكيد مزدوج"""
        confirm = QMessageBox.warning(
            self, "🚨 تحذير أمني شديد الخطورة", 
            "تنبيه حسّاس: استعادة نسخة احتياطية قديمة ستقوم بحذف وتبديل البيانات الحالية والمبيعات الحالية بالكامل!\n\nهل أنت متأكد تماماً من رغبتك في الاستمرار واستبدال النظام؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, "اختر ملف النسخة الاحتياطية للاستعادة", "", "Backup Files (*.backup)"
        )
        if not file_path:
            return
            
        self.btn_manual_restore.setEnabled(False)
        self.btn_manual_restore.setText("⌛ جاري إعادة تهيئة الجداول وحقن البيانات...")
        QApplication.processEvents()
        
        success, msg = self.controller.restore_database(file_path)
        
        self.btn_manual_restore.setEnabled(True)
        self.btn_manual_restore.setText("🔄 استعادة قاعدة بيانات سابقة")
        
        if success:
            QMessageBox.information(
                self, "تمت الاستعادة بنجاح 🚀", 
                "تم إعادة بناء وتغذية السستم من الملف الاحتياطي القديم بنجاح بنسبة 100%! يرجى إعادة تشغيل البرنامج لتنشيط الجداول."
            )
        else:
            QMessageBox.critical(self, "فشل عملية الاستعادة", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = BackupManagementWidget()
    w.show()
    sys.exit(app.exec())