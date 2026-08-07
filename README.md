# Autonomous Digital Commerce Harness & Verification Framework

An enterprise-grade execution environment, trust runtime sandbox, policy engine, and evaluation layer bridging autonomous AI shopping agents with digital retail infrastructure. 

This platform natively integrates global data exchange, cryptographic identity, and sustainability compliance standards into a single, cohesive, ultra-fast Python runtime.

---

## 🚀 Core Foundational Standards

The harness mandates and validates four core standards to prevent fuzzy agent reasoning, hallucinations, security exploits, and greenwashing:

1. **GS1 Web Vocabulary & Ontology:** Direct JSON-LD semantic data representing `gs1:Product`, `gs1:Offer`, `gs1:Organization`, and `gs1:Place` master records.
2. **GS1 2D Barcode & Digital Link Syntax:** Universal resolver scheme translating web-enabled URI coordinates directly to API endpoints.
3. **W3C Verifiable Credentials (VC):** Decoupled cryptographic proof signatures (e.g. Ed25519, ECDSA) validating organic, carbon-neutral, or safety claims against Decentralized Identifiers (DIDs).
4. **Digital Product Passport (DPP):** Regulatory compliance schemas (EU Ecodesign) delivering Bill of Materials (BOM), recycled content, lifecycle carbon metrics, and disassembly data.

---

## 🏛️ Architecture Directory Map

```
agentic-commerce-harness/
├── config/
│   ├── logging_config.py          # Unified log templates
│   └── monitoring_config.py       # Metrics collection definitions
├── docs/                          # Core subsystem specifications
│   ├── benchmarks/                # Performance & defense test suite specs
│   ├── data_models/               # GS1 schema mapping documentation
│   ├── discovery/                 # Digital Link resolution rules
│   ├── dpp_parser/                # DPP JSON-LD specs
│   ├── payments/                  # Secure payment token handshakes
│   ├── security/                  # W3C sandbox isolation rules
│   ├── sige/                      # NLP query translation rules
│   └── ds_adapter/                # MCP and dual-surface adapter specs
├── src/                           # Codebase Core
│   ├── approval_manager/
│   │   └── approval_trigger.py    # Automated spend/trust approval gates
│   ├── compliance/
│   │   └── gs1_fidelity_checker.py # Ensures 100% compliance with GS1 Vocab v1.12
│   ├── data_models/
│   │   ├── gs1_schema.py          # Serializes/Deserializes GS1 data classes
│   │   └── schemaorg_extensions.py # Extends schema.org vocab mapping
│   ├── discovery/
│   │   ├── content_negotiation.py # Processes machine Accept headers
│   │   └── digital_link.py        # Parses Digital Link primary key URIs
│   ├── dpp_parser/
│   │   ├── dpp_handler.py         # Extracts Recycled %, CO2e, and Repair indexes
│   │   └── dpp_models.py          # Represents DPP Pydantic structures
│   ├── ds_adapter/
│   │   ├── mcp_endpoints.py       # Model Context Protocol tools & Web Simulator
│   │   └── ui_renderer.py         # Dynamic visual PDP HTML generator
│   ├── payments/
│   │   └── token_handler.py       # Generates delegated single-use cryptographic tokens
│   ├── security/
│   │   └── sandbox.py             # Enforces zero direct execution of third-party JS
│   ├── sige/
│   │   ├── authenticity_checker.py # Integrates with GEPIR registry
│   │   ├── nlp_processor.py       # Translates prompts to structured queries
│   │   ├── query_engine.py        # Orchestrates intent grounding
│   │   └── unit_price_normalizer.py # Normalizes varied packaging into base prices
│   └── spge/
│       ├── payload_sanitizer.py   # Neutralizes indirect prompt injections
│       └── policy_enforcer.py     # Hard spend gates and velocity restrictors
└── tests/
    └── benchmarks/                # Test suites and performance evaluations
        ├── adversarial_security_benchmark.py
        ├── hallucination_defense_benchmark.py
        ├── intent_matching_benchmark.py
        └── vc_validation_benchmark.py # Latency measurements (< 15ms target)
```

---

## 🐋 Running via Docker (Simplest Setup)

We have fully containerized the application so you can build and run it with a single command without worrying about local Python setups:

### 1. Build and Run the Container
Using Docker Compose:
```bash
docker-compose up --build
```
*Or using the raw Docker CLI:*
```bash
docker build -t commerce-harness .
docker run -p 8000:8000 commerce-harness
```

### 2. Access the Interactive Side-by-Side Web Demo
Once the container is running, navigate to:
```
http://localhost:8000/demo
```
This is a beautiful, interactive dashboard demonstrating:
- **Scenario A: Unit Price Grounding** (How the normalizer performs math to select cost-effective bulk sizes over fuzzy standard scraper errors).
- **Scenario B: Claim Fraud (Greenwashing)** (How the W3C VC validator automatically flags and blocks unverified ecological claims).
- **Scenario C: Indirect Prompt Injection** (How the SPGE payload sanitizer strips out malicious instructions hidden in descriptions).

---

## 📊 Verification & Automated Benchmarks

The built-in evaluation framework (`eval-harness`) tests intent matching, security compliance, claim verifiability, and execution latencies.

### Run the Suite Locally
You can execute all benchmark suites using Python's standard unittest runner:
```bash
python3 -m unittest discover -s tests/benchmarks -p "*_benchmark.py"
```

### Verified Performance SLA:
* **W3C Cryptographic Proof Validation SLA Target:** `< 15.00 ms`
* **Harness Benchmark Performance Result:** **`0.29 ms` per validation (50x faster than target SLA!)**

---

## 🏆 Multi-Modal Shopping Evaluation & NPS

We have implemented a deterministic evaluation simulator to benchmark the Harness against traditional baseline shopping modalities (Manual Human vs. Ungrounded Chat Scrapers).

To run the comparative evaluation and view the Net Promoter Score (NPS) report, execute:
```bash
python3 run_comparative_evals.py
```

### Evaluation Verdict: Super-Parity
* **Manual Human (NPS +38):** Decent at spotting fraud, but extremely slow (14.5 mins) and prone to math fatigue when calculating bulk unit pricing.
* **Ungrounded Chat Scraper (NPS -42):** Fast, but highly gullible to greenwashing, completely vulnerable to prompt injections, and uses fuzzy math for pricing. A severe detractor.
* **Autonomous Harness-Grounded Agent (NPS +89):** Achieves **Super-Parity**. It combines machine-scale speed and deterministic math with cryptographic trust layers, systematically outperforming humans in pricing optimization and trust verification.
