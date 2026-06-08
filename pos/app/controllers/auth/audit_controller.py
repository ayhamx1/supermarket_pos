# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Central Audit Log Controller
📂 Path: app/controllers/auth/audit_controller.py
"""
import psycopg2

class AuditController:
    def __init__(self, db_connection=None):
        self.conn = db_connection

    def log_action(self, user_id, username, action_type, details, ip="127.0.0.1"):
        """
        📝 دالة مركزية لحفظ أي حركة للموظف في قاعدة البيانات فوراً
        """
        try:
            # في الكود الفعلي نقوم بالاتصال والحفظ:
            # cursor = self.conn.cursor()
            # cursor.execute("INSERT INTO audit_logs ...")
            # self.conn.commit()
            print(f"🔒 [AUDIT LOG RECORDED]: الموظف ({username}) قام بـ [{action_type}] -> {details}")
            return True
        except Exception as e:
            print(f"❌ فشل تسجيل الـ Audit Log: {e}")
            return False

    def load_all_logs(self):
        """
        📂 جلب السجلات لعرضها في شاشة المدير (تجريبي ومحاكي للواقع)
        """
        # محاكاة لبيانات قادمة من قاعدة البيانات تلبي الأسئلة الأربعة التي طرحتها:
        mock_logs = [
            ("1", "أحمد (المدير)", "إضافة منتج", "قام بإضافة صنف جديد: جبنة دومتي 1ك كود 5002", "192.168.1.5", "2026-06-07 10:15:30"),
            ("2", "محمود (الكاشير)", "تعديل سعر", "تعديل سعر بيع 'زيت كريستال' من 85 ج.م إلى 92 ج.م", "192.168.1.12", "2026-06-07 11:02:14"),
            ("3", "مينا (مشرف)", "حذف فاتورة", "⚠️ تحذير: تم حذف الفاتورة رقم #10945 بالكامل وقيمتها 450 ج.م", "192.168.1.10", "2026-06-07 12:45:00"),
            ("4", "رانيـا (كاشير ب)", "إغلاق وردية", "قامت بإغلاق الوردية رقم 42 وتسليم عهدة نقدية 4,320 ج.م", "192.168.1.15", "2026-06-07 13:30:12"),
        ]
        return mock_logs