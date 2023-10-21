import os
import requests


class IvyClient:
    def __init__(
        self, api_key, base_url="https://ivycheck-backend.onrender.com/"
    ) -> None:
        self.base_url = base_url

        if api_key is None:
            api_key = os.getenv("IVYCHECK_API_KEY")

        if api_key is None:
            raise ValueError(
                "API_KEY is not passed and not set in the environment variables"
            )

        self.api_key = api_key

    def complete(self, slug, field_values, stage=None, version=None):
        """Call to openai completion API."""

        url = self.base_url + "api/v1/complete"

        headers = {"Authorization": f"Bearer {self.api_key}"}

        data = {
            "slug": slug,
            "stage": stage,
            "version": version,
            "field_values": field_values,
        }

        response = requests.post(url, headers=headers, json=data)
        
        return response.json()

    def check_endpoint_health(self):
        """Check the health of the endpoint."""

        url = self.base_url + "api/v1/health"

        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.get(url, headers=headers)

        return response.json()
