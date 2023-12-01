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
        rubrics: List[Dict[str, str]] = [],
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        """
        Create a new test dataset inside an existing project.

        Example:
        ```python
        test_dataset = ivy.TestDataset.create(
            project_id="abcdef",
            eval_llm="gpt-4",
            name="Test ChatBot with rubric instructions",
            description="Our standard test cases for ChatBot evaluation",
            rubrics=[
                {
                    "name": "Politeness",
                    "instruction": "Is the response polite?",
                },
                {
                    "name": "Humour",
                    "instruction": "Is the response funny or entertaining?",
                },
            ],
        )
        ```

        :param project_id: The ID of the project to create the test dataset in.
        :param eval_llm: The LLM to use for evaluation.
        :param rubrics: The rubrics to use for evaluation. A dictionary of rubric names and instructions. Example: `[{"name": "Accuracy", "instruction": "Is the response accurate?"}]`
        :param name: The name of the test dataset.
        :param description: The description of the test dataset.
        """
        assert project_id is not None, "Project Id is required."

        test_config = {}
        test_config["eval_llm"] = eval_llm  # get_llm_config_id_from_name(eval_llm)
        test_config["rubrics"] = rubrics

        test_config = self._format_test_config(test_config)

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
        """
        Create an [Evaluator](#evaluator) object for this test dataset. After creating the evaluator, you can use the [`test_case_iterator`](#test-case-iterator) method to iterate over the test cases and evaluate them.

        :param evaluator_description: The description of the evaluation. Use it to describe what you are evaluating.
        :param segments: A dictionary of segments to filter the test cases. Example: `{"customer": "Amazon"}`
        """
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

        Example:
        ```python
        test_dataset.add_test_case(
            input={"user_input": "How can I cancel my subscription online?"},
            segments={"customer": "ChatBotUser", "difficulty": "easy"},
        )
        ```

        :param input: The input to the model. Example: `{"user_input": "How can I cancel my subscription online?"}`
        :param message_history: The message history of the conversation. Example: `[{"role": "system", "content": "You are a helpful assistant."}]`
        :param context: Additional context of the conversation. Can contain retrieved documents provided as list of dictionaries. Example: `[{"title": "How to cancel your subscription", "url": "https://example.com/cancel-subscription"}]`
        :param golden_answer: The golden answer for the test case. This is the correct response to the input.
        :param golden_context: The golden context for the test case. This is the expected context for the input. Useful if you want to evaluate if the system retrieved the correct documents.
        :param segments: A dictionary of segments to filter the test cases. Example: `{"customer": "Amazon"}`
        :param info: Any additional information to store with the test case.
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
        """
        Delete a test case dataset.

        :param testdataset_id: The ID of the test dataset to delete.
        """
        # dataset_id = testdataset_id or self.id
        if not testdataset_id:
            raise ValueError("Dataset ID has not been set or provided.")
        endpoint = f"/test_case_datasets/{testdataset_id}"
        return self.client._make_request("DELETE", endpoint)

    def add_rubric(self, name: str, instruction: str):
        """
        Add an evaluation rubric to this test dataset.

        :param name: The name of the rubric.
        :param instruction: The instruction for how to evaluate the rubric.
        """
        test_config = self.test_config
        rubrics = test_config.get("rubrics", [])
        rubrics.append({"name": name, "description": instruction})
        test_config["rubrics"] = rubrics
        self.update(test_config=test_config)

    def delete_rubric(self, name: str):
        """
        Delete an evaluation rubric from this test dataset.

        :param name: The name of the rubric to delete.
        """
        test_config = self.test_config
        rubrics = test_config.get("rubrics", [])
        rubrics = [rubric for rubric in rubrics if rubric["name"] != name]
        test_config["rubrics"] = rubrics
        self.update(test_config=test_config)

    def set_eval_llm(self, eval_llm: str):
        """
        Set the LLM to use for evaluation.

        :param eval_llm: The LLM to use for evaluation. Example: `gpt-4`
        """
        test_config = self.test_config
        test_config["eval_llm"] = eval_llm
        self.update(test_config=test_config)

    def update(
        self,
        test_config: Optional[Dict] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        testdataset_id: Optional[str] = None,
    ):
        """
        Update this test dataset.

        :param test_config: The test config to update. Example: `{"eval_llm": "gpt-4"}`
        :param name: The name of the test dataset.
        :param description: The description of the test dataset.
        :param testdataset_id: The ID of the test dataset to update.
        """
        dataset_id = testdataset_id or self.id
        if not dataset_id:
            raise ValueError("Dataset ID has not been set.")

        test_case_data = TestCaseDatasetUpdate(
            test_config=test_config or self.test_config,
            name=name or self.name,
            description=description or self.description,
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

    @classmethod
    def _format_test_config(cls, test_config):
        """Rename the instruction field to description for backend compatibility"""
        if "rubrics" in test_config:
            for rubric in test_config["rubrics"]:
                if "instruction" in rubric:
                    rubric["description"] = rubric.pop("instruction")
        return test_config
