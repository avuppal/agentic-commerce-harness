# src/ds_adapter/mcp_endpoints.py

import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Safe import fallback for pyld
try:
    from pyld import jsonld
    HAS_PYLD = True
except ImportError:
    logging.warning("pyld library not found. Falling back to native JSON-LD serialization.")
    HAS_PYLD = False

# Import harness modules to expose them as MCP tools
from src.discovery.digital_link import DigitalLink
from src.vc_handler.vc_validator import VerifiableCredentialValidator
from src.sige.unit_price_normalizer import UnitPriceNormalizer
from src.spge.payload_sanitizer import PayloadSanitizer
from src.spge.policy_enforcer import PolicyEnforcer

app = FastAPI(
    title="Autonomous Commerce Harness MCP Server",
    description="Model Context Protocol (MCP) and Machine Surface exposing GS1, W3C, and SPGE tools.",
    version="1.0.0"
)

# Mock databases for demonstration and integration
mock_products = {
    "1234567890123": {
        "@context": "https://gs1.org/voc/",
        "@id": "urn:product:1234567890123",
        "@type": "Product",
        "gs1:gtin": "1234567890123",
        "gs1:brandName": "OrganicHarvest",
        "gs1:description": "100% Organic Cold Pressed Almond Milk. Verified Non-GMO.",
        "gs1:gpcCategoryCode": "50131700",  # Milk/Milk Substitutes
        "gs1:netContent": {
            "@type": "QuantitativeValue",
            "gs1:value": 946,
            "gs1:unitCode": "ml"
        },
        "gs1:countryOfOrigin": "US",
        "gs1:allergenInformation": [
            {
                "@type": "gs1:Allergen",
                "gs1:allergen": "Almonds",
                "gs1:allergenStatus": "CONTAINS"
            }
        ]
    }
}

# --- Request Schemas for Tool Calls ---
class DigitalLinkRequest(BaseModel):
    uri: str

class VCValidationRequest(BaseModel):
    credential_data: Dict[str, Any]

class UnitPriceRequest(BaseModel):
    price: float
    net_content: Any

class SanitizeRequest(BaseModel):
    text: str

class PurchasePolicyRequest(BaseModel):
    amount: float
    domain: str
    category: str


# --- Tool Definition Directory ---
mcp_tools = [
    {
        "name": "getProductData",
        "description": "Retrieves product master data in GS1 Web Vocabulary JSON-LD format using its GTIN.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "gtin": {"type": "string", "description": "The 13 or 14-digit Global Trade Item Number."}
            },
            "required": ["gtin"]
        }
    },
    {
        "name": "resolveDigitalLink",
        "description": "Parses and resolves a GS1 Digital Link URI, extracting GTIN, serials, and acceptable content negotiation headers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "uri": {"type": "string", "description": "The canonical GS1 Digital Link URI."}
            },
            "required": ["uri"]
        }
    },
    {
        "name": "validateCredential",
        "description": "Cryptographically validates a W3C Verifiable Credential, checking the signature, issuer DID, and StatusList2021 revocation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "credential_data": {"type": "object", "description": "The full W3C Verifiable Credential JSON dictionary."}
            },
            "required": ["credential_data"]
        }
    },
    {
        "name": "normalizeUnitPrice",
        "description": "Parses net content (QuantitativeValue/string) and normalizes product prices to base units ($/g, $/ml, $/count) for benchmarking.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "price": {"type": "number", "description": "The total retail price of the offer."},
                "net_content": {"type": "object", "description": "The net content object or string."}
            },
            "required": ["price", "net_content"]
        }
    },
    {
        "name": "sanitizePayload",
        "description": "Sanitizes unverified text descriptions to prevent indirect prompt injection attacks prior to parsing.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The unverified description or product title."}
            },
            "required": ["text"]
        }
    },
    {
        "name": "checkPurchasePolicy",
        "description": "Evaluates spend thresholds, velocity controls, and domain whitelists to ensure strict financial policy compliance.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "amount": {"type": "number", "description": "The transaction amount in USD equivalent."},
                "domain": {"type": "string", "description": "The vendor domain executing the sale."},
                "category": {"type": "string", "description": "The classification category of the product."}
            },
            "required": ["amount", "domain", "category"]
        }
    }
]


