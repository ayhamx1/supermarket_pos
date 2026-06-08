# -*- coding: utf-8 -*-
"""
Supermarket POS - Admin Main Top Dashboard (Windows 11 Fluent Design Style)
Path: ui/admin/admin_main.py
"""
import sys
import os

# 🎯 التعديل الجوهري لحماية المسارات عند الاستدعاء من المجلد الرئيسي أو الفرعي
current_file_dir = os.path.dirname(os.path.abspath(__file__))
# 1. تهيئة مسار المشروع الرئيسي فوراً ومنحه الأولوية القصوى ليتعرف بايثون على كل السجلات المجاورة
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 2. استدعاء مكتبات الـ GUI الأساسية
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QPushButton, QMenu
from PyQt6.QtGui import QFont, QAction
from PyQt6.QtCore import Qt

# 🛡️ استيراد شاشة الإدارة المالية والجرد من مسار التحكم الخلفي المعتمد
try:
    from app.controllers.admin.financial_controller import FinancialController
except Exception as e:
    print(f"⚠️ خطأ كرتيكال في استيراد FinancialController الخلفي: {e}")
    FinancialController = None

# =========================================================================
# 🛡️ 3. دالة حماية التشغيل ضد انهيار السيستم
# =========================================================================
def create_safe_placeholder(screen_name, error_msg):
    """دالة لإنشاء شاشة بديلة مؤقتة في حال وجود خطأ بملف الشاشة الأصلي تمنع كراش السيستم"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    lbl = QLabel(f"⚙️ شاشة ({screen_name}) قيد التجهيز أو ينقصها ملفات الربط الخلفي.\n\nتفاصيل الخطأ: {error_msg}")
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lbl.setStyleSheet("color: #64748B; font-size: 14px; font-weight: 500;")
    layout.addWidget(lbl)
    return widget

# ==============================================================================
# 📂 كتل استيراد الواجهات وشاشات التحكم (ui/admin/admin_main.py)
# ==============================================================================

# جلب شاشة لوحة المؤشرات (Index 0)
try: 
    from ui.admin.dashboard_widget import DashboardWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد DashboardWidget: {e}")
    DashboardWidget = None

# جلب شاشة المنتجات (Index 1)
try: 
    from ui.admin.products_management import ProductsManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد ProductsManagementWidget: {e}")
    ProductsManagementWidget = None

# جلب شاشة حركات وجرد المخزون (Index 2)
try: 
    from ui.admin.inventory_management import InventoryManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد InventoryManagementWidget: {e}")
    InventoryManagementWidget = None

# جلب شاشة فواتير المشتريات (Index 3)
try: 
    from ui.admin.purchases_management import PurchasesManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد PurchasesManagementWidget: {e}")
    PurchasesManagementWidget = None

# جلب شاشة الشركاء والعملاء (Index 4)
try: 
    from ui.admin.partners_management import PartnersManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد PartnersManagementWidget: {e}")
    PartnersManagementWidget = None

# جلب شاشة الموظفين والحسابات (Index 5)
try: 
    from ui.admin.users_management import UsersManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد UsersManagementWidget: {e}")
    UsersManagementWidget = None

# جلب شاشة التقارير والتحليلات (Index 6)
try: 
    from ui.admin.reports_management import ReportsManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد ReportsManagementWidget: {e}")
    ReportsManagementWidget = None

# جلب شاشة الخزنة المركزية (Index 7)
try: 
    from ui.admin.vault_management import VaultManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد VaultManagementWidget: {e}")
    VaultManagementWidget = None

# جلب شاشة العروض والخصومات (Index 8)
try: 
    from ui.admin.promotions_management import PromotionsManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد PromotionsManagementWidget: {e}")
    PromotionsManagementWidget = None

# جلب شاشة إعدادات النظام والهوية (Index 9) ✨
try: 
    from ui.admin.settings_management import SettingsManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد SettingsManagementWidget: {e}")
    SettingsManagementWidget = None

# جلب شاشة الأقسام والتصنيفات (Index 10)
try: 
    from ui.admin.categories_management import CategoriesManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد CategoriesManagementWidget: {e}")
    CategoriesManagementWidget = None

# جلب شاشة وطباعة الباركود والملصقات (Index 11) ✨
try: 
    from ui.admin.barcode_management import BarcodeManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد BarcodeManagementWidget: {e}")
    BarcodeManagementWidget = None

# جلب شاشة المصروفات التشغيلية (Index 12)
try:
    from ui.admin.expenses_management import ExpensesManagementWidget
except Exception as e:
    print(f"CRITICAL IMPORT ERROR in Expenses: {str(e)}")
    ExpensesManagementWidget = None

# جلب شاشة مصفوفة الصلاحيات والأمن (Index 13)
try: 
    from ui.admin.permissions_management import PermissionsManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد PermissionsManagementWidget: {e}")
    PermissionsManagementWidget = None

# جلب شاشة مرتجع المبيعات (Index 14)
try: 
    from ui.admin.sales_returns_management import SalesReturnsManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد SalesReturnsManagementWidget: {e}")
    SalesReturnsManagementWidget = None

# جلب شاشة مرتجع المشتريات (Index 15)
try: 
    from ui.admin.purchase_returns_management import PurchaseReturnsManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد PurchaseReturnsManagementWidget: {e}")
    PurchaseReturnsManagementWidget = None

# جلب شاشة سجل العمليات والرقابة (Index 16)
try: 
    from ui.admin.audit_logs_management import AuditLogsManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد AuditLogsManagementWidget: {e}")
    AuditLogsManagementWidget = None

# جلب شاشة إدارة الورديات وجرد الكاشير (Index 17) ✨
try:
    from ui.admin.shifts_management import ShiftsManagementWidget
except Exception as e:
    print(f"CRITICAL IMPORT ERROR in ShiftsManagement: {str(e)}")
    ShiftsManagementWidget = None

# جلب شاشة إدارة التنبيهات والإشعارات الذكية (Index 18) ✨
try: 
    from ui.admin.notifications_management import NotificationsManagementWidget
except Exception as e: 
    print(f"⚠️ خطأ استيراد NotificationsManagementWidget: {e}")
    NotificationsManagementWidget = None

WINDOWS_FLUENT_STYLE = """
    QMainWindow { background-color: #F3F3F3; }
    QFrame#topNavBar { background-color: #FFFFFF; border-bottom: 1px solid #E5E5E5; min-height: 52px; max-height: 52px; padding-left: 16px; padding-right: 16px; }
    QLabel#appBrand { color: #1B1B1B; font-weight: 600; font-size: 15px; font-family: 'Segoe UI', 'Arial'; }
    QPushButton#navBtn { background-color: transparent; color: #5D5D5D; border: none; border-radius: 4px; padding: 6px 12px; font-size: 13px; font-weight: 400; font-family: 'Segoe UI', 'Arial'; margin: 2px 1px; }
    QPushButton#navBtn:hover { background-color: #F5F5F5; color: #1B1B1B; }
    QPushButton#navBtn:checked { background-color: #E9E9E9; color: #0067B8; font-weight: 600; }
    QLabel#userActiveLbl { color: #1B1B1B; font-size: 12px; font-weight: 400; background-color: #F9F9F9; border: 1px solid #E5E5E5; padding: 5px 12px; border-radius: 4px; font-family: 'Segoe UI', 'Arial'; }
    QPushButton#logoutTopBtn { background-color: transparent; color: #1B1B1B; border: 1px solid #CCCCCC; border-radius: 4px; padding: 5px 12px; font-size: 12px; font-weight: 400; font-family: 'Segoe UI', 'Arial'; }
    QPushButton#logoutTopBtn:hover { background-color: #C42B1C; color: #FFFFFF; border-color: #C42B1C; }
    QMenu { background-color: #F9F9F9; border: 1px solid #DFDFDF; border-radius: 6px; padding: 4px; }
    QMenu::item { padding: 6px 24px 6px 16px; font-size: 13px; font-weight: 400; color: #1B1B1B; border-radius: 4px; font-family: 'Segoe UI', 'Arial'; }
    QMenu::item:selected { background-color: #E5E5E5; color: #1B1B1B; }
    QMenu::separator { height: 1px; background-color: #EEEEEE; margin: 4px 0px; }
"""

class AdminMainWindow(QMainWindow):
    def __init__(self, admin_name="أحمد", admin_id=1):
        super().__init__()
        self.admin_name = admin_name
        self.admin_id = admin_id # حفظ الآيدي لاستخدامه في جرد عهدة الورديات
        
        self.setWindowTitle("لوحة إدارة السوبرماركت المركزية")
        self.resize(1280, 720)
        self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.setStyleSheet(WINDOWS_FLUENT_STYLE)
        
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        base_layout = QVBoxLayout(central_widget)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.setSpacing(0)
        
        # ==========================================
        # 1. بناء شريط التنقل العلوي بنمط Windows 11
        # ==========================================
        top_bar = QFrame()
        top_bar.setObjectName("topNavBar")
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(16, 0, 16, 0)
        top_bar_layout.setSpacing(4)
        
        brand_lbl = QLabel("نظام إدارة المبيعات")
        brand_lbl.setObjectName("appBrand")
        brand_lbl.setFont(QFont("Segoe UI", 12))
        top_bar_layout.addWidget(brand_lbl)
        top_bar_layout.addSpacing(24)
        
        # زر شاشة الرئيسية (Index 0)
        btn_home = QPushButton("الرئيسية")
        btn_home.setObjectName("navBtn")
        btn_home.setCheckable(True)
        btn_home.setAutoExclusive(True)
        btn_home.setChecked(True)
        btn_home.clicked.connect(lambda: self.switch_page(0, "لوحة المؤشرات الرئيسية"))
        top_bar_layout.addWidget(btn_home)
        
        # قائمة إدارة المخازن والتكاويد
        btn_catalog = QPushButton("المخازن والتكويد")
        btn_catalog.setObjectName("navBtn")
        menu_catalog = QMenu(self)
        
        act_prod = QAction("إدارة المنتجات والأصناف", self)
        act_prod.triggered.connect(lambda: self.switch_page(1, "إدارة المنتجات والأصناف"))
        act_inv = QAction("جرد وحركات المخزون الحالي", self)
        act_inv.triggered.connect(lambda: self.switch_page(2, "إدارة جرد وحركات المخزون"))
        act_cats = QAction("إدارة الأقسام والتصنيفات", self)
        act_cats.triggered.connect(lambda: self.switch_page(10, "هيكلة وتصنيفات الأقسام المركزية"))
        act_barcode = QAction("توليد وطباعة الباركود والملصقات", self)
        act_barcode.triggered.connect(lambda: self.switch_page(11, "إدارة وطباعة الباركود والملصقات"))

        menu_catalog.addActions([act_prod, act_inv, menu_catalog.addSeparator(), act_cats, act_barcode])
        btn_catalog.setMenu(menu_catalog)
        top_bar_layout.addWidget(btn_catalog)
        
        # قائمة الحركات والتعاملات التجارية والمالية
        btn_trade = QPushButton("المعاملات التجارية")
        btn_trade.setObjectName("navBtn")
        menu_trade = QMenu(self)
        
        act_pur = QAction("فواتير المشتريات وإدارة الموردين", self)
        act_pur.triggered.connect(lambda: self.switch_page(3, "إدارة المشتريات وحسابات الموردين"))
        act_part = QAction("حسابات العملاء والآجل والموردين الموحدة", self)
        act_part.triggered.connect(lambda: self.switch_page(4, "حسابات الشركاء والديون الموحدة"))
        
        # 🎯 تعديل الربط لفتح نافذة الجرد المالي المتطورة المنفصلة كـ Dialog
        act_vault = QAction("💵 إدارة الخزنة المركزية وجرد عهد الورديات", self)
        act_vault.triggered.connect(self.open_financial_controller_dialog)
        
        act_shifts = QAction("إدارة الورديات وجرد الكاشير", self)
        act_shifts.triggered.connect(lambda: self.switch_page(17, "إدارة الورديات وجرد الكاشير"))
        
        act_expenses = QAction("إدارة المصروفات التشغيلية", self)
        act_expenses.triggered.connect(lambda: self.switch_page(12, "إدارة المصروفات التشغيلية"))
        act_promo = QAction("العروض والخصومات الذكية", self)
        act_promo.triggered.connect(lambda: self.switch_page(8, "مركز إدارة الحملات الترويجية والخصومات"))
        
        act_sales_ret = QAction("مرتجع بيع من عميل", self)
        act_sales_ret.triggered.connect(lambda: self.switch_page(14, "إدخال مرتجع مبيعات وتعديل الخزنة"))
        act_pur_ret = QAction("مرتجع شراء إلى مورد", self)
        act_pur_ret.triggered.connect(lambda: self.switch_page(15, "إدخال مرتجع مشتريات للموردين"))
        
        menu_trade.addActions([
            act_pur, act_part, menu_trade.addSeparator(),
            act_vault, act_shifts, act_expenses, menu_trade.addSeparator(), 
            act_promo, menu_trade.addSeparator(), 
            act_sales_ret, act_pur_ret
        ])
        btn_trade.setMenu(menu_trade)
        top_bar_layout.addWidget(btn_trade)
        
        # زر شاشة التقارير المالية المباشر (Index 6)
        btn_reports = QPushButton("التقارير المالية")
        btn_reports.setObjectName("navBtn")
        btn_reports.setCheckable(True)
        btn_reports.setAutoExclusive(True)
        btn_reports.clicked.connect(lambda: self.switch_page(6, "مركز التقارير الذكية والتحليلات المالية"))
        top_bar_layout.addWidget(btn_reports)
        
        # قائمة مصفوفة الإعدادات والأمان ونظام التشغيل
        btn_settings = QPushButton("الإدارة والأمان")
        btn_settings.setObjectName("navBtn")
        menu_settings = QMenu(self)
        
        act_notif = QAction("🔔 مركز التنبيهات والإشعارات الفورية", self)
        act_notif.triggered.connect(lambda: self.switch_page(8, "مركز التنبيهات والإشعارات الذكية"))
        menu_settings.addAction(act_notif)
        
        act_users = QAction("إدارة الموظفين والحسابات", self)
        act_users.triggered.connect(lambda: self.switch_page(5, "إدارة الموظفين والحسابات"))
        act_perms = QAction("مصفوفة الصلاحيات والأمن", self)
        act_perms.triggered.connect(lambda: self.switch_page(13, "مصفوفة التحكم في الصلاحيات والأمن"))
        
        act_audit = QAction("🛡️ سجل الرقابة وعمليات النظام (Audit Log)", self)
        act_audit.triggered.connect(lambda: self.switch_page(16, "سجل عمليات الموظفين والرقابة والأمان"))
        
        act_sys_settings = QAction("⚙️ إعدادات النظام والفواتير والضرائب", self)
        act_sys_settings.triggered.connect(lambda: self.switch_page(9, "إعدادات النظام والهوية"))
        
        menu_settings.addActions([act_users, act_perms, act_audit, menu_settings.addSeparator(), act_sys_settings])
        btn_settings.setMenu(menu_settings)
        top_bar_layout.addWidget(btn_settings)
        
        top_bar_layout.addStretch()
        
        user_lbl = QLabel(f"المستخدم: {self.admin_name}")
        user_lbl.setObjectName("userActiveLbl")
        user_lbl.setFont(QFont("Segoe UI", 9))
        top_bar_layout.addWidget(user_lbl)
        
        btn_logout = QPushButton("تسجيل الخروج")
        btn_logout.setObjectName("logoutTopBtn")
        btn_logout.clicked.connect(self.close)
        top_bar_layout.addWidget(btn_logout)
        
        base_layout.addWidget(top_bar)
        
        # ==========================================
        # 2. مكدس واجهات العرض المركزية (المحتوى الداخلي)
        # ==========================================
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #F3F3F3; padding: 16px;")
        
        self.screens_map = [
            (DashboardWidget, "لوحة المؤشرات الرئيسية"),             # Index 0
            (ProductsManagementWidget, "إدارة المنتجات"),           # Index 1
            (InventoryManagementWidget, "حركات وجرد المخزون"),       # Index 2
            (PurchasesManagementWidget, "فواتير المشتريات"),         # Index 3
            (PartnersManagementWidget, "الشركاء والعملاء"),          # Index 4
            (UsersManagementWidget, "الموظفين والحسابات"),          # Index 5
            (ReportsManagementWidget, "التقارير والتحليلات"),         # Index 6
            (VaultManagementWidget, "الخزنة المركزية"),            # Index 7
            (NotificationsManagementWidget, "مركز التنبيهات والإشعارات الذكية"), # Index 8
            (SettingsManagementWidget, "إعدادات النظام والهوية"),     # Index 9
            (CategoriesManagementWidget, "الأقسام والتصنيفات"),       # Index 10
            (BarcodeManagementWidget, "إدارة وطباعة الباركود والملصقات"), # Index 11
            (ExpensesManagementWidget, "المصروفات التشغيلية"),       # Index 12
            (PermissionsManagementWidget, "مصفوفة الصلاحيات والأمن"), # Index 13
            (SalesReturnsManagementWidget, "مرتجع المبيعات"),         # Index 14
            (PurchaseReturnsManagementWidget, "مرتجع المشتريات"),     # Index 15
            (AuditLogsManagementWidget, "سجل العمليات والرقابة"),      # Index 16
            (ShiftsManagementWidget, "إدارة الورديات وجرد الكاشير")    # Index 17
        ]

        for cls, name in self.screens_map:
            try:
                if cls is not None:
                    instance = cls()
                else:
                    raise Exception("ملف الكود غير متوفر أو يحتوي على أخطاء في الاستدعاء المسبق.")
            except Exception as err:
                instance = create_safe_placeholder(name, err)
                
            self.stacked_widget.addWidget(instance)

        base_layout.addWidget(self.stacked_widget)

    def switch_page(self, index, title_text):
        """التنقل المباشر لتحديث مكدس الشاشات وتتبع حركة المدير"""
        print(f"نظام القائمة العلوية - فتح الصفحة رقم: {index} -> {title_text}")
        self.stacked_widget.setCurrentIndex(index)

    def open_financial_controller_dialog(self):
        """🎯 دالة منبثقة لتشغيل شاشة الجرد المالي بأمان وحماية كـ Dialog مستقل"""
        if FinancialController is not None:
            # إنشاء الكائن وتمرير رقم الأدمين الحالي لحفظ السجلات بدقة
            financial_dialog = FinancialController(admin_id=self.admin_id, parent=self)
            financial_dialog.exec()
        else:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "خطأ في النظام", "لم يتم العثور على ملف التحكم المالي الخلفي الخلفي أو الكود يحتوي على أخطاء استيراد داخلي.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    
    # تمرير بيانات تجريبية للأدمين
    window = AdminMainWindow(admin_name="أحمد", admin_id=1)
    window.showMaximized()
    sys.exit(app.exec())