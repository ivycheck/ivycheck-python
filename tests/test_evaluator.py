import os
import pytest
import requests_mock
from fixtures import (
    ivy_client,
    common_dataset_payload,
    test_dataset,
    mock_evaluator,
    mocker,
)


def test_evaluate_test_dataset(ivy_client, test_dataset, mock_evaluator, mocker):
    # Mock up test cases that you expect to come from the iterator

    # evaluate does not return. therefore we just test the correct calls to the mocked API.
    for test_case, evaluate in mock_evaluator.test_case_iterator():
        evaluate(test_case, run_in_background=False)

    # call to test dataset, to eval dataset, and one for every evaluation
    assert mocker.call_count == 2 + len(mock_evaluator.test_cases)
    assert set([x.path for x in mocker.request_history[2:]]) == {
        "/evaluations/create_and_run/"
    }
    assert mocker.request_history[0].path == "/test_case_datasets/mock_dataset_id"
    assert mocker.request_history[1].path == "/evaluation_datasets/"

    assert mock_evaluator.evaluation_dataset_id == "mock_evaluation_dataset_id"
    assert mock_evaluator.test_dataset_id == "mock_dataset_id"
