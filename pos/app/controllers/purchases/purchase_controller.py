# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Purchase Controller
📂 Path: app/controllers/purchases/purchase_controller.py
"""
from app.repositories.purchase_repo import PurchaseRepository
from app.models.purchase import PurchaseInvoice, Supplier

class PurchaseController:
    def __init__(self):
        self.repo = PurchaseRepository()

    def load_suppliers(self):
        """الدالة الأساسية الأصلية"""
        return self.repo.get_suppliers()

    def load_all_suppliers(self):
        """✅ الدالة الجديدة المضافة لحل الـ AttributeError في شاشة المشتريات"""
        return self.load_suppliers()

    def create_supplier(self, name, phone, company, address):
        supplier = Supplier(name, phone, company, address)
        return self.repo.add_supplier(supplier)

    def process_purchase_invoice(self, supplier_id, total, tax, discount, payment_type, notes, items_list):
        invoice = PurchaseInvoice(supplier_id, total, tax, discount, payment_type, notes)
        return self.repo.save_purchase_invoice(invoice, items_list)

    def process_purchase_return(self, barcode, qty, supplier_id, reason):
        return self.repo.save_purchase_return(barcode, qty, supplier_id, reason)