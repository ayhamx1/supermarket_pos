# -*- coding: utf-8 -*-
"""
Supermarket POS - Expenses Controller
Path: app/controllers/finance/expense_controller.py
"""
from app.repositories.expense_repo import ExpenseRepository
from app.repositories.vault_repo import VaultRepository

class ExpenseController:
    def __init__(self):
        self.repo = ExpenseRepository()
        self.vault_repo = VaultRepository()

    def load_expenses_log(self, start_date=None, end_date=None, category=None):
        return self.repo.get_expenses(start_date, end_date, category)

    def process_new_expense(self, user_id, category, amount, notes):
        if amount <= 0:
            return False, "يجب أن تكون قيمة المصروف أكبر من صفر"
        if not notes:
            return False, "يرجى كتابة تفاصيل البيان المالي للمصروف"

        # التحقق من وجود وردية مفتوحة للموظف لسحب النقدية منها
        active_shift = self.vault_repo.get_active_shift(user_id)
        if not active_shift:
            return False, "لا يمكن تسجيل مصروفات؛ لا توجد وردية مالية مفتوحة حالياً لسحب النقدية"

        shift_id = active_shift[0]
        success_id = self.repo.register_expense(user_id, shift_id, category, amount, notes)
        return success_id is not None, "تم تسجيل المصروف وخصمه من الخزنة بنجاح" if success_id else "فشلت عملية التسجيل"

    def load_analytical_summary(self, start_date, end_date):
        return self.repo.get_expenses_summary_by_category(start_date, end_date)