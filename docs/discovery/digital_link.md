# GS1 Digital Link URI Resolution & Content Negotiation

This document describes how the Autonomous Commerce Harness utilizes the GS1 Digital Link URI Standard to resolve product identifiers and dynamically route requests based on HTTP Accept headers.

## 1. Primary Key Discovery & Resolution

The harness uses the GS1 Digital Link URI format as the universal primary key for product discovery, resolution, and Digital Product Passport (DPP) retrieval.

### Canonical URI Structure
```
https://id.brand.com/01/{GTIN}/10/{BATCH}/21/{SERIAL}
```

* **`01`**: Global Trade Item Number (GTIN-13/14)
* **`10`**: Batch/Lot Number (Optional)
* **`21`**: Serial Number (Optional)

## 2. Dynamic Content Negotiation (Accept Headers)

The resolver dynamically negotiates payload formats based on HTTP `Accept` headers to optimize for both machines (AI Agents) and humans:

1. **`Accept: application/ld+json`** (AI Agents)
   * Resolves to direct, unstyled JSON-LD graph data compliant with the **GS1 Web Vocabulary v1.12**.
2. **`Accept: application/vc+ld+json`** (Cryptographic Claims/DPP Verification)
   * Returns W3C Verifiable Credentials datasets representing ecological, health, or compliance claims.
3. **`Accept: text/html`** (Human oversight)
   * Triggers redirection to the human-optimized visual Product Detail Page (PDP).

## 3. Linkset Redirection Relationship Types (rel)

Redirection headers contain standard link relation types (`rel`):
* **`gs1:pip`**: Product Information Page (HTML PDP).
* **`gs1:dpp`**: Digital Product Passport (JSON-LD endpoint).
* **`gs1:certificationInfo`**: Verifiable Credentials issuer endpoint.
