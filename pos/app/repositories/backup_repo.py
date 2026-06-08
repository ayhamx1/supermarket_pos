# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Backup & Restore Repository
📂 Path: app/repositories/backup_repo.py
"""
import os
import subprocess
import datetime
from app.config.database import DB_PARAMS

class BackupRepository:
    def __init__(self):
        self.db_params = DB_PARAMS

    def execute_backup(self, target_path):
        """إنشاء نسخة احتياطية كاملة للملف المحدد"""
        try:
            # تعيين كلمة المرور مؤقتاً في متغيرات بيئة النظام لتخطي طلبها من الـ Terminal
            os.environ['PGPASSWORD'] = self.db_params['password']
            
            command = [
                'pg_dump',
                '-h', self.db_params['host'],
                '-p', str(self.db_params['port']),
                '-U', self.db_params['user'],
                '-F', 'c',  # صيغة مخصصة ومضغوطة (Custom Format)
                '-b',       # تضمين البيانات الكبيرة (Large Objects)
                '-v',       # وضع التفاصيل المباشرة
                '-f', target_path,
                self.db_params['database']
            ]
            
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True, "تمت عملية النسخ الاحتياطي بنجاح."
        except subprocess.CalledProcessError as e:
            return False, f"فشل المحرك في إتمام النسخ! تأكد من تثبيت PostgreSQL الأدوات المساعدة.\nالخطأ: {e.stderr.decode('utf-8', errors='ignore')}"
        except Exception as e:
            return False, str(e)

    def execute_restore(self, source_path):
        """استعادة قاعدة البيانات بالكامل من ملف احتياطي سابق"""
        try:
            os.environ['PGPASSWORD'] = self.db_params['password']
            
            command = [
                'pg_restore',
                '-h', self.db_params['host'],
                '-p', str(self.db_params['port']),
                '-U', self.db_params['user'],
                '-d', self.db_params['database'],
                '-c',  # مسح الجداول القديمة قبل إعادة بنائها لتفادي تداخل البيانات (Clean)
                '-v',
                source_path
            ]
            
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True, "تمت استعادة قاعدة البيانات بنجاح تام."
        except subprocess.CalledProcessError as e:
            return False, f"فشل الاسترجاع الحتمي!\nالخطأ: {e.stderr.decode('utf-8', errors='ignore')}"
        except Exception as e:
            return False, str(e)

    def trigger_auto_backup(self):
        """دالة للنسخ التلقائي المخفي، تقوم بالحفظ داخل مجلد المشروع في فولدر باسم backups"""
        backup_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "backups"))
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"auto_backup_{timestamp}.backup"
        full_path = os.path.join(backup_dir, filename)
        
        success, msg = self.execute_backup(full_path)
        return success, full_path