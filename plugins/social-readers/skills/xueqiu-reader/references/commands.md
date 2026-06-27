# 雪球 opencli 命令参考

## 常用命令

| 用户需求 | 命令示例 |
|----------|----------|
| 个股讨论 | `opencli xueqiu status --symbol SH600519` |
| 用户动态 | `opencli xueqiu user --uid <id>` |
| 搜索 | `opencli xueqiu search --keyword 半导体` |
| 热门 | `opencli xueqiu hot` |

代码格式：`SH600519` / `SZ000001` / `BJ832000`

## 发现命令

```bash
opencli list | grep -i xueqiu
opencli xueqiu --help
```

## 情绪解读

- 讨论量突增 + 股价未涨 → 关注度高，可能酝酿波动
- 大V集中看空 + 基本面未变 → 可能是反向指标（谨慎）

## Fallback

直连 API 不可用时的情绪数据 → `finance-sentiment-cn` skill
