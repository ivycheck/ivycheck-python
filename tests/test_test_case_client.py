# test_ivy_client.py

import os
import pytest
import requests_mock
from ivycheck.ivy_client import IvyClient
from ivycheck.subclients.test_case_client import TestCaseClient
from fixtures import ivy_client


def test_create_test_case(ivy_client):
    project_id = "project_id_example"
    eval_llm = "gpt-4"
    name = "example name"
    description = "example description"

    # Mock the POST request to create a test dataset
    with requests_mock.Mocker() as m:
        m.post(
            f"{ivy_client.base_url}/test_case_datasets/",
            json={"id": "test_dataset_id", "name": name, "description": description},
            status_code=201,
        )

        test_dataset = ivy_client.TestDataset.create(
            project_id=project_id, eval_llm=eval_llm, name=name, description=description
        )

        assert test_dataset.id == "test_dataset_id"
        assert test_dataset.name == name
        assert test_dataset.description == description


# Further tests would continue in a similar pattern, mocking out the requests
# and ensuring that your code interacts with those responses correctly.
