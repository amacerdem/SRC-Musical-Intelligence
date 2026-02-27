# LLM Library — Musical Mind Agent Knowledge Base

## Problem Statement

The M3 Mobile frontend already has a sophisticated narrative engine (m3-observations.ts, mind-insights.ts), but it's **hardcoded TypeScript templates** using i18n keys — limited, rigid, can't go deep, can't have a real conversation. We need to replace this with an LLM-powered agent that can have cutting-edge science conversations at the user's depth level, interpret their real-time analysis, and grow with them.

The raw knowledge exists (555 mechanism docs, 492 paper summaries, 131 beliefs, 96 models, M3-LOGOS spec) but none of it is in a format optimized for LLM consumption.

## Architecture — 5-Layer Context Stack

```
┌──────────────────────────────────────────────────────────┐
│ Layer 0: PERSONA — always in context (~1.5K tokens)      │
│   System prompt, guardrails, tone, identity              │
├──────────────────────────────────────────────────────────┤
│ Layer 1: USER PROFILE — always in context (~500 tokens)  │
│   Persona, genes, level, tier, language, session summary │
├──────────────────────────────────────────────────────────┤
│ Layer 2: VOCABULARY — always in context (~2K tokens)     │
│   M3-LOGOS 6D/12D names, observation rules, tier gates   │
├──────────────────────────────────────────────────────────┤
│ Layer 3: KNOWLEDGE — RAG-retrieved (~2K tokens)          │
│   Belief cards, dimension cards, concept cards, personas │
│   Retrieved based on user's question + current state     │
├──────────────────────────────────────────────────────────┤
│ Layer 4: LITERATURE — RAG-retrieved (~1.5K tokens)       │
│   Paper summaries, mechanism explanations, findings      │
│   Retrieved for deep questions at Premium/Research tier   │
├──────────────────────────────────────────────────────────┤
│ Layer 5: LIVE DATA — tool use (on demand)                │
│   Real-time beliefs, dimension state, session comparison │
│   Music analysis results, trend detection                │
└──────────────────────────────────────────────────────────┘
Total context budget: ~8K tokens + conversation history (~2K) = ~10K
```

## File Structure

```
Musical_Intelligence/brain/llm/
├── __init__.py
├── config.py                         — Model settings, API keys, tier definitions
│
├── knowledge/                        — Structured knowledge base (JSONL files)
│   ├── __init__.py
│   ├── beliefs.jsonl                 — 131 belief description cards
│   ├── dimensions_6d.jsonl           — 6 psychology dimensions
│   ├── dimensions_12d.jsonl          — 12 cognition dimensions
│   ├── dimensions_24d.jsonl          — 24 neuroscience dimensions
│   ├── personas.jsonl                — 24 persona conversation profiles
│   ├── concepts.jsonl                — ~80 neuroscience concepts
│   ├── neurochemicals.jsonl          — DA, NE, OPI, 5HT accessible descriptions
│   ├── observations.jsonl            — Tier-gated observation templates
│   └── cross_references.jsonl        — BRECVEMA/GEMS/BMRQ/MUSIC mappings
│
├── prompts/                          — System prompt templates
│   ├── __init__.py
│   ├── persona_tr.md                 — Turkish persona definition
│   ├── persona_en.md                 — English persona definition
│   ├── guardrails.md                 — Behavioral boundaries
│   ├── vocabulary.md                 — M3-LOGOS vocabulary rules
│   └── tier_rules.md                 — What each subscription tier sees
│
├── rag/                              — RAG pipeline
│   ├── __init__.py
│   ├── chunker.py                    — Document → chunks (512 token target)
│   ├── embedder.py                   — Chunks → vectors (text-embedding-3-small)
│   ├── indexer.py                    — Build/update ChromaDB index
│   ├── retriever.py                  — Query → top-k relevant chunks
│   └── collections.py                — Collection definitions & metadata
│
├── agent/                            — Agent logic
│   ├── __init__.py
│   ├── context_builder.py            — Assemble full prompt per query
│   ├── router.py                     — Smart routing (Haiku vs Sonnet)
│   ├── tools.py                      — MI system tool definitions
│   ├── interpreter.py                — Belief/dimension → natural language
│   └── conversation.py               — Conversation memory management
│
└── processing/                       — One-time knowledge generation scripts
    ├── __init__.py
    ├── gen_beliefs.py                — C³ docs → beliefs.jsonl
    ├── gen_dimensions.py             — M3-LOGOS → dimensions_*.jsonl
    ├── gen_personas.py               — M3 Mobile data → personas.jsonl
    ├── gen_concepts.py               — Literature summaries → concepts.jsonl
    ├── gen_observations.py           — M3-LOGOS §8 → observations.jsonl
    ├── index_literature.py           — Literature/ → ChromaDB embeddings
    └── index_mechanisms.py           — Building/C³-Brain → ChromaDB embeddings
```

