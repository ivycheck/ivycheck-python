import os
from ivycheck.ivy_client import IvyClient

# Set up your API key and base URL
ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])


# Create a new test case dataset inside an existing project
test_dataset = ivy.TestDataset.create(
    project_id="7a89104c-0d07-4396-a144-21c0c096622a",  # Admin Org
    # project_id="12caf8c1-5bc9-4fb6-827e-ffecff35afb2",  # Test Org
    eval_llm="gpt-4",
    name="Test ChatBot Data",
    description="Our standard test cases for ChatBot evaluation",
    rubrics=[
        {
            "name": "Politeness",
            "description": "Is the response polite?",
        },
        {
            "name": "Humour",
            "description": "Is the response funny or entertaining?",
        },
    ],
)

# Add test cases to the dataset
test_dataset.add_test_case(
    input={"user_input": "How can I cancel my subscription online?"},
    segments={"customer": "ChatBotUser", "difficulty": "easy"},
)

test_dataset.add_test_case(
    input={"user_input": "How much is the Premium Plan?"},
    segments={"customer": "ChatBotUser", "difficulty": "hard"},
)
