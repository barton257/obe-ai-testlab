"""SPARTANS 业务接口封装。

依赖 automation/clients/obe_http.py 的通用底座。
签名和参数默认值来自 testnet 前端 JS 与实调结果（2026-08-17 爬取）。

已知坑：
- bot/list 的 orderBy 必须是数组（["totalPnl"] / ["updated_at"]），传字符串会 400
- bot/list 的 tags 必须是字符串（"" 或 "Private"），传数组会 400
- invest/cancel 路径前端写成 "/botapi//v1/invest/cancel"（双斜杠），实际服务是否兼容待验证
"""
from __future__ import annotations

from automation.clients.obe_http import ObeClient


class SpartansClient:
    def __init__(self, http: ObeClient):
        self.http = http

    # ── 机器人 ──
    def bot_list(
        self,
        *,
        page: int = 1,
        limit: int = 10,
        asc: bool = False,
        order_by: list[str] | None = None,
        bot_alias: str = "",
        strategy_type: str = "",
        reserved: bool = False,
        days: int = 7,
        tags: str = "",
    ) -> dict:
        return self.http.post("/botapi/v1/bot/list", {
            "asc": asc,
            "orderBy": order_by or ["updated_at"],
            "page": page,
            "limit": limit,
            "botAlias": bot_alias,
            "strategyType": strategy_type,
            "reserved": reserved,
            "days": days,
            "tags": tags,
        })

    def bot_detail(self, bot_alias: str, *, days: int = 30) -> dict:
        return self.http.post("/botapi/v1/bot/detail", {"botAlias": bot_alias, "days": days})

    def bot_all_concise(self) -> dict:
        return self.http.post("/botapi/v1/bot/all/concise", {})

    def bot_summary(self) -> dict:
        return self.http.get("/botapi/v1/bot/summary")

    def bot_recommend_top3(self) -> dict:
        return self.http.post("/botapi/v1/bot/recommend/top3", {})

    def bot_position_current(self, strategy_id: int, *, page: int = 1, page_size: int = 20) -> dict:
        return self.http.post("/botapi/v1/bot/position/current", {
            "strategyId": strategy_id, "page": page, "pageSize": page_size,
        })

    def bot_trade_history(self, strategy_id: int, *, page: int = 1, page_size: int = 20) -> dict:
        return self.http.post("/botapi/v1/bot/trade/histroy", {
            "strategyId": strategy_id, "page": page, "pageSize": page_size,
        })

    # ── 订阅/赎回 ──
    def purchase(self, user_id: str, bot_id: int, amount: float) -> dict:
        return self.http.post("/botapi/v1/invest/purchase", {
            "userId": str(user_id), "botId": bot_id, "amount": amount,
        })

    def redeem(self, user_id: str, bot_id: int, settle_amount: float) -> dict:
        return self.http.post("/botapi/v1/invest/redeem", {
            "userId": str(user_id), "botId": bot_id, "settleAmount": settle_amount,
        })

    def cancel(self, user_id: str, bot_id: int) -> dict:
        # 前端路径实际是 "/botapi//v1/invest/cancel"，保留双斜杠以贴近前端行为
        return self.http.post("/botapi//v1/invest/cancel", {
            "userId": str(user_id), "botId": bot_id,
        })

    def invest_history(self, user_id: str, *, page: int = 1, limit: int = 10) -> dict:
        return self.http.post("/botapi/v1/invest/history", {
            "page": page, "limit": limit, "userId": str(user_id),
        })

    def user_summary(self) -> dict:
        return self.http.post("/botapi/v1/invest/user/summary", {})

    def user_board(self) -> dict:
        return self.http.get("/botapi/v1/invest/user/board")

    def user_board_linechart(self, days: int = 7) -> dict:
        return self.http.get(f"/botapi/v1/invest/user/board/linechart?days={days}")
