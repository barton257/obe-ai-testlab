"""验证 Bug S1（赎回超权益穿透）严重级别。

思路：
    1. 用户当前的资产快照（钱包 + 各 bot 权益）
    2. 调 redeem 传 settleAmount=999_999_999
    3. 立即查 history，看新记录 status
    4. 等一个批次窗口
    5. 再查 history + user_summary，看是否真扣款

结论：
    - 批次后 status=Failed / Cancel，资金无变化 → S1 降级 S2（前置无校验但异步兜底）
    - 批次后 status=Finished 且资金真的错动 → S1 坐实，生产阻塞

用法：
    # 用 .env.local 里当前 AUTH_TOKEN（默认 User1 的 token）跑
    python scripts/verify_bug_s1.py

    # 指定 bot 和自定义超额金额
    python scripts/verify_bug_s1.py --bot-id 1342 --settle-amount 999999999

    # 用 User2 的 token（先跑 spartans_login.py --user USER2 --key USER2_AUTH_TOKEN）
    AUTH_TOKEN=$USER2_AUTH_TOKEN python scripts/verify_bug_s1.py --user-id 10732177
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(REPO_ROOT / ".env.local")

sys.path.insert(0, str(REPO_ROOT))

from automation.clients.obe_http import ObeApiError, ObeClient  # noqa: E402
from projects.spartans.tests.api.client import SpartansClient  # noqa: E402


def snapshot(client: SpartansClient, user_id: str, tag: str) -> dict:
    summary = client.user_summary()["data"]
    board = client.user_board()["data"]
    history = client.invest_history(user_id, limit=3)["data"]
    print(f"\n─── {tag} ───")
    print(f"  钱包 avail : {summary['availableBalance']}")
    print(f"  资产 total : {summary['total']}")
    print(f"  最新 history:")
    for h in history["bots"][:3]:
        print(f"    #{h['id']} {h['tradeType']:8s} {h['status']:8s} "
              f"amt={h['tradeAmount']} units={h['tradeUnits']} bot={h['botAlias']}")
    return {"summary": summary, "history": history}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--user-id", default=os.environ.get("USER1_UID", "10732164"))
    ap.add_argument("--bot-id", type=int, default=1342)
    ap.add_argument("--settle-amount", type=float, default=999_999_999)
    ap.add_argument("--wait", type=int, default=660,
                    help="批次等待秒数，默认 660 (Testnet 10min + buffer)")
    ap.add_argument("--skip-wait", action="store_true", help="不等批次，只跑同步阶段")
    args = ap.parse_args()

    client = SpartansClient(ObeClient.from_env())
    user_id = args.user_id

    pre = snapshot(client, user_id, "BEFORE redeem")

    print(f"\n→ 调用 redeem(userId={user_id}, botId={args.bot_id}, settleAmount={args.settle_amount})")
    try:
        resp = client.redeem(user_id, args.bot_id, args.settle_amount)
        print(f"  服务端同步响应: code=0 msg={resp.get('msg')!r}")
    except ObeApiError as e:
        print(f"  ✓ 被同步拒绝: code={e.code} msg={e.msg}")
        print("\n结论：前置校验存在，S1 降级 S3（接口不算严重 bug）")
        return 0

    print("→ 立即查询 history...")
    post_sync = snapshot(client, user_id, "AFTER redeem (SYNC)")

    if args.skip_wait:
        print("\n[--skip-wait] 跳过批次等待。稍后再手动跑一次比较 history。")
        return 0

    print(f"\n→ 等待批次窗口 {args.wait}s ...")
    for i in range(args.wait, 0, -30):
        time.sleep(min(30, i))
        print(f"  剩余 {max(0, i-30)}s ...", flush=True)

    post_batch = snapshot(client, user_id, "AFTER batch")

    # 结论判定
    before_avail = pre["summary"]["availableBalance"]
    after_avail = post_batch["summary"]["availableBalance"]
    delta = after_avail - before_avail

    print("\n─── 结论 ───")
    print(f"  钱包 availableBalance 变动: {delta:+.4f}")

    latest = post_batch["history"]["bots"][0]
    print(f"  最新 history #{latest['id']}: status={latest['status']} "
          f"amt={latest['tradeAmount']} units={latest['tradeUnits']}")

    if latest["status"] == "Failed" or latest["status"] == "Cancel":
        print("\n判定：批次异步兜底拒绝了超额赎回")
        print("      → S1 可降级 S2/S3（前置无校验，但资金安全）")
    elif latest["tradeAmount"] > pre["summary"]["total"] * 2:
        print("\n判定：⚠️ 批次结算了超额金额，可能造成资金错动")
        print("      → S1 坐实！生产阻塞级别")
    else:
        print("\n判定：批次按用户实际权益结算了（截断了金额）")
        print("      → S1 降级 S3（接口设计不严谨但资金安全）")

    print(f"\n完整 history 详情：{json.dumps(latest, ensure_ascii=False, indent=2)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
