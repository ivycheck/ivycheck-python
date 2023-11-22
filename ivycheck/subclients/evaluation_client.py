from ..schemas import EvaluationCreate, EvaluationUpdate
from typing import Optional, Dict


class EvaluationClient:
    def __init__(self, client):
        self.client = client

    def create(
        self,
        test_case_id: str,
        evaluation_dataset_id: str,
        output: Dict,
        evaluation_result: Optional[Dict] = None,
        config: Optional[Dict] = None,
    ) -> Dict:
        evaluation_data = EvaluationCreate(
            test_case_id=test_case_id,
            evaluation_dataset_id=evaluation_dataset_id,
            config=config,
            evaluation_result=evaluation_result,
            output=output,
        )
        endpoint = f"/evaluations/"
        return self.client._make_request(
            "POST", endpoint, json=evaluation_data.model_dump(exclude_none=True)
        )

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

    def delete(self, evaluation_id: str) -> Dict:
        endpoint = f"/evaluations/{evaluation_id}"
        return self.client._make_request("DELETE", endpoint)
