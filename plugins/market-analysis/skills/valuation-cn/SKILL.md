---
name: valuation-cn
description: >
  A-share valuation: forward PE, PEG, PE digestion to 30x anchor, peer comparison, simplified SOTP.
  Data from Tencent quotes + Tonghuashun consensus EPS. Triggers: 估值, PEG, 前向PE, PE消化,
  贵不贵, 合理价位, 同业对比PE, 板块内低估, DCF简化, 可比估值, A-share valuation.
---

# Valuation CN — A股估值

## Step 1: Single-Stock Valuation

执行 `references/workflow.md` § `full_valuation(code)`：

```python
# 见 references/workflow.md
result = full_valuation("688017")
# → pe_fwd, peg, digest_years, rating
```

## Step 2: Peer Comparison

同板块标的批量对比：

```python
peer_valuation(["002463", "002916", "600183"])
```

PEG 低于同业中位数 + 增速不低于同业 → 板块内低估。

## Step 3: Investment Framework

```
壁垒 → 增速 → PE消化 → PEG校验

1. 有壁垒吗？(供应链不可替代) → 没有则排除
2. CAGR > 30% 才有意义
3. PE_fwd 消化到 30x < 2年 → 合理
4. PEG < 1 便宜 | 1-1.5 合理 | > 2 不推荐
```

公式详见 `references/formulas.md`。

## Step 4: Cross-Validate with Earnings

- 一致预期 EPS → `research-data`
- 实际季报 → `fundamental-data`
- 叙事验证 → `thread-stock` 四层漏斗

## Reference Files

| 文件 | 内容 |
|------|------|
| `references/formulas.md` | 前向PE / PEG / PE消化公式 |
| `references/workflow.md` | full_valuation + peer_valuation 完整代码 |
