# Autonomous Commerce Harness: V3 Capability & Gap Analysis PRD

## 1. Executive Summary
While the V1 and V2 architectures establish a world-class foundational layer for intent grounding, mathematical price normalization, and cryptographic trust, a gap analysis against the **W3C Ecommerce for Humans and AI Agents** whitepaper reveals several missing behavioral, data, and ecosystem integration capabilities. 

This V3 Enhancement PRD maps out the necessary expansions to achieve full compliance with the theoretical whitepaper journey, introducing "Grill Me" constraint elicitation, comprehensive shopper memory arrays, brand optimization mechanics (Agentic SEO), and absolute utilization of the GS1 syntax.

---

## 2. Missing Capability 1: The "Grill Me" Principle (Constraint Elicitation)

**The Gap:** Currently, the Semantic Intent Grounding Engine (SIGE) passively translates whatever the user inputs. If the user provides a vague prompt (e.g., "Buy me milk"), the agent attempts to map it but lacks a systematic process to interrogate the user for missing mandatory constraints.

**The Enhancement:** Implement an **Active "Grill Me" Elicitation Loop**.
* **Mechanism:** Before touching the product catalog, the agent must evaluate the user's prompt against a mandatory schema checklist. If critical vectors (budget, dietary constraints, preferred brand, urgency) are missing or ambiguous, the agent actively pauses and interrogates ("grills") the user.
* **Example Output:** *"You asked for milk. To ensure I don't buy something you hate, please specify: 1) What is your hard budget limit? 2) Are there any lactose or nut allergies? 3) Do you require verified USDA Organic claims?"*
* **Architecture Impact:** This requires a new module in SIGE: `sige/elicitation_engine.py` that manages a state machine for constraint fulfillment prior to catalog search.

---

## 3. Missing Capability 2: Persistent & Cross-Merchant Data Arrays

**The Gap:** The current harness treats every transaction as a stateless event. It does not remember what the user bought yesterday, nor does it track authorized sellers globally.

**The Enhancement:** Implement a **Shopper Telemetry & Memory Matrix**.
* **Past Shopping Behavior:** Implement a vector database (RAG) of the user's historical purchases. The agent must prioritize exact SKUs or brands the user has a high Net Promoter Score (NPS) with natively.
* **Cross-Merchant Shopping:** The agent must be capable of parallel-querying the same GTIN across multiple merchants (Amazon, Walmart, Direct-to-Consumer) to dynamically build a cart that optimizes for combined shipping and lowest total cart cost, rather than just single-item price.
* **Authorized Storefronts (Whitelisting):** Expand the SPGE to maintain a strict, cryptographically signed list of authorized merchants. If a third-party seller on a marketplace offers the product at a steep discount, the agent must check if that seller is an "Authorized Retailer" via the brand's GS1 schema. If not, it flags it as a counterfeit risk.

---

## 4. Missing Capability 3: Agentic Brand Optimization (Agentic SEO)

**The Gap:** The framework outlines how the *agent* behaves, but lacks a specification for how *brands* ensure they are successfully discovered and chosen by these autonomous agents.

**The Enhancement:** Define and enforce the **Agentic SEO standard** for Brands.
To ensure a seamless agentic experience, brands must adopt the following optimizations:
1. **Exhaustive GS1 Web Vocab:** Brands must stop relying on HTML text descriptions. They must publish rich, complete JSON-LD graphs exposing `gs1:gpcCategoryCode`, `gs1:allergenInformation`, and `gs1:nutritionalAttribute`.
2. **Deterministic Pricing Data:** Brands must explicitly publish `gs1:netContent` (e.g., exact milliliter or gram counts) so the harness's mathematical normalizer can accurately rank them as cost-effective.
3. **Cryptographic Proofs:** Brands cannot just write "Sustainable" on their packaging. They must issue W3C Verifiable Credentials (signed by trusted bodies) attached to their Digital Links, allowing agents to instantly verify claims and bypass the greenwashing filters.

---

## 5. Missing Capability 4: Full Spectrum GS1 & W3C Utilization

**The Gap:** The harness currently resolves Digital Links and checks basic signatures, but it is not utilizing the *full depth* of the GS1 and W3C specifications.

**The Enhancement:** Deepen the GS1 and W3C parsers.
* **Granular 2D Digital Link Resolution:** Currently, we parse the GTIN (`01`). We must expand the resolver to act upon Batch/Lot (`10`) and Serial Number (`21`) identifiers. This allows the agent to check if a *specific serialized item* is subject to a manufacturer recall before buying it.
* **Complex Offer Graphs:** Fully utilize the `gs1:Offer` class to parse complex logic, such as volume discounts ("Buy 2 get 10% off"), which the agent must factor into its unit-price normalization math.
* **Full Digital Product Passport (DPP) Lifecycle:** Go beyond basic recycled content percentages. The agent should parse the entire circularity graph, including repairability indexes and end-of-life disposal costs, allowing corporate buyers to enforce strict ESG procurement rules automatically.

---

## 6. Alignment with the Whitepaper Shopping Journey

The enhanced V3 architecture creates a perfectly mapped 1:1 journey with the whitepaper:
1. **The User Intent Phase:** The agent uses the "Grill Me" loop to definitively establish explicit boundaries and parses past shopping behavior (RAG memory) for implicit preferences.
2. **The Discovery Phase:** The agent executes a cross-merchant search, pulling structured JSON-LD payloads.
3. **The Grounding & Verification Phase:** The harness mathematically normalizes prices, checks authorized merchant whitelists, and verifies W3C cryptographic claims (Zero Trust Model).
4. **The Execution Phase:** If everything falls within the established guardrails, the agent purchases via tokenized payment. If ambiguity exists, it routes to the Human-in-the-Loop visual UI.
5. **The XAI Phase:** The agent logs exactly why an item was chosen using the `explainability_logger.py`, referencing the precise GS1 attributes and VC signatures that led to the decision.
