"""骨架示例：斯巴达订阅接口用例。

testcase: projects/spartans/testcases/spartans-subscribe-P0-正常-最小订阅金额.yaml

真实客户端与接口路径待接入。请勿把当前占位当作正式实现。
"""
import os

import pytest


pytestmark = pytest.mark.skip(reason="骨架示例，等待真实客户端与 OpenAPI 接入")


@pytest.fixture
def obe_client():
    # from automation.clients.obe_http import ObeClient
    # return ObeClient(base_url=os.environ["OBE_TESTNET_BASE_URL"], token=os.environ["OBE_TOKEN"])
    raise NotImplementedError


def test_subscribe_min_amount_happy_path(obe_client):
    bot_name = "OBE-Jason"
    amount = os.environ.get("SPARTANS_MIN_SUBSCRIBE_AMOUNT", "10")

    resp = obe_client.post(
        f"/api/spartans/bots/{bot_name}/subscribe",
        json={"amount": amount, "risk_disclosure_accepted": True},
    )

    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] in {"queued", "accepted"}
    assert body["bot_name"] == bot_name


def test_subscribe_below_min_rejected(obe_client):
    resp = obe_client.post(
        "/api/spartans/bots/OBE-Jason/subscribe",
        json={"amount": "0.01", "risk_disclosure_accepted": True},
    )
    assert resp.status_code == 400
    assert "min" in resp.json().get("error_code", "").lower()


def test_subscribe_without_risk_disclosure_rejected(obe_client):
    resp = obe_client.post(
        "/api/spartans/bots/OBE-Jason/subscribe",
        json={"amount": "10", "risk_disclosure_accepted": False},
    )
    assert resp.status_code == 400
