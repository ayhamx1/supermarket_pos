# -*- coding: utf-8 -*-
"""
📊 Supermarket POS - Central Dashboard Controller
📂 Path: app/controllers/admin/dashboard_controller.py
"""
import psycopg2

class DashboardController:
    def __init__(self, db_connection=None):
        # الاحتفاظ باتصال قاعدة البيانات المركزي للمستقبل
        self.conn = db_connection

    def get_financial_summary(self):
        """
        💰 جلب الحسابات المالية لليوم الحالي وشحن كروت الـ KPI
        """
        try:
            # هنا يمكنك كتابة استعلامات الـ SQL الفعلية مستقبلاً:
            # cursor = self.conn.cursor()
            # cursor.execute("SELECT SUM(total_price) FROM invoices WHERE DATE(created_at) = CURRENT_DATE;")
            
            return {
                "today_sales": "12,450.50 ج.م",
                "today_profit": "2,840.00 ج.م",
                "active_invoices": "142 فاتورة",
                "active_cashiers": "3 نقاط بيع"
            }
        except Exception as e:
            print(f"⚠️ خطأ جلب الملخص المالي: {e}")
            return {"today_sales": "0.00 ج.م", "today_profit": "0.00 ج.م", "active_invoices": "0", "active_cashiers": "0"}

    def get_top_products(self):
        """
        🔥 جلب أعلى 5 منتجات حركة ومبيعاً خلال اليوم لشاشة المؤشرات
        """
        try:
            # محاكاة ذكية للبيانات الأكثر حركة اليوم لتغذية الـ table_products
            return [
                ("علبة سمنة كريستال 1ك", "85 قطعة", "8,500 ج.م"),
                ("شيبسي عائلي متنوع", "210 قطعة", "2,100 ج.م"),
                ("مكرونة الملكة 400ج", "150 قطعة", "1,200 ج.م"),
                ("لبن جهينة كامل الدسم 1 لتر", "60 قطعة", "2,280 ج.م"),
                ("بيبسي كنز دايت", "95 قطعة", "950 ج.م"),
            ]
        except Exception as e:
            print(f"⚠️ خطأ جلب أعلى المنتجات مبيعاً: {e}")
            return []

    def get_low_stock_alerts(self):
        """
        🚨 جلب الأصناف الحرجة التي وصلت أو اقتربت من حد الطلب (تنبيهات النواقص)
        """
        try:
            # بيانات دقيقة تطابق الـ 5 أعمدة المطلوبة في الـ table_alerts بالواجهة
            # [الكود، اسم المنتج، المتاح بالرف، حد الأمان، الحالة]
            return [
                ("1004", "زيت حلوة خليط 1 لتر", "5 زجاجات", "20 زجاجة", "🚨 حرِج جداً"),
                ("2011", "أرز الضحى فاخر 1 كيلو", "12 كجم", "50 كجم", "⚠️ قارب على النفاد"),
                ("3044", "صابون دوف كلاسيك 135ج", "3 قطع", "15 قطعة", "🚨 حرِج جداً"),
                ("1099", "جبنة عبور لاند تتراباك 250ج", "8 علب", "40 علبة", "⚠️ قارب على النفاد"),
            ]
        except Exception as e:
            print(f"⚠️ خطأ جلب تنبيهات النواقص: {e}")
            return []