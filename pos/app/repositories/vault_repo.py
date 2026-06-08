# -*- coding: utf-8 -*-
"""
Supermarket POS - Vault & Shifts Repository
Path: app/repositories/vault_repo.py
"""
import psycopg2
from app.config.database import DB_PARAMS

class VaultRepository:
    def __init__(self):
        self.db_params = DB_PARAMS

    def get_active_shift(self, user_id):
        """التحقق مما إذا كانت هناك وردية مفتوحة للمستخدم الحالي"""
        query = """
            SELECT id, opening_balance, created_at 
            FROM shifts 
            WHERE user_id = %s AND status = 'open' 
            LIMIT 1;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            return row
        except Exception as e:
            print(f"Database Error in get_active_shift: {str(e)}")
            return None

    def open_shift(self, user_id, opening_balance):
        """فتح وردية جديدة وتسجيل عهدة البداية"""
        query = """
            INSERT INTO shifts (user_id, opening_balance, status) 
            VALUES (%s, %s, 'open') RETURNING id;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (user_id, opening_balance))
            shift_id = cursor.fetchone()[0]
            
            # تسجيل حركة إيداع عهدة افتتاحية في الخزنة
            cursor.execute("""
                INSERT INTO vault_transactions (shift_id, transaction_type, amount, notes)
                VALUES (%s, 'deposit', %s, 'رصيد افتتاح عهدة الوردية');
            """, (shift_id, opening_balance))
            
            conn.commit()
            cursor.close()
            conn.close()
            return shift_id
        except Exception as e:
            print(f"Database Error in open_shift: {str(e)}")
            return None

    def get_shift_totals(self, shift_id):
        """حساب إجمالي الحركات المالية خلال الوردية الحالية لصياغة التقرير"""
        query = """
            SELECT 
                COALESCE(SUM(CASE WHEN transaction_type = 'deposit' THEN amount ELSE 0 END), 0) as total_deposits,
                COALESCE(SUM(CASE WHEN transaction_type = 'withdrawal' THEN amount ELSE 0 END), 0) as total_withdrawals
            FROM vault_transactions 
            WHERE shift_id = %s;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (shift_id,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            return row
        except Exception as e:
            print(f"Database Error in get_shift_totals: {str(e)}")
            return (0, 0)

    def close_shift(self, shift_id, closing_balance, actual_balance, notes):
        """إغلاق الوردية الحالية وتسجيل الفروقات الجردية إن وجدت"""
        query = """
            UPDATE shifts 
            SET closing_balance = %s, actual_balance = %s, status = 'closed', closed_at = NOW(), notes = %s
            WHERE id = %s;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (closing_balance, actual_balance, notes, shift_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Database Error in close_shift: {str(e)}")
            return False

    def add_transaction(self, shift_id, trans_type, amount, notes):
        """تسجيل عملية سحب أو إيداع نقدية في الخزنة"""
        query = """
            INSERT INTO vault_transactions (shift_id, transaction_type, amount, notes)
            VALUES (%s, %s, %s, %s);
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (shift_id, trans_type, amount, notes))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Database Error in add_transaction: {str(e)}")
            return False

    def get_vault_history(self):
        """جلب آخر الحركات المسجلة في الخزنة لجرد الخزنة العام"""
        query = """
            SELECT t.created_at, t.transaction_type, t.amount, t.notes, s.user_id
            FROM vault_transactions t
            JOIN shifts s ON t.shift_id = s.id
            ORDER BY t.created_at DESC LIMIT 50;
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
            print(f"Database Error in get_vault_history: {str(e)}")
            return []