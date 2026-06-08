# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Purchase Repository
📂 Path: app/repositories/purchase_repo.py
"""
import psycopg2
from app.config.database import DB_PARAMS

class PurchaseRepository:
    def __init__(self):
        self.db_params = DB_PARAMS

    def get_suppliers(self):
        """جلب قائمة الموردين"""
        conn = psycopg2.connect(**self.db_params); cursor = conn.cursor()
        cursor.execute("SELECT id, supplier_name, company FROM suppliers ORDER BY supplier_name ASC;")
        rows = cursor.fetchall(); cursor.close(); conn.close()
        return rows

    def add_supplier(self, supplier):
        """إضافة مورد جديد"""
        query = """
            INSERT INTO suppliers (supplier_name, phone, company, address)
            VALUES (%s, %s, %s, %s) RETURNING id;
        """
        conn = psycopg2.connect(**self.db_params); cursor = conn.cursor()
        cursor.execute(query, (supplier.supplier_name, supplier.phone, supplier.company, supplier.address))
        supplier_id = cursor.fetchone()[0]
        conn.commit(); cursor.close(); conn.close()
        return supplier_id

    def save_purchase_invoice(self, invoice, items, user_id=1):
        """حفظ فاتورة شراء وتحديث المخزون تلقائياً بـ Transaction واحدة"""
        conn = psycopg2.connect(**self.db_params); cursor = conn.cursor()
        try:
            # 1. إدخال الفاتورة الرئيسية
            cursor.execute("""
                INSERT INTO purchase_invoices (supplier_id, total_amount, tax, discount, payment_type, notes, user_id, invoice_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW()) RETURNING id;
            """, (invoice.supplier_id, invoice.total_amount, invoice.tax, invoice.discount, invoice.payment_type, invoice.notes, user_id))
            invoice_id = cursor.fetchone()[0]

            # 2. إدخال تفاصيل الفاتورة وتحديث المخزن لكل صنف
            for item in items:
                # item: (barcode, qty, cost_price)
                barcode, qty, cost = item[0], int(item[1]), float(item[2])
                
                # أ: إدخال في جدول تفاصيل المشتريات
                cursor.execute("""
                    INSERT INTO purchase_invoice_details (invoice_id, barcode, qty, cost_price)
                    VALUES (%s, %s, %s, %s);
                """, (invoice_id, barcode, qty, cost))

                # ب: تحديث المخزون تلقائياً (زيادة الكمية وتحديث سعر الشراء/التكلفة الجديد)
                cursor.execute("""
                    UPDATE items 
                    SET stock_qty = stock_qty + %s, cost_price = %s 
                    WHERE barcode = %s;
                """, (qty, cost, barcode))

                # ج: تسجيل الحركة في سجل حركة المخزن لتبويب الـ Inventory
                cursor.execute("""
                    INSERT INTO inventory_movements (barcode, tx_type, qty, from_warehouse, user_id, notes, tx_date)
                    VALUES (%s, 'IN', %s, 'المخزن الرئيسي', %s, %s, NOW());
                """, (barcode, qty, user_id, f"فاتورة شراء رقم #{invoice_id}"))

            conn.commit()
            return invoice_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close(); conn.close()

    def save_purchase_return(self, barcode, qty, supplier_id, reason, user_id=1):
        """مرتجع شراء: خصم من المخزن وتسجيل المرتجع"""
        conn = psycopg2.connect(**self.db_params); cursor = conn.cursor()
        try:
            # 1. التأكد من توفر الكمية المراد إرجاعها بالمخزن
            cursor.execute("SELECT stock_qty FROM items WHERE barcode = %s;", (barcode,))
            current_stock = cursor.fetchone()[0]
            if current_stock < qty:
                return False, "الكمية المراد إرجاعها أكبر من الرصيد الحالي بالمخزن!"

            # 2. خصم الكمية المرتجعة من المخزن تلقائياً
            cursor.execute("UPDATE items SET stock_qty = stock_qty - %s WHERE barcode = %s;", (qty, barcode))

            # 3. تسجيل المرتجع في جدول المرتجعات
            cursor.execute("""
                INSERT INTO purchase_returns (barcode, supplier_id, qty, reason, user_id, return_date)
                VALUES (%s, %s, %s, %s, %s, NOW());
            """, (barcode, supplier_id, qty, reason, user_id))

            # 4. تسجيل المرتجع كحركة مخزنية صادر (OUT/DAMAGE) للتتبع
            cursor.execute("""
                INSERT INTO inventory_movements (barcode, tx_type, qty, from_warehouse, user_id, notes, tx_date)
                VALUES (%s, 'OUT', %s, 'المخزن الرئيسي', %s, %s, NOW());
            """, (barcode, qty, user_id, f"مرتجع شراء للمورد: {reason}"))

            conn.commit()
            return True, "تم حفظ مرتجع الشراء وتحديث المخزون بنجاح"
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close(); conn.close()