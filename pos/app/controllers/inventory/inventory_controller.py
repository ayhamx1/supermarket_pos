# -*- coding: utf-8 -*-
"""
Supermarket POS - Inventory Controller
Path: app/controllers/inventory/inventory_controller.py
"""
from app.repositories.inventory_repo import InventoryRepository

class InventoryController:
    def __init__(self):
        self.repo = InventoryRepository()

    def get_stock_list(self, search_query="", low_stock_only=False):
        return self.repo.get_inventory_status(search_query, low_stock_only)

    def process_adjustment(self, item_id, new_quantity, notes):
        if not item_id:
            return False, "يرجى تحديد الصنف أولاً"
        if new_quantity < 0:
            return False, "لا يمكن أن تكون الكمية الجديدة بالسالب"
        
        success = self.repo.apply_stock_adjustment(item_id, new_quantity, notes)
        return success, "تمت تسوية كمية المخزون بنجاح" if success else "فشلت عملية التسوية"

    def get_movements_log(self, item_id):
        return self.repo.get_item_movements(item_id)