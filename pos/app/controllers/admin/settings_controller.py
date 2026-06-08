# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Settings Management Controller
📂 Path: app/controllers/admin/settings_controller.py
"""

class SettingsController:
    def __init__(self):
        # بيانات محاكاة افتراضية للإعدادات
        self.settings_data = {
            "company_name": "سوبرماركت الخير والبركة",
            "company_address": "القاهرة - مدينة نصر - شارع الطيران",
            "company_phone": "01012345678",
            "tax_number": "123-456-789",
            "tax_rate": "14.0",
            "logo_path": "",
            "invoice_footer": "شكراً لزيارتكم.. الفاتورة لا ترد ولا تستبدل بعد 14 يوم",
            "receipt_printer": "Xprinter XP-80C",
            "report_printer": "HP LaserJet Pro M402"
        }

    def get_settings(self):
        """جلب الإعدادات الحالية للنظام"""
        return self.settings_data

    def save_settings(self, updated_data):
        """حفظ التعديلات الجديدة"""
        self.settings_data.update(updated_data)
        # هنا يتم كتابة كود الحفظ الفعلي في قاعدة البيانات أو ملف التكوين
        return True, "تم حفظ جميع الإعدادات وتحديث النظام فوراً!"