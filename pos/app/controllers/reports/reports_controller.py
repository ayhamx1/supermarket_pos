# -*- coding: utf-8 -*-
"""
Supermarket POS - Reports Controller
Path: app/controllers/reports/reports_controller.py
"""
from app.repositories.report_repo import ReportsRepository
from datetime import datetime, timedelta

class ReportsController:
    def __init__(self):
        self.repo = ReportsRepository()

    def generate_report(self, report_type, start_date_str=None, end_date_str=None):
        # تعيين تواريخ افتراضية إذا لم تُرسل
        start_date = start_date_str if start_date_str else datetime.now().strftime('%Y-%m-%d 00:00:00')
        end_date = end_date_str if end_date_str else datetime.now().strftime('%Y-%m-%d 23:59:59')

        if report_type == "sales":
            return self.repo.get_sales_report(start_date, end_date)
        elif report_type == "profits":
            return self.repo.get_profits_report(start_date, end_date)
        elif report_type == "inventory":
            return self.repo.get_inventory_report()
        elif report_type == "stagnant":
            # الأصناف الراكدة منذ 30 يوماً كخيار قياسي
            threshold = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            return self.repo.get_stagnant_items_report(threshold)
        elif report_type == "purchases":
            return self.repo.get_purchases_report(start_date, end_date)
        elif report_type == "suppliers":
            return self.repo.get_suppliers_report()
        elif report_type == "customers":
            return self.repo.get_customers_report()
        elif report_type == "vault":
            return self.repo.get_vault_report(start_date, end_date)
        
        return []