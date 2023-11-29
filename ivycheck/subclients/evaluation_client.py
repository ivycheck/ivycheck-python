from ..schemas import EvaluationCreate, EvaluationUpdate
from typing import Optional, Dict


class EvaluationClient:
    """
    Provides an interface to create, read, and delete evaluations.
    """

    def __init__(self, client):
        self.client = client
        self.id = None
        self.test_case_id = None
        self.evaluation_dataset_id = None
        self.evaluation_result = None
        self.output = None
        self.config = None

    def create_and_run(
        self,
        test_case_id: str,
        evaluation_dataset_id: str,
        output: str,
        # evaluation_result: Optional[Dict] = None,
        # config: Optional[Dict] = None,
        run_in_background: bool = True,
    ):
        """
        Submit an LLM output for evaluation.

        :param test_case_id: The ID of the executed test case.
        :param evaluation_dataset_id: The ID of the evaluation dataset to add this evaluation to.
        :param output: The output of the LLM.
        :param run_in_background: Whether to run the evaluation in the background. Default: `True`. If set to `False`, the evaluation will be run synchronously and the response will contain the evaluation result.
        """
        evaluation_data = EvaluationCreate(
            test_case_id=test_case_id,
            evaluation_dataset_id=evaluation_dataset_id,
            # config=config,
            # evaluation_result=evaluation_result,
            output={"response": output},
        )

        params = {"run_in_background": run_in_background}

        endpoint = f"/evaluations/create_and_run/"

        response = self.client._make_request(
            "POST",
            endpoint,
            json=evaluation_data.model_dump(exclude_none=True),
            params=params,
        )

        # Store the evaluation-related properties after creation.
        self.id = response["id"]
        self.test_case_id = response.get("test_case_id")
        self.evaluation_dataset_id = response.get("evaluation_dataset_id")
        self.evaluation_result = response.get("evaluation_result")
        self.output = response.get("output")
        self.config = response.get("config")

        return self

    def _read(self, evaluation_id: str = None):
        evaluation_id = evaluation_id or self.id
        if not evaluation_id:
            raise ValueError("Evaluation ID has not been set or provided.")
        endpoint = f"/evaluations/{evaluation_id}"
        return self.client._make_request("GET", endpoint)

    def _update(
        self,
        evaluation_id: Optional[str] = None,
        test_case_id: Optional[str] = None,
        evaluation_dataset_id: Optional[str] = None,
        evaluation_result: Optional[Dict] = None,
        output: Optional[Dict] = None,
        config: Optional[Dict] = None,
    ):
        evaluation_id = evaluation_id or self.id
        if not evaluation_id:
            raise ValueError("Evaluation ID has not been set or provided.")

        attrs_to_update = {
            "test_case_id": test_case_id,
            "evaluation_dataset_id": evaluation_dataset_id,
            "evaluation_result": evaluation_result,
            "output": output,
            "config": config,
        }
        # Only include attributes that are not None for the update,
        # to avoid overwriting attributes that aren't intended to be changed.
        attrs_to_update = {k: v for k, v in attrs_to_update.items() if v is not None}

        evaluation_data = EvaluationUpdate(**attrs_to_update)
        endpoint = f"/evaluations/{evaluation_id}"
        response = self.client._make_request(
            "PUT", endpoint, json=evaluation_data.model_dump()
        )

        # Optionally, update the instance's internal state with the new data.
        self.test_case_id = test_case_id or self.test_case_id
        self.evaluation_dataset_id = evaluation_dataset_id or self.evaluation_dataset_id
        self.evaluation_result = evaluation_result or self.evaluation_result
        self.output = output or self.output
        self.config = config or self.config

        return self

    def delete(self, evaluation_id: str):
        """
        Delete an evaluation.

        :param evaluation_id: The ID of the evaluation to delete.
        """
        # evaluation_id = evaluation_id or self.id
        if not evaluation_id:
            raise ValueError("Evaluation ID has not been set or provided.")
        endpoint = f"/evaluations/{evaluation_id}"
        self.client._make_request("DELETE", endpoint)
        # Clear the instance's internal state since the evaluation has been deleted.
        self.id = None

    def load(self, evaluation_id: Optional[str] = None):
        """
        Load an evaluation.

        :param evaluation_id: The ID of the evaluation to load.
        """
        evaluation_id = evaluation_id or self.id
        if not evaluation_id:
            raise ValueError("Evaluation ID has not been set or provided.")
        response = self._read(evaluation_id)

        self.id = response["id"]
        self.test_case_id = response.get("test_case_id")
        self.evaluation_dataset_id = response.get("evaluation_dataset_id")
        self.evaluation_result = response.get("evaluation_result")
        self.output = response.get("output")
        self.config = response.get("config")

        return self