## Knowledge Card Schema

### beliefs.jsonl (131 entries)

```jsonl
{
  "index": 4,
  "key": "harmonic_stability",
  "function": "F1",
  "type": "Core",
  "mechanism": "BCH",
  "parent_24d": "harmonic_tension",
  "parent_12d": "tension_arc",
  "parent_6d": "intensity",
  "what_tr": "Müziğin tonal merkeze ne kadar yakın durduğu — akorlar 'eve dönüş' hissi veriyor mu?",
  "what_en": "How close the music stays to its tonal center — do the chords feel like 'coming home'?",
  "high_tr": "Güçlü tonal zemin. Akorlar tanıdık bir çekim alanında. Beyin rahat tahmin ediyor.",
  "high_en": "Strong tonal ground. Chords orbit a familiar center. The brain predicts comfortably.",
  "low_tr": "Tonal merkez belirsiz. Müzik yerçekimsiz bir alanda yüzüyor. Tahmin zor.",
  "low_en": "Tonal center ambiguous. Music floats in zero-gravity. Prediction is hard.",
  "analogy_tr": "Bir pusulanın kuzeyi göstermesi gibi — harmonic_stability müziğin tonal 'kuzey'ini ne kadar net gösterdiğini ölçer.",
  "analogy_en": "Like a compass pointing north — harmonic_stability measures how clearly the music points to its tonal 'north'.",
  "neural": "OFC + amygdala tonal syntax violation detection (Koelsch 2014)",
  "citations": ["Lerdahl & Krumhansl 2007", "Koelsch 2014"],
  "tier_visible": "research"
}
```

### dimensions_6d.jsonl (6 entries)

```jsonl
{
  "index": 0,
  "key": "discovery",
  "name_en": "Discovery",
  "name_tr": "Keşif",
  "beliefs_count": 21,
  "children_12d": ["expectancy", "information_rate"],
  "gene_affinity": "entropy",
  "persona_family": "Explorers",
  "what_tr": "Müziğin seni ne kadar şaşırttığı, bilgilendirdiği ve beklentilerini zorladığı.",
  "what_en": "How much the music surprises, informs, and challenges your expectations.",
  "high_tr": "Müzik seni yeni bir yere götürüyor. Tahmin motoru sürprizler üretiyor. Öğrenme gerçekleşiyor.",
  "high_en": "The music is taking you somewhere new. Your prediction engine is generating surprises. Learning is happening.",
  "low_tr": "Tanıdık sular. Tahmin sistemi alanı haritalamış. Ne geleceğini bilmenin huzuru.",
  "low_en": "Familiar waters. Your prediction system has mapped the terrain. Comfort in knowing what comes next.",
  "rising_tr": "Keşif moduna geçiyorsun. Her yeni ses bilgi taşıyor.",
  "rising_en": "You're entering exploration mode. Every new sound carries information.",
  "falling_tr": "Keşif azalıyor. Müzik tanınır hale geliyor, beyin enerji tasarrufu yapıyor.",
  "falling_en": "Discovery is decreasing. Music is becoming recognizable, brain is conserving energy.",
  "scientific_basis": "Meyer 1956 (expectancy), Huron 2006 (ITPRA), Pearce 2005 (IDyOM), Clark 2013 (predictive processing)",
  "brecvema": "Musical expectancy",
  "gems_mapping": "Wonder",
  "color": "#38BDF8"
}
```

### personas.jsonl (24 entries)

```jsonl
{
  "id": 3,
  "name": "Chaos Explorer",
  "family": "Explorers",
  "gene_dominant": "entropy",
  "dimension_profile": {"discovery": 0.95, "intensity": 0.70, "flow": 0.35, "depth": 0.15, "trace": 0.20, "sharing": 0.15},
  "tagline_tr": "Bilinmeyene doğru koşan zihin.",
  "tagline_en": "A mind that runs toward the unknown.",
  "conversation_tone": "energetic, intellectually curious, loves novelty, asks 'what if' questions",
  "preferred_topics": ["predictive processing", "information entropy", "statistical learning", "complexity"],
  "avoid_topics": ["routine", "familiarity", "comfort zone"],
  "metaphor_style": "exploration metaphors — uncharted maps, deep sea diving, space exploration",
  "greeting_tr": "Bugün hangi bilinmeyen sularda yüzüyorsun?",
  "greeting_en": "What unknown waters are you swimming in today?",
  "population_pct": 2.5,
  "shadow": "May dismiss familiar music too quickly. Growth comes from finding depth in repetition."
}
```

### concepts.jsonl (~80 entries)

```jsonl
{
  "key": "prediction_error",
  "name_tr": "Tahmin Hatası",
  "name_en": "Prediction Error",
  "tier_min": "free",
  "category": "predictive_processing",
  "related_6d": ["discovery", "intensity"],
  "related_beliefs": [20, 21, 28, 84, 85],
  "summary_tr": "Beynin 'bir sonraki ses ne olacak' tahmini ile gerçekleşen ses arasındaki fark. Müzikal duygunun temel kaynağı.",
  "summary_en": "The gap between the brain's prediction of 'what sound comes next' and what actually occurs. The fundamental source of musical emotion.",
  "deep_tr": "Bayes güncellemesi: gain = π_obs/(π_obs + π_pred). Büyük tahmin hatası = büyük sürpriz = dopamin salınımı (Salimpoor 2011). Küçük tahmin hatası = beklenti doğrulandı = huzur.",
  "deep_en": "Bayesian update: gain = π_obs/(π_obs + π_pred). Large prediction error = big surprise = dopamine release (Salimpoor 2011). Small prediction error = expectation confirmed = comfort.",
  "fun_fact_tr": "Beyin saniyede yaklaşık 5-8 müzikal tahmin üretir — her biri küçük bir 'mini deney'.",
  "fun_fact_en": "The brain generates roughly 5-8 musical predictions per second — each one a tiny 'mini-experiment'.",
  "citations": ["Clark 2013", "Koelsch et al. 2019", "Salimpoor et al. 2011"],
  "paper_ids": ["c3-clark-2013", "c3-koelsch-2019", "c3-salimpoor-2011"]
}
```

## RAG Collections (ChromaDB)

| Collection | Source | Documents | Avg Chunk | Use Case |
|-----------|--------|-----------|-----------|----------|
| `knowledge_cards` | beliefs + dimensions + concepts JSONL | ~260 | 200 tok | Always: structured Q&A |
| `literature_c3` | 492 paper summaries | ~2,500 | 512 tok | Deep: "why does X happen?" |
| `literature_c0` | 121 temporal neuroscience entries | ~600 | 512 tok | Deep: temporal mechanisms |
| `mechanisms` | 555 Building/C³-Brain docs | ~2,200 | 512 tok | Research tier: "how does BCH work?" |

**Total vectors**: ~5,560 — well within ChromaDB local capacity.

## Agent Tools (Claude API tool_use)

```python
TOOLS = [
    {
        "name": "get_current_beliefs",
        "description": "Get the user's current 131 belief values from their most recent listening session",
        "input_schema": {"type": "object", "properties": {"session_id": {"type": "string"}}}
    },
    {
        "name": "get_dimensions",
        "description": "Get 6D/12D/24D dimension values from current or historical session",
        "input_schema": {"type": "object", "properties": {
            "session_id": {"type": "string"},
            "layer": {"type": "string", "enum": ["6d", "12d", "24d"]}
        }}
    },
    {
        "name": "analyze_track",
        "description": "Run MI analysis on a track and return dimension summary",
        "input_schema": {"type": "object", "properties": {"track_id": {"type": "string"}}}
    },
    {
        "name": "compare_sessions",
        "description": "Compare two listening sessions — show belief/dimension deltas",
        "input_schema": {"type": "object", "properties": {
            "session_a": {"type": "string"},
            "session_b": {"type": "string"}
        }}
    },
    {
        "name": "get_belief_trajectory",
        "description": "Get time-series trajectory of specific beliefs across sessions",
        "input_schema": {"type": "object", "properties": {
            "belief_keys": {"type": "array", "items": {"type": "string"}},
            "period": {"type": "string", "enum": ["week", "month", "all"]}
        }}
    },
    {
        "name": "search_knowledge",
        "description": "Search the knowledge base for concepts, beliefs, or literature",
        "input_schema": {"type": "object", "properties": {
            "query": {"type": "string"},
            "collection": {"type": "string", "enum": ["knowledge_cards", "literature_c3", "literature_c0", "mechanisms"]}
        }}
    }
]
```

## Smart Router Logic

```python
def route_message(message: str, user_tier: str, conversation_depth: int) -> str:
    """Select model based on message complexity and user tier."""

    # Simple greetings, short answers → Haiku
    if conversation_depth < 3 and is_simple_query(message):
        return "claude-haiku-4-5-20251001"

    # Deep science questions, analysis interpretation → Sonnet
    if user_tier in ("premium", "research") or requires_tool_use(message):
        return "claude-sonnet-4-5-20250929"

    # Default: Sonnet (quality over cost for knowledge product)
    return "claude-sonnet-4-5-20250929"
```

## Implementation Phases

### Phase 1: Knowledge Base Foundation (first)
**Deliverables**: JSONL knowledge files + processing scripts

1. Create `Musical_Intelligence/brain/llm/` package structure
2. Write `gen_dimensions.py` → parse M3-LOGOS.md → generate `dimensions_6d/12d/24d.jsonl`
3. Write `gen_beliefs.py` → parse Docs/C³/Models + M3-LOGOS §6 → generate `beliefs.jsonl`
4. Write `gen_personas.py` → parse M3 Mobile persona data → generate `personas.jsonl`
5. Write `gen_concepts.py` → extract core concepts from literature → generate `concepts.jsonl`
6. Write `gen_observations.py` → M3-LOGOS §8 + m3-observations.ts → `observations.jsonl`
7. Write cross_references from M3-LOGOS §9 (BRECVEMA, GEMS, BMRQ, MUSIC mappings)

### Phase 2: System Prompt Engineering (second)
**Deliverables**: Prompt templates that define the agent

1. Write `persona_tr.md` — Turkish personality definition
2. Write `persona_en.md` — English personality definition
3. Write `guardrails.md` — behavioral boundaries (observe don't judge, no therapy, etc.)
4. Write `vocabulary.md` — M3-LOGOS term usage rules
5. Write `tier_rules.md` — what Free/Basic/Premium/Research users see
6. Write `context_builder.py` — assemble Layers 0-2 into system prompt

### Phase 3: RAG Pipeline (third)
**Deliverables**: Embedded knowledge + retrieval

1. Set up ChromaDB local instance
2. Write `chunker.py` — document → 512-token chunks with metadata
3. Write `embedder.py` — OpenAI text-embedding-3-small wrapper
4. Write `indexer.py` — JSONL + literature → ChromaDB collections
5. Write `retriever.py` — query → top-5 chunks with tier filtering
6. Run indexing: knowledge cards (~260) + literature (~3,100) + mechanisms (~2,200)

### Phase 4: Agent Core (fourth)
**Deliverables**: Working conversational agent

1. Write `agent/router.py` — Haiku/Sonnet selection
2. Write `agent/interpreter.py` — belief/dimension → natural language
3. Write `agent/tools.py` — MI system tool definitions
4. Write `agent/conversation.py` — conversation history (SQLite)
5. Write `agent/context_builder.py` — full 5-layer context assembly
6. Integration test: send message → get response with correct tier vocabulary

### Phase 5: API Integration (fifth)
**Deliverables**: FastAPI endpoints for M3 Mobile

1. Add `Lab/backend/routers/agent.py`:
   - `POST /api/agent/chat` — send message, get response
   - `GET /api/agent/history/{user_id}` — conversation history
   - `POST /api/agent/interpret` — analyze track + generate commentary
2. Add authentication (user_id + tier validation)
3. Add conversation persistence
4. M3 Mobile integration

### Phase 6: Music Interpretation Engine (later)
**Deliverables**: Post-analysis natural language commentary

1. Real-time belief trajectory narration
2. "This piece makes your X do Y because Z" explanations
3. Comparative analysis ("this piece vs that piece")
4. Personalized recommendations based on profile gaps
5. Weekly/monthly evolution narratives

## Conversation Examples

### Free Tier (6D Surface)
```
User: Neden bazı şarkılar beni heyecanlandırıyor?
Agent: Bu senin Discovery boyutunla ilgili. Beynin sürekli "bir sonraki
ses ne olacak?" diye tahmin üretiyor. Tahminlerin yanlış çıktığında —
müzik seni şaşırttığında — bir sürpriz sinyali oluşuyor. Bu sinyal
heyecan hissini tetikliyor. Senin Discovery'n genelde yüksek çıkıyor,
bu da tahmin motorunun aktif çalıştığı, sürprizlere açık bir zihin
olduğunu gösteriyor.
```

### Basic Tier (12D Narrative)
```
User: Groove tam olarak nedir? Neden bazı müzikler hareket ettiriyor?
Agent: Groove iki şeyin birleşimi: Entrainment (beynindeki nöral
osilatörlerin ritme kilitlenmesi) ve Auditory-Motor Integration (bu
kilitlemenin motor sisteme aktarılması). Witek'in 2014 araştırması
şaşırtıcı bir şey buldu: groove en güçlü olduğu an ne çok basit ne de
çok karmaşık ritimler — orta seviye senkopasyon. Beynin "neredeyse
tahmin edebiliyorum ama tam değil" dediği nokta. Senin Flow boyutun
şu an 0.85 — Kineticist ailesinden Groove Mechanic'e yakınsın.
```

### Premium Tier (24D Deep)
```
User: Chills deneyimini nörobilimsel olarak açıklayabilir misin?
Agent: Chills, Dopaminergic Drive ile Hedonic Valuation'ın kesişim
noktasında gerçekleşiyor. Salimpoor'un 2011 Nature Neuroscience
çalışması bunu iki aşamalı gösterdi:

Aşama 1 — Anticipation: Caudate nucleus'ta dopamin birikmeye başlıyor.
Senin wanting_ramp belief'in (index 78) yükseliyor. Beyin "bir şey
geliyor" diyor ama henüz ne olduğunu bilmiyor.

Aşama 2 — Consummation: Müzik doruk noktasına ulaştığında Nucleus
Accumbens'te dopamin patlaması + endojen opioid salınımı. Bu an senin
pleasure belief'inin (index 83) spike yaptığı an.

İlginç olan: chills_proximity (index 79) bir Anticipation belief'i —
yani beynin chills'in ne zaman geleceğini TAHMİN etmeye çalışıyor.
Ve bu tahmin her seferinde biraz daha iyi oluyor.
```

## Key Design Decisions

1. **JSONL over JSON/YAML**: Her satır bağımsız bir kayıt. Embedding'e uygun, filtrelenebilir, streaming-friendly.

2. **ChromaDB over Pinecone**: Local, ücretsiz, ~5,600 vektör rahat kaldırır. Ölçeklenince Pinecone'a geçiş kolay.

3. **Bilingual (TR/EN)**: Tüm knowledge card'lar her iki dilde. Agent kullanıcının dilini algılayıp o dildeki field'ları kullanır.

4. **Tier-gated retrieval**: RAG retriever, kullanıcının tier'ına göre filtreler. Free user 24D detay göremez.

5. **Processing scripts idempotent**: gen_*.py scriptleri her çalıştığında aynı JSONL'i üretir. Kaynak değişirse tekrar çalıştırılır.

6. **Conversation in SQLite**: Başlangıç için yeterli. user_id, session_id, messages, timestamps. PostgreSQL'e geçiş trivial.

## Dependencies

```
# Core
anthropic>=0.40.0          # Claude API
chromadb>=0.5.0             # Vector DB
openai>=1.50.0              # Embeddings (text-embedding-3-small)

# Processing
tiktoken>=0.7.0             # Token counting for chunking

# Storage
# SQLite (stdlib)           # Conversation history
```
