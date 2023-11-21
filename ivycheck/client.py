import os
import requests
from .models import TestCaseDatasetCreate
from typing import Optional, Dict


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
        self.TestDataset = TestDataset(self)

    def _make_request(self, method: str, endpoint: str, **kwargs):
        # Internal helper method to make requests
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)

        if response.ok:
            return response.json() if not kwargs.get("stream", False) else response
        else:
            response.raise_for_status()

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


class TestDataset:
    def __init__(self, client):
        self.client = client

    def create(
        self,
        prompt_id: Optional[str] = None,
        test_config: Optional[Dict] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        # Use the Pydantic model to validate the input
        dataset_info = TestCaseDatasetCreate(
            prompt_id=prompt_id,
            test_config=test_config,
            name=name,
            description=description,
        )
        validated_data = dataset_info.model_dump(
            exclude_none=True
        )  # Exclude fields that are None

        return self.client._make_request(
            "POST", "/test_case_datasets/", json=validated_data
        )

    def delete():
        pass

    def update():
        pass

    def read():
        pass
