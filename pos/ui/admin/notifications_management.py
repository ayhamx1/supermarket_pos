# -*- coding: utf-8 -*-
"""
🔔 Supermarket POS - Premium Fluent Notifications Management UI
📂 Path: ui/admin/notifications_management.py
"""
import sys
import os

# 🛡️ حارس المسارات لتشغيل الملف بشكل مستقل وتجنب ModuleNotFoundError
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from app.controllers.admin.notifications_controller import NotificationsController

class NotificationsManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.controller = NotificationsController()
        self.current_filter = "all"
        
        # تصميم فلوينت متناسق مع ويندوز 11
        self.setStyleSheet("""
            QWidget { background-color: #F3F3F3; font-family: 'Segoe UI', 'Arial'; color: #1B1B1B; }
            QLabel#mainTitle { font-size: 18px; font-weight: 600; color: #1B1B1B; }
            
            /* ستايل كروت العدادات العلوية */
            QFrame#counterCard { background-color: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 6px; padding: 12px; }
            QLabel#cardValue { font-size: 20px; font-weight: bold; color: #0067B8; }
            QLabel#cardLabel { font-size: 12px; color: #5D5D5D; font-weight: 500; }
            
            /* أزرار الفلترة */
            QPushButton#filterBtn { background-color: #FFFFFF; border: 1px solid #CCCCCC; border-radius: 4px; padding: 6px 14px; font-size: 13px; font-weight: 500; }
            QPushButton#filterBtn:hover { background-color: #F5F5F5; }
            QPushButton#filterBtn:checked { background-color: #0067B8; color: white; border-color: #0067B8; }
            
            /* الجداول */
            QTableWidget { background-color: #FFFFFF; border: 1px solid #E5E5E5; border-radius: 4px; gridline-color: #E5E5E5; }
            QHeaderView::section { background-color: #FAFAFA; font-weight: bold; border: none; border-bottom: 1px solid #E5E5E5; padding: 6px; font-size: 13px; }
        """)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # 👑 ترويسة الشاشة المركزية
        title_lbl = QLabel("🔔 مركز الإشعارات الذكية وحماية حركة التشغيل والمديونيات")
        title_lbl.setObjectName("mainTitle")
        main_layout.addWidget(title_lbl)

        # 📊 لوحة العدادات الرقمية العلوية (Cards)
        counters_layout = QHBoxLayout()
        counters_layout.setSpacing(12)

        self.card_all = self.create_counter_card("🎯 إجمالي التنبيهات غير المقروءة", "0")
        self.card_shortage = self.create_counter_card("📦 تنبيهات نواقص الأصناف", "0", "#C42B1C")
        self.card_expiry = self.create_counter_card("⏳ تنبيهات انتهاء الصلاحية", "0", "#E67E22")
        self.card_debt = self.create_counter_card("💰 تنبيهات الديون والمتأخرات", "0", "#27AE60")

        counters_layout.addWidget(self.card_all)
        counters_layout.addWidget(self.card_shortage)
        counters_layout.addWidget(self.card_expiry)
        counters_layout.addWidget(self.card_debt)
        main_layout.addLayout(counters_layout)

        # 🕹️ شريط أزرار الفلترة السريعة
        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(8)

        self.btn_all = QPushButton("الكل")
        self.btn_shortage = QPushButton("📦 نواقص المخزن")
        self.btn_expiry = QPushButton("⏳ تواريخ الصلاحية")
        self.btn_debt = QPushButton("💰 مديونيات وآجل")

        for btn, f_type in [(self.btn_all, "all"), (self.btn_shortage, "shortage"), (self.btn_expiry, "expiry"), (self.btn_debt, "debt")]:
            btn.setObjectName("filterBtn")
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            btn.clicked.connect(lambda checked, t=f_type: self.handle_filter_change(t))
            filter_bar.addWidget(btn)
            
        self.btn_all.setChecked(True)
        filter_bar.addStretch()
        main_layout.addLayout(filter_bar)

        # 📋 جدول عرض التنبيهات التفصيلي
        self.table_notif = QTableWidget()
        self.table_notif.setColumnCount(4)
        self.table_notif.setHorizontalHeaderLabels(["التوقيت", "نوع التنبيه", "تفاصيل الإشعار الفنية", "الإجراء"])
        
        # 🛡️ الاستدعاء الصحيح والآمن في PyQt6 للتحكم بالحجم لتجنب الـ AttributeError السابق
        self.table_notif.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table_notif.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch) # تمديد عمود التفاصيل
        
        main_layout.addWidget(self.table_notif)

        # شحن البيانات والعدادات فوراً عند تشغيل الواجهة
        self.update_badges()
        self.refresh_notifications_table()

    def create_counter_card(self, title, init_val, color="#0067B8"):
        """بناء كرت العداد العلوي بشكل فلوينت أنيق"""
        card = QFrame()
        card.setObjectName("counterCard")
        lay = QVBoxLayout(card)
        lay.setSpacing(4)
        
        lbl_val = QLabel(init_val)
        lbl_val.setObjectName("cardValue")
        lbl_val.setStyleSheet(f"color: {color};")
        
        lbl_title = QLabel(title)
        lbl_title.setObjectName("cardLabel")
        
        lay.addWidget(lbl_val)
        lay.addWidget(lbl_title)
        
        # حفظ الإشارة إلى ليبل القيمة لتحديثه لاحقاً ديناميكياً
        card.value_label = lbl_val
        return card

    def update_badges(self):
        """تحديث الأرقام الظاهرة في الكروت العلوية من الكنترولر"""
        cnt = self.controller.get_counters()
        self.card_all.value_label.setText(str(cnt["all"]))
        self.card_shortage.value_label.setText(str(cnt["shortage"]))
        self.card_expiry.value_label.setText(str(cnt["expiry"]))
        self.card_debt.value_label.setText(str(cnt["debt"]))

    def handle_filter_change(self, filter_type):
        """التعامل مع تغيير زر الفلترة الحالي"""
        self.current_filter = filter_type
        self.refresh_notifications_table()

    def refresh_notifications_table(self):
        """بناء رص صفوف جدول التنبيهات بناءً على الفلتر المختار"""
        data = self.controller.get_notifications(self.current_filter)
        self.table_notif.setRowCount(len(data))
        
        type_mapping = {"shortage": "📦 نقص مخزون", "expiry": "⏳ صلاحية قريبة", "debt": "💰 حدود الديون"}
        
        for row_idx, item in enumerate(data):
            # 1. التوقيت
            self.table_notif.setItem(row_idx, 0, QTableWidgetItem(item["date"]))
            
            # 2. نوع التنبيه
            self.table_notif.setItem(row_idx, 1, QTableWidgetItem(type_mapping.get(item["type"], "إشعار")))
            
            # 3. التفاصيل
            details_item = QTableWidgetItem(item["details"])
            # إذا كان التنبيه غير مقروء، نجعله بخط عريض (Bold) لتمييزه
            if item["status"] == "unread":
                font = details_item.font()
                font.setBold(True)
                details_item.setFont(font)
                details_item.setForeground(QColor("#000000"))
            else:
                details_item.setForeground(QColor("#7A7A7A"))
            self.table_notif.setItem(row_idx, 2, details_item)
            
            # 4. زر الإجراء (تعيين كمقروء / معالجة)
            if item["status"] == "unread":
                btn_action = QPushButton("✔ تم الاطلاع")
                btn_action.setObjectName("filterBtn")
                btn_action.setStyleSheet("padding: 2px 8px; font-size: 11px; background-color: #E9E9E9;")
                btn_action.clicked.connect(lambda checked, i=item["id"]: self.handle_mark_read(i))
                self.table_notif.setCellWidget(row_idx, 3, btn_action)
            else:
                lbl_done = QLabel("🔒 مقروء ومؤمن")
                lbl_done.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lbl_done.setStyleSheet("color: #7A7A7A; font-size: 12px;")
                self.table_notif.setCellWidget(row_idx, 3, lbl_done)

    def handle_mark_read(self, notif_id):
        """إجراء قراءة التنبيه وتحديث العدادات والجدول فوراً"""
        if self.controller.mark_as_read(notif_id):
            self.update_badges()
            self.refresh_notifications_table()

# ميزة التشغيل الفردي والمعزول لفحص الشاشة بدقة
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotificationsManagementWidget()
    window.setWindowTitle("فحص مركز التنبيهات والإشعارات الذكية - مستقل")
    window.resize(950, 500)
    window.show()
    sys.exit(app.exec())