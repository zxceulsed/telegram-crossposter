# src/handlers/__init__.py

from aiogram import Router
from .admin import router as admin_router
from .repost import router as repost_router

# Основной роутер для подключения в main.py
router = Router()
router.include_router(admin_router)
router.include_router(repost_router)

__all__ = ["router"]