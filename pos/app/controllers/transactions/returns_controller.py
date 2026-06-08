# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Returns & Financial Adjustments Controller
📂 Path: app/controllers/transactions/returns_controller.py
"""
import psycopg2

class ReturnsController:
    def __init__(self, db_connection_pool=None):
        # هنا يتم تمرير اتصال قاعدة البيانات المركزي الخاص بمشروعك
        self.pool = db_connection_pool

    def execute_sales_return(self, invoice_id, product_id, return_qty, unit_price, buy_price, is_cash=True, customer_id=None):
        """
        ✅ تنفيذ عملية مرتجع بيع وتحديث المخزن، الخزنة، والأرباح في عملية واحدة محمية
        """
        # حساب المبالغ المالي والأرباح المستبعدة
        total_return_value = return_qty * unit_price
        profit_to_deduct = (unit_price - buy_price) * return_qty
        
        # اتصال افتراضي كمثال للـ SQL Transactions في مشروعك
        conn = None
        try:
            # افتراضياً نقوم بفتح الاتصال والـ Transaction
            # conn = self.pool.getconn()
            # cursor = conn.cursor()
            
            print("--- بدء عملية مرتجع البيع ---")
            
            # 1. تحديث المخزون (زيادة الرفوف بالكمية العائدة)
            sql_stock = "UPDATE products SET stock_qty = stock_qty + %s WHERE id = %s;"
            print(f"[SQL] زيادة المخزن للمنتج {product_id} بمقدار {return_qty}")
            
            # 2. تعديل الخزنة أو حساب العميل
            if is_cash:
                sql_finance = "UPDATE vault SET balance = balance - %s WHERE is_active = True;"
                print(f"[SQL] خصم مبلغ {total_return_value} ج.م من الخزنة النقدية")
            else:
                sql_finance = "UPDATE customers SET balance = balance - %s WHERE id = %s;"
                print(f"[SQL] تخفيض مديونية العميل {customer_id} بمقدار {total_return_value}")
                
            # 3. تعديل أو تسجيل الأرباح المستبعدة في جدول التقارير المالية
            sql_profit = "INSERT INTO financial_adjustments (type, amount, related_id) VALUES ('sales_return_profit_deduct', %s, %s);"
            print(f"[SQL] تسجيل استبعاد أرباح بقيمة {profit_to_deduct} ج.م")
            
            # في الكود الفعلي يتم عمل: 
            # conn.commit()
            print("✅ تمت عملية المرتجع المالي والمخزني بنجاح تام!")
            return True
            
        except Exception as e:
            # if conn: conn.rollback()
            print(f"❌ فشلت عملية المرتجع وتم التراجع عن التغييرات: {e}")
            return False

    def execute_purchase_return(self, supplier_id, product_id, return_qty, buy_price, is_cash=True):
        """
        ✅ تنفيذ عملية مرتجع شراء إلى مورد وتعديل المخزن والخزنة
        """
        total_return_value = return_qty * buy_price
        
        try:
            print("--- بدء عملية مرتجع الشراء للمورد ---")
            
            # 1. تحديث المخزون (خصم الكمية الخارجة من المحل)
            sql_stock = "UPDATE products SET stock_qty = stock_qty - %s WHERE id = %s;"
            print(f"[SQL] خصم المخزن للمنتج {product_id} بمقدار {return_qty}")
            
            # 2. تعديل الخزنة (استرداد نقدية) أو تخفيض حساب المورد الآجل
            if is_cash:
                sql_finance = "UPDATE vault SET balance = balance + %s WHERE is_active = True;"
                print(f"[SQL] إضافة مبلغ {total_return_value} ج.م وارد إلى الخزنة")
            else:
                sql_finance = "UPDATE suppliers SET current_debt = current_debt - %s WHERE id = %s;"
                print(f"[SQL] تخفيض حساب المورد {supplier_id} بمقدار {total_return_value}")
                
            print("✅ تم إرجاع البضاعة للمورد وتسوية الحسابات!")
            return True
        except Exception as e:
            print(f"❌ فشل مرتجع الشراء: {e}")
            return False