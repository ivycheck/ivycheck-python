from ..schemas import EvaluationDatasetCreate, EvaluationDatasetUpdate
from typing import Optional, Dict, List


class EvaluationDatasetClient:
    """
    Provides an interface to read and delete evaluation datasets.
    """

    def __init__(self, client):
        self.client = client
        self.id = None  # Initialize self.id to store the EvaluationDataset ID

    def _create(
        self,
        test_case_dataset_id: str,
        description: Optional[str] = None,
        aggregate_results: Optional[Dict] = None,
        config: Optional[Dict] = None,
    ):
        assert test_case_dataset_id is not None, "Test Case Dataset Id is required."

        evaluation_dataset_data = EvaluationDatasetCreate(
            test_case_dataset_id=test_case_dataset_id,
            description=description,
            aggregate_results=aggregate_results,
            config=config,
        )
        endpoint = f"/evaluation_datasets/"
        response = self.client._make_request(
            "POST",
            endpoint,
            json=evaluation_dataset_data.model_dump(exclude_unset=True),
        )

        self.id = response[
            "id"
        ]  # Assume response contains the ID of the created evaluation dataset
        # Optionally store other attributes as needed

        return self  # Return self to allow method chaining

    def load(self, evaluation_dataset_id: str):
        """
        Load an evaluation dataset

        :param evaluation_dataset_id: The ID of the evaluation dataset to load.
        """
        data = self._read(evaluation_dataset_id)
        self.id = data["id"]
        # Load other relevant data into the instance as needed
        return self  # Return self to allow method chaining

    def _read(self, evaluation_dataset_id: str = None):
        evaluation_dataset_id = evaluation_dataset_id or self.id
        if not evaluation_dataset_id:
            raise ValueError("Evaluation Dataset ID has not been set or provided.")
        endpoint = f"/evaluation_datasets/{evaluation_dataset_id}"
        return self.client._make_request("GET", endpoint)

    def _update(
        self,
        test_case_dataset_id: str,
        description: Optional[str] = None,
        aggregate_results: Optional[Dict] = None,
        config: Optional[Dict] = None,
        evaluation_dataset_id: str = None,
    ):
        evaluation_dataset_id = evaluation_dataset_id or self.id
        if not evaluation_dataset_id:
            raise ValueError("Evaluation Dataset ID has not been set or provided.")

        evaluation_dataset_data = EvaluationDatasetUpdate(
            test_case_dataset_id=test_case_dataset_id,
            description=description,
            aggregate_results=aggregate_results,
            config=config,
        )
        endpoint = f"/evaluation_datasets/{evaluation_dataset_id}"
        response = self.client._make_request(
            "PUT", endpoint, json=evaluation_dataset_data.dict(exclude_unset=True)
        )

        # Optionally update the instance's internal state

        return self  # Return self to allow method chaining

    def delete(self, evaluation_dataset_id: str):
        """
        Delete an evaluation dataset.

        :param evaluation_dataset_id: The ID of the evaluation dataset to delete.
        """
        # evaluation_dataset_id = evaluation_dataset_id or self.id
        if not evaluation_dataset_id:
            raise ValueError("Evaluation Dataset ID has not been set or provided.")
        endpoint = f"/evaluation_datasets/{evaluation_dataset_id}"
        return self.client._make_request("DELETE", endpoint)

    def _read_by_org(self):
        # This method doesn't fit into a stateful design since it's about a collection
        # It may be better suited to a separate collection management class
        endpoint = "/evaluation_datasets/by_org/"
        return self.client._make_request("GET", endpoint)
