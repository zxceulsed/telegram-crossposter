# src/handlers/repost.py
import asyncio
from aiogram import Router, types
from src.services.db import Database
from src.services.vk_service import VKService
from src.services.ok_service import OKService

router = Router()
db = Database()

@router.message()
async def repost_message(message: types.Message):
    cfg = db.get_by_source(str(message.chat.id))
    if not cfg:
        await message.answer(f"Источник не настроен: {message.chat.id}")
        return

    vk_api_key, vk_group_id, ok_token, ok_gid, ok_app, ok_session, delay = cfg
    text = message.text or message.caption or "(текст отсутствует)"

    # Ждем указанную задержку
    await asyncio.sleep(delay * 3600)

    vk = VKService(vk_api_key, vk_group_id)
    ok = OKService(ok_app, ok_session, ok_token, ok_gid)

    # Публикация в VK
    vk_resp = vk.post_text(text)
    if vk_resp.get("error"):
        await message.answer(f"Ошибка VK: {vk_resp['error']['error_msg']}")
    else:
        await message.answer("Успешно опубликовано в VK.")

    # Публикация в OK
    ok_resp = ok.post_text(text)
    if ok_resp.status_code == 200:
        await message.answer("Успешно опубликовано в OK.")
    else:
        await message.answer(f"Ошибка OK: {ok_resp.status_code}")
