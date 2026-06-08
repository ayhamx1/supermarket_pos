# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Categories Repository
📂 Path: app/repositories/category_repo.py
"""
import psycopg2
from app.config.database import DB_PARAMS

class CategoriesRepository:
    def __init__(self):
        self.db_params = DB_PARAMS

    def get_all_categories_with_counts(self):
        """جلب الأقسام وإحصاء عدد المنتجات التابعة لكل قسم"""
        query = """
            SELECT 
                ROW_NUMBER() OVER (ORDER BY category) as id,
                category,
                COUNT(id) as total_products
            FROM items
            GROUP BY category
            UNION
            -- لضمان ظهور الأقسام الافتراضية حتى لو كانت فارغة ولم يُضف إليها منتجات بعد
            SELECT 1, 'مشروبات', 0 WHERE NOT EXISTS (SELECT 1 FROM items WHERE category='مشروبات')
            UNION
            SELECT 2, 'ألبان وأجبان', 0 WHERE NOT EXISTS (SELECT 1 FROM items WHERE category='ألبان وأجبان')
            UNION
            SELECT 3, 'منظفات', 0 WHERE NOT EXISTS (SELECT 1 FROM items WHERE category='منظفات')
            UNION
            SELECT 4, 'مجمدات', 0 WHERE NOT EXISTS (SELECT 1 FROM items WHERE category='مجمدات')
            UNION
            SELECT 5, 'بقوليات ومواد جافة', 0 WHERE NOT EXISTS (SELECT 1 FROM items WHERE category='بقوليات ومواد جافة')
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
            print(f"Database Error in category_repo: {str(e)}")
            return [
                (1, "مشروبات", 0),
                (2, "ألبان وأجبان", 0),
                (3, "منظفات", 0),
                (4, "مجمدات", 0)
            ]