# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Treasury Controller
📂 Path: app/controllers/vault/vault_controller.py
"""
from app.repositories.vault_repo import VaultRepository

class VaultController:
    def __init__(self):
        self.repo = VaultRepository()

    def fetch_balance(self):
        return self.repo.get_vault_balance()

    def process_deposit(self, amount, notes, user_id):
        return self.repo.add_transaction('DEPOSIT', amount, notes, user_id)

    def process_withdrawal(self, amount, notes, user_id, is_expense=False):
        tx_type = 'EXPENSE' if is_expense else 'WITHDRAWAL'
        return self.repo.add_transaction(tx_type, amount, notes, user_id)

    def fetch_shifts_to_close(self):
        return self.repo.get_active_shifts_summary()