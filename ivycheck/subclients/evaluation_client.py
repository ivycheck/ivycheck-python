from ..schemas import EvaluationCreate, EvaluationUpdate
from typing import Optional, Dict


class EvaluationClient:
    def __init__(self, client):
        self.client = client

    def create_evaluation(
        self,
        test_case_id: str,
        evaluation_dataset_id: str,
        evaluation_result: Dict,
        output: Dict,
        config: Optional[Dict] = None,
    ) -> Dict:
        evaluation_data = EvaluationCreate(
            test_case_id=test_case_id,
            evaluation_dataset_id=evaluation_dataset_id,
            config=config,
            evaluation_result=evaluation_result,
            output=output,
        )
        return self._make_request(
            "POST", "/", data=evaluation_data.model_dump(exclude_none=True)
        )

    def read_evaluation(self, evaluation_id: str) -> Dict:
        return self._make_request("GET", f"/{evaluation_id}")

    def update_evaluation(
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
        return self._make_request(
            "PUT", f"/{evaluation_id}", data=evaluation_data.dict()
        )

    def delete_evaluation(self, evaluation_id: str) -> Dict:
        return self._make_request("DELETE", f"/{evaluation_id}")
