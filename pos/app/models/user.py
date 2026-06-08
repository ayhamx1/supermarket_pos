# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - User & Permissions Models
📂 Path: app/models/user.py
"""

class User:
    def __init__(self, username, full_name, role, password="", is_active=True, id=None):
        """
        تمثيل بيانات المستخدم والدور الوظيفي الخاص به
        الأدوار المدعومة: 'ADMIN' (مدير), 'CASHIER' (كاشير), 'ACCOUNTANT' (محاسب), 'STOCKKEEPER' (أمين مخزن)
        """
        self.id = id
        self.username = str(username).strip().lower()
        self.full_name = str(full_name).strip()
        self.role = str(role).strip().upper() 
        self.password = password
        self.is_active = is_active


class Permission:
    def __init__(self, role, screen_name, can_view=False, can_add=False, can_edit=False, can_delete=False):
        """
        تمثيل صلاحيات دور معين على مستوى الشاشات والأزرار داخلها
        """
        self.role = str(role).strip().upper()
        self.screen_name = str(screen_name).strip() # اسم الشاشة (مثل: products, inventory, purchases)
        self.can_view = bool(can_view)     # صلاحية فتح الشاشة رؤية
        self.can_add = bool(can_add)       # صلاحية الإضافة (زر حفظ/ترحيل)
        self.can_edit = bool(can_edit)     # صلاحية التعديل (زر تعديل/تسوية)
        self.can_delete = bool(can_delete) # صلاحية الحذف (زر حذف صنف)