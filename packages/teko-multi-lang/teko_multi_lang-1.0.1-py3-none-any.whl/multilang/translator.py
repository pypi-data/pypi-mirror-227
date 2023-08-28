import logging
import re
import time
import json

import requests
from cachetools import cached, TTLCache

_logger = logging.getLogger(__name__)

translator_url = {
    "dev": "http://multilan.dev.tekoapis.net/api/v1/sources/client",
    "stag": "http://multilan.dev.tekoapis.net/api/v1/sources/client",
    "prod": "http://multilan.dev.tekoapis.net/api/v1/sources/client"
}
catch_ttl = 900


class Translator:
    lang: str
    cache_ttl: int
    codes: dict
    server_url: str
    client_id: int

    def __init__(self, client_id: int, env_mode: str, caching_time: int,  default_lang='en'):
        self.lang = lang
        self.server_url = translator_url.get(env_mode, "dev")
        self.codes = {}
        self.client_id = client_id
        self.lang = default_lang
        try:
            global catch_ttl
            catch_ttl = caching_time
            self.get_codes_from_translator_service()
        except Exception:
            self.get_codes_from_local_files()

    @cached(cache=TTLCache(maxsize=128, ttl=catch_ttl))
    def get_codes_from_translator_service(self):
        print("Get codes from server...")
        try:
            resp: requests.Response = requests.request(
                "GET", self.server_url, params={"client_id": self.client_id}, timeout=0.2)
            if resp.status_code != 200 or (resp.status_code == 200 and resp.json().get('code') != 200):
                _logger.warning(
                    f"Have errors when calling to TRANSLATOR SERVER with response: {resp.text}")
            else:
                self.codes = resp.json().get("data").get("sources")
        except Exception:
            _logger.warning("Have exception when get codes from translator service")

    @cached(cache=TTLCache(maxsize=128, ttl=86400))
    def get_codes_from_local_files(self):
        print("Get codes from local files...")
        try:
            pass
        except Exception:
            return self.codes

    def t(self, code, lang=None, params=None):
        try:
            lang = lang or self.lang
            if not lang:
                return code
            self.get_codes_from_translator_service()
            codes = self.codes.get(lang)
            text = codes.get(code)
            pattern = re.compile('{{[a-zA-Z0-9_-]*}}')
            if params:
                for param in params:
                    if codes.get(param):
                        text = pattern.sub(codes[param], text, 1)
                    else:
                        text = pattern.sub(param, text, 1)
            return text
        except Exception:
            return code

