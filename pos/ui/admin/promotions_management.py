# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Promotions Management UI
📂 Path: ui/admin/promotions_management.py
"""
import sys
import os

# =========================================================================
# 🛠️ حل مشكلة الـ ModuleNotFoundError تلقائياً عند التشغيل المنفرد للشاشة
# =========================================================================
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
                             QTableWidgetItem, QPushButton, QHeaderView, QFrame, 
                             QLineEdit, QComboBox, QDateTimeEdit, QMessageBox, QApplication)
from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtGui import QFont
from app.controllers.marketing.promo_controller import PromotionsController

PROMO_STYLE = """
    QWidget { background-color: #F8FAFC; font-family: 'Segoe UI', 'Arial'; color: #1E293B; }
    QFrame#card { background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 15px; }
    QLineEdit, QComboBox, QDateTimeEdit { border: 1px solid #CBD5E1; border-radius: 6px; padding: 8px; background: white; font-size: 14px; }
    QPushButton#saveBtn { background-color: #10B981; color: white; font-weight: bold; border-radius: 6px; padding: 10px; border: none; }
    QPushButton#saveBtn:hover { background-color: #059669; }
    QTableWidget { background-color: white; border: 1px solid #E2E8F0; border-radius: 8px; }
"""

class PromotionsManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = PromotionsController()
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(PROMO_STYLE)
        
        self.init_ui()
        self.load_promotions_to_table()

    def init_ui(self):
        main_layout = QVBoxLayout(self); main_layout.setContentsMargins(20, 20, 20, 20); main_layout.setSpacing(15)
        
        title = QLabel("🎁 مركز إدارة العروض والخصومات الذكية"); title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        main_layout.addWidget(title)
        
        # ليأوت أفقي يقسم الشاشة لنموذج الإدخال (يمين) وجدول العروض الحالي (يسار)
        body_layout = QHBoxLayout()
        
        # ----------------- 🛠️ نموذج إنشاء العرض -----------------
        form_card = QFrame(); form_card.setObjectName("card"); form_card.setFixedWidth(340)
        form_layout = QVBoxLayout(form_card); form_layout.setSpacing(10)
        
        form_layout.addWidget(QLabel("🎯 اسم الحملة الترويجية:"))
        self.txt_promo_name = QLineEdit(); self.txt_promo_name.setPlaceholderText("مثال: عروض عيد الأضحى")
        form_layout.addWidget(self.txt_promo_name)
        
        form_layout.addWidget(QLabel("🏷️ نوع العرض الترويجي:"))
        self.combo_type = QComboBox()
        self.combo_type.addItems(["خصم نسبة مئوية (%)", "خصم مبلغ ثابت (ج.م)", "اشترِ X واحصل على Y مجاناً", "عرض وقتي / ساعات سعيدة"])
        self.combo_type.currentIndexChanged.connect(self.handle_type_change)
        form_layout.addWidget(self.combo_type)
        
        form_layout.addWidget(QLabel("🔍 باركود الصنف المستهدف:"))
        self.txt_barcode = QLineEdit(); self.txt_barcode.setPlaceholderText("امسح أو اكتب باركود المنتج")
        form_layout.addWidget(self.txt_barcode)
        
        # حقول متغيرة ديناميكياً حسب نوع العرض
        self.lbl_value = QLabel("قيمة الخصم:"); form_layout.addWidget(self.lbl_value)
        self.txt_value = QLineEdit(); self.txt_value.setPlaceholderText("0.00")
        form_layout.addWidget(self.txt_value)
        
        # حقول عروض التجميع (Buy X Get Y) - مخفية تلقائياً وتظهر عند الحاجة
        self.lbl_buy_qty = QLabel("الكمية المطلوبة للشراء (X):"); self.lbl_buy_qty.hide(); form_layout.addWidget(self.lbl_buy_qty)
        self.txt_buy_qty = QLineEdit("0"); self.txt_buy_qty.hide(); form_layout.addWidget(self.txt_buy_qty)
        self.lbl_get_qty = QLabel("الكمية المجانية الممنوحة (Y):"); self.lbl_get_qty.hide(); form_layout.addWidget(self.lbl_get_qty)
        self.txt_get_qty = QLineEdit("0"); self.txt_get_qty.hide(); form_layout.addWidget(self.txt_get_qty)
        
        # التواريخ والأوقات
        form_layout.addWidget(QLabel("📅 تاريخ ووقت البدء:"))
        self.date_start = QDateTimeEdit(QDateTime.currentDateTime())
        self.date_start.setCalendarPopup(True); form_layout.addWidget(self.date_start)
        
        form_layout.addWidget(QLabel("📅 تاريخ ووقت الانتهاء:"))
        self.date_end = QDateTimeEdit(QDateTime.currentDateTime().addDays(7))
        self.date_end.setCalendarPopup(True); form_layout.addWidget(self.date_end)
        
        btn_save = QPushButton("✨ إطلاق وتفعيل العرض فوراً"); btn_save.setObjectName("saveBtn")
        btn_save.clicked.connect(self.save_promotion)
        form_layout.addWidget(btn_save); form_layout.addStretch()
        
        body_layout.addWidget(form_card)
        
        # ----------------- 📋 جدول العروض الحالية -----------------
        table_card = QFrame(); table_card.setObjectName("card")
        table_layout = QVBoxLayout(table_card)
        
        table_layout.addWidget(QLabel("📊 سجل حركات وعروض المتجر الحية:"))
        self.table_promos = QTableWidget(); self.table_promos.setColumnCount(7)
        self.table_promos.setHorizontalHeaderLabels(["العرض", "النوع", "المنتج", "تفاصيل الخصم", "تاريخ البدء", "تاريخ الانتهاء", "الحالة"])
        self.table_promos.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_layout.addWidget(self.table_promos)
        
        body_layout.addWidget(table_card, 2)
        main_layout.addLayout(body_layout)

    def handle_type_change(self, index):
        """إظهار وإخفاء الحقول بناءً على نوع العرض المختار"""
        if index == 2: # Buy X Get Y
            self.lbl_value.hide(); self.txt_value.hide()
            self.lbl_buy_qty.show(); self.txt_buy_qty.show()
            self.lbl_get_qty.show(); self.txt_get_qty.show()
        else:
            self.lbl_value.show(); self.txt_value.show()
            self.lbl_buy_qty.hide(); self.txt_buy_qty.hide()
            self.lbl_get_qty.hide(); self.txt_get_qty.hide()
            
        if index == 0: self.lbl_value.setText("نسبة الخصم (%):")
        elif index == 1: self.lbl_value.setText("مبلغ الخصم المستقطع (ج.م):")
        elif index == 3: self.lbl_value.setText("خصم الساعات السعيدة (%):")

    def load_promotions_to_table(self):
        try:
            self.table_promos.setRowCount(0)
            promos = self.controller.fetch_promotions()
            if not promos:
                return
            
            type_mapping = {
                "PERCENT": "خصم نسبة مئوية", "AMOUNT": "خصم مبلغ ثابت",
                "BUY_X_GET_Y": "اشترِ X واحصل على Y", "TIME_BOUND": "عرض وقتي محدد"
            }
            
            for r_idx, row in enumerate(promos):
                self.table_promos.insertRow(r_idx)
                self.table_promos.setItem(r_idx, 0, QTableWidgetItem(str(row[1]))) # الاسم
                self.table_promos.setItem(r_idx, 1, QTableWidgetItem(type_mapping.get(row[2], str(row[2])))) # النوع
                self.table_promos.setItem(r_idx, 2, QTableWidgetItem(f"{row[4]} ({row[3]})")) # المنتج والباركود
                
                # تفاصيل الخصم
                if row[2] == "BUY_X_GET_Y":
                    detail_text = f"اشترِ {row[6]} احصل على {row[7]} مجاناً"
                elif row[2] == "PERCENT" or row[2] == "TIME_BOUND":
                    detail_text = f"خصم {row[5]}%"
                else:
                    detail_text = f"خصم {row[5]} ج.م"
                    
                self.table_promos.setItem(r_idx, 3, QTableWidgetItem(detail_text))
                
                start_str = row[8].strftime('%Y-%m-%d %H:%M') if hasattr(row[8], 'strftime') else str(row[8])
                end_str = row[9].strftime('%Y-%m-%d %H:%M') if hasattr(row[9], 'strftime') else str(row[9])
                
                self.table_promos.setItem(r_idx, 4, QTableWidgetItem(start_str))
                self.table_promos.setItem(r_idx, 5, QTableWidgetItem(end_str))
                
                # زر التبديل السريع للحالة (نشط / معطل)
                status_btn = QPushButton("🟢 نشط (اضغط للتعطيل)" if row[10] else "🔴 معطل (اضغط للتفعيل)")
                status_btn.setStyleSheet("background: #E2E8F0; border: none; padding: 4px; border-radius: 4px;" if not row[10] else "background: #D1FAE5; color: #065F46; border: none; padding: 4px; border-radius: 4px;")
                status_btn.clicked.connect(lambda ch, p_id=row[0], curr_st=row[10]: self.toggle_status(p_id, curr_st))
                self.table_promos.setCellWidget(r_idx, 6, status_btn)
        except Exception as e:
            print(f"Error loading promotions table: {e}")

    def save_promotion(self):
        name = self.txt_promo_name.text().strip()
        barcode = self.txt_barcode.text().strip()
        type_idx = self.combo_type.currentIndex()
        
        types = ["PERCENT", "AMOUNT", "BUY_X_GET_Y", "TIME_BOUND"]
        p_type = types[type_idx]
        
        start_dt = self.date_start.dateTime().toPyDateTime()
        end_dt = self.date_end.dateTime().toPyDateTime()
        
        if not name or not barcode:
            QMessageBox.warning(self, "تنبيه", "يرجى ملء اسم العرض وباركود المنتج المستهدف!")
            return
            
        try:
            val = float(self.txt_value.text()) if type_idx != 2 else 0.0
            buy_q = int(self.txt_buy_qty.text()) if type_idx == 2 else 0
            get_q = int(self.txt_get_qty.text()) if type_idx == 2 else 0
            
            self.controller.create_promo(name, p_type, barcode, val, buy_q, get_q, start_dt, end_dt)
            QMessageBox.information(self, "نجاح", "تم إدراج الحملة الترويجية وتفعيلها بنجاح! 🎉")
            
            self.txt_promo_name.clear(); self.txt_barcode.clear(); self.txt_value.setText("0.00")
            self.load_promotions_to_table()
        except ValueError:
            QMessageBox.critical(self, "خطأ مدخلات", "يرجى إدخال قيم رقمية صحيحة في خانات الأرقام والكميات!")

    def toggle_status(self, promo_id, current_status):
        self.controller.change_status(promo_id, not current_status)
        self.load_promotions_to_table()

# =========================================================================
# 🚀 كود التشغيل المستقل (يضمن توجيه اللغة الصحيح عند تشغيل الملف بمفرده)
# =========================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)  # دعم الاتجاه العربي
    
    window = PromotionsManagementWidget()
    window.setWindowTitle("فحص معزول - شاشة إدارة العروض")
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec())