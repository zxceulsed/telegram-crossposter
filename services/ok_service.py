# src/services/ok_service.py

import requests
import json
from typing import List
from src.utils.signature import generate_sig

OK_API_BASE = 'https://api.ok.ru'

class OKService:
    def __init__(self, app_key: str, session_key: str, access_token: str, group_id: str):
        self.app_key = app_key
        self.session_key = session_key
        self.access_token = access_token
        self.group_id = group_id  # ID группы Одноклассников

    def post_text(self, text: str) -> requests.Response:

        url = f"{OK_API_BASE}/api/mediatopic/post"
        attachment = json.dumps({
            "media": [
                {"type": "text", "text": text}
            ]
        }, ensure_ascii=False)

        params = {
            'application_key': self.app_key,
            'method': 'mediatopic.post',
            'gid': self.group_id,
            'type': 'GROUP_THEME',
            'access_token': self.access_token,
            'attachment': attachment,
            'format': 'json'
        }
        params['sig'] = generate_sig(params, self.session_key)
        return requests.post(url, params=params)

    def get_upload_url(self, count: int = 1) -> dict | None:

        url = f"{OK_API_BASE}/fb.do"
        params = {
            'application_key': self.app_key,
            'method': 'photosV2.getUploadUrl',
            'gid': self.group_id,
            'count': count,
            'access_token': self.access_token,
            'format': 'json'
        }
        params['sig'] = generate_sig(params, self.session_key)
        resp = requests.get(url, params=params)
        return resp.json() if resp.status_code == 200 else None

    def upload_photos(self, upload_url: str, photo_paths: List[str]) -> dict | None:
        files = [(f'pic{i+1}', open(path, 'rb')) for i, path in enumerate(photo_paths)]
        resp = requests.post(upload_url, files=files)
        return resp.json() if resp.status_code == 200 else None

    def post_photos_with_text(self, photo_tokens: List[str], text: str) -> requests.Response:
        url = f"{OK_API_BASE}/api/mediatopic/post"
        attachment = json.dumps({
            "media": [
                {"type": "photo", "list": [{"id": token} for token in photo_tokens]},
                {"type": "text", "text": text}
            ]
        }, ensure_ascii=False)

        params = {
            'application_key': self.app_key,
            'method': 'mediatopic.post',
            'gid': self.group_id,
            'type': 'GROUP_THEME',
            'access_token': self.access_token,
            'attachment': attachment,
            'format': 'json'
        }
        params['sig'] = generate_sig(params, self.session_key)
        return requests.post(url, params=params)