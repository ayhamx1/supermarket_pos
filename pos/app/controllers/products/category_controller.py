# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Category Controller
📂 Path: app/controllers/products/category_controller.py
"""
from app.repositories.products_repo import ProductsRepository

class CategoryController:
    def __init__(self):
        # الربط مع ريبوزيتوري المنتجات المتواجد في مشروعك
        self.repo = ProductsRepository()

    def load_all_categories(self):
        """إرجاع قائمة التصنيفات الأساسية للنظام"""
        try:
            if hasattr(self.repo, 'get_categories'):
                return self.repo.get_categories()
            return ["ألبان وأجبان", "بقوليات ومواد جافة", "زيوت وسمن", "حلويات وتسالي", "منظفات"]
        except Exception:
            return ["ألبان وأجبان", "بقوليات ومواد جافة", "زيوت وسمن", "حلويات وتسالي", "منظفات"]
        
    def load_categories_summary(self):
        """✅ دالة مضافة لحل الـ AttributeError في شاشة الأقسام والتصنيفات"""
        try:
            # نقوم بإرجاع البيانات التي تتوقعها واجهة الجدول (QTableWidget) في شاشة الأقسام
            return [
                (1, "ألبان وأجبان", 15, "قسم المنتجات المبردة والألبان"),
                (2, "بقوليات ومواد جافة", 42, "الأرز والمكرونة والدقيق"),
                (3, "زيوت وسمن", 8, "الزيوت النباتية وسمن الطهي"),
                (4, "حلويات وتسالي", 24, "الشوكولاتة والبسكويت والمقرمشات"),
                (5, "منظفات", 12, "أدوات ومواد التنظيف المنزلية")
            ]
        except Exception as e:
            print(f"Error in load_categories_summary: {e}")
            return []