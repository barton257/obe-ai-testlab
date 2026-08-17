"""OBE 通用 HTTP 底座。

跨业务共享的 session 管理、header 注入、业务错误码转异常。
业务专属端点封装放在 projects/<业务>/tests/api/client.py。
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests


class ObeApiError(RuntimeError):
    """业务返回 code != 0 时抛出。HTTP 层错误保留原 requests 异常。"""

    def __init__(self, code: int, msg: str, path: str, payload: Any = None):
        self.code = code
        self.msg = msg
        self.path = path
        self.payload = payload
        super().__init__(f"[{code}] {msg} @ {path}")


@dataclass
class ObeClient:
    base_url: str
    token: str
    identify: str = ""
    platform: str = "WEB"
    client_version: str = "1.0.0"
    frontend_origin: str = ""
    timeout: float = 15.0

    def __post_init__(self) -> None:
        self._s = requests.Session()
        self._s.headers.update({
            "authorization": f"Bearer {self.token}",
            "identify": self.identify,
            "platform": self.platform,
            "x-client-version": self.client_version,
            "accept": "application/json",
            "accept-language": "zh-CN",
            "content-type": "application/json",
        })
        if self.frontend_origin:
            self._s.headers.update({
                "origin": self.frontend_origin,
                "referer": self.frontend_origin + "/",
            })

    @classmethod
    def from_env(cls) -> "ObeClient":
        return cls(
            base_url=os.environ["SPARTANS_API_BASE"],
            token=os.environ["AUTH_TOKEN"],
            identify=os.environ.get("AUTH_IDENTIFY", ""),
            frontend_origin=os.environ.get("SPARTANS_FRONTEND_BASE", ""),
        )

    def request(self, method: str, path: str, *, json: dict | None = None) -> dict:
        url = self.base_url.rstrip("/") + path
        r = self._s.request(method, url, json=json, timeout=self.timeout)
        r.raise_for_status()
        body = r.json()
        if isinstance(body, dict) and body.get("code") not in (0, None):
            raise ObeApiError(body.get("code"), body.get("msg", ""), path, body)
        return body

    def get(self, path: str) -> dict:
        return self.request("GET", path)

    def post(self, path: str, json: dict | None = None) -> dict:
        return self.request("POST", path, json=json or {})
