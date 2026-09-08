# 05. Performance, analytics và CRO

## 1. Measurement contract

Trước khi chạy campaign hoặc audit, chốt:

| Thành phần | Ví dụ |
|---|---|
| Business outcome | won order, revenue, margin, repeat order |
| Primary key event | `generate_lead` hoặc `request_quote_success` |
| Secondary event | `form_start`, `click_phone`, `click_zalo`, `download_spec` |
| Required dimensions | source/medium, landing page, query cluster, service, device |
| System of record | CRM/kế toán cho revenue; GA4/GSC cho digital signals |
| QA owner | Marketing Ops + Dev + Sales |

GA4 có các báo cáo traffic acquisition và key events; attribution là quy tắc phân bổ credit, không phải bằng chứng nhân quả tuyệt đối. Cần ghi rõ model và lookback window khi báo cáo.

## 2. Event schema tối thiểu

```text
event_name
timestamp
session_id / lead_id
source, medium, campaign
landing_page, content_cluster
service/product
device, location
form_status / error_code
crm_status
revenue_value / margin_value (khi được phép)
```

Không gửi PII vào analytics. Lead ID và CRM join key phải theo chính sách bảo mật của tổ chức.

## 3. CRO diagnosis tree

```text
Low form submit
  ├─ Low qualified traffic? query/page/channel
  ├─ Low intent? promise/offer mismatch
  ├─ UX friction? fields, mobile, speed, error
  ├─ Trust gap? proof, process, pricing, risk
  └─ Technical failure? event, API, CRM routing
```

## 4. Experiment card

Mỗi test ghi: problem, evidence, hypothesis, change, audience, primary metric, guardrail metric, duration/sample logic, owner, result, decision.

Không gọi một thay đổi là thắng nếu chỉ tăng click nhưng giảm qualified rate, close rate hoặc margin.

## 5. Dashboard 4 lớp

1. **Executive**: revenue, margin, qualified pipeline, CAC/payback, repeat.
2. **Channel**: organic, AI referral, paid, direct, partner; attribution model.
3. **Asset**: URL/cluster, impressions, clicks, engagement, key events, assisted path.
4. **Operations**: crawl/index, tracking QA, form errors, SLA sales, data freshness.

## 6. QA cadence

- Hàng tuần: anomaly, tracking, lead routing, query/page changes, rank drops.
- Hàng tháng: cluster performance, CRO backlog, CRM quality, content refresh.
- Hàng quý: attribution caveats, incrementality test nếu khả thi, budget reallocation, entity/proof update.
