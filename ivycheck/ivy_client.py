import os
import requests
from .subclients.test_case_client import TestCaseClient
from .subclients.test_dataset_client import TestDatasetClient


# https://ivycheck-backend.onrender.com/
class IvyClient:
    def __init__(self, api_key=None, base_url=None) -> None:
        self.base_url = base_url

        if api_key is None:
            api_key = os.getenv("IVYCHECK_API_KEY")

        if api_key is None:
            raise ValueError(
                "API_KEY is not passed and not set in the environment variables"
            )
        self.api_key = api_key

        if base_url is None:
            if os.getenv("IVYCHECK_BASE_URL") is None:
                self.base_url = "https://ivycheck-backend.onrender.com/"
            else:
                self.base_url = os.getenv("IVYCHECK_BASE_URL")
        else:
            self.base_url = base_url

        self.base_url = self.base_url.rstrip("/")

        # Initialize a session object for connection pooling and session-wide configurations
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})

        # Initialie the differen subclients
        self.TestDataset = TestDatasetClient(self)
        self.TestCase = TestCaseClient(self)

    def _make_request(self, method: str, endpoint: str, **kwargs):
        # Internal helper method to make requests
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)

        response.raise_for_status()  # Raise an error for bad HTTP status codes
        return response.json()

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

        data = {
            "slug": slug,
            "stage": stage,
            "version": version,
            "field_values": field_values,
            "stream": stream,
            "raw_response": raw_response,
        }

        return self._make_request("POST", "/api/v1/complete", json=data, stream=stream)

    def check_endpoint_health(self):
        """Check the health of the endpoint."""
        return self._make_request("GET", "/api/v1/health")
