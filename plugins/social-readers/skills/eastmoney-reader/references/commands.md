# 东财 opencli 命令参考

## 安装

```bash
npm install -g @jackwener/opencli
opencli doctor
```

## 常用命令（以 `opencli eastmoney --help` 为准）

| 用户需求 | 命令示例 |
|----------|----------|
| 个股新闻 | `opencli eastmoney news --symbol 600519` |
| 研报 | `opencli eastmoney report --symbol 600519` |
| 资金流向 | `opencli eastmoney fundflow --symbol 600519` |
| 龙虎榜 | `opencli eastmoney longhu --date 2026-05-09` |
| 板块行情 | `opencli eastmoney sector` |
| 热门股票 | `opencli eastmoney hot` |

## 发现命令

```bash
opencli list | grep -i eastmoney
opencli eastmoney --help
```

## 注意

- READ-ONLY：禁止 post/comment 等写操作
- 部分命令需 Browser Bridge（`opencli doctor` 检查 COOKIE 类适配器）
