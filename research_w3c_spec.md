# Research PRD & Design Specification: W3C Agentic Shopping Algorithm

This specification outlines the architectural standards, algorithmic flows, and data structures required to implement a W3C-compliant **AI Agent Shopping Algorithm** within the Autonomous Digital Commerce Harness. 

It aligns your positional statements on behavioral tracking, NLP grounding, and predictive modeling with the design patterns recommended in **W3C Ecommerce for Humans & AI Agents Workshop (Issue #29)**.

---

## 1. Executive Position Statement & Goals

The AI Agent Shopping Algorithm must move away from ungrounded HTML scraping and fuzzy chat shopping towards a **trusted, deterministic, and verifiable transaction model**. It translates raw digital body language, user prompts, and structured product graphs into mathematically sound purchasing decisions.

### Core Objectives:
1. **Accurately Assess Customer Intent:** Capture both explicit prompts and implicit behavioral signals in real-time.
2. **Fidelity and Trust Enforcement:** Validate merchant reputations and environmental/dietary claims using cryptographic signatures.
3. **Failsafe Guardrails:** Prevent exploit vectors (indirect prompt injection) and enforce financial spending policies.
4. **Post-Purchase Explainability (XAI):** Generate human-readable audit trails detailing exactly why an agent chose, filtered, or rejected an item.

---

## 2. Behavioral & Action Tracking Model (Implicit Intent)

While natural language defines *what* the user is looking for, their digital body language indicates *how close* they are to committing. The harness must track these implicit signals:

| Tracking Vector | Metrics Captured | Algorithmic Significance |
| :--- | :--- | :--- |
| **Clickstream Analysis** | Page views, hover durations, tab switches, cart additions. | Establishes a baseline interest score per SKU. |
| **Velocity Triggers** | Rate of price refreshes, checkout form clicks, rapid scroll patterns. | High-frequency refreshes or rapid clicks indicate high purchase intent and urgency. |
| **Feature Usage & Churn** | Help center visits, cancellation-button hovering, shipping policy lookups. | Predicts churn risk, transaction hesitation, or friction points. |

### Intent Calculation Formula
An individual product's **Propensity Score ($P_{intent}$)** is calculated dynamically:

$$P_{intent} = (w_1 \cdot C) + (w_2 \cdot V) - (w_3 \cdot F)$$

Where:
* $C$: Clickstream weight (cumulative interest)
* $V$: Velocity multiplier (rate of engagement indicating urgency)
* $F$: Friction multiplier (churn/hesitation signals)
* $w_n$: Configurable normalization weights

---

## 3. Natural Language Processing & Semantic Grounding (Explicit Intent)

To process natural language text (chat history, user queries, voice transcripts), the algorithm implements a three-stage NLP pipeline:

```
[ User Prompt: "Organic gluten-free oat milk" ]
                       |
                       v
                 1. Tokenizer
         (Breaks text into lemma tokens)
                       |
                       v
         2. Semantic Vector Embedding
        (Maps text to dense coordinates)
                       |
                       v
         3. Intent Classifier (SIGE)
   (Predicts query categories & constraints)
```

1. **Tokenization & Lemmatization:** Normalizes text, removing noise while isolating core descriptive nouns and adjectives.
2. **Semantic Vector Embedding:** Translates tokens into a multi-dimensional semantic vector space (using cosine similarity models) to group search terms with catalog items regardless of keyword vocab differences (e.g. mapping "soy drink" to "milk substitute").
3. **Intent Classification & Constraints Extraction:** Classifies the intent into structured slots:
   - **`gs1:gpcCategoryCode`**: Taxonomy category.
   - **Hard Constraints**: Allergens to avoid (e.g. `gs1:allergenInformation` FREE_FROM:Gluten).
   - **Soft Preferences**: Environmental claims (e.g. USDA Organic).

---

## 4. W3C Spec: Verification & Automated Shortlisting Algorithm

Based on W3C Ecommerce recommendations, the shopping sequence must follow a rigorous, non-hallucinated verification pipeline before checkout:

```
                    [ Unified Product Stream ]
                                |
                                v
               [ Filter 1: Hard Constraints Gate ]
                   (Allergen and budget check)
                                |
                                v
               [ Filter 2: Claim Verification Gate ]
                 (W3C Verifiable Credentials verify)
                                |
                                v
                [ Filter 3: Propensity Modeling ]
                  (Lead scoring & price compare)
                                |
                                v
                   [ Shortlist Compilation ]
                                |
                                v
                   [ Step-Up Threshold Check ]
                  /                         \
        (Pass: Score >= 90%)         (Fail: Score < 90%)
                /                             \
               v                               v
     [ Automated Checkout ]           [ Human Approval (PDP) ]
```

### Algorithmic Phase Details

#### Step 1: Hard Constraints Filtering
Directly discards any SKU that violates predefined human guardrails (e.g. allergens present, or price exceeding maximum context budget).

#### Step 2: Cryptographic Claim Verification (W3C VC check)
- Extracts the product's listed certification claims.
- For each claim, resolves the issuer's public key from their Decentralized Identifier (DID) Document.
- Verifies the cryptographic signature of the W3C Verifiable Credential (VC).
- Performs a check on the `StatusList2021` revocation list.
- **Rules:** 
  - If a certificate is missing or invalid: Claim validity score = 0%.
  - If certificate is verified: Claim validity score = 100%.

#### Step 3: Automated Shortlisting & Propensity Scoring
Sorts the remaining compliant candidates using the propensity models, prioritizing:
1. Low unit-price (normalized via `unit_price_normalizer.py` to standard $/ml or $/g).
2. High claim verification scores (W3C trust metrics).
3. Trusted merchant domain reputation.

#### Step 4: Step-Up Routing Threshold
- If the top-scoring product has a **trust/compliance score of 100%** and the transaction value is within the agent's autonomous limit, route immediately to **Automated Checkout**.
- If claims are unverified, domain is untrusted, or budget limit is exceeded, route to **Human-in-the-Loop PDP Web UI** for step-up authorization.

#### Step 5: Explainability (XAI) Generation
The agent must generate an audit-ready, natural-language explanation of its action:
* *Example Output:* `"Product A was shortlisted because it represents the lowest unit cost ($0.62/oz) and has a 100% verified USDA Organic certification from issuer did:key:123. Product B was rejected because its organic claim had no cryptographic verification (Greenwashing Flag)."`

---

## 5. Practical Application: How Agents Capture Human Intent

To bridge human desires with autonomous execution, the agent captures and refines intent across three operational layers:

### A. Explicit Grounding Layer (Stated Intent)
- **Concept:** Translating human natural-language statements into structured schema constraints.
- **Workflow:** When a user prompts the agent, the NLP pipeline translates phrases (e.g. "for my daughter's allergy") into strict filters in the metadata model (e.g. `gs1:allergenInformation = FREE_FROM:Nuts`). This prevents the agent from evaluating non-compliant options, ensuring immediate alignment with stated constraints.

### B. Implicit Telemetry Layer (Digital Body Language)
- **Concept:** Detecting unstated user priorities (urgency, hesitation, interest level) from action patterns.
- **Workflow:** The harness continuously calculates the product's Propensity Score ($P_{intent}$) based on clickstream, scroll speeds, and page refresh velocities. The agent queries this score via MCP:
  - *High Velocity Triggers* signify high urgency $\rightarrow$ The agent automatically prioritizes immediate shipping speeds over minor price variances.
  - *Friction/Cancellation Hovers* signify hesitation $\rightarrow$ The agent automatically exposes warranty information or shifts focus to lower-cost trust models.

### C. Interactive Alignment Layer (The Refinement Loop)
- **Concept:** Gracefully resolving ambiguity when intent vectors conflict.
- **Workflow:** When the agent's decision confidence falls below the $90\%$ autonomous threshold (e.g. choosing between a cheap unverified option vs. a premium organic certified option), it halts execution. The DS-Adapter triggers a visual visual PDP step-up gate. When the human selects an option, the agent commits the preference to its memory database, calibrating its decision weights ($w_n$) for all future shopping cycles.

