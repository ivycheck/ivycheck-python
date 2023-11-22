from ..schemas import TestCaseDatasetCreate, TestCaseDatasetUpdate
from typing import Optional, Dict


class TestDatasetClient:
    def __init__(self, client):
        self.client = client

    def create(
        self,
        project_id: str,
        eval_llm: str = "gpt-4",
        test_config: Optional[Dict] = {},
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        assert project_id is not None, "Project Id is required."

        test_config["eval_llm"] = eval_llm  # get_llm_config_id_from_name(eval_llm)

        # Use the Pydantic model to validate the input
        dataset_info = TestCaseDatasetCreate(
            prompt_id=project_id,  # mapping to old field name
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

    def delete(self, testdataset_id: str):
        endpoint = f"/test_case_datasets/{testdataset_id}"
        return self.client._make_request("DELETE", endpoint)

    def update(
        self,
        testcasedataset_id: str,
        test_config: Optional[Dict] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        # Internal validation with Pydantic
        test_case_data = TestCaseDatasetUpdate(
            test_config=test_config,
            name=name,
            description=description,
        )

        # Serialize the data for the request and exclude any unset fields
        json_data = test_case_data.model_dump(exclude_unset=True)

        # The endpoint for updating a test case dataset
        endpoint = f"/test_case_datasets/{testcasedataset_id}"

        # Make the API request
        return self._make_request("PUT", endpoint, json=json_data)

    def read(self, testcasedataset_id: str):
        endpoint = f"/test_case_datasets/{testcasedataset_id}"
        return self.client._make_request("GET", endpoint)

    def read_by_org(self):
        endpoint = f"/test_case_datasets/by_org/"
        return self.client._make_request("GET", endpoint)

    def read_by_prompt(self, prompt_id: str):
        endpoint = f"/test_case_datasets/by_prompt/{prompt_id}"
        return self.client._make_request("GET", endpoint)
