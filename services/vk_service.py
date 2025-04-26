# src/services/vk_service.py

import requests
import aiohttp
import os
from typing import Optional
from src.config import config

VK_API_VERSION = '5.131'
VK_WALL_POST_URL = 'https://api.vk.com/method/wall.post'
VK_GET_UPLOAD_SERVER_URL = 'https://api.vk.com/method/photos.getWallUploadServer'
VK_SAVE_WALL_PHOTO_URL = 'https://api.vk.com/method/photos.saveWallPhoto'
TELEGRAM_FILE_BASE = 'https://api.telegram.org/file/bot'

class VKService:
    def __init__(self, token: str, group_id: str):
        self.token = token
        # Всегда храним положительный group_id; для owner_id ставим минус
        self.group_id = abs(int(group_id))

    def post_text(self, message: str, attachments: str = "") -> dict:

        resp = requests.post(
            VK_WALL_POST_URL,
            params={
                'access_token': self.token,
                'owner_id': f"-{self.group_id}",
                'from_group': 1,
                'message': message,
                'attachments': attachments,
                'v': VK_API_VERSION
            }
        )
        return resp.json()

    def get_upload_server_url(self) -> Optional[str]:
        data = requests.post(
            VK_GET_UPLOAD_SERVER_URL,
            params={
                'access_token': self.token,
                'group_id': self.group_id,
                'v': VK_API_VERSION
            }
        ).json()
        return data.get('response', {}).get('upload_url')

    async def upload_photo_to_server(self, upload_url: str, photo_path: str) -> Optional[dict]:
        async with aiohttp.ClientSession() as session:
            with open(photo_path, 'rb') as f:
                data = {'photo': f}
                async with session.post(upload_url, data=data) as resp:
                    if resp.status == 200:
                        return await resp.json()
        return None

    def save_wall_photo(self, upload_data: dict) -> Optional[str]:
        resp = requests.post(
            VK_SAVE_WALL_PHOTO_URL,
            params={
                'access_token': self.token,
                'group_id': self.group_id,
                'photo': upload_data['photo'],
                'server': upload_data['server'],
                'hash': upload_data['hash'],
                'v': VK_API_VERSION
            }
        ).json()
        items = resp.get('response', [])
        if items:
            owner_id = items[0]['owner_id']
            photo_id = items[0]['id']
            return f"photo{owner_id}_{photo_id}"
        return None

    async def download_telegram_photo(self, bot, file_id: str) -> Optional[str]:
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        url = f"{TELEGRAM_FILE_BASE}{config.API_TOKEN}/{file_path}"
        local_path = f"temp_{file_id}.jpg"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(local_path, 'wb') as f:
                        f.write(await resp.read())
                    return local_path
        return None