# --- REST & MCP Endpoint Routers ---

@app.get("/mcp/tools", response_model=List[dict])
async def list_tools():
    """Exposes all available Model Context Protocol tools to LLM Agents (REQ-DS-01)."""
    logging.info("Listing MCP tools requested.")
    return mcp_tools


@app.get("/mcp/tools/product/{gtin}")
async def get_product_data(gtin: str, request: Request):
    """Retrieves product master data by GTIN. Uses Accept header context (REQ-DS-01)."""
    product = mock_products.get(gtin)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with GTIN {gtin} not found.")

    accept_header = request.headers.get("accept", "")
    
    # Process using PyLD if available, else native dictionary output
    if HAS_PYLD and "application/ld+json" in accept_header:
        try:
            compacted = jsonld.compact(product, product.get("@context"))
            return JSONResponse(content=compacted, media_type="application/ld+json")
        except Exception as e:
            logging.error(f"PyLD compaction failure: {e}")
            return JSONResponse(content=product, media_type="application/ld+json")
    
    # Standard JSON-LD response
    return JSONResponse(content=product, media_type="application/ld+json")


@app.post("/mcp/tools/resolve-link")
async def resolve_link(payload: DigitalLinkRequest):
    """MCP tool wrapper for resolving and routing GS1 Digital Link URIs."""
    try:
        resolver = DigitalLink(payload.uri)
        parsed = resolver.parse()
        route = resolver.route()
        return {
            "status": "success",
            "parsed_components": parsed,
            "route_action": route
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to resolve digital link: {e}")


@app.post("/mcp/tools/validate-vc")
async def validate_vc(payload: VCValidationRequest):
    """MCP tool wrapper for cryptographically validating W3C Verifiable Credentials."""
    try:
        validator = VerifiableCredentialValidator()
        result = validator.validate(payload.credential_data)
        return {
            "status": "success",
            "validation_result": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"VC Validation failed: {e}")


@app.post("/mcp/tools/normalize-price")
async def normalize_price(payload: UnitPriceRequest):
    """MCP tool wrapper for unit price normalizations across package boundaries."""
    try:
        normalizer = UnitPriceNormalizer()
        result = normalizer.normalize(payload.price, payload.net_content)
        if not result:
            raise ValueError("Incompatible net content structure.")
        return {
            "status": "success",
            "normalization": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Normalization failed: {e}")


@app.post("/mcp/tools/sanitize")
async def sanitize_text(payload: SanitizeRequest):
    """MCP tool wrapper to filter indirect prompt injections from product data."""
    try:
        sanitized = PayloadSanitizer.sanitize(payload.text)
        return {
            "status": "success",
            "original_text": payload.text,
            "sanitized_text": sanitized,
            "neutralized": sanitized != payload.text
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Sanitization failed: {e}")


@app.post("/mcp/tools/check-policy")
async def check_policy(payload: PurchasePolicyRequest):
    """MCP tool wrapper to validate spend thresholds, domain whitelist compliance, and rate limiting."""
    try:
        # Load a default policy config
        policy_config = {
            "spend_limit": 1000.0,
            "velocity_window": "daily",
            "whitelist_domains": ["organic-retail.com", "trusted-merchant.com", "brand.com"]
        }
        enforcer = PolicyEnforcer(policy_config)
        
        # Enforce spend limits
        spend_ok = enforcer.enforce_spend_limit(payload.amount)
        # Enforce domain validation
        domain_ok = enforcer.enforce_velocity_controls(1, payload.domain) # 1 transaction
        
        is_allowed = spend_ok and domain_ok
        
        return {
            "status": "success",
            "allowed": is_allowed,
            "checks": {
                "spend_limit_passed": spend_ok,
                "domain_whitelist_passed": domain_ok
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Policy enforcement evaluation failed: {e}")
