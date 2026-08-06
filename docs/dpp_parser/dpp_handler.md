# Digital Product Passport (DPP) JSON-LD Parsing

This document outlines the capabilities and expected behavior of the DPP handler component responsible for parsing and processing Digital Product Passport (DPP) data in JSON-LD format.

## 1. DPP Schema Requirements

The DPP data is expected to conform to the schema requirements mandated by the EU Ecodesign for Sustainable Products Regulation (ESPR). This includes, but is not limited to:

*   **Bill of Materials (BOM):** Detailed information on recycled content percentages.
*   **Carbon Footprint:** Data aligned with ISO 14067 / GHG Protocol, covering each lifecycle phase.
*   **Repairability Index:** A score (typically 1-10) indicating the product's repairability.
*   **Circularity Instructions:** Guidance on product end-of-life and circular economy practices.

## 2. Interaction with GS1 Digital Link

The DPP handler retrieves DPP data by processing responses from the GS1 Digital Link service. Specifically, it identifies and extracts DPP information by looking for the `gs1:dpp` link relation type within the Linkset Redirection headers, as described in section 3.2 of the Product Requirement Document.

## 3. Parsing and Validation Logic

The `dpp_handler` component is responsible for the following:

*   **JSON-LD Extraction:** It parses the JSON-LD payload associated with the DPP, extracting the required fields corresponding to the schema requirements mentioned above.
*   **Data Transformation:** Performs any necessary data transformations to standardize or normalize the extracted information for downstream consumption.
*   **Integrity and Completeness Validation:** Validates the DPP data against expected standards and business rules to ensure its accuracy and completeness. This is critical for reliable use by agents.

## 4. Agent Utility Integration

The output of the `dpp_handler` is designed to be directly consumable by AI agents. The parsed and validated DPP data enables agents to:

*   Evaluate product compliance against corporate Environmental, Social, and Governance (ESG) policies.
*   Filter out SKUs that do not meet specific ESG criteria prior to initiating a purchase.

This ensures that procurement decisions are aligned with sustainability and regulatory requirements.