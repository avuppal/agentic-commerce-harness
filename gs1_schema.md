

## Structured Intent Query Model

This model defines the structure for agent-driven intent queries, enabling precise filtering and preference matching. It includes a category code for initial product filtering, a list of hard constraints that must be met, and a list of soft preferences for ranking and scoring.

```json
{
  "@context": "http://gs1.org/voc/",
  "@type": "StructuredIntentQuery",
  "gpcCategoryCode": "10000169", // Milk & Cream (Fresh)
  "hardConstraints": {
    "allergenInformation": "FREE_FROM:Gluten"
  },
  "softPreferences": {
     "claim": "USDA Organic"
  }
}
```
