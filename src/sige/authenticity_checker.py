import httpx

class GEPIRClient:
    def __init__(self, base_url: str = "https://api.gs1.org/gepir/v1/"):
        self.base_url = base_url
        self.client = httpx.Client()

    def check_product_authenticity(self, gtin: str) -> dict:
        """
        Checks product authenticity using the GEPIR API.

        Args:
            gtin: The Global Trade Item Number (GTIN) of the product.

        Returns:
            A dictionary containing the API response.
        """
        endpoint = f"products?gtin={gtin}"
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.client.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return {"error": str(e)}
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {url}: {e}")
            return {"error": str(e)}

    def close(self):
        self.client.close()

if __name__ == "__main__":
    # Example usage:
    gepir_client = GEPIRClient()
    # Replace '078900000107' with a valid GTIN for testing
    gtin_to_check = "078900000107"
    authenticity_data = gepir_client.check_product_authenticity(gtin_to_check)
    print(f"Authenticity check for GTIN {gtin_to_check}:\n{authenticity_data}")
    gepir_client.close()
