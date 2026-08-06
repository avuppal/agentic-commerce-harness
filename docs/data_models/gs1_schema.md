# GS1 Web Vocabulary and Schema.org Extension

This document outlines the implementation of the GS1 Web Vocabulary and its extension with Schema.org for structured product data.

## Overview

The Autonomous Commerce Harness mandates that product data endpoints expose RDF/JSON-LD compliant structured data based on the [GS1 Web Vocabulary](http://gs1.org/voc/). This ensures machine-readable and deterministic product information for AI agents.

## Core Class Alignment

The implementation aligns with the following core GS1 classes:

*   `gs1:Product`
*   `gs1:Offer`
*   `gs1:Organization`
*   `gs1:Place`

## Mandated Attributes for Agent Processing

To facilitate agent processing and ensure data consistency, the following attributes are mandated:

*   **`gs1:gtin`**: Global Trade Item Number (13/14 digit canonical product identifier).
*   **`gs1:gpcCategoryCode`**: Global Product Classification code for accurate taxonomy indexing.
*   **`gs1:netContent`**: Quantified measures (e.g., mass, volume) to allow agent unit-price benchmarking.
*   **`gs1:allergenInformation`**: Structured allergen disclosures with explicit status (e.g., `CONTAINED_IN`, `FREE_FROM`, `MAY_CONTAIN`).
*   **`gs1:nutritionalAttribute`**: Standardized nutritional values per serving size.
*   **`gs1:countryOfOrigin`**: ISO country codes for supply chain validation.
