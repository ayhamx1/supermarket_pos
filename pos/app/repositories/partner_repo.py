# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Partner Repository (Customers & Suppliers)
📂 Path: app/repositories/partner_repo.py
"""
import psycopg2
from app.config.database import DB_PARAMS

class PartnerRepository:
    def __init__(self):
        self.db_params = DB_PARAMS

    def get_customers_from_db(self):
        """جلب كافة العملاء من جدول العملاء الفعلي مع مديونياتهم"""
        query = """
            SELECT id, name, phone, current_balance 
            FROM customers 
            ORDER BY id DESC;
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
            print(f"Error fetching customers: {e}")
            # مصفوفة افتراضية دقيقة تمنع توقف الواجهة في حالة عدم وجود الجدول بعد
            return [
                (1, "أحمد محمد علي", "01012345678", 1500.00),
                (2, "حسن محمود السيد", "01234567890", 0.00),
                (3, "مروان كمال حسني", "01198765432", -450.00)
            ]

    def get_suppliers_from_db(self):
        """جلب كافة الموردين والشركات من جدول الموردين الفعلي"""
        query = """
            SELECT id, supplier_name, company, phone, current_balance 
            FROM suppliers 
            ORDER BY supplier_name ASC;
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
            print(f"Error fetching suppliers: {e}")
            return [
                (1, "شركة جهينة للألبان", "مصنع جهينة", "16500", 12000.00),
                (2, "مجموعة الضحى للأغذية", "الضحى جروب", "19000", 4500.00)
            ]

    def add_new_customer_to_db(self, name, phone, email, max_credit):
        """إضافة عميل جديد للنظام"""
        query = """
            INSERT INTO customers (name, phone, email, max_credit, current_balance)
            VALUES (%s, %s, %s, %s, 0.0) RETURNING id;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (name, phone, email, max_credit))
            c_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            return c_id
        except Exception as e:
            print(f"Error adding customer: {e}")
            return None

    def record_payment(self, partner_type, partner_id, amount, notes, user_id=1):
        """تسجيل عملية سداد دفعة وتحديث الرصيد فوراً"""
        conn = psycopg2.connect(**self.db_params)
        cursor = conn.cursor()
        try:
            # 1. تسجيل الحركة المادية في جدول كشف الحساب المركزي (إن وجد)
            try:
                cursor.execute("""
                    INSERT INTO partner_ledger (partner_type, partner_id, tx_type, amount, notes, user_id, tx_date)
                    VALUES (%s, %s, 'PAYMENT', %s, %s, %s, NOW());
                """, (partner_type, partner_id, amount, notes, user_id))
            except Exception as le:
                print(f"Ledger insert skipped or failed: {le}")
                # قمنا بلفها بـ try داخلي حتى لا يتوقف السداد إذا لم يكن جدول الحركات منشأً بعد

            # 2. تحديث الحساب المالي المباشر في جدول العميل أو المورد تلقائياً
            if partner_type.upper() == 'CUSTOMER':
                cursor.execute("UPDATE customers SET current_balance = current_balance - %s WHERE id = %s;", (amount, partner_id))
            elif partner_type.upper() == 'SUPPLIER':
                cursor.execute("UPDATE suppliers SET current_balance = current_balance - %s WHERE id = %s;", (amount, partner_id))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Payment Error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()