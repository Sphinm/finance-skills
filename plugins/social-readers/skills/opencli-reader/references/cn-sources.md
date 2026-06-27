# A股 opencli 中国区源速查

## 优先级

| 用户源 | 专用 skill |
|--------|-----------|
| 东财 | `eastmoney-reader` |
| 雪球 | `xueqiu-reader` |
| 财联社 | `cls-reader` |
| 其他 | **本 skill** |

## 中国区 opencli 站点

| 源 | slug | 常见用途 |
|----|------|----------|
| 东方财富 | `eastmoney` | 新闻/研报/资金/龙虎榜 |
| 雪球 | `xueqiu` | 讨论/情绪 |
| 新浪财经 | `sinafinance` | 行情/新闻 |
| 同花顺 | `10jqka` | 部分公开页 |
| 微博 | `weibo` | 财经大V动态 |
| 知乎 | `zhihu` | 行业讨论 |

## 发现命令

```bash
opencli list -f json | python3 -c "import json,sys; [print(x['site'],x['name']) for x in json.load(sys.stdin) if any(k in x.get('site','') for k in ['east','xueqiu','sina','weibo','zhihu','10jqka'])]"
opencli <site> --help
```

## READ-ONLY

禁止 invoke 写操作：post, comment, like, follow, send 等。

## Fallback 链

```
opencli 失败 → data-providers 直连 API（quote-data / signal-data / news-announce）
```
