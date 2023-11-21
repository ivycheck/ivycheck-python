from ..schemas import EvaluationDatasetCreate, EvaluationDatasetUpdate
from typing import Optional, Dict, List


class EvaluationDatasetClient:
    def create_evaluation_dataset(
        self,
        test_case_dataset_id: str,
        description: Optional[str] = None,
        aggregate_results: Optional[Dict] = None,
        config: Optional[Dict] = None,
    ) -> Dict:
        evaluation_dataset_data = EvaluationDatasetCreate(
            test_case_dataset_id=test_case_dataset_id,
            description=description,
            aggregate_results=aggregate_results,
            config=config,
        )
        return self._make_request("POST", "/", data=evaluation_dataset_data.dict())

    def read_evaluation_dataset(self, evaluation_dataset_id: str) -> Dict:
        endpoint = f"/{evaluation_dataset_id}"
        return self._make_request("GET", endpoint)

    def update_evaluation_dataset(
        self,
        evaluation_dataset_id: str,
        test_case_dataset_id: str,
        description: Optional[str] = None,
        aggregate_results: Optional[Dict] = None,
        config: Optional[Dict] = None,
    ) -> Dict:
        evaluation_dataset_data = EvaluationDatasetUpdate(
            test_case_dataset_id=test_case_dataset_id,
            description=description,
            aggregate_results=aggregate_results,
            config=config,
        )
        endpoint = f"/{evaluation_dataset_id}"
        return self._make_request("PUT", endpoint, data=evaluation_dataset_data.dict())

    def delete_evaluation_dataset(self, evaluation_dataset_id: str) -> Dict:
        endpoint = f"/{evaluation_dataset_id}"
        return self._make_request("DELETE", endpoint)

    def read_evaluation_datasets_by_org(self) -> List[Dict]:
        endpoint = "/by_org/"
        return self._make_request("GET", endpoint)
