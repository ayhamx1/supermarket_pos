# -*- coding: utf-8 -*-
"""
Supermarket POS - Reports & Analytics Repository
Path: app/repositories/report_repo.py
"""
import psycopg2
from app.config.database import DB_PARAMS

class ReportsRepository:
    def __init__(self):
        self.db_params = DB_PARAMS

    def get_sales_report(self, start_date, end_date):
        """1. تقرير المبيعات التفصيلي والإجمالي"""
        query = """
            SELECT 
                created_at::date, 
                COUNT(id) as total_invoices, 
                SUM(total_amount) as gross_sales, 
                SUM(paid_amount) as collected, 
                SUM(total_amount - paid_amount) as remaining_credit
            FROM sales_invoices
            WHERE created_at BETWEEN %s AND %s
            GROUP BY created_at::date
            ORDER BY created_at::date DESC;
        """
        return self._execute_query(query, (start_date, end_date))

    def get_profits_report(self, start_date, end_date):
        """2. تقرير الأرباح الصافية (سعر البيع - سعر التكلفة)"""
        query = """
            SELECT 
                si.created_at::date,
                SUM(s_item.quantity * s_item.unit_price) as total_sales,
                SUM(s_item.quantity * it.cost_price) as total_cost,
                SUM((s_item.quantity * s_item.unit_price) - (s_item.quantity * it.cost_price)) as net_profit
            FROM sales_invoice_items s_item
            JOIN sales_invoices si ON s_item.invoice_id = si.id
            JOIN items it ON s_item.item_id = it.id
            WHERE si.created_at BETWEEN %s AND %s
            GROUP BY si.created_at::date
            ORDER BY si.created_at::date DESC;
        """
        return self._execute_query(query, (start_date, end_date))

    def get_inventory_report(self):
        """3. تقرير المخزون الحالي وتقييم البضاعة بسعر التكلفة والبيع"""
        query = """
            SELECT 
                name, 
                barcode, 
                stock_quantity, 
                cost_price, 
                sale_price,
                (stock_quantity * cost_price) as total_cost_value,
                (stock_quantity * sale_price) as total_sale_value
            FROM items
            ORDER BY stock_quantity DESC;
        """
        return self._execute_query(query)

    def get_stagnant_items_report(self, threshold_date):
        """4. تقرير الأصناف الراكدة (التي لم تُبع منذ تاريخ معين)"""
        query = """
            SELECT id, barcode, name, stock_quantity, sale_price 
            FROM items 
            WHERE id NOT IN (
                SELECT DISTINCT item_id 
                FROM sales_invoice_items sii
                JOIN sales_invoices si ON sii.invoice_id = si.id
                WHERE si.created_at >= %s
            ) AND stock_quantity > 0
            ORDER BY stock_quantity DESC;
        """
        return self._execute_query(query, (threshold_date,))

    def get_purchases_report(self, start_date, end_date):
        """5. تقرير المشتريات وحركة المصاريف مع الشركات"""
        query = """
            SELECT 
                pi.created_at::date, 
                p.company_name, 
                COUNT(pi.id) as invoices_count, 
                SUM(pi.total_amount) as total_purchases
            FROM purchase_invoices pi
            JOIN partners p ON pi.supplier_id = p.id
            WHERE pi.created_at BETWEEN %s AND %s
            GROUP BY pi.created_at::date, p.company_name
            ORDER BY pi.created_at::date DESC;
        """
        return self._execute_query(query, (start_date, end_date))

    def get_suppliers_report(self):
        """6. تقرير الموردين وإجمالي المديونيات المستحقة لهم"""
        query = """
            SELECT company_name, name, phone, balance 
            FROM partners 
            WHERE type = 'supplier' AND balance > 0
            ORDER BY balance DESC;
        """
        return self._execute_query(query)

    def get_customers_report(self):
        """7. تقرير العملاء وحجم الديون الآجلة ونقاط الولاء"""
        query = """
            SELECT name, phone, balance, loyalty_points 
            FROM partners 
            WHERE type = 'customer'
            ORDER BY balance DESC;
        """
        return self._execute_query(query)

    def get_vault_report(self, start_date, end_date):
        """8. تقرير حركة الخزنة وحجم التدفّق المالي"""
        query = """
            SELECT 
                created_at, 
                transaction_type, 
                amount, 
                notes
            FROM vault_transactions
            WHERE created_at BETWEEN %s AND %s
            ORDER BY created_at DESC;
        """
        return self._execute_query(query, (start_date, end_date))

    def _execute_query(self, query, params=None):
        try:
            conn = psycopg2.connect(**self.db_params)
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        except Exception as e:
            print(f"Database Error in report_repo: {str(e)}")
            return []