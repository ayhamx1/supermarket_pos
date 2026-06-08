# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - User Controller
📂 Path: app/controllers/users/user_controller.py
"""
from app.repositories.user_repo import UserRepository
from app.models.user import User

class UserController:
    def __init__(self):
        self.repo = UserRepository()

    def load_users(self):
        return self.repo.get_all_users()

    def create_user(self, username, full_name, role, password):
        user = User(username, full_name, role, password)
        return self.repo.add_user(user)

    def load_permissions(self, role):
        return self.repo.get_role_permissions(role)

    def save_permission(self, role, screen, v, a, e, d):
        return self.repo.update_permission_matrix(role, screen, v, a, e, d)

    def verify_action_access(self, role, screen, action):
        """تستدعى من أي شاشة (كاشير/مخزن) قبل تنفيذ الضغط على أي زر حساس"""
        return self.repo.check_button_access(role, screen, action)