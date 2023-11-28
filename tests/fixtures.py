import os
import pytest
import requests_mock
from ivycheck.ivy_client import IvyClient


@pytest.fixture
def ivy_client():
    # Mocking os.environ to safely use an API key without exposing it in the tests
    with pytest.MonkeyPatch.context() as m:
        m.setenv("IVYCHECK_API_KEY", "fake_api_key")
        client = IvyClient(api_key="fake_api_key", print_output=False)
    return client


# Define a common dataset creation payload in a fixture for reuse
@pytest.fixture
def common_dataset_payload():
    return {
        "project_id": "7a89104c-0d07-4396-a144-21c0c096622a",
        "eval_llm": "gpt-4",
        "name": "Test ChatBot Data",
        "description": "Our standard test cases for ChatBot evaluation",
        "rubrics": [
            {"name": "Politeness", "instruction": "Is the response polite?"},
            {"name": "Humour", "instruction": "Is the response funny or entertaining?"},
        ],
    }


@pytest.fixture
def test_dataset(ivy_client, common_dataset_payload):
    dataset_data = common_dataset_payload.copy()
    dataset_data["id"] = "mock_dataset_id"

    with requests_mock.Mocker() as m:
        m.post(
            f"{ivy_client.base_url}/test_case_datasets/",
            json=dataset_data,
            status_code=201,
        )

        dataset = ivy_client.TestDataset.create(**common_dataset_payload)
    return dataset


@pytest.fixture
def mock_evaluator(ivy_client, test_dataset, common_dataset_payload):
    evaluator_data = {
        # ... populate with the mock data structure for an evaluator ...
    }

    mock_test_dataset_response_data = common_dataset_payload.copy()
    mock_test_dataset_response_data["test_cases"] = {}

    mock_evaluation_dataset_data = {"id": "mock_evaluation_dataset_id"}

    with requests_mock.Mocker() as m:
        m.post(f"{ivy_client.base_url}/evaluators/", json=evaluator_data)
        m.get(
            f"{ivy_client.base_url}/test_case_datasets/mock_dataset_id",
            json=mock_test_dataset_response_data,
        )
        m.post(
            f"{ivy_client.base_url}/evaluation_datasets/",
            json=mock_evaluation_dataset_data,
        )
        yield test_dataset.evaluate("ChatBot Evaluation")


@pytest.fixture
def mocker():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def mock_evaluator(ivy_client, test_dataset, common_dataset_payload, mocker):
    evaluator_data = {}
    mocker.post(f"{ivy_client.base_url}/evaluators/", json=evaluator_data)

    mock_evaluation_dataset_data = {"id": "mock_evaluation_dataset_id"}
    mocker.post(
        f"{ivy_client.base_url}/evaluation_datasets/",
        json=mock_evaluation_dataset_data,
    )

    mock_test_dataset_response_data = common_dataset_payload.copy()
    mock_test_dataset_response_data["test_cases"] = [
        {
            "id": "test_case_1",
            "input": {"user_input": "How can I cancel my subscription online?"},
        },
        {
            "id": "test_case_1",
            "input": {"user_input": "How can I change my plan?"},
        },
    ]
    mocker.get(
        f"{ivy_client.base_url}/test_case_datasets/mock_dataset_id",
        json=mock_test_dataset_response_data,
    )

    evaluations_url = f"{ivy_client.base_url}/evaluations/create_and_run/"
    mocker.post(
        evaluations_url,
        json={
            "id": "evaluation_id",
            "evaluation_results": "Sorry, I can't help with that.",
        },
        status_code=200,
    )

    # Return a mocked instance of the evaluator
    mocked_evaluator = test_dataset.evaluate("ChatBot Evaluation")
    yield mocked_evaluator
