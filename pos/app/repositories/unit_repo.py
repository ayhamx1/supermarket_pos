# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Units Repository
📂 Path: app/repositories/unit_repo.py
"""
import psycopg2
from app.config.database import DB_PARAMS

class UnitsRepository:
    def __init__(self):
        self.db_params = DB_PARAMS

    def get_all_units_with_counts(self):
        """جلب الوحدات وإحصاء عدد المنتجات التابعة لكل وحدة قياس"""
        query = """
            SELECT 
                ROW_NUMBER() OVER (ORDER BY unit) as id,
                unit,
                COUNT(id) as total_products
            FROM items
            GROUP BY unit
            UNION
            -- ضمان ظهور الوحدات الأساسية حتى لو كانت فارغة ولم تربط بمنتجات بعد
            SELECT 1, 'قطعة (Item)', 0 WHERE NOT EXISTS (SELECT 1 FROM items WHERE unit='قطعة (Item)')
            UNION
            SELECT 2, 'كرتونة (Carton)', 0 WHERE NOT EXISTS (SELECT 1 FROM items WHERE unit='كرتونة (Carton)')
            UNION
            SELECT 3, 'كيلو جرام (Kg)', 0 WHERE NOT EXISTS (SELECT 1 FROM items WHERE unit='كيلو جرام (Kg)')
            UNION
            SELECT 4, 'لتر (Ltr)', 0 WHERE NOT EXISTS (SELECT 1 FROM items WHERE unit='لتر (Ltr)')
            ORDER BY total_products DESC;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Database Error in unit_repo: {str(e)}")
            return [
                (1, "قطعة (Item)", 0),
                (2, "كرتونة (Carton)", 0),
                (3, "كيلو جرام (Kg)", 0),
                (4, "لتر (Ltr)", 0)
            ]