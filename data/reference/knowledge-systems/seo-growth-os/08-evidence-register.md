# 08. Evidence register và nguồn

## 1. Nguồn chính thức bên ngoài

| Chủ đề | Nguồn | Cách dùng |
|---|---|---|
| AI features | [Google: AI features and your website](https://developers.google.com/search/docs/appearance/ai-features) | SEO vẫn là nền; không có tối ưu đặc biệt đảm bảo xuất hiện |
| Generative AI content | [Google: guidance on generative AI content](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content) | tránh scaled content không thêm giá trị; people-first |
| Helpful content | [Google: creating helpful, reliable, people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content) | đánh giá originality, completeness, focus, usefulness |
| Structured data | [Google: structured data introduction](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data) | structured data là tín hiệu mô tả; không xem là bảo đảm rich result |
| GA4 attribution | [Google Analytics: get started with attribution](https://support.google.com/analytics/answer/10596866) | ghi model/lookback; attribution không tự chứng minh causal lift |
| GA4 acquisition | [GA4 traffic acquisition report](https://support.google.com/analytics/answer/12923437) | traffic source và key event reporting |
| GEO research | [Aggarwal et al., GEO](https://arxiv.org/abs/2311.09735) | nền nghiên cứu cho khái niệm GEO; không biến kết quả nghiên cứu thành benchmark mọi ngành |

## 2. Nguồn nội bộ chính

| Nguồn | Đóng góp |
|---|---|
| `.agent/workflows/semantic-seo.md` | research → intent/entity → outline → article → fact-check/audit |
| `data/reference/study-workspace/.../SEO/win-flavor-aeo.md` | AEO protocol, answer-first, prompt testing, claim caveats |
| `data/reference/study-workspace/.../Marketing/content-systems.md` | business goal → persona → intent → cluster → distribution/measurement |
| `clients/MayMacCTH/outputs/00. Business Brief & SEO Direction.md` | organic landing → form → qualified lead → quote → order → repeat |
| `clients/MayMacCTH/outputs/06. KPI Framework Revised.md` | KPI tree và forecast formula sau baseline |
| `clients/General-B2B/brands/MQ-Flavor/customer-journey-topical-map.md` | B2B persona, TOFU/MOFU/BOFU và content role |
| `data/reference/study-workspace/.../Automation/internal-link-pipeline.md` | anchor/context/destination/diversity QA |
| `data/reference/study-workspace/.../Web-Design/everest-logistics-web-design.md` | IA theo mental model, CTA theo cam kết, form/service design |
| `tools/rank-checker/README.md` | rank, SERP features, alerts, schedule và export |

## 3. Claim status trong workspace

Các số liệu WIN Flavor AEO và các forecast trong quotation/audit phải được xem là **internal reported / needs verification** nếu chưa có dataset, analytics export hoặc source gốc. Khi viết case study/public content, dùng claim matrix và phân biệt correlation với causation.

## 4. Mẫu claim log

| Claim | Source | Scope/date | Status | Owner | Safe wording |
|---|---|---|---|---|---|
| [claim] | [URL/file] | [scope] | verified / open | [name] | [wording] |

## 5. Lịch cập nhật

- Hàng tháng: refresh data/analytics và open claims.
- Hàng quý: re-run prompt benchmark, audit AI/SEO assumptions, review growth model.
- Khi platform thay đổi: cập nhật module 03 và ghi ngày thay đổi.
