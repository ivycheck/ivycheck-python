import os
from ivycheck.ivy_client import IvyClient
from ivycheck.evaluator import Evaluator

# Set up your API key and base URL
ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])

# Create a new test case dataset inside an existing project
test_dataset = ivy.TestDataset.create(
    project_id="7a89104c-0d07-4396-a144-21c0c096622a",  # Admin Org
    # project_id="12caf8c1-5bc9-4fb6-827e-ffecff35afb2",  # Test Org
    eval_llm="gpt-4",
    name="Test ChatBot 7",
    description="Test Dataset 7",
    test_config={
        "rubrics": [
            {
                "name": "Politeness",
                "description": "Is the response polite?",
            }
        ]
    },
)

# Add test cases to the dataset
ivy.TestCase.create(
    dataset_id=test_dataset["id"],
    input={"user_input": "How can I cancel my subscription?"},
    segments={"customer": "ChatBotUser", "difficulty": "easy"},
)

ivy.TestCase.create(
    dataset_id=test_dataset["id"],
    input={"user_input": "How much is the Pro Plan?"},
    segments={"customer": "ChatBotUser", "difficulty": "hard"},
)

# Create an Evaluator object for a given test dataset with an optional segments filter
evaluator = Evaluator.create(ivy, test_dataset_id=test_dataset["id"])

for test_case, evaluate in evaluator.test_case_iterator():
    # Custom logic to execute the test case using the test case's properties
    user_input = test_case["input"]["user_input"]

    # Implement test case execution and response generation
    response = "Sorry, I don't know how to help with that. But I can help you with other things."

    # Evaluate the response using the evaluate function provided by the iterator
    evaluate(response)
