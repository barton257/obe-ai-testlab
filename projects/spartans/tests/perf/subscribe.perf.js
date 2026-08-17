// 骨架示例：斯巴达订阅接口压测。
// testcase 参考: projects/spartans/testcases/spartans-subscribe-P0-*.yaml
//
// 目标接口: POST /api/spartans/bots/{bot}/subscribe
// 期望 QPS: 100
// 期望 P95: < 800ms
// 是否影响资金: 是（仅在 Testnet 运行）
//
// 运行前请确认 OBE_TESTNET_BASE_URL / OBE_TOKEN 已注入，且 bot 处于运行状态。

import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  scenarios: {
    subscribe_ramp: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '30s', target: 20 },
        { duration: '1m', target: 100 },
        { duration: '30s', target: 0 },
      ],
      gracefulRampDown: '10s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<800'],
  },
};

const BASE = __ENV.OBE_TESTNET_BASE_URL;
const TOKEN = __ENV.OBE_TOKEN;
const BOT = __ENV.SPARTANS_BOT ?? 'OBE-Jason';
const AMOUNT = __ENV.SPARTANS_MIN_SUBSCRIBE_AMOUNT ?? '10';

export default function () {
  if (!BASE || !TOKEN) {
    throw new Error('missing OBE_TESTNET_BASE_URL or OBE_TOKEN');
  }

  const res = http.post(
    `${BASE}/api/spartans/bots/${BOT}/subscribe`,
    JSON.stringify({ amount: AMOUNT, risk_disclosure_accepted: true }),
    {
      headers: {
        Authorization: `Bearer ${TOKEN}`,
        'Content-Type': 'application/json',
      },
      tags: { endpoint: 'subscribe' },
    },
  );

  check(res, {
    'status is 200': (r) => r.status === 200,
    'body has queued|accepted': (r) => {
      try {
        const b = r.json();
        return b.status === 'queued' || b.status === 'accepted';
      } catch (_) {
        return false;
      }
    },
  });

  sleep(1);
}
