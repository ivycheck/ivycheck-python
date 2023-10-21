# IvyCheck SDK

This is the official Python SDK for the IvyCheck API. Use this SDK to easily interact with the IvyCheck API in your Python applications. See [ivycheck.com](https://ivycheck.com) for more info.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install IvyCheck.

```bash
pip install ivycheck
```

## Usage

Set your API key as an environment variable.
Alternatively, you can pass it directly to the constructor.

```bash
export IVYCHECK_API_KEY=<your API key>
```

Use the SDK in your Python code as described in the docs: https://docs.ivycheck.com/

<!--
```python
from ivycheck.client import IvyClient

ivy = IvyClient(api_key=os.environ['IVYCHECK_API_KEY'])

chat_response = ivy.complete(
    slug="translation-2",
    field_values={"user_input": "It's raining cats and dogs!"},
    # stage="production",
    version=2,  # specify stage or version
    stream=False,  # get streaming response
    raw_response=False,  # get full model response or only the response message.
)

print(chat_response["message"])  # ¡Está lloviendo perros y gatos! ...

``` -->
