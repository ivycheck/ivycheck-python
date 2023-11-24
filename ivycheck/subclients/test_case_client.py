from ..schemas import TestCaseCreate, TestCaseUpdate
from typing import Optional, Dict, List


class TestCaseClient:
    def __init__(self, client):
        self.client = client
        self.id = None  # Initialize self.id to store the TestCase ID

    # Create a test case and store its ID in the instance for further operations
    def create(
        self,
        input: Dict,
        dataset_id: str,
        message_history: Optional[List] = None,
        context: Optional[List] = None,
        golden_answer: Optional[str] = None,
        golden_context: Optional[List] = None,
        segments: Optional[Dict] = None,
        info: Optional[Dict] = None,
    ):
        assert dataset_id is not None, "Dataset Id is required."

        test_case_data = TestCaseCreate(
            input=input,
            dataset_id=dataset_id,
            message_history=message_history,
            context=context,
            golden_answer=golden_answer,
            golden_context=golden_context,
            segments=segments,
            info=info,
        )
        json_data = test_case_data.model_dump(exclude_unset=True)
        response = self.client._make_request("POST", "/test_cases/", json=json_data)

        self.id = response["id"]
        return self  # Return self to allow method chaining

    # Read a test case by its ID and load it into the instance
    def load(self, testcase_id: str):
        data = self._read(testcase_id)
        self.id = data["id"]
        # Load other relevant data into the instance as needed
        return self  # Return self to allow method chaining

    # Read a test case using the instance ID
    def _read(self, testcase_id: str = None):
        testcase_id = testcase_id or self.id
        if not testcase_id:
            raise ValueError("Test Case ID has not been set or provided.")
        endpoint = f"/test_cases/{testcase_id}"
        return self.client._make_request("GET", endpoint)

    # Update a test case and reflect the changes within the instance
    def update(
        self,
        input: Optional[Dict] = None,
        message_history: Optional[List] = None,
        context: Optional[List] = None,
        golden_answer: Optional[str] = None,
        golden_context: Optional[List] = None,
        segments: Optional[Dict] = None,
        info: Optional[Dict] = None,
        testcase_id: str = None,
    ):
        testcase_id = testcase_id or self.id
        if not testcase_id:
            raise ValueError("Test Case ID has not been set or provided.")

        test_case_data = TestCaseUpdate(
            input=input,
            message_history=message_history,
            context=context,
            golden_answer=golden_answer,
            golden_context=golden_context,
            segments=segments,
            info=info,
        )
        json_data = test_case_data.model_dump(exclude_unset=True)
        endpoint = f"/test_cases/{testcase_id}"
        response = self.client._make_request("PUT", endpoint, json=json_data)

        # Optionally update the instance's internal state with the new data

        return self  # Return self to allow method chaining

    # Delete using the instance ID
    def delete(self, testcase_id: str = None):
        testcase_id = testcase_id or self.id
        if not testcase_id:
            raise ValueError("Test Case ID has not been set or provided.")
        endpoint = f"/test_cases/{testcase_id}"
        return self.client._make_request("DELETE", endpoint)
