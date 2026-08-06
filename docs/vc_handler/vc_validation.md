# Verifiable Credentials (VCs) Integration and Verification

This document outlines the integration and verification procedures for Verifiable Credentials (VCs) within the Autonomous Commerce Harness.

## 1. Purpose of VCs

Verifiable Credentials are used to cryptographically back certified product claims, such as "Organic", "Fair Trade", "Halal", "Energy Star", and "Carbon Neutral". This mechanism eliminates the risk of "greenwashing" and prevents AI agents from acting on hallucinated marketing claims found in unverified product descriptions.

## 2. VC Structure and Components

VCs adhere to the W3C Verifiable Credentials Data Model. Key components include:

*   **Issuer**: The issuer of a VC must be an accredited certification body. This body must possess a public Decentralized Identifier (DID), such as `did:key` or `did:web`, which can be used to verify the issuer's authenticity.
*   **Proof**: Each VC must contain a cryptographic signature attached to its JSON-LD payload. Common signature suites include `Ed25519Signature2020` or `ECDSA`. This signature ensures the integrity and authenticity of the VC.

## 3. Agent Verification Workflow

AI agents follow a defined workflow to verify the authenticity and validity of VCs:

1.  **Fetch VC Payload**: The agent retrieves the VC's JSON-LD payload.
2.  **Extract Claim DID**: The Decentralized Identifier (DID) of the claim is extracted from the VC.
3.  **Verify Cryptographic Signature**: The agent verifies the VC's cryptographic signature against the issuer's DID Document, ensuring the VC has not been tampered with and was indeed issued by the claimed entity.
4.  **Check Revocation Status**: The agent checks the VC's revocation status, typically using mechanisms like `StatusList2021`, to ensure the credential is still valid and has not been revoked.
5.  **Outcome**: Upon successful verification, the agent receives a `CLAIM_VERIFIED` signal. If any step fails, the claim is considered invalid.

## 4. Integration with GS1 Digital Link

VCs can be retrieved as part of the data offered through the GS1 Digital Link standard. When querying a GS1 Digital Link URI, agents can request VC data using the `Accept` header:

*   `Accept: application/vc+ld+json`: This header specifically requests the Verifiable Credentials associated with the product.

Additionally, the GS1 Digital Link specification provides a link relation type, `gs1:certificationInfo`, which can point to the VC issuer's endpoint.

## 5. Relationship with Digital Product Passports (DPP)

While VCs provide verification for specific claims and certifications, they complement the data within Digital Product Passports (DPPs). DPPs focus on broader product lifecycle information, such as Bill of Materials, carbon footprint, and repairability. The verified claims from VCs can enrich DPP data, especially for evaluating products against corporate Environmental, Social, and Governance (ESG) policies.