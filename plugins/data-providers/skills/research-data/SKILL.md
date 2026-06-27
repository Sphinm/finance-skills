---
name: research-data
description: >
  A-share equity research reports: Eastmoney report API (list + PDF download + ratings + 3yr EPS),
  Tonghuashun consensus EPS forecast, iwencai NL semantic report search.
  Triggers: 研报, 机构评级, 一致预期, EPS预测, 下载研报PDF, iwencai,
  卖方报告, 深度报告, 行业研报, any A-share research report retrieval.
---

# Research Data — A股研报层

## Step 1: Prerequisites

```bash
pip install requests pandas
```

iwencai 语义搜索需 API Key，见 `references/common.md`。

## Step 2: Match Request

| 用户需求 | 数据源 | 参考 |
|----------|--------|------|
| 研报列表/PDF/评级 | 东财 reportapi | `references/api.md` §2.1 |
| 一致预期 EPS | 同花顺 THS | §2.2 |
| NL 语义搜研报 | iwencai | §2.3 |

## Step 3: Quality Checks

- 同花顺「预测机构数」< 3 → 谨慎使用
- 东财 PDF 下载 403 → 换 User-Agent 或走列表摘要

## Related Skills

- 估值计算 → `valuation-cn`
- 批量主题检索 → `trading-data` workflows
