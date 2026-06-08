# -*- coding: utf-8 -*-
"""
🏪 Supermarket POS - Shift & Cashier Management Controller
📂 Path: app/controllers/admin/shift_controller.py
"""
from datetime import datetime

class ShiftController:
    def __init__(self, db_connection=None):
        self.conn = db_connection
        # محاكاة لبيانات الوردية الحالية (لو كانت مفتوحة)
        self.current_shift = {
            "shift_id": "SH-2026-0089",
            "cashier_name": "أحمد محمود (كاشير 1)",
            "open_time": "2026-06-07 08:00 AM",
            "opening_balance": 500.00,  # مبلغ العهدة المستلمة
            "system_sales": 3450.50,     # المبيعات المحسوبة إلكترونياً
        }

    def get_active_shift_details(self):
        """جلب تفاصيل الوردية النشطة حالياً"""
        return self.current_shift

    def open_new_shift(self, cashier_name, opening_balance):
        """فتح وردية جديدة وتسجيل عهدة البداية"""
        # هنا يتم كتابة استعلام الـ SQL لإدخال سجل جديد في جدول shifts
        self.current_shift = {
            "shift_id": f"SH-2026-{datetime.now().strftime('%M%S')}",
            "cashier_name": cashier_name,
            "open_time": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "opening_balance": float(opening_balance),
            "system_sales": 0.00
        }
        return True, f"تم فتح الوردية بنجاح برقم {self.current_shift['shift_id']}"

    def close_current_shift(self, actual_cash):
        """إغلاق الوردية وجرد الخزنة وحساب العجز أو الزيادة"""
        if not self.current_shift:
            return False, "لا توجد وردية مفتوحة حالياً لإغلاقها!"
        
        opening = self.current_shift["opening_balance"]
        sales = self.current_shift["system_sales"]
        
        # المبلغ المفترض وجوده في الدرج = العهدة الافتتاحية + المبيعات الإلكترونية
        expected_total = opening + sales
        actual_cash = float(actual_cash)
        
        difference = actual_cash - expected_total
        
        # تجهيز تقرير الإغلاق والتسليم
        report = {
            "shift_id": self.current_shift["shift_id"],
            "expected_total": expected_total,
            "actual_cash": actual_cash,
            "difference": difference,
            "status": "متطابق" if difference == 0 else ("🚨 عجز" if difference < 0 else "📈 زيادة")
        }
        
        # تفريغ الوردية الحالية في السيستم بعد الحفظ في قاعدة البيانات
        self.current_shift = None
        return True, report