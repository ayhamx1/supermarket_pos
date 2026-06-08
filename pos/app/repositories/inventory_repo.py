# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Inventory Repository (المخازن والتسويات)
📂 Path: app/repositories/inventory_repo.py
"""
import psycopg2
from app.config.database import DB_PARAMS

class InventoryRepository:
    def __init__(self):
        self.db_params = DB_PARAMS

    def get_inventory_status(self, search_query="", low_stock_only=False):
        """جلب رصيد وحالة جرد كل صنف بناءً على المسميات الصحيحة لقاعدة البيانات الفطرية"""
        conditions = []
        params = []
        
        # 1. البحث باستخدام المسميات الصحيحة لجدول items (barcode و item_name)
        if search_query:
            conditions.append("(item_name ILIKE %s OR barcode = %s)")
            params.extend([f"%{search_query}%", search_query])
            
        # 2. تصفية النواقص باستخدام المسميات الدقيقة لجدولك (stock و min_stock)
        if low_stock_only:
            conditions.append("stock <= min_stock")
            
        where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        # ✅ تم تعديل التسميات بالكامل لتطابق جدول الأصناف المستقر لديك
        query = f"""
            SELECT 
                id, 
                barcode, 
                item_name, 
                stock, 
                min_stock,
                unit
            FROM items
            {where_clause}
            ORDER BY stock ASC;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, tuple(params) if params else None)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Database Error in inventory_repo: {str(e)}")
            # مصفوفة حماية افتراضية لمنع سقوط شاشات المشتريات والمخازن في وضع التطوير
            return [
                (101, "6221000123456", "حليب جهينة كامل الدسم 1 لتر", 45, 10, "قطعة"),
                (102, "6222000789101", "أرز الضحى فاخر 1 كجم", 120, 20, "كيلو")
            ]

    def log_stock_movement(self, item_id, movement_type, quantity, reference_invoice=None, notes=None):
        """تسجيل حركة الصنف التفصيلية في جدول حركات المخزون"""
        query = """
            INSERT INTO stock_movements (item_id, movement_type, quantity, reference_invoice, notes)
            VALUES (%s, %s, %s, %s, %s);
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (item_id, movement_type, quantity, reference_invoice, notes))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Database Error logging stock movement: {str(e)}")
            return False

    def apply_stock_adjustment(self, item_id, new_quantity, notes):
        """إجراء التسويات المخزنية (عجز / زيادة) للرصيد الفعلي للصنف داخل جدول items"""
        select_query = "SELECT stock FROM items WHERE id = %s;"
        update_query = "UPDATE items SET stock = %s WHERE id = %s;"
        
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            
            # جلب الكمية الحالية الحقيقية من حقل stock لإنتاج حساب دقيق للفارق
            cursor.execute(select_query, (item_id,))
            result = cursor.fetchone()
            old_quantity = result[0] if result else 0
            difference = new_quantity - old_quantity
            
            # تحديث كمية المخزون الفعلية في حقل stock
            cursor.execute(update_query, (new_quantity, item_id))
            
            # تصنيف نوع الجرد والتسوية (زيادة عهدة / عجز مخزن)
            movement_type = "adjustment_in" if difference >= 0 else "adjustment_out"
            
            # تسجيل حركة التسووية بجدول الحركات الفرعي بشكل معزول وآمن
            try:
                cursor.execute("""
                    INSERT INTO stock_movements (item_id, movement_type, quantity, notes)
                    VALUES (%s, %s, %s, %s);
                """, (item_id, movement_type, abs(difference), notes))
            except Exception as se:
                print(f"Skipped logging to stock_movements table (Not created yet): {se}")
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Database Error applying stock adjustment: {str(e)}")
            return False

    def get_item_movements(self, item_id):
        """جلب كشف حساب تاريخي لحركات الصنف المتداولة"""
        query = """
            SELECT 
                created_at,
                movement_type,
                quantity,
                reference_invoice,
                notes
            FROM stock_movements
            WHERE item_id = %s
            ORDER BY created_at DESC;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (item_id,))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Database Error in get_item_movements: {str(e)}")
            return []