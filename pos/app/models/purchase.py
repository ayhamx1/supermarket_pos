# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Purchase & Supplier Models
📂 Path: app/models/purchase.py
"""

class Supplier:
    def __init__(self, supplier_name, phone="", company="", address="", id=None):
        """
        تمثيل بيانات المورد (Suppliers) المسؤول عن توريد البضائع
        """
        self.id = id  # سيتولد تلقائياً من قاعدة البيانات (SERIAL)
        self.supplier_name = str(supplier_name).strip()
        self.phone = str(phone).strip()
        self.company = str(company).strip()
        self.address = str(address).strip()

    def to_dict(self):
        return {
            "id": self.id,
            "supplier_name": self.supplier_name,
            "phone": self.phone,
            "company": self.company,
            "address": self.address
        }


class PurchaseInvoice:
    def __init__(self, supplier_id, total_amount, tax=0.0, discount=0.0, payment_type="CASH", notes="", id=None):
        """
        تمثيل رأس فاتورة الشراء (Purchase Invoice Header)
        """
        self.id = id  # رقم الفاتورة التلقائي
        self.supplier_id = int(supplier_id) if supplier_id else None
        self.total_amount = float(total_amount)
        self.tax = float(tax)
        self.discount = float(discount)
        self.payment_type = str(payment_type).strip()  # CASH أو CREDIT
        self.notes = str(notes).strip()


class PurchaseInvoiceDetail:
    def __init__(self, invoice_id, barcode, qty, cost_price, id=None):
        """
        تمثيل تفاصيل الفاتورة (Invoice Line Items) صنف بصنف
        """
        self.id = id
        self.invoice_id = int(invoice_id)
        self.barcode = str(barcode).strip()
        self.qty = int(qty)
        self.cost_price = float(cost_price)