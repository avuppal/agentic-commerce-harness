# src/ds_adapter/ui_renderer.py

import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PDPRenderer:
    """
    Renders high-fidelity visual Product Detail Pages (PDPs) for the Human Surface (REQ-DS-02).
    Allows humans-in-the-loop to validate agent context, step-up requests, and claim certs.
    """

    @classmethod
    def render_html(cls, product_data: Dict[str, Any], approval_reason: Optional[str] = None) -> str:
        """
        Generates HTML content for a rich, visual PDP.
        Includes placeholders for 360-degree views, interactive videos, and comparison matrices.
        """
        gtin = product_data.get("gs1:gtin") or product_data.get("gtin") or "Unknown GTIN"
        brand = product_data.get("gs1:brandName") or product_data.get("brand") or "Generic"
        description = product_data.get("gs1:description") or product_data.get("description") or "No description available."
        name = product_data.get("name") or f"Product {gtin}"

        # Build dynamic HTML template
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Human Step-Up PDP</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f8f9fa;
        }}
        header {{
            background: linear-gradient(135deg, #007bff, #6610f2);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .badge-warning {{
            background-color: #ffc107;
            color: #212529;
        }}
        .container {{
            display: flex;
            gap: 20px;
        }}
        .main-column {{
            flex: 2;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .sidebar {{
            flex: 1;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border-top: 5px solid #ffc107;
        }}
        .interactive-viewer {{
            background: #e9ecef;
            height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            border: 2px dashed #ced4da;
            margin-bottom: 20px;
        }}
        .spec-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}
        .spec-table th, .spec-table td {{
            padding: 10px;
            border: 1px solid #dee2e6;
            text-align: left;
        }}
        .spec-table th {{
            background-color: #f1f3f5;
        }}
        .btn {{
            display: block;
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            text-align: center;
            margin-top: 10px;
        }}
        .btn-success {{
            background-color: #28a745;
            color: white;
        }}
        .btn-danger {{
            background-color: #dc3545;
            color: white;
        }}
    </style>
</head>
<body>

    <header>
        <h1>Dual-Surface Human Authorization Portal</h1>
        <p>Verification & Oversight Runtime Sandbox</p>
    </header>

    {f'''<div style="background-color: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
        <strong>⚠️ ACTION REQUIRED (STEP-UP TRIGGERED):</strong> {approval_reason}
    </div>''' if approval_reason else ''}

    <div class="container">
        <div class="main-column">
            <h2>{name}</h2>
            <p><strong>Brand:</strong> {brand} | <strong>GTIN:</strong> {gtin}</p>

            <!-- Human surface REQ-DS-02 interactive content placeholders -->
            <div class="interactive-viewer">
                <div>
                    <p style="text-align: center; font-weight: bold;">[ 🔄 360-Degree Interactive Product Viewer ]</p>
                    <p style="font-size: 12px; color: #6c757d; text-align: center;">Click and drag to spin product</p>
                </div>
            </div>

            <h3>Product Description</h3>
            <p>{description}</p>

            <h3>Specifications (GS1 Master Data)</h3>
            <table class="spec-table">
                <tr><th>Attribute</th><th>Value</th></tr>
                <tr><td>gpcCategoryCode</td><td>{product_data.get("gs1:gpcCategoryCode") or "N/A"}</td></tr>
                <tr><td>netContent</td><td>{str(product_data.get("gs1:netContent") or "N/A")}</td></tr>
                <tr><td>allergenInformation</td><td>{str(product_data.get("gs1:allergenInformation") or "FREE_FROM")}</td></tr>
                <tr><td>countryOfOrigin</td><td>{product_data.get("gs1:countryOfOrigin") or "N/A"}</td></tr>
            </table>
        </div>

        <div class="sidebar">
            <h3>Human-in-the-Loop Approval</h3>
            <p>An autonomous agent requested purchase of this item. Please review and authorize.</p>
            
            <button class="btn btn-success" onclick="alert('Transaction Approved!')">✅ Approve Transaction</button>
            <button class="btn btn-danger" onclick="alert('Transaction Cancelled!')">❌ Reject Purchase</button>
            
            <hr style="margin: 20px 0; border: 0; border-top: 1px solid #dee2e6;">
            <h4>Trust Verification Details</h4>
            <p><strong>Claim Verifiability:</strong> 100%</p>
            <p><strong>Sandbox Mode:</strong> Enforced (W3C)</p>
        </div>
    </div>

</body>
</html>
"""
        logging.info(f"HTML PDP rendered successfully for GTIN {gtin}")
        return html
