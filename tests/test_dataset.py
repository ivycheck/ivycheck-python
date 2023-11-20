import os

# Assuming `SampleClient` has a method `create_test_case_dataset`
# and it is defined in a module called `client_module`
from ivycheck.client import IvyClient

# Set up your API key and base URL
ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])

# Call the `create_test_case_dataset` method with dummy arguments
dataset_response = ivy.create_test_case_dataset(
    prompt_id="7a89104c-0d07-4396-a144-21c0c096622a",  
    test_config=None,
    name="Dummy Test Case Dataset",
    description="This is a dummy description for a test case dataset",
)

# Check the response type and contents
assert type(dataset_response) is dict
# Optionally, print the response or check for specific fields
print(dataset_response)  # Or perform other checks as needed
