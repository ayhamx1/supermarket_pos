# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Inventory Model
📂 Path: app/models/inventory.py
"""

class InventoryTransaction:
    def __init__(self, barcode, tx_type, qty, user_id, notes="", from_warehouse="الرئيسي", to_warehouse=None):
        """
        تمثيل حركة مخزنية (وارد، صادر، تالف، تسوية، تحويل)
        """
        self.barcode = str(barcode).strip()
        self.tx_type = str(tx_type).strip()  # 'IN', 'OUT', 'DAMAGE', 'ADJUSTMENT', 'TRANSFER'
        self.qty = int(qty)
        self.user_id = int(user_id)
        self.notes = str(notes).strip()
        self.from_warehouse = str(from_warehouse).strip()
        self.to_warehouse = str(to_warehouse).strip() if to_warehouse else None