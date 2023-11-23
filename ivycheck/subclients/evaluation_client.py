from ..schemas import EvaluationCreate, EvaluationUpdate
from typing import Optional, Dict


class EvaluationClient:
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
        output: Dict,
        evaluation_result: Optional[Dict] = None,
        config: Optional[Dict] = None,
    ) -> "EvaluationClient":
        evaluation_data = EvaluationCreate(
            test_case_id=test_case_id,
            evaluation_dataset_id=evaluation_dataset_id,
            config=config,
            evaluation_result=evaluation_result,
            output=output,
        )
        endpoint = f"/evaluations/create_and_run/"
        response = self.client._make_request(
            "POST", endpoint, json=evaluation_data.model_dump(exclude_none=True)
        )

        # Store the evaluation-related properties after creation.
        self.id = response["id"]
        self.test_case_id = response.get("test_case_id")
        self.evaluation_dataset_id = response.get("evaluation_dataset_id")
        self.evaluation_result = response.get("evaluation_result")
        self.output = response.get("output")
        self.config = response.get("config")

        # Return the EvaluationClient instance for method chaining.
        return self

    def read(self, evaluation_id: str) -> Dict:
        endpoint = f"/evaluations/{evaluation_id}"
        return self.client._make_request("GET", endpoint)

    def update(
        self,
        evaluation_id: str,
        test_case_id: str,
        evaluation_dataset_id: str,
        evaluation_result: Dict,
        output: Dict,
        config: Optional[Dict] = None,
    ) -> Dict:
        evaluation_data = EvaluationUpdate(
            test_case_id=test_case_id,
            evaluation_dataset_id=evaluation_dataset_id,
            config=config,
            evaluation_result=evaluation_result,
            output=output,
        )
        endpoint = f"/evaluations/{evaluation_id}"
        return self.client._make_request(
            "PUT", endpoint, json=evaluation_data.model_dump()
        )

    def delete(self):
        assert self.id is not None, "Evaluation ID is not set."
        endpoint = f"/evaluations/{self.id}"
        response = self.client._make_request("DELETE", endpoint)

    def load(self, evaluation_id: str) -> "EvaluationClient":
        endpoint = f"/evaluations/{evaluation_id}"
        response = self.client._make_request("GET", endpoint)

        # Assuming the response contains the data needed to populate the object
        self.id = response["id"]
        self.test_case_id = response.get("test_case_id")
        self.evaluation_dataset_id = response.get("evaluation_dataset_id")
        self.evaluation_result = response.get("evaluation_result")
        self.output = response.get("output")
        self.config = response.get("config")

        # Return the EvaluationClient instance for method chaining.
        return self
