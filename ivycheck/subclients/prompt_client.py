from ..schemas import TestCaseCreate, TestCaseUpdate
from typing import Optional, Dict, List


class PromptClient:
    def __init__(self, client):
        self.client = client

    def complete(
        self,
        project_id: str,
        prompt_version: int = None,
        field_values: Dict = None,
        stream: bool = False,
        raw_response: bool = False,
    ):
        assert project_id is not None, "Project Id is required."

        data = {
            "project_id": project_id,
            "prompt_version": prompt_version,
            "field_values": field_values,
            "stream": stream,
            "raw_response": raw_response,
        }

        return self.client._make_request(
            "POST", "/api/v1/complete", json=data, stream=stream
        )
