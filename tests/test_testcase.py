import os
from ivycheck.ivy_client import IvyClient

# Set up your API key and base URL
ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])

# Call the `create_test_case_dataset` method with dummy arguments
dataset_response = ivy.TestCase.create(
    dataset_id="eb7ae285-da32-4380-9fa7-1f5aeb3eb13e",
    input={"user_input": "This is a dummy input"},
)

# Check the response type and contents
assert type(dataset_response) is dict
# Optionally, print the response or check for specific fields
print(dataset_response)  # Or perform other checks as needed
