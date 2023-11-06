import os
import requests


# https://ivycheck-backend.onrender.com/
class IvyClient:
    def __init__(self, api_key, base_url="http://localhost:8000/") -> None:
        self.base_url = base_url

        if api_key is None:
            api_key = os.getenv("IVYCHECK_API_KEY")

        if api_key is None:
            raise ValueError(
                "API_KEY is not passed and not set in the environment variables"
            )

        self.api_key = api_key

    def complete(
        self,
        slug,
        field_values,
        stage=None,
        version=None,
        stream=False,
        raw_response=False,
    ):
        """Call to openai completion API."""

        url = self.base_url + "api/v1/complete"

        headers = {"Authorization": f"Bearer {self.api_key}"}

        data = {
            "slug": slug,
            "stage": stage,
            "version": version,
            "field_values": field_values,
            "stream": stream,
            "raw_response": raw_response,
        }

        # handle streaming vs non-streaming here.
        # if streaming: json.loads(response.text) or response.json()
        response = requests.post(url, headers=headers, json=data, stream=stream)

        return response

    def check_endpoint_health(self):
        """Check the health of the endpoint."""

        url = self.base_url + "api/v1/health"

        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.get(url, headers=headers)

        return response.json()
