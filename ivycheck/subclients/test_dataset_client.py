from ..schemas import TestCaseDatasetCreate, TestCaseDatasetUpdate
from typing import Optional, Dict, List
from ivycheck.evaluator import Evaluator


class TestDatasetClient:
    def __init__(self, client):
        self.client = client

    def create(
        self,
        project_id: str,
        eval_llm: str = "gpt-4",
        rubrics: Optional[Dict[str, str]] = {},
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        assert project_id is not None, "Project Id is required."

        test_config = {}
        test_config["eval_llm"] = eval_llm  # get_llm_config_id_from_name(eval_llm)
        test_config["rubrics"] = rubrics

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

        self.id = response["id"]
        self.name = response.get("name")
        self.description = response.get("description")
        self.test_config = response.get("test_config")

        return self

    def evaluate(self, evaluator_description: str = None):
        # Create an Evaluator object for this test dataset instance
        evaluator = Evaluator.create(
            self.client,
            test_dataset_id=self.id,
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

        Assuming this `self` instance already has a reference to the dataset_id
        that we can use to link the test case to the dataset.
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

    def load(self, testdataset_id: str):
        """
        Load an existing test dataset by its ID.

        :param testdataset_id: The ID of the test dataset to load.
        """
        data = self.read(testdataset_id)

        # Assuming 'data' contains all the information about the test dataset,
        # including its ID, name, description, etc.
        self.id = data["id"]
        self.name = data.get("name")
        self.description = data.get("description")
        self.test_config = data.get("test_config")

        # Return the TestDatasetClient instance for method chaining
        return self
