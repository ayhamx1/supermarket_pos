# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Promotions Repository
📂 Path: app/repositories/promo_repo.py
"""
import psycopg2
from app.config.database import DB_PARAMS

class PromotionsRepository:
    def __init__(self):
        self.db_params = DB_PARAMS

    def add_promotion(self, name, p_type, barcode, disc_val, buy_q, get_q, start, end):
        """إضافة عرض ترويجي جديد للنظام"""
        query = """
            INSERT INTO promotions (promo_name, promo_type, barcode, discount_value, buy_qty, get_qty, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """
        conn = psycopg2.connect(**self.db_params); cursor = conn.cursor()
        cursor.execute(query, (name, p_type, barcode, disc_val, buy_q, get_q, start, end))
        promo_id = cursor.fetchone()[0]
        conn.commit(); cursor.close(); conn.close()
        return promo_id

    def get_all_promotions(self):
        """جلب كافة العروض الحالية مع أسماء الأصناف المرتبطة بها"""
        query = """
            SELECT p.id, p.promo_name, p.promo_type, p.barcode, i.item_name, 
                   p.discount_value, p.buy_qty, p.get_qty, p.start_date, p.end_date, p.is_active
            FROM promotions p
            LEFT JOIN items i ON p.barcode = i.barcode
            ORDER BY p.id DESC;
        """
        conn = psycopg2.connect(**self.db_params); cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall(); cursor.close(); conn.close()
        return rows

    def toggle_promo_status(self, promo_id, status):
        """تفعيل أو إيقاف العرض يدوياً من لوحة التحكم"""
        query = "UPDATE promotions SET is_active = %s WHERE id = %s;"
        conn = psycopg2.connect(**self.db_params); cursor = conn.cursor()
        cursor.execute(query, (status, promo_id))
        conn.commit(); cursor.close(); conn.close()