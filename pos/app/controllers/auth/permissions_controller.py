# -*- coding: utf-8 -*-
"""
Supermarket POS - Permissions & Audit Controller
Path: app/controllers/auth/permissions_controller.py
"""
from app.repositories.user_repo import UserRepository

class PermissionsController:
    def __init__(self):
        self.repo = UserRepository()

    def load_users_list(self):
        return self.repo.get_all_users()

    def get_permissions_for_role(self, role_name):
        res = self.repo.get_role_permissions(role_name)
        return {
            'screen_pos': res[0],
            'button_discount': res[1],
            'button_change_price': res[2],
            'button_delete_item': res[3]
        }

    def update_role_matrix(self, role_name, screen_pos, btn_discount, btn_price, btn_delete):
        perms = {
            'screen_pos': screen_pos,
            'button_discount': btn_discount,
            'button_change_price': btn_price,
            'button_delete_item': btn_delete
        }
        success = self.repo.save_user_permissions(role_name, perms)
        return success

    def write_audit(self, user_id, action_type, description):
        return self.repo.log_action(user_id, action_type, description)

    def load_audit_history(self):
        return self.repo.get_audit_logs()