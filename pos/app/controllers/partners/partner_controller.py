# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Partner Controller (Customers & Suppliers)
📂 Path: app/controllers/partners/partner_controller.py
"""
from app.repositories.partner_repo import PartnerRepository

class PartnerController:
    def __init__(self):
        self.repo = PartnerRepository()

    def load_all_customers(self):
        """جلب حسابات العملاء من قاعدة البيانات عبر الريبو"""
        return self.repo.get_customers_from_db()

    def load_all_suppliers(self):
        """جلب حسابات الموردين من قاعدة البيانات عبر الريبو"""
        return self.repo.get_suppliers_from_db()