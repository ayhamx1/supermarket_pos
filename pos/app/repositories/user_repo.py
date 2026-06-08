# -*- coding: utf-8 -*-
"""
Supermarket POS - Users & Permissions Repository
Path: app/repositories/user_repo.py
"""
import psycopg2
from app.config.database import DB_PARAMS

class UserRepository:
    def __init__(self):
        self.db_params = DB_PARAMS

    def get_all_users(self):
        """جلب قائمة الموظفين مع أدوارهم الوظيفية وحالة الحساب"""
        query = """
            SELECT u.id, u.username, u.full_name, u.role, u.is_active 
            FROM users u
            ORDER BY u.id ASC;
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
            print(f"Database Error in user_repo (get_all_users): {str(e)}")
            return []

    def save_user_permissions(self, role_name, permissions_dict):
        """تحديث مصفوفة صلاحيات الشاشات والأزرار لدور وظيفي معين"""
        query = """
            INSERT INTO role_permissions (role_name, screen_pos, button_discount, button_change_price, button_delete_item)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (role_name) 
            DO UPDATE SET 
                screen_pos = EXCLUDED.screen_pos,
                button_discount = EXCLUDED.button_discount,
                button_change_price = EXCLUDED.button_change_price,
                button_delete_item = EXCLUDED.button_delete_item;
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (
                role_name,
                permissions_dict.get('screen_pos', False),
                permissions_dict.get('button_discount', False),
                permissions_dict.get('button_change_price', False),
                permissions_dict.get('button_delete_item', False)
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Database Error saving permissions: {str(e)}")
            return False

    def get_role_permissions(self, role_name):
        """جلب صلاحيات دور معين للتحقق منها أثناء تصفح الموظف"""
        query = "SELECT screen_pos, button_discount, button_change_price, button_delete_item FROM role_permissions WHERE role_name = %s;"
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (role_name,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            return row if row else (True, True, True, True)  # الافتراضي مفتوح في حال عدم التقييد
        except Exception as e:
            print(f"Database Error fetching permissions: {str(e)}")
            return (True, True, True, True)

    def log_action(self, user_id, action_type, description):
        """تسجيل حركة في سجل العمليات والأمان (Audit Log)"""
        query = """
            INSERT INTO audit_logs (user_id, action_type, description)
            VALUES (%s, %s, %s);
        """
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            cursor.execute(query, (user_id, action_type, description))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Database Error in log_action: {str(e)}")
            return False

    def get_audit_logs(self):
        """جلب سجل العمليات لتعقبه من قبل الإدارة"""
        query = """
            SELECT a.created_at, u.full_name, u.role, a.action_type, a.description 
            FROM audit_logs a
            JOIN users u ON a.user_id = u.id
            ORDER BY a.created_at DESC LIMIT 100;
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
            print(f"Database Error fetching audit logs: {str(e)}")
            return []