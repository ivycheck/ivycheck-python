import os
import pytest
import requests_mock
from ivycheck.ivy_client import IvyClient
from fixtures import ivy_client, common_dataset_payload, test_dataset


def test_create_test_dataset(ivy_client, common_dataset_payload):
    mock_response_data = common_dataset_payload.copy()
    mock_response_data["id"] = "new_dataset_id"

    with requests_mock.Mocker() as m:
        m.post(
            f"{ivy_client.base_url}/test_case_datasets/",
            json=mock_response_data,
            status_code=201,
        )

        # Use ** expansion to unpack dictionary keys and values as method parameters
        test_dataset = ivy_client.TestDataset.create(**common_dataset_payload)

        assert test_dataset.id == "new_dataset_id"
        assert test_dataset.name == common_dataset_payload["name"]
        assert test_dataset.description == common_dataset_payload["description"]


def test_add_test_case(ivy_client, test_dataset):
    test_case_input = {"user_input": "How can I cancel my subscription online?"}
    segments = {"customer": "ChatBotUser", "difficulty": "easy"}

    with requests_mock.Mocker() as m:
        m.post(
            f"{ivy_client.base_url}/test_cases/",
            json={"id": "test_case_id"},
            status_code=201,
        )

        test_case = test_dataset.add_test_case(input=test_case_input, segments=segments)

        assert test_case.id == "test_case_id"
