"""根级 conftest：加载 .env.local，让所有 pytest 都能通过 os.environ 拿凭证。"""
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env.local"))
