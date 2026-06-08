# -*- coding: utf-8 -*-
"""
⚙️ Supermarket POS - Promotions Controller
📂 Path: app/controllers/marketing/promo_controller.py
"""
from app.repositories.promo_repo import PromotionsRepository

class PromotionsController:
    def __init__(self):
        self.repo = PromotionsRepository()

    def create_promo(self, name, p_type, barcode, disc_val, buy_q, get_q, start, end):
        return self.repo.add_promotion(name, p_type, barcode, disc_val, buy_q, get_q, start, end)

    def fetch_promotions(self):
        return self.repo.get_all_promotions()

    def change_status(self, promo_id, status):
        self.repo.toggle_promo_status(promo_id, status)