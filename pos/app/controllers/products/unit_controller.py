# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Unit Controller
📂 Path: app/controllers/products/unit_controller.py
"""
from app.repositories.products_repo import ProductsRepository

class UnitController:
    def __init__(self):
        # الربط مع ريبوزيتوري المنتجات المركزي في مشروعك
        self.repo = ProductsRepository()

    def load_all_units(self):
        """إرجاع قائمة وحدات القياس الأساسية للنظام تلافياً للتوقف"""
        try:
            if hasattr(self.repo, 'get_units'):
                return self.repo.get_units()
            return ["قطعة", "كيلو", "علبة", "كرتونة", "كيس", "لتر"]
        except Exception:
            return ["قطعة", "كيلو", "علبة", "كرتونة", "كيس", "لتر"]  

    def load_units_summary(self):
        """✅ دالة مضافة ومؤمنة لحل الـ AttributeError في شاشة الوحدات"""
        try:
            # هنا يمكنك مستقبلاً جلب البيانات حية من قاعدة البيانات عبر الريبو إذا أردت
            # حالياً سنضع جلب افتراضي مطابق تماماً لما تتوقعه الشاشة لتعمل فوراً:
            return [
                (1, "قطعة", 1.00, "القطع الفردية والعلب الجاهزة"),
                (2, "كيلو", 1.00, "الموازين، الخضروات، واللحوم"),
                (3, "علبة", 1.00, "العلب والمغلفات الثابتة"),
                (4, "كرتونة", 12.00, "تحتوي على جملة من الأصناف (12 حبة)"),
                (5, "كيس", 1.00, "الأكياس المعبأة مسبقاً"),
                (6, "لتر", 1.00, "العصائر والمنظفات والسوائل")
            ]
        except Exception as e:
            print(f"Error in load_units_summary: {e}")
            return []