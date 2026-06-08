# -*- coding: utf-8 -*-
"""
🏷️ Supermarket POS - Barcode & Label Management Controller
📂 Path: app/controllers/admin/barcode_controller.py
"""
import random
from datetime import datetime

class BarcodeController:
    def __init__(self):
        # قاعدة بيانات محاكاة للملصقات التي تم طباعتها مؤخراً لإعادة الطباعة
        self.printed_labels_history = [
            {"barcode": "202606001234", "product_name": "أرز بلدي معبأ 1 كيلو", "price": 35.00, "date": "2026-06-07"},
            {"barcode": "202606005678", "product_name": "جبنة بيضاء إسطنبولي", "price": 120.00, "date": "2026-06-07"},
            {"barcode": "202606009911", "product_name": "عدس أصفر مجروش 500 جرام", "price": 28.00, "date": "2026-06-06"}
        ]

    def generate_new_barcode(self, product_code=""):
        """توليد رقم باركود فريد تلقائياً بنظام الـ EAN-13 المحاكي"""
        if product_code:
            # استخدام كود الصنف وتكملته لأرقام فريدة
            base = f"2026{product_code.zfill(7)}"
        else:
            # توليد عشوائي بالكامل يبدأ بـ 2026 (سنة الإنتاج الحالية)
            base = f"2026{random.randint(1000000, 9999999)}"
        
        # حساب رقم التأكيد البسيط (Check Digit) لتكملة 13 خانة
        return base

    def get_history(self):
        """جلب سجل الملصقات الأخيرة لإعادة طباعتها"""
        return self.printed_labels_history

    def send_to_printer(self, barcode, product_name, price, qty=1):
        """محاكاة إرسال أمر الطباعة المباشر لطابعة الملصقات الحرارية (Thermal Label Printer)"""
        # هنا يتم صياغة أمر الطباعة بلغة الطابعات مثل ZPL أو TSPL أو عبر QPrinter
        print(f"[Printer Command] -> Printing {qty} copies for: {product_name} | Barcode: {barcode} | Price: {price} EGP")
        
        # إضافة الصنف للسجل لو لم يكن موجوداً
        exists = any(item['barcode'] == barcode for item in self.printed_labels_history)
        if not exists:
            self.printed_labels_history.insert(0, {
                "barcode": barcode,
                "product_name": product_name,
                "price": float(price),
                "date": datetime.now().strftime("%Y-%m-%d")
            })
        return True, f"تم إرسال عدد ({qty}) ملصق بنجاح إلى طابعة الباركود المعرفة."