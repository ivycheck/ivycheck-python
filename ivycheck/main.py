import requests
import os

from typing import Optional, Dict

endpoint_url = (
    "https://dee-test-git-fix-prompt-exec-logging-for-endpoint-deekard.vercel.app/"
)
# endpoint_url = "http://localhost:8000/"


def complete(
    slug: str,
    field_values: Optional[Dict],
    stage: Optional[str] = None,
    version: Optional[int] = None,
):
    url = endpoint_url + "api/v1/test_run"

    headers = {"Authorization": f"Bearer {read_api_key()}"}

    data = {
        "slug": slug,
        "stage": stage,
        "version": version,
        "field_values": field_values,
    }

    response = requests.post(url, headers=headers, json=data)

    print(response)

    return response.json()


def health():
    url = endpoint_url + "external/health"
    headers = {"Authorization": f"Bearer {read_api_key()}"}
    response = requests.get(url, headers=headers)
    print(response)
    return response.json()


def read_api_key():
    # Use the get() method of the os.environ object to read the value of an environment variable
    api_key = os.environ.get("RECHECKAI_API_KEY")

    # Check if the API key exists
    if not api_key:
        raise ValueError("API_KEY is not set in the environment variables")

    return api_key
