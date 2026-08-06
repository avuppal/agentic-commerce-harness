# Semantic Intent Grounding Engine (SIGE) Overview

The Semantic Intent Grounding Engine (SIGE) is responsible for converting unstructured, ambiguous natural language requests into structured, verified, and authentic product query criteria.

## Core Capabilities

### 1. Ambiguous Request Translation (REQ-SIGE-01)
SIGE utilizes natural language processing (implemented in `src/sige/nlp_processor.py`) to map unstructured shopper prompts into structured, formal query attributes. 
* **Example Prompt:** *"Find some organic, gluten-free oat milk"*
* **Target Query Context:**
  ```json
  {
    "gs1:gpcCategoryCode": "Milk/Milk Substitutes",
    "gs1:allergenInformation": "FREE_FROM:Gluten",
    "claims": ["Organic"]
  }
  ```

### 2. Product Authenticity Matching (REQ-SIGE-02)
To eliminate fuzzy reasoning and protect against fraud, SIGE integrates with the **GS1 Verified by GS1 (GEPIR API)** registry.
* **GTIN Matching:** Resolves the brand manufacturer's identity directly from the global registry.
* **Fidelity validation:** Rejects product claims if the registered manufacturer does not match the claim controllers.

### 3. Unit Price Normalization (REQ-SIGE-03)
Different vendors package products in varying quantities (e.g. 100g, 1L, 16oz). SIGE integrates `src/sige/unit_price_normalizer.py` to:
* Parse diverse package descriptions or `gs1:netContent` fields.
* Perform mathematical conversion to standard base units (grams, milliliters, pieces).
* Expose normalized unit prices to the AI agent to allow exact cost-efficiency benchmarking.
