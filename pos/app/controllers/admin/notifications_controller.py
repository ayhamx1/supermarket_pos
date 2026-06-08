# -*- coding: utf-8 -*-
"""
🔔 Supermarket POS - Smart Notifications Controller
📂 Path: app/controllers/admin/notifications_controller.py
"""
from datetime import datetime

class NotificationsController:
    def __init__(self):
        # محاكاة لبيانات التنبيهات القادمة من قاعدة البيانات
        self.notifications_db = [
            # 1. تنبيهات النواقص (Stock Shortages)
            {"id": 1, "type": "shortage", "title": "نقص حاد في المخزون", "details": "زيت عباد الشمس 1 لتر - المتبقي 3 قطع (الحد الأدنى الآمن: 15)", "date": "اليوم 10:15 ص", "status": "unread"},
            {"id": 2, "type": "shortage", "title": "صنف شارف على النفاد", "details": "حليب جهينة كامل الدسم 1 لتر - المتبقي 5 قطع (الحد الأدنى الآمن: 20)", "date": "أمس", "status": "read"},
            
            # 2. تنبيهات انتهاء الصلاحية (Expiry Dates)
            {"id": 3, "type": "expiry", "title": "منتجات توشك على انتهاء الصلاحية", "details": "زبادي طبيعي 105 جرام (دفعة رقم #441) - تنتهي خلال 3 أيام (10-06-2026)", "date": "اليوم 08:30 ص", "status": "unread"},
            {"id": 4, "type": "expiry", "title": "صلاحية قريبة جداً", "details": "جبنة شيدر مستوردة - تنتهي خلال 7 أيام (14-06-2026)", "date": "أمس", "status": "unread"},
            
            # 3. تنبيهات الديون والمتأخرات (Debts & Credits)
            {"id": 5, "type": "debt", "title": "تجاوز الحد الائتماني لعميل", "details": "العميل: شركة الأمل للتوريدات - المديونية الحالية: 8,500 ج.م (الحد الأقصى: 5,000 ج.م)", "date": "اليوم 11:00 ص", "status": "unread"},
            {"id": 6, "type": "debt", "title": "فاتورة آجل متأخرة التحصيل", "details": "العميل: الأستاذ محمد كريم - متبقي عليه مبلغ 1,200 ج.م منذ 45 يوماً", "date": "قبل يومين", "status": "read"}
        ]

    def get_notifications(self, filter_type="all"):
        """جلب الإشعارات مفلترة حسب النوع"""
        if filter_type == "all":
            return self.notifications_db
        return [n for n in self.notifications_db if n["type"] == filter_type]

    def mark_as_read(self, notif_id):
        """تحديث حالة الإشعار ليصبح مقروءاً"""
        for n in self.notifications_db:
            if n["id"] == notif_id:
                n["status"] = "read"
                return True
        return False

    def get_counters(self):
        """جلب عدادات الإشعارات غير المقروءة لكل قسم"""
        return {
            "all": len([n for n in self.notifications_db if n["status"] == "unread"]),
            "shortage": len([n for n in self.notifications_db if n["type"] == "shortage" and n["status"] == "unread"]),
            "expiry": len([n for n in self.notifications_db if n["type"] == "expiry" and n["status"] == "unread"]),
            "debt": len([n for n in self.notifications_db if n["type"] == "debt" and n["status"] == "unread"]),
        }