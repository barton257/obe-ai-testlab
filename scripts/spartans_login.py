"""交互式登录换 token（斯巴达 Testnet）。

Testnet 登录流程（爬自前端 JS 2026-08-17）：
    1. POST /api/login/check     → 查询用户绑定的第二因素
    2. POST /api/code/send       → 发邮箱 OTP（触发 6 位验证码到邮箱）
    3. POST /api/login           → 提交 email + password + emailCode → 返回 JWT

用法：
    # 交互模式：提示输入邮箱、密码、OTP，成功后写入 .env.local
    python scripts/spartans_login.py --user USER2

    # 打印 token 不写文件
    python scripts/spartans_login.py --email kakarotto2613@163.com --password 12345678 --print

支持的 --user 别名：USER1 / USER2 / USER3 / BOT1 / BOT2
（读取 .env.local 中对应的 EMAIL/PASSWORD，避免明文入命令行历史）

⚠️  OTP 验证码需要人肉从邮箱抓取。这是安全设计，脚本无法绕过。
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv, set_key
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

REPO_ROOT = Path(__file__).resolve().parents[1]
ENV_LOCAL = REPO_ROOT / ".env.local"

load_dotenv(ENV_LOCAL)

API_BASE = os.environ.get("SPARTANS_API_BASE", "https://bullapitest.1bullex.com")
FRONTEND_BASE = os.environ.get("SPARTANS_FRONTEND_BASE", "https://testnet.1bullex.com")
IDENTIFY = os.environ.get("AUTH_IDENTIFY", "50fef74bea1e07a867d8760f0e")


def _headers() -> dict[str, str]:
    return {
        "accept": "application/json",
        "accept-language": "zh-CN",
        "content-type": "application/json",
        "origin": FRONTEND_BASE,
        "referer": FRONTEND_BASE + "/zh-cn/login",
        "platform": "WEB",
        "x-client-version": "1.0.0",
        "identify": IDENTIFY,
    }


_session: requests.Session | None = None


def _get_session() -> requests.Session:
    global _session
    if _session is None:
        s = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1.0,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["POST", "GET"],
        )
        s.mount("https://", HTTPAdapter(max_retries=retry))
        _session = s
    return _session


def _post(path: str, body: dict) -> dict:
    # 本地代理/网络偶发 SSL EOF，最多重试 3 次
    last_err: Exception | None = None
    for _ in range(3):
        try:
            r = _get_session().post(
                API_BASE + path, headers=_headers(), json=body, timeout=15,
            )
            r.raise_for_status()
            return r.json()
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            last_err = e
    raise RuntimeError(f"POST {path} 反复失败: {last_err}")


def check_bindings(email: str) -> dict:
    resp = _post("/api/login/check", {"email": email})
    if resp.get("code") != 0:
        raise RuntimeError(f"login/check failed: {resp}")
    return resp["data"]


def send_email_code(email: str) -> None:
    resp = _post("/api/code/send", {"email": email, "action": "login"})
    if resp.get("code") != 0:
        raise RuntimeError(f"code/send failed: {resp}")


def do_login(email: str, password: str, email_code: str) -> dict:
    """成功返回包含 token 的 data。

    字段名和完整 body 来自前端反爬：/api/login 需要完整 shape，
    OTP 字段名是 `code` 而非 `emailCode`。
    """
    resp = _post("/api/login", {
        "areaCode": "",
        "code": email_code,
        "country": "",
        "currency": "",
        "email": email,
        "googleCode": "",
        "mobile": "",
        "password": password,
        "invitationCode": "",
        "webHash": "",
    })
    if resp.get("code") != 0:
        raise RuntimeError(f"login failed: {resp.get('msg')} — {resp}")
    return resp["data"]


def resolve_creds(user_alias: str | None, email: str | None, password: str | None) -> tuple[str, str]:
    if user_alias:
        e = os.environ.get(f"{user_alias}_EMAIL")
        p = os.environ.get(f"{user_alias}_PASSWORD")
        if not e or not p:
            raise SystemExit(f"{user_alias}_EMAIL / {user_alias}_PASSWORD 未在 .env.local 中设置")
        return e, p
    if not email:
        email = input("邮箱: ").strip()
    if not password:
        password = getpass.getpass("密码: ")
    return email, password


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", help="别名（USER1/USER2/USER3/BOT1/BOT2），从 .env.local 读凭证")
    ap.add_argument("--email")
    ap.add_argument("--password")
    ap.add_argument("--otp", help="邮箱验证码；不传则交互输入")
    ap.add_argument("--print", dest="print_only", action="store_true",
                    help="只打印 token 不写入 .env.local")
    ap.add_argument("--key", default="AUTH_TOKEN",
                    help="写入 .env.local 的 key，默认覆盖 AUTH_TOKEN；例：USER2_AUTH_TOKEN")
    args = ap.parse_args()

    email, password = resolve_creds(args.user, args.email, args.password)

    print(f"→ 查询 {email} 绑定情况...", file=sys.stderr)
    bindings = check_bindings(email)
    print(f"  Google={bindings['isGoogleBind']} Email={bindings['isEmailBind']} "
          f"Mobile={bindings['isMobileBind']} Passkey={bindings['isPasskeyBind']}", file=sys.stderr)

    if bindings["isGoogleBind"]:
        print("⚠️  账号绑定了 Google Authenticator。本脚本目前只支持邮箱 OTP。", file=sys.stderr)
        print("   在 web 上把 2FA 切换为邮箱验证码后重试。", file=sys.stderr)
        return 2

    if not bindings["isEmailBind"]:
        print("⚠️  账号未绑定邮箱 OTP，无法自动登录。", file=sys.stderr)
        return 2

    print(f"→ 发送邮箱验证码到 {email}...", file=sys.stderr)
    send_email_code(email)
    print("  ✓ 已发送。请到邮箱查收 6 位数字验证码。", file=sys.stderr)

    otp = args.otp or input("验证码: ").strip()

    print("→ 提交登录...", file=sys.stderr)
    data = do_login(email, password, otp)

    token = data.get("token") or data.get("access_token") or data.get("authToken")
    if not token:
        print(f"⚠️  未能在响应中定位 token 字段。完整响应：\n{json.dumps(data, ensure_ascii=False, indent=2)}",
              file=sys.stderr)
        return 3
    # 服务端返回 "Bearer <jwt>"，去掉前缀只保留 JWT 本体
    if token.startswith("Bearer "):
        token = token[len("Bearer "):]

    uid = (data.get("info") or {}).get("UUID")
    if uid:
        print(f"  用户 UID: {uid}", file=sys.stderr)

    if args.print_only:
        print(token)
    else:
        ENV_LOCAL.touch(exist_ok=True)
        set_key(str(ENV_LOCAL), args.key, token, quote_mode="never")
        print(f"✓ token 已写入 {ENV_LOCAL} 的 {args.key}", file=sys.stderr)
        print(f"  token 前 40 字符: {token[:40]}...", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
