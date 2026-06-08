# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Backup Controller
📂 Path: app/controllers/system/backup_controller.py
"""
from app.repositories.backup_repo import BackupRepository

class BackupController:
    def __init__(self):
        self.repo = BackupRepository()

    def create_manual_backup(self, path):
        return self.repo.execute_backup(path)

    def restore_database(self, path):
        return self.repo.execute_restore(path)

    def run_auto_backup(self):
        return self.repo.trigger_auto_backup()