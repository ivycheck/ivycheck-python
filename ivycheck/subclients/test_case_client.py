from ..schemas import TestCaseCreate, TestCaseUpdate
from typing import Optional, Dict, List


class TestCaseClient:
    """
    Provides an interface to create, read, and delete test cases.
    """

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
        """
        Create a new test case.

        :param input: The input to the model. Example: `{"user_input": "How can I cancel my subscription online?"}`
        :param dataset_id: The ID of the dataset to add the test case to.
        :param message_history: The message history of the conversation. Example: `[{"role": "system", "content": "You are a helpful assistant."}]`
        :param context: Additional context of the conversation. Can contain retrieved documents provided as list of dictionaries. Example: `[{"title": "How to cancel your subscription", "url": "https://example.com/cancel-subscription"}]`
        :param golden_answer: The golden answer for the test case. This is the correct response to the input.
        :param golden_context: The golden context for the test case. This is the expected context for the input. Useful if you want to evaluate if the system retrieved the correct documents.
        :param segments: A dictionary of segments to filter the test cases. Example: `{"customer": "Amazon"}`
        :param info: Any additional information to store with the test case.
        """
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
        """
        Load a test case

        :param testcase_id: The ID of the test case to load.
        """
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
    def delete(self, testcase_id: str):
        """
        Delete a test case

        :param testcase_id: The ID of the test case to delete.
        """
        # testcase_id = testcase_id or self.id
        if not testcase_id:
            raise ValueError("Test Case ID has not been set or provided.")
        endpoint = f"/test_cases/{testcase_id}"
        return self.client._make_request("DELETE", endpoint)
