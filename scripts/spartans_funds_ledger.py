"""专用资金账户台账维护工具。

记录 FUNDS 账户（UID 见 .env.local 的 FUNDS_UID）的全部资金变动。

三个子命令：
    sync    从 invest/history 拉订阅/赎回记录，按 ref_id 去重后追加到台账
    add     手工补录一笔（划转/开平仓/分润/各类费用/资金费率）
    verify  用台账累计额与接口实际余额对账

⚠️ 采集边界：invest/history 只返回订阅与赎回。划转、开平仓、分润、手续费、
   平台使用费、资金费率均无可用接口（2026-08-18 已探测多个路径全 404），
   必须用 add 手工补录。详见 projects/spartans/funds/README.md。

台账双写 LEDGER.md（人读）和 ledger.csv（机读），两者必须一致。
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
load_dotenv(REPO_ROOT / ".env.local")

from automation.clients.obe_http import ObeClient  # noqa: E402
from projects.spartans.tests.api.client import SpartansClient  # noqa: E402

FUNDS_DIR = REPO_ROOT / "projects" / "spartans" / "funds"
CSV_PATH = FUNDS_DIR / "ledger.csv"
MD_PATH = FUNDS_DIR / "LEDGER.md"

COLUMNS = [
    "time", "type", "amount", "currency", "from", "to",
    "fee_type", "ref_id", "bot", "balance_after", "source", "note",
]

# invest/history 的 tradeType → 台账 type 与资金流向
TRADE_TYPE_MAP = {
    "Purchase": ("subscribe", "available_balance", "bot"),
    "Redeem": ("redeem", "bot", "available_balance"),
}


def _client() -> SpartansClient:
    token = os.environ.get("FUNDS_AUTH_TOKEN")
    if not token:
        raise SystemExit(
            "FUNDS_AUTH_TOKEN 未设置。先刷新 token：\n"
            "  python scripts/spartans_login.py --user FUNDS --otp 123456 --key FUNDS_AUTH_TOKEN"
        )
    return SpartansClient(ObeClient(
        base_url=os.environ["SPARTANS_API_BASE"],
        token=token,
        identify=os.environ.get("AUTH_IDENTIFY", ""),
        frontend_origin=os.environ.get("SPARTANS_FRONTEND_BASE", ""),
    ))


def _funds_uid() -> str:
    uid = os.environ.get("FUNDS_UID")
    if not uid:
        raise SystemExit("FUNDS_UID 未在 .env.local 设置")
    return uid


def read_rows() -> list[dict]:
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_rows(rows: list[dict]) -> None:
    """按时间正序写回 CSV，并重新渲染 Markdown。"""
    rows = sorted(rows, key=lambda r: (r.get("time", ""), str(r.get("ref_id", ""))))
    FUNDS_DIR.mkdir(parents=True, exist_ok=True)

    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLUMNS})

    _render_md(rows)


def _render_md(rows: list[dict]) -> None:
    total = sum(float(r["amount"]) for r in rows if r.get("amount"))
    subs = sum(float(r["amount"]) for r in rows if r.get("type") == "subscribe")
    reds = sum(float(r["amount"]) for r in rows if r.get("type") == "redeem")
    fees = sum(float(r["amount"]) for r in rows
               if r.get("fee_type") or r.get("type", "").startswith("fee_"))
    manual = sum(1 for r in rows if r.get("source") == "manual")

    lines = [
        "# 专用资金账户台账",
        "",
        "> 本文件由 `scripts/spartans_funds_ledger.py` 生成，**不要手改**。",
        "> 补录用 `add` 子命令，字段定义与采集边界见 [`README.md`](README.md)。",
        "",
        f"- 账户 UID：`{os.environ.get('FUNDS_UID', '10732178')}`",
        "- 初始入金：**1000 USDT**（2026-08-18 开户基线）",
        f"- 记录笔数：**{len(rows)}**（其中手工补录 {manual} 笔）",
        f"- 资金净变动：**{total:+.8f} USDT**",
        f"- 理论余额：**{1000 + total:.8f} USDT**",
        "",
        "| 项 | 金额 (USDT) |",
        "|---|---:|",
        f"| 订阅流出 | {subs:+.8f} |",
        f"| 赎回流入 | {reds:+.8f} |",
        f"| 各类费用 | {fees:+.8f} |",
        f"| **合计** | **{total:+.8f}** |",
        "",
        "## 明细（时间倒序）",
        "",
        "| 时间 | 类型 | 金额 | 从 | 到 | 费种 | 单号 | 机器人 | 余额 | 来源 | 备注 |",
        "|---|---|---:|---|---|---|---|---|---:|---|---|",
    ]
    for r in reversed(rows):
        amt = f"{float(r['amount']):+.8f}" if r.get("amount") else ""
        lines.append(
            f"| {r.get('time','')} | `{r.get('type','')}` | {amt} | "
            f"{r.get('from','')} | {r.get('to','')} | {r.get('fee_type','') or '—'} | "
            f"{r.get('ref_id','') or '—'} | {r.get('bot','') or '—'} | "
            f"{r.get('balance_after','') or '—'} | {r.get('source','')} | {r.get('note','')} |"
        )

    lines += [
        "",
        "## 采集缺口",
        "",
        "`invest/history` 只覆盖订阅与赎回。以下类型无可用接口，需 `add` 手工补录：",
        "",
        "划转 · 开仓 · 平仓 · 分润 · 手续费 · 平台使用费 · 资金费率",
        "",
        "若后端提供了钱包流水接口，请补进采集器 —— 这是台账当前最大的缺口。",
        "",
    ]
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def cmd_sync(args: argparse.Namespace) -> int:
    c, uid = _client(), _funds_uid()
    rows = read_rows()
    known = {str(r.get("ref_id")) for r in rows if r.get("ref_id")}

    resp = c.invest_history(uid, page=1, limit=args.limit)["data"]
    fetched = resp.get("bots") or []
    print(f"接口返回 {resp.get('total')} 笔，本次取 {len(fetched)} 笔")

    added = 0
    for b in fetched:
        ref = str(b.get("id"))
        if ref in known:
            continue
        tt = b.get("tradeType")
        if tt not in TRADE_TYPE_MAP:
            print(f"  ⚠️ 跳过未知 tradeType={tt}（#{ref}），请手工补录")
            continue

        kind, src, dst = TRADE_TYPE_MAP[tt]
        bot = b.get("botAlias") or b.get("botName") or ""
        amt = float(b.get("tradeAmount") or 0)
        # 站在可用余额视角：订阅为负，赎回为正
        signed = -amt if kind == "subscribe" else amt
        ts = b.get("createdAt")
        when = (datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")
                if ts else "")

        rows.append({
            "time": when,
            "type": kind,
            "amount": f"{signed:.8f}",
            "currency": "USDT",
            "from": f"bot:{bot}" if src == "bot" else src,
            "to": f"bot:{bot}" if dst == "bot" else dst,
            "fee_type": "",
            "ref_id": ref,
            "bot": bot,
            "balance_after": "",
            "source": "api",
            "note": f"status={b.get('status')} units={b.get('tradeUnits')}",
        })
        known.add(ref)
        added += 1
        print(f"  + #{ref} {kind} {signed:+.8f} {bot}")

    if added:
        write_rows(rows)
        print(f"\n✓ 新增 {added} 笔，台账共 {len(rows)} 笔")
    else:
        print("\n无新增记录")

    if resp.get("total", 0) > len(fetched):
        print(f"⚠️ 接口共 {resp['total']} 笔但只取了 {len(fetched)} 笔，"
              f"用 --limit 调大以覆盖全部历史")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    rows = read_rows()
    when = args.time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows.append({
        "time": when,
        "type": args.type,
        "amount": f"{args.amount:.8f}",
        "currency": args.currency,
        "from": args.frm,
        "to": args.to,
        "fee_type": args.fee_type or "",
        "ref_id": args.ref_id or "",
        "bot": args.bot or "",
        "balance_after": args.balance_after or "",
        "source": "manual",
        "note": args.note or "",
    })
    write_rows(rows)
    print(f"✓ 已补录：{when} {args.type} {args.amount:+.8f} {args.currency}")
    print(f"  台账共 {len(rows)} 笔")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    c = _client()
    rows = read_rows()
    total = sum(float(r["amount"]) for r in rows if r.get("amount"))
    expected = args.initial + total

    s = c.user_summary()["data"]
    actual = float(s.get("availableBalance"))

    print(f"初始入金      : {args.initial:.8f}")
    print(f"台账净变动    : {total:+.8f}  ({len(rows)} 笔)")
    print(f"理论可用余额  : {expected:.8f}")
    print(f"接口可用余额  : {actual:.8f}")
    diff = actual - expected
    print(f"差额          : {diff:+.8f}")

    if abs(diff) < 1e-6:
        print("\n✓ 对平")
        return 0

    print("\n⚠️ 不平。可能原因（按概率排序）：")
    print("  1. 有未采集的费用类记录（分润/手续费/平台费/资金费率）—— 用 add 补录")
    print("  2. 有订阅仍在批次处理中（status != Finished），资金已扣但份额未铸")
    print("  3. 发生了台账未覆盖的划转或开平仓")
    print("  不要直接改数字凑平；先定位原因，再补录冲正记录。")

    board = c.user_board()["data"]
    print(f"\n参考：user_board rpnl={board.get('rpnl')} upnl={board.get('upnl')} "
          f"subscription={board.get('subscription')}")
    print("（rpnl/upnl 只有总量快照，没有逐笔明细，仅供判断差额来源）")
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("sync", help="从 invest/history 同步订阅/赎回")
    p.add_argument("--limit", type=int, default=100, help="拉取条数，默认 100")
    p.set_defaults(func=cmd_sync)

    p = sub.add_parser("add", help="手工补录一笔资金变动")
    p.add_argument("--type", required=True, help=(
        "subscribe/redeem/transfer/open_position/close_position/pnl_realized/"
        "profit_share/fee_trading/fee_platform/funding_rate/other"))
    p.add_argument("--amount", type=float, required=True,
                   help="带符号：账户资金减少为负，增加为正")
    p.add_argument("--currency", default="USDT")
    p.add_argument("--from", dest="frm", required=True,
                   help="资金来源，如 available_balance / bot:Kakarotto / external")
    p.add_argument("--to", required=True, help="资金去向，同 --from 取值")
    p.add_argument("--fee-type", dest="fee_type",
                   help="费种：trading/platform/funding/profit_share")
    p.add_argument("--ref-id", dest="ref_id", help="关联单号")
    p.add_argument("--bot", help="相关机器人 alias")
    p.add_argument("--balance-after", dest="balance_after", help="该笔后的可用余额")
    p.add_argument("--time", help="变动时间 YYYY-MM-DD HH:MM:SS，默认当前")
    p.add_argument("--note", help="备注；测试产生的请写明用例名")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("verify", help="台账与接口余额对账")
    p.add_argument("--initial", type=float, default=1000.0, help="初始入金，默认 1000")
    p.set_defaults(func=cmd_verify)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
