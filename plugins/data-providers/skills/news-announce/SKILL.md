---
name: news-announce
description: >
  A-share news and regulatory announcements: Eastmoney stock news, CLS telegraph (财联社快讯),
  Eastmoney 7x24 global news, CNINFO (巨潮) announcement search and download, mootdx F10 announcement summary.
  Triggers: 个股新闻, 财联社, 快讯, 7x24资讯, 公告, 巨潮, 信息披露,
  减持公告, 业绩预告公告, any A-share news or announcement lookup.
---

# News & Announce — A股新闻与公告层

## Step 1: Prerequisites

```bash
pip install requests pandas mootdx
```

## Step 2: Match Request

| 用户需求 | 数据源 | 参考 |
|----------|--------|------|
| 个股新闻 | 东财 search-api | `references/api.md` §5.1 |
| 财联社快讯 | cls.cn | §5.2 |
| 7×24 全球资讯 | 东财 np-weblist | §5.3 |
| 公告全文检索/下载 | 巨潮 cninfo | `references/announcements.md` §7.1 |
| 最新公告摘要 | mootdx F10 | `references/announcements.md` §7.2 |

## Related Skills

- 财报数据 → `fundamental-data`
- 财报前后分析 → `earnings-preview` / `earnings-recap`
