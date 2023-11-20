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

    def create_test_case_dataset(
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

        headers = {"Authorization": f"Bearer {self.api_key}"}

        url = self.base_url.rstrip("/") + "/test_case_datasets/"

        response = requests.post(url, headers=headers, json=validated_data)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def delete_test_dataset():
        pass

    def update_test_dataset():
        pass

    def read_test_dataset():
        pass
