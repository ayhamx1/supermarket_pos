# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Product Model
📂 Path: app/models/product.py
"""

class Product:
    def __init__(self, barcode, item_name, category_id, unit, cost_price, selling_price, discount=0.0, stock_qty=0):
        """
        تمثيل صنف أو منتج داخل نظام السوبرماركت (MVC Architecture)
        """
        self.barcode = str(barcode).strip()
        self.item_name = str(item_name).strip()
        # تحويل كود القسم إلى رقم صحيح إذا كان متاحاً، وإلا يبقى None ليتوافق مع الـ NULL في قاعدة البيانات
        self.category_id = int(category_id) if category_id is not None else None
        self.unit = str(unit).strip()
        self.cost_price = float(cost_price)
        self.selling_price = float(selling_price)
        self.discount = float(discount)
        self.stock_qty = int(stock_qty)

    def to_dict(self):
        """
        تحويل بيانات الكائن إلى قاموس (Dictionary) ليسهل التعامل معها أو تمريرها للـ UI
        """
        return {
            "barcode": self.barcode,
            "item_name": self.item_name,
            "category_id": self.category_id,
            "unit": self.unit,
            "cost_price": self.cost_price,
            "selling_price": self.selling_price,
            "discount": self.discount,
            "stock_qty": self.stock_qty
        }

    def __repr__(self):
        return f"<Product {self.barcode} - {self.item_name}>"