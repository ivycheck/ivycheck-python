from ..schemas import TestCaseDatasetCreate, TestCaseDatasetUpdate
from typing import Optional, Dict, List
from ivycheck.evaluator import Evaluator
from ivycheck.helperfunctions import remove_keys_from_dict_list


class TestDatasetClient:
    def __init__(self, client):
        self.client = client

    def create(
        self,
        project_id: str,
        eval_llm: str = "gpt-4",
        rubrics: Optional[Dict[str, str]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        assert project_id is not None, "Project Id is required."

        test_config = {}
        test_config["eval_llm"] = eval_llm  # get_llm_config_id_from_name(eval_llm)
        if rubrics is not None:
            test_config["rubrics"] = rubrics
        else:
            test_config["rubrics"] = {}

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

        response = self.client._make_request(
            "POST", "/test_case_datasets/", json=validated_data
        )

        self.project_id = project_id
        self.id = response["id"]
        self.name = response.get("name")
        self.description = response.get("description")
        self.test_config = response.get("test_config")

        return self

    def evaluate(
        self, evaluator_description: str = None, segments: Optional[Dict] = None
    ):
        if not self.id:
            raise ValueError("Dataset ID is not set.")

        # Create an Evaluator object for this test dataset instance
        evaluator = Evaluator.create(
            self.client,
            test_dataset_id=self.id,
            segments=segments,
            evaluator_description=evaluator_description,
        )

        return evaluator

    def add_test_case(
        self,
        input: Dict,
        message_history: Optional[List] = None,
        context: Optional[List] = None,
        golden_answer: Optional[str] = None,
        golden_context: Optional[List] = None,
        segments: Optional[Dict] = None,
        info: Optional[Dict] = None,
    ):
        """
        Add a test case to this dataset.

        """
        # Here, we assume self has an attribute `id` that stores the ID of the dataset.
        # If this is not currently the case, you need to make sure each instance of
        # TestDatasetClient has access to the dataset ID it's associated with.
        return self.client.TestCase.create(
            input=input,
            dataset_id=self.id,  # Use the dataset ID from the instance.
            message_history=message_history,
            context=context,
            golden_answer=golden_answer,
            golden_context=golden_context,
            segments=segments,
            info=info,
        )

    def delete(self, testdataset_id: str = None):
        dataset_id = testdataset_id or self.id
        if not dataset_id:
            raise ValueError("Dataset ID has not been set or provided.")
        endpoint = f"/test_case_datasets/{dataset_id}"
        return self.client._make_request("DELETE", endpoint)

    def update(
        self,
        test_config: Optional[Dict] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        testdataset_id: str = None,
    ):
        dataset_id = testdataset_id or self.id
        if not self.id:
            raise ValueError("Dataset ID has not been set.")

        test_case_data = TestCaseDatasetUpdate(
            test_config=test_config,
            name=name,
            description=description,
        )
        json_data = test_case_data.model_dump(exclude_unset=True)
        endpoint = f"/test_case_datasets/{self.id}"
        response = self.client._make_request("PUT", endpoint, json=json_data)

        # Optionally, update the instance's internal state with the new data
        self.name = name or self.name
        self.description = description or self.description
        self.test_config = test_config or self.test_config

        return self

    def _read(self, testdataset_id: str = None):
        dataset_id = testdataset_id or self.id
        if not dataset_id:
            raise ValueError("Dataset ID has not been set or provided.")
        endpoint = f"/test_case_datasets/{dataset_id}"
        response = self.client._make_request("GET", endpoint)
        # filter keys
        response["test_cases"] = remove_keys_from_dict_list(
            response["test_cases"], ["created_by", "updated_by", "owner_org"]
        )
        return response

    def load(self, testdataset_id: str):
        """
        Load an existing test dataset by its ID.

        :param testdataset_id: The ID of the test dataset to load.
        """
        data = self._read(testdataset_id)

        # Assuming 'data' contains all the information about the test dataset,
        # including its ID, name, description, etc.
        self.id = data["id"]
        self.name = data.get("name")
        self.description = data.get("description")
        self.test_config = data.get("test_config")
        self.project_id = data.get("prompt_id")

        # Return the TestDatasetClient instance for method chaining
        return self
