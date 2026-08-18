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
# Tier 上限基线，与 tests/fixtures/tier_config.yaml 的 max_subscribe 对齐
SUBSCRIBE_TIER_MAX = float(os.environ.get("SPARTANS_TEST_TIER_MAX", "100000000"))
BATCH_WINDOW = int(os.environ.get("SPARTANS_BATCH_WINDOW_SECS", "660"))


@pytest.fixture(scope="module")
def client() -> SpartansClient:
    return SpartansClient(ObeClient.from_env())


# 动账用例专用：走 FUNDS 账户，避免污染 User1 并便于资金台账对账
FUNDS_MIN_BALANCE = float(os.environ.get("FUNDS_MIN_BALANCE", "50"))


@pytest.fixture(scope="module")
def funds_client() -> SpartansClient:
    """专用资金账户客户端（UID 见 .env.local 的 FUNDS_UID）。

    余额低于阈值直接 skip，而不是跑到一半失败 —— 失败原因会指向业务断言，
    掩盖"其实是没钱了"这个真实原因。

    ⚠️ 用本 fixture 的用例都会真实动账，跑完必须同步台账：
        python scripts/spartans_funds_ledger.py sync
    """
    token = os.environ.get("FUNDS_AUTH_TOKEN")
    if not token:
        pytest.skip("FUNDS_AUTH_TOKEN 未配置，见 projects/spartans/funds/README.md")

    c = SpartansClient(ObeClient(
        base_url=os.environ["SPARTANS_API_BASE"],
        token=token,
        identify=os.environ.get("AUTH_IDENTIFY", ""),
        frontend_origin=os.environ.get("SPARTANS_FRONTEND_BASE", ""),
    ))
    avail = float(c.user_summary()["data"]["availableBalance"])
    if avail < FUNDS_MIN_BALANCE:
        pytest.skip(
            f"资金账户余额不足：{avail} < {FUNDS_MIN_BALANCE} USDT，需补充后再跑"
        )
    return c


@pytest.fixture(scope="module")
def funds_uid() -> str:
    uid = os.environ.get("FUNDS_UID")
    if not uid:
        pytest.skip("FUNDS_UID 未配置")
    return uid


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
        # 不写死 Running：bot 在批次结算窗口内会短暂变 Settling，属正常状态机。
        # 2026-08-18 实测该用例因此偶发失败（断言 Running 但实际 Settling）。
        assert data["status"] in ("Running", "Settling"), (
            f"bot 状态异常: {data['status']}"
        )
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

    def test_purchase_negative_amount_rejected(self, client):
        """负数金额应被拒绝（不应穿透成"反向充值"）。"""
        with pytest.raises(ObeApiError) as exc:
            client.purchase(USER1_ID, BOT_ID, -1)
        assert exc.value.msg in ("amount_not_allowed", "amount_below_min")


# ── 已知缺陷的回归用例（xfail strict：后端修复后自动转红提醒摘标记）──────────
#
# 三条 bug 报告见 ../../bugs/2026-08-17-spartans-S{2,2,3}-*.md
# strict=True 的含义：修复后用例意外通过 → pytest 报 XPASS 失败，
# 强制我们回来删掉标记，避免缺陷修复后回归用例长期躺在 xfail 里没人管。

