# -*- coding: utf-8 -*-
"""
Supermarket POS - Expenses Repository
Path: app/repositories/expense_repo.py
"""
import psycopg2
from app.config.database import DB_PARAMS

class ExpenseRepository:
    def __init__(self):
        self.db_params = DB_PARAMS

    def get_expenses(self, start_date=None, end_date=None, category=None):
        """جلب المصروفات مع الفلترة حسب التاريخ أو بند المصروف"""
        conditions = []
        params = []

        if start_date and end_date:
            conditions.append("e.created_at BETWEEN %s AND %s")
            params.extend([start_date, end_date])
        if category and category != "كل البنود":
            conditions.append("e.category = %s")
            params.append(category)

        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

        query = f"""
            SELECT e.id, e.created_at, e.category, e.amount, e.notes, u.full_name
            FROM expenses e
            JOIN users u ON e.user_id = u.id
            {where_clause}
            ORDER BY e.created_at DESC;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Database Error in expense_repo (get_expenses): {str(e)}")
            return []

    def register_expense(self, user_id, shift_id, category, amount, notes):
        """تسجيل مصروف جديد وسحبه تلقائياً من الخزنة وحركة الوردية الحالية"""
        insert_expense_query = """
            INSERT INTO expenses (user_id, shift_id, category, amount, notes)
            VALUES (%s, %s, %s, %s, %s) RETURNING id;
        """
        insert_vault_query = """
            INSERT INTO vault_transactions (shift_id, transaction_type, amount, notes)
            VALUES (%s, 'withdrawal', %s, %s);
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            
            # 1. تسجيل المصروف في جدول المصروفات
            cursor.execute(insert_expense_query, (user_id, shift_id, category, amount, notes))
            expense_id = cursor.fetchone()[0]
            
            # 2. إدراج حركة سحب نقدية تلقائية من الخزنة لضمان مطابقة الجرد الفعلي للدرج
            vault_notes = f"سحب تمويل لمصروف تشغيلي ({category}) - {notes}"
            cursor.execute(insert_vault_query, (shift_id, amount, vault_notes))
            
            conn.commit()
            cursor.close()
            conn.close()
            return expense_id
        except Exception as e:
            print(f"Database Error in register_expense: {str(e)}")
            return None

    def get_expenses_summary_by_category(self, start_date, end_date):
        """حساب إجمالي المصروفات مجمعة حسب البند لصياغة التقارير التحليلية"""
        query = """
            SELECT category, SUM(amount) as total_amount
            FROM expenses
            WHERE created_at BETWEEN %s AND %s
            GROUP BY category
            ORDER BY total_amount DESC;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (start_date, end_date))
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Database Error in expenses summary: {str(e)}")
            return []