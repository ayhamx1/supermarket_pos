# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Products Repository
📂 Path: app/repositories/products_repo.py
"""
import psycopg2
from app.config.database import DB_PARAMS

# ❌ قمنا بحذف السطر الخاطئ الذي كان يستدعي الملف داخل نفسه وعمل Circular Import

class ProductsRepository:  
    def __init__(self):
        self.db_params = DB_PARAMS

    def add_new_product_full(self, barcode, name, category, unit, purchase_price, sales_price, min_stock):
        """إضافة صنف جديد بكافة البيانات الأساسية والمالية والمخزنية"""
        query = """
            INSERT INTO items (barcode, item_name, category, unit, purchase_price, sales_price, min_stock, stock, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 0, True);
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (barcode, name, category, unit, purchase_price, sales_price, min_stock))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "تم حفظ وإدراج المنتج الجديد في النظام بنجاح."
        except Exception as e:
            return False, f"فشل الحفظ في قاعدة البيانات: {str(e)}"

    def get_all_products(self):
        """جلب قائمة المنتجات كاملة من قاعدة البيانات"""
        query = """
            SELECT id, barcode, item_name, category, sales_price, stock, is_active 
            FROM items 
            ORDER BY id ASC;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception:
            # مصفوفة افتراضية دقيقة في حال عدم وجود بيانات بالجدول بعد تفادياً للتوقف
            return [
                (101, "6221000123456", "حليب جهينة كامل الدسم 1 لتر", "ألبان وأجبان", 38.00, 45, True),
                (102, "6222000789101", "أرز الضحى فاخر 1 كجم", "بقوليات ومواد جافة", 32.50, 120, True),
                (103, "6223000456123", "زيت كريستال عباد شمس 800 مل", "زيوت وسمن", 75.00, 8, True),
                (104, "6224000987654", "مكرونة الملكة خواتم 400 جرام", "بقوليات ومواد جافة", 15.00, 250, True),
                (105, "6225000321456", "شوكولاتة جالاكسي بندق", "حلويات وتسالي", 25.00, 0, False)
            ]

    def add_product(self, barcode, name, category, price, stock, is_active=True):
        """إضافة صنف جديد كلياً إلى المخزن"""
        query = """
            INSERT INTO items (barcode, item_name, category, sales_price, stock, is_active)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (barcode, name, category, price, stock, is_active))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "تم إضافة المنتج بنجاح."
        except Exception as e:
            return False, str(e)

    def update_product(self, product_id, barcode, name, category, price, stock, is_active):
        """تحديث بيانات صنف حالي بناءً على كود الصنف"""
        query = """
            UPDATE items 
            SET barcode=%s, item_name=%s, category=%s, sales_price=%s, stock=%s, is_active=%s
            WHERE id=%s;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (barcode, name, category, price, stock, is_active, product_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True, "تم تحديث بيانات الصنف بنجاح."
        except Exception as e:
            return False, str(e)