# Dual-Surface Adapter (DS-Adapter) & Human Step-Up Interface

The Dual-Surface Adapter (DS-Adapter) is the critical module that allows the Autonomous Commerce Harness to serve both AI agents (via high-speed machine endpoints) and human managers (via visual validation interfaces) seamlessly.

## Dual Surfaces

```
                          [ GS1 Product Master Data ]
                                       |
                                       v
                                [ DS-Adapter ]
                                 /          \
                                /            \
                               v              v
               [ Machine Surface (MCP) ]     [ Human Surface (PDP) ]
               - Structured JSON-LD Graph     - Interactive Visual Web PDP
               - Target Latency: < 45ms       - 360-degree spinners
```

### 1. Machine Surface (REQ-DS-01)
* **Design:** Exposes Model Context Protocol (MCP) tool endpoints for LLM agents.
* **Payload:** Provides direct, unstyled JSON-LD response data optimized for machine semantic parsing.
* **Response Latency Target:** **< 45ms** (verified via latency benchmarks).

### 2. Human Surface (REQ-DS-02)
* **Design:** Dynamically renders rich, high-fidelity visual Product Detail Pages (PDPs).
* **Enhanced Content:** Integrates interactive components (such as 360-degree product views, comparison matrices, and video players) to facilitate quick and accurate human validation of claims and items.

---

## Step-Up Triggers & Workflow (REQ-DS-03)

Critical transactions or high-risk claims automatically halt the automated agent workflow and request human visual step-up approval:

1. **Order Cost Threshold:** When the total checkout amount exceeds the maximum allowed spend cap (e.g. `$X`).
2. **Claim Verification Score < 100%:** When product certification claims (e.g. Organic, Non-GMO) have incomplete or failing W3C Verifiable Credentials.
3. **Unverified Purchase Domains:** When an agent attempts to execute a purchase from a merchant domain that is not included on the organization's whitelist.

Upon trigger, the DS-Adapter suspends the execution thread and exposes the authorization state directly to the **Human Surface Portal** for manual override.
