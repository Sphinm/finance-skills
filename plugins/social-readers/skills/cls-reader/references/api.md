# 财联社快讯 API

## 直连 HTTP（无需 opencli）

```python
import requests

UA = "Mozilla/5.0"


def cls_telegraph(limit: int = 20) -> list[dict]:
    """财联社实时电报"""
    url = "https://www.cls.cn/nodeapi/telegraphList"
    params = {"app": "CailianpressWeb", "os": "web", "sv": "8.4.6", "rn": str(limit)}
    r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=10)
    data = r.json().get("data", {}).get("roll_data", [])
    return [
        {
            "time": item.get("ctime", ""),
            "title": item.get("title", ""),
            "content": item.get("content", ""),
            "level": item.get("level", ""),  # 重要程度
        }
        for item in data
    ]


def cls_search(keyword: str, limit: int = 10) -> list[dict]:
    """财联社搜索"""
    url = "https://www.cls.cn/api/sw"
    params = {"app": "CailianpressWeb", "os": "web", "sv": "8.4.6", "keyword": keyword, "rn": str(limit)}
    r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=10)
    return r.json().get("data", [])
```

## opencli 备用

```bash
opencli list | grep -i cls
```

## 解读

| level | 含义 |
|-------|------|
| A | 重大政策/公司事件，立即关联持仓 |
| B | 行业动态，关注板块 |
| C | 一般资讯 |
