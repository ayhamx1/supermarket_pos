# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Reports & Analytics Models
📂 Path: app/models/report.py
"""

class DailySummary:
    def __init__(self, total_sales, total_cost, net_profit, total_invoices, date_str):
        """
        تمثيل ملخص مالي ليوم محدد (المبيعات، التكلفة، الأرباح الصافية)
        """
        self.total_sales = float(total_sales)
        self.total_cost = float(total_cost)
        self.net_profit = float(net_profit)
        self.total_invoices = int(total_invoices)
        self.date_str = str(date_str)


class TopSellingItem:
    def __init__(self, barcode, item_name, total_qty_sold, total_revenue):
        """
        تمثيل بيانات الأصناف الأكثر حركة ومبيعاً
        """
        self.barcode = str(barcode)
        self.item_name = str(item_name)
        self.total_qty_sold = int(total_qty_sold)
        self.total_revenue = float(total_revenue)