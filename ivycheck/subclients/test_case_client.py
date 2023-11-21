from ..schemas import TestCaseCreate, TestCaseUpdate
from typing import Optional, Dict, List


class TestCaseClient:
    def __init__(self, client):
        self.client = client

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
        return self.client._make_request("POST", "/test_cases/", json=json_data)

    def read(self, testcase_id: str):
        endpoint = f"/test_cases/{testcase_id}"
        return self.client._make_request("GET", endpoint)

    def update(
        self,
        testcase_id: str,
        input: Optional[Dict] = None,
        message_history: Optional[List] = None,
        context: Optional[List] = None,
        golden_answer: Optional[str] = None,
        golden_context: Optional[List] = None,
        segments: Optional[Dict] = None,
        info: Optional[Dict] = None,
    ):
        test_case_data = TestCaseUpdate(
            input=input,
            message_history=message_history,
            context=context,
            golden_answer=golden_answer,
            golden_context=golden_context,
            segments=segments,
            info=info,
        )
        json_data = test_case_data.dict(exclude_unset=True)
        endpoint = f"/test_cases/{testcase_id}"
        return self.client._make_request("PUT", endpoint, json=json_data)

    def delete(self, testcase_id: str):
        endpoint = f"/test_cases/{testcase_id}"
        return self.client._make_request("DELETE", endpoint)

    def read_testcases_by_org(self):
        """
        Retrieves a list of test cases associated with the organization of the authed user.
        """
        endpoint = "/test_cases/by_org/"
        return self.client._make_request("GET", endpoint)

    def read_testcases_by_prompt(self, prompt_id: str):
        """
        Retrieves a list of test cases associated with a specific prompt_id.

        :param prompt_id: The ID of the prompt.
        """
        endpoint = f"/test_cases/by_prompt/{prompt_id}"
        return self.client._make_request("GET", endpoint)

    def read_testcases_by_dataset(self, dataset_id: str):
        """
        Retrieves a list of test cases associated with a specific dataset_id.

        :param dataset_id: The ID of the dataset.
        """
        endpoint = f"/test_cases/by_dataset/{dataset_id}"
        return self.client._make_request("GET", endpoint)
