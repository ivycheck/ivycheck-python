import os
from typing import Optional
import requests
from .subclients.test_case_client import TestCaseClient
from .subclients.test_dataset_client import TestDatasetClient
from .subclients.evaluation_client import EvaluationClient
from .subclients.prompt_execution_client import PromptExecutionClient
from .subclients.evaluation_dataset_client import EvaluationDatasetClient
from .subclients.prompt_client import PromptClient
from ivycheck.helperfunctions import APIRequestError


# https://ivycheck-backend.onrender.com/
class IvyClient:
    """
    The main client class for interacting with the IvyCheck API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        print_output: bool = True,
    ) -> None:
        """
        :param api_key: The IvyCheck API key
        :param base_url: The base URL of the IvyCheck API. Defaults to the production API.
        :param print_output: Whether to print output to the console. Defaults to `True`.
        """
        self.base_url = base_url
        self.print_output = print_output

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

        # Initialize the different subclients
        self.TestDataset = TestDatasetClient(self)
        self.TestCase = TestCaseClient(self)
        self.Evaluation = EvaluationClient(self)
        self.EvaluationDataset = EvaluationDatasetClient(self)
        self.Prompt = PromptClient(self)
        self.PromptExecution = PromptExecutionClient(self)

    def _make_request(self, method: str, endpoint: str, stream=False, **kwargs):
        # Internal helper method to make HTTP requests
        url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, url, **kwargs)

        try:
            response.raise_for_status()  # Raise an exception for HTTP errors
            if stream:
                return response.iter_content(decode_unicode=True)
            else:
                return response.json()
        except requests.exceptions.HTTPError as http_err:
            # Attempt to extract error details from the response
            try:
                # Try to parse the response as JSON and extract the 'detail' field
                error_json = response.json()
                error_detail = error_json.get("detail", "No detail provided")
            except ValueError:
                # If response is not JSON or doesn't contain 'detail', use the text
                error_detail = response.text or "No detail provided"
            raise APIRequestError(
                f"HTTP error occurred: {http_err} - Detail: {error_detail}"
            ) from http_err
        except requests.exceptions.RequestException as req_err:
            # For non-HTTP exceptions, just pass the exception message
            raise APIRequestError(f"Request error occurred: {req_err}") from req_err

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
