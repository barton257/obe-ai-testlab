"""SPARTANS API smoke 测试 + 订阅→赎回端到端。

testcases:
  - projects/spartans/testcases/spartans-subscribe-P0-正常-最小订阅金额.yaml
  - projects/spartans/testcases/spartans-subscribe-P0-异常-金额为零.yaml  (待补)

环境变量来自 .env.local（运行前 `source .env.local` 或通过 pytest-dotenv 加载）。

批次窗口：Testnet=10 分钟，用 SPARTANS_BATCH_WINDOW_SECS 覆盖（默认 660 = 11 min）。
"""
import os
import time

import pytest
from dotenv import load_dotenv

from automation.clients.obe_http import ObeApiError, ObeClient
from projects.spartans.tests.api.client import SpartansClient

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../../../.env.local"))

USER1_ID = os.environ.get("USER1_UID", "10732164")
BOT_ID = int(os.environ.get("BOT1_ID", "1342"))
BOT_ALIAS = "Kakarotto"
# 下单最小额度；生产测试时可通过环境变量改为其他值
SUBSCRIBE_MIN = float(os.environ.get("SPARTANS_TEST_MIN_AMOUNT", "1"))
SUBSCRIBE_MAX = float(os.environ.get("SPARTANS_TEST_MAX_AMOUNT", "10"))
BATCH_WINDOW = int(os.environ.get("SPARTANS_BATCH_WINDOW_SECS", "660"))


@pytest.fixture(scope="module")
def client() -> SpartansClient:
    return SpartansClient(ObeClient.from_env())


# ── 只读 smoke ────────────────────────────────────────────────────────────────

class TestSmokeReadOnly:
    def test_bot_summary(self, client):
        data = client.bot_summary()["data"]
        assert data["totalSubscribers"] >= 0
        assert data["totalNav"] >= 0

    def test_bot_list_returns_bots(self, client):
        data = client.bot_list(limit=5)["data"]
        assert data["total"] > 0
        assert len(data["bots"]) > 0
        first = data["bots"][0]
        assert "id" in first and "nameAlias" in first

    def test_bot_detail_kakarotto(self, client):
        data = client.bot_detail(BOT_ALIAS)["data"]
        assert data["nameAlias"] == BOT_ALIAS
        assert data["status"] == "Running"
        assert "profitShareRatio" in data
        assert "aum" in data and data["aum"] >= 0

    def test_user_summary_fields(self, client):
        data = client.user_summary()["data"]
        assert "total" in data
        assert "availableBalance" in data
        assert data["total"] >= 0

    def test_user_board_distributions(self, client):
        data = client.user_board()["data"]
        assert "distributions" in data
        total_rate = sum(d["rate"] for d in data["distributions"])
        assert abs(total_rate - 1.0) < 0.01, f"distribution rates should sum to ~1, got {total_rate}"

    def test_invest_history_pagination(self, client):
        resp = client.invest_history(USER1_ID, page=1, limit=5)
        data = resp["data"]
        assert "total" in data
        assert "bots" in data
        assert len(data["bots"]) <= 5


# ── 边界/异常分支（不改变账户状态）──────────────────────────────────────────

class TestPurchaseErrorBranches:
    def test_purchase_amount_zero_rejected(self, client):
        with pytest.raises(ObeApiError) as exc:
            client.purchase(USER1_ID, BOT_ID, 0)
        assert exc.value.msg == "amount_not_allowed"

    def test_purchase_no_balance_rejected(self, client):
        """金额远超余额时服务端拒绝。"""
        with pytest.raises(ObeApiError) as exc:
            client.purchase(USER1_ID, BOT_ID, 999_999_999)
        assert exc.value.msg == "balance_not_enough"

    def test_purchase_without_auth_rejected(self, client):
        """无 token 请求应返回 401。"""
        from automation.clients.obe_http import ObeClient as _C
        unauth = SpartansClient(_C(
            base_url=os.environ["SPARTANS_API_BASE"], token="invalid",
        ))
        with pytest.raises(ObeApiError) as exc:
            unauth.purchase(USER1_ID, BOT_ID, 1)
        assert exc.value.code == 401


# ── 端到端：最小额度订阅 → 等批次 → 赎回 ────────────────────────────────────

@pytest.mark.e2e
@pytest.mark.slow
class TestSubscribeRedeemE2E:
    """完整链路测试，需要等批次窗口（约 10 min），跑时加 -m e2e 标记。"""

    def test_purchase_min_amount(self, client):
        resp = client.purchase(USER1_ID, BOT_ID, SUBSCRIBE_MIN)
        assert resp.get("code", 0) == 0
        assert resp.get("msg") == "success"

    def test_purchase_appears_in_history(self, client):
        history = client.invest_history(USER1_ID, limit=1)["data"]["bots"]
        assert len(history) >= 1
        latest = history[0]
        assert latest["botId"] == BOT_ID
        assert latest["tradeType"] == "Purchase"

    @pytest.mark.skipif(
        os.environ.get("SKIP_BATCH_WAIT") == "1",
        reason="SKIP_BATCH_WAIT=1 跳过等待",
    )
    def test_wait_for_batch(self):
        """等批次窗口完成，share 铸造后才能赎回。"""
        print(f"\n等待批次处理，最长 {BATCH_WINDOW}s ...")
        time.sleep(BATCH_WINDOW)

    def test_redeem_min_amount(self, client):
        resp = client.redeem(USER1_ID, BOT_ID, SUBSCRIBE_MIN)
        assert resp.get("msg") == "success"

    def test_redeem_appears_in_history(self, client):
        history = client.invest_history(USER1_ID, limit=1)["data"]["bots"]
        assert history[0]["tradeType"] == "Redeem"
        assert history[0]["botId"] == BOT_ID