class TestKnownDefectRegressions:
    @pytest.mark.writes_funds
    @pytest.mark.xfail(
        strict=True,
        reason="S2 订阅金额穿透：0<amount<min 静默通过，见 bugs/2026-08-17-spartans-S2-订阅金额小于最小值未拦截.md",
    )
    def test_purchase_below_min_rejected(self, client):
        """低于 Tier 最小值（1 USDT）应拒绝，当前穿透。

        标 writes_funds：穿透期间这条会真实下单 0.5 USDT。
        """
        with pytest.raises(ObeApiError) as exc:
            client.purchase(USER1_ID, BOT_ID, 0.5)
        assert exc.value.msg in ("amount_below_min", "amount_not_allowed")

    @pytest.mark.writes_funds
    @pytest.mark.xfail(
        strict=True,
        reason="S2 赎回静默截断：settleAmount 超权益时截断而非拒绝，见 bugs/2026-08-17-spartans-S2-赎回金额超权益静默截断.md",
    )
    def test_redeem_exceeds_equity_rejected(self, client):
        """赎回金额远超权益应拒绝，当前静默截断到实际权益。

        标 writes_funds：截断期间这条会真实赎回全部权益。
        """
        with pytest.raises(ObeApiError) as exc:
            client.redeem(USER1_ID, BOT_ID, 999_999_999)
        assert exc.value.msg == "settle_amount_exceeds_equity"

    @pytest.mark.writes_funds
    @pytest.mark.xfail(
        strict=True,
        reason="S3 body.userId 与 JWT 不一致时静默忽略而非拒绝，见 bugs/2026-08-17-spartans-S3-userId与JWT不匹配未拦截.md",
    )
    def test_purchase_wrong_user_id_rejected(self, client):
        """body.userId != JWT.api 应显式拒绝，当前静默按 JWT 用户下单。

        标 writes_funds：静默忽略期间这条会以 JWT 用户（User1）真实下单 1 USDT。
        """
        other_uid = os.environ.get("USER2_UID", "10732177")
        with pytest.raises(ObeApiError) as exc:
            client.purchase(other_uid, BOT_ID, SUBSCRIBE_MIN)
        assert exc.value.msg == "identity_mismatch"


# ── 金额边界正向用例（会真实下单，默认不跑）────────────────────────────────

@pytest.mark.writes_funds
class TestPurchaseAmountBoundaries:
    """Tier 边界的正向验证。

    基线来自 tests/fixtures/tier_config.yaml：min_subscribe=1, max_subscribe=100000000。
    """

    def test_purchase_equal_min_accepted(self, client):
        """恰好等于最小值应通过。"""
        resp = client.purchase(USER1_ID, BOT_ID, SUBSCRIBE_MIN)
        assert resp.get("msg") == "success"

    def test_purchase_above_max_rejected(self, client):
        """超过 Tier 最大值应拒绝。

        ⚠️ 当前账户无法把 max 和余额两个约束分开验证：
        tier_config 的 max_subscribe=100000000，而测试账户可用余额约 9.5k，
        任何 > max 的金额必然先撞 balance_not_enough，测不到 max 校验本身。
        因此这里只断言"被拒绝"，不断言具体错误码；
        真正验证 max 需要一个余额 > max 的账户，或后端提供可配置的低 max Tier。
        见 roadmap P1 待办。
        """
        over_max = SUBSCRIBE_TIER_MAX + 1
        with pytest.raises(ObeApiError) as exc:
            client.purchase(USER1_ID, BOT_ID, over_max)
        assert exc.value.code != 0


# ── 端到端：最小额度订阅 → 等批次 → 赎回 ────────────────────────────────────

@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.writes_funds
class TestSubscribeRedeemE2E:
    """完整链路测试，需要等批次窗口（约 10 min）。

    ⚠️ 会真实下单扣款，故加 writes_funds 标记。
    2026-08-18 教训：本类原先只有 e2e/slow 标记，裸跑 `pytest` 会直接下单，
    实测误扣 1 USDT（记录 #1828）且因中途打断没走到 redeem，钱留在 bot 里。

    正确跑法：pytest projects/spartans/tests/api/test_spartans_api.py -m writes_funds -v
    """

    def test_purchase_min_amount(self, funds_client, funds_uid):
        resp = funds_client.purchase(funds_uid, BOT_ID, SUBSCRIBE_MIN)
        assert resp.get("code", 0) == 0
        assert resp.get("msg") == "success"

    def test_purchase_appears_in_history(self, funds_client, funds_uid):
        history = funds_client.invest_history(funds_uid, limit=1)["data"]["bots"]
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

    def test_redeem_min_amount(self, funds_client, funds_uid):
        resp = funds_client.redeem(funds_uid, BOT_ID, SUBSCRIBE_MIN)
        assert resp.get("msg") == "success"

    def test_redeem_appears_in_history(self, funds_client, funds_uid):
        history = funds_client.invest_history(funds_uid, limit=1)["data"]["bots"]
        assert history[0]["tradeType"] == "Redeem"
        assert history[0]["botId"] == BOT_ID
