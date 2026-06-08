# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Customer & Partner Models
📂 Path: app/models/partner.py
"""

class Customer:
    def __init__(self, name, phone="", email="", max_credit=1000.0, current_balance=0.0, id=None):
        """
        تمثيل بيانات العميل وحد الائتمان المسموح به للآجل
        """
        self.id = id
        self.name = str(name).strip()
        self.phone = str(phone).strip()
        self.email = str(email).strip()
        self.max_credit = float(max_credit) # الحد الأقصى للدين
        self.current_balance = float(current_balance) # المديونية الحالية (حساب عليه)


class PartnerTransaction:
    def __init__(self, partner_type, partner_id, tx_type, amount, notes="", id=None):
        """
        تمثيل حركة مالية في كشف الحساب (فاتورة آجل، سداد نقدي، مرتجع)
        """
        self.id = id
        self.partner_type = str(partner_type).strip() # 'CUSTOMER' أو 'SUPPLIER'
        self.partner_id = int(partner_id)
        self.tx_type = str(tx_type).strip() # 'INVOICE' (فاتورة), 'PAYMENT' (سداد دفعة)
        self.amount = float(amount)
        self.notes = str(notes).strip()