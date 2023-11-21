from ..schemas import EvaluationDatasetCreate, EvaluationDatasetUpdate
from typing import Optional, Dict, List


class EvaluationDatasetClient:
    def __init__(self, client):
        self.client = client

    def create(
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
        endpoint = f"/evaluation_datasets/"
        return self.client._make_request(
            "POST",
            endpoint,
            json=evaluation_dataset_data.model_dump(exclude_unset=True),
        )

    def read(self, evaluation_dataset_id: str) -> Dict:
        endpoint = f"/evaluation_datasets/{evaluation_dataset_id}"
        return self.client._make_request("GET", endpoint)

    def update(
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
        endpoint = f"/evaluation_datasets/{evaluation_dataset_id}"
        return self.client._make_request(
            "PUT", endpoint, json=evaluation_dataset_data.dict()
        )

    def delete(self, evaluation_dataset_id: str) -> Dict:
        endpoint = f"/evaluation_datasets/{evaluation_dataset_id}"
        return self.client._make_request("DELETE", endpoint)

    def read_by_org(self) -> List[Dict]:
        endpoint = "/evaluation_datasets/by_org/"
        return self.client._make_request("GET", endpoint)
