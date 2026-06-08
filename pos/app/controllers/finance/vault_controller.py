# -*- coding: utf-8 -*-
"""
Supermarket POS - Vault & Shifts Controller
Path: app/controllers/finance/vault_controller.py
"""
from app.repositories.vault_repo import VaultRepository

class VaultController:
    def __init__(self):
        self.repo = VaultRepository()

    def check_shift_status(self, user_id):
        return self.repo.get_active_shift(user_id)

    def start_new_shift(self, user_id, opening_balance):
        if opening_balance < 0:
            return False, "لا يمكن بدء الوردية بعهدة سالبة"
        shift_id = self.repo.open_shift(user_id, opening_balance)
        return shift_id is not None, shift_id

    def execute_cash_operation(self, shift_id, trans_type, amount, notes):
        if amount <= 0:
            return False, "يجب أن تكون القيمة المالية أكبر من صفر"
        if not notes:
            return False, "يرجى كتابة سبب أو بيان الحركة المالية"
        
        success = self.repo.add_transaction(shift_id, trans_type, amount, notes)
        return success, "تم تسجيل الحركة المالية بنجاح" if success else "فشلت العملية"

    def calculate_shift_report(self, shift_id, opening_balance):
        deposits, withdrawals = self.repo.get_shift_totals(shift_id)
        # الرصيد الدفتري المتوقع = العهدة الافتتاحية + الإيداعات - السحوبات
        expected_balance = opening_balance + deposits - withdrawals
        return expected_balance, deposits, withdrawals

    def finalize_shift(self, shift_id, closing_balance, actual_balance, notes):
        success = self.repo.close_shift(shift_id, closing_balance, actual_balance, notes)
        return success

    def load_vault_logs(self):
        return self.repo.get_vault_history()