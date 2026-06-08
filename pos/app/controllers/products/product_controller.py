# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Product Controller
📂 Path: app/controllers/products/product_controller.py
"""

# استدعاء الكلاس بالجمع ProductsRepository
from app.repositories.products_repo import ProductsRepository
from app.models.product import Product
from app.repositories.categories_repo import CategoriesRepository # عدل المسار حسب اسم الملف عندك

class ProductController:
    def __init__(self):
        self.repo = ProductsRepository()
        # 2. أضف كائن مستودع الأصناف هنا 🚀
        self.categories_repo = CategoriesRepository()

    def load_all_products(self):
        return self.repo.get_all_products()

    def load_categories(self):
        return self.repo.get_all_categories() # تحديث الاسم هنا

    def search_products(self, text):
        return self.repo.search_products(text)

    def save_new_product(self, data):
        product = Product(
            barcode=data['barcode'],
            item_name=data['item_name'],
            category_id=data['category_id'],
            unit=data['unit'],
            cost_price=data['cost_price'],
            selling_price=data['selling_price'],
            discount=data['discount'],
            stock_qty=data['stock_qty']
        )
        self.repo.add_product(product)

   # 🚀 التحديث النهائي والآمن المتوافق مع بيانات الواجهة الحقيقية
    def validate_and_create_product(self, *args):
        """
        تستقبل المتغيرات الـ 7 القادمة من واجهة إضافة المنتج وتتعامل مع اسم القسم ديناميكياً
        """
        if len(args) < 7:
            return False, f"خطأ: عدد الحقول المرسلة غير كامل (المستلم: {len(args)} حقول)"

        # تفكيك القيم حسب الترتيب المطبوع في الترمنال
        barcode       = args[0]
        name          = args[1]
        category_name = args[2]  # قادم كنص: 'ألبان وأجبان'
        unit          = args[3]
        cost          = args[4]
        price         = args[5]
        discount      = args[6]  # القيمة الأخيرة

        # 1. التحقق الأساسي من إدخال البيانات المهمة
        if not barcode or not name:
            return False, "تنبيه: يجب إدخال باركود واسم المنتج!"

        try:
            if float(price) < 0 or float(cost) < 0:
                return False, "تنبيه: لا يمكن أن يكون السعر أو التكلفة بالسالب!"
        except ValueError:
            return False, "تنبيه: الأسعار يجب أن تكون أرقاماً صالحة!"

        # 2. تحويل اسم القسم (category_name) إلى الرقم المعرّف (category_id)
        category_id = None
        try:
            # جلب كل الأقسام المتاحة من قاعدة البيانات
            all_categories = self.load_categories()  
            # البحث عن القسم الذي يطابق الاسم القادم من الواجهة
            for cat in all_categories:
                # ملاحظة: قم بتغيير المفاتيح ('id' و 'category_name') حسب أسماء الحقول في الـ Dictionary أو الكلاس الخاص بالأصناف عندك
                if isinstance(cat, dict):
                    if cat.get('category_name') == category_name or cat.get('name') == category_name:
                        category_id = cat.get('id')
                        break
                else:
                    # إذا كانت الأقسام تعود كـ Objects وليس Dictionaries
                    if getattr(cat, 'category_name', None) == category_name or getattr(cat, 'name', None) == category_name:
                        category_id = getattr(cat, 'id', None)
                        break

            # إذا لم نجد القسم في قاعدة البيانات، نعطيه رقم افتراضي أو نوقف العملية لسلامة البيانات
            if category_id is None:
                return False, f"خطأ: القسم المختار ({category_name}) غير معرّف برقم في قاعدة البيانات!"

        except Exception as e:
            return False, f"خطأ أثناء التحقق من رقم القسم: {str(e)}"

        # 3. تجهيز البيانات النهائية واستدعاء دالة الحفظ
        try:
            data = {
                'barcode': barcode,
                'item_name': name,
                'category_id': category_id,  # الآن نمرر الـ ID الرقمي الآمن وعمليتك ستنجح بامتياز!
                'unit': unit,
                'cost_price': float(cost),
                'selling_price': float(price),
                'discount': float(discount) if discount else 0.0,
                'stock_qty': 0.0  # القيمة الابتدائية للمخزون
            }
            
            # حفظ المنتج في قاعدة البيانات
            self.save_new_product(data)
            return True, "تم حفظ المنتج الجديد بنجاح وبشكل متوافق."
            
        except Exception as e:
            return False, f"فشل حفظ المنتج في قاعدة البيانات: {str(e)}"

    def update_existing_product(self, original_barcode, data):
        product = Product(
            barcode=data['barcode'],
            item_name=data['item_name'],
            category_id=data['category_id'],
            unit=data['unit'],
            cost_price=data['cost_price'],
            selling_price=data['selling_price'],
            discount=data['discount'],
            stock_qty=data['stock_qty']
        )
        self.repo.update_product(original_barcode, product)

    def delete_product(self, barcode):
        self.repo.delete_product(barcode)