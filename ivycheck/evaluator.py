from __future__ import annotations

# If you're on Python 3.7+, include this import at the top of the evaluator.py file
from typing import Optional, Dict, TYPE_CHECKING

# Import the client only if type checking
if TYPE_CHECKING:
    from ivycheck.ivy_client import IvyClient


class Evaluator:
    """
    Provides an interface to iterate over test cases of a dataset and submit the results to IvyCheck for evaluation.
    """

    def __init__(
        self,
        client,
        test_dataset_id: str,
        segments: Optional[Dict] = None,
        evaluator_description: Optional[str] = None,
    ):
        """
        Initializes the Evaluator object.

        :param client: An instance of IvyClient
        :param test_dataset_id: ID of the test dataset to evaluate
        :param segments: Optional filter to only evaluate test cases that match the segments
        :param evaluator_description: Description of the evaluation dataset
        """
        self.client = client
        self.test_dataset_id = test_dataset_id
        self.segments = segments
        self.evaluation_dataset_id = None
        self.test_cases = None
        self.evaluator_description = (
            evaluator_description if evaluator_description else "Automated Evaluation"
        )
        self._prepare_evaluation_dataset()

        if self.client.print_output:
            print(f"Evaluation URL: {self.eval_url}")

    @classmethod
    def create(
        cls,
        client: "IvyClient",  # is of type IvyClient but this causes a circular import atm
        test_dataset_id: str,
        segments: Optional[Dict] = None,
        evaluator_description: Optional[str] = None,
    ):
        return cls(client, test_dataset_id, segments, evaluator_description)

    @property
    def eval_url(self):
        if self.evaluation_dataset_id is None:
            raise ValueError("Evaluation Dataset ID has not been set.")
        else:
            return self.client._make_request(
                "GET", f"/evaluation_datasets/url/{self.evaluation_dataset_id}"
            )

    # construct URL from project ID and evaluation dataset ID intead of calling endpoing
    # @property
    # def eval_url(self):
    #     if self.evaluation_dataset_id is None:
    #         raise ValueError("Evaluation Dataset ID has not been set.")
    #     else:
    #         return f"https://app.ivycheck.com/projects/{self.client.TestDataset.project_id}/evals/{self.evaluation_dataset_id}"

    def _prepare_evaluation_dataset(self):
        # Reads the test dataset and creates the evaluation dataset
        test_dataset = self.client.TestDataset._read(
            testdataset_id=self.test_dataset_id
        )
        evals = self.client.EvaluationDataset._create(
            test_case_dataset_id=self.test_dataset_id,
            description=self.evaluator_description,
            aggregate_results={
                "status": "running",
                "stats": {
                    "completed": 0,
                    "total": len(test_dataset.get("test_cases", [])),
                },
            },
        )
        self.evaluation_dataset_id = evals.id
        # Filter test_cases if segments is provided
        if self.segments:
            self.test_cases = [
                tc
                for tc in test_dataset["test_cases"]
                if self._test_case_matches_segments(tc)
            ]
        else:
            self.test_cases = test_dataset["test_cases"]

    def _test_case_matches_segments(self, test_case):
        # Implement the logic to check if a test case matches the segments filter
        if not self.segments:
            return True
        for key, value in self.segments.items():
            if test_case["segments"].get(key) != value:
                return False
        return True

    def test_case_iterator(self):
        """
        Iterator for test cases that yields a tuple containing the test case data and a method to evaluate it.

        Example usage:
        ```python
        test_dataset = ivy.TestDataset.load("abc-def")

        evaluator = test_dataset.evaluate("ChatBot Evaluation")

        for test_case, evaluate in evaluator.test_case_iterator():
            user_input = test_case["input"]["user_input"]
            response = custom_llm(user_input)
            evaluate(response, run_in_background=True)
        ```
        """
        if not self.test_cases:
            raise ValueError("Test cases have not been loaded.")
        for test_case in self.test_cases:
            yield (test_case, self._make_evaluate_func(test_case["id"]))

    def _make_evaluate_func(self, test_case_id):
        # Create function that captures the test case ID and takes a response as its only argument
        def evaluate_func(response: str, run_in_background=True):
            self.client.Evaluation.create_and_run(
                evaluation_dataset_id=self.evaluation_dataset_id,
                test_case_id=test_case_id,
                output=response,
                run_in_background=run_in_background,
            )

        return evaluate_func
