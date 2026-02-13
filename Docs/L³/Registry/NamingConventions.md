# L³ Naming Conventions

**Scope**: Rules governing dimension names, group identifiers, and output ranges in L³.

---

## 1. Group Names

| Convention | Format | Example |
|------------|--------|---------|
| Canonical name | lowercase English | `"alpha"`, `"epsilon"`, `"theta"` |
| Display name | Greek letter | `α`, `β`, `γ`, `δ`, `ε`, `ζ`, `η`, `θ` |
| Code class | PascalCase + `Group` | `AlphaGroup`, `EpsilonGroup`, `ThetaGroup` |
| Code file | lowercase `.py` | `alpha.py`, `epsilon.py`, `theta.py` |

## 2. Dimension Names

| Rule | Convention | Example |
|------|-----------|---------|
| Format | `snake_case` | `reward_intensity`, `skin_conductance` |
| Group prefix | Optional, used in cross-group contexts | `alpha.shared_attribution`, `epsilon.surprise` |
| Vocabulary suffix | `_vocab` for η dimensions | `valence_vocab`, `groove_vocab` |
| Polarity naming | Same as base axis (no prefix) | ζ: `valence`, `arousal`, `tension` |

## 3. Range Conventions

| Range | Groups | Meaning |
|-------|--------|---------|
| `[0, 1]` | α, β, γ, δ, ε, η, θ | Unipolar normalized |
| `[-1, +1]` | ζ only | Bipolar semantic axes |

## 4. Index Conventions

| Convention | Format | Example |
|------------|--------|---------|
| Global index | Integer `[0:104]` | `#45` = ε0 (surprise) |
| Local index | Group symbol + number | `ε0`, `ζ5`, `θ12` |
| Dimension name | snake_case | `surprise`, `liking`, `continuing` |

## 5. File Naming

| File Type | Convention | Example |
|-----------|-----------|---------|
| Group spec | `{Name}.md` | `Alpha.md`, `Epsilon.md` |
| Adapter doc | `{UNIT}-L3-ADAPTER.md` | `SPU-L3-ADAPTER.md` |
| Index file | `00-INDEX.md` | Always present in every directory |

---

**Parent**: [00-INDEX.md](00-INDEX.md)
