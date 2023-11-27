import os
from ivycheck.ivy_client import IvyClient

# Set up your API key and base URL
ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])


# Create a new test case dataset inside an existing project
test_dataset = ivy.TestDataset.create(
    project_id="7a89104c-0d07-4396-a144-21c0c096622a",  # Admin Org
    # project_id="12caf8c1-5bc9-4fb6-827e-ffecff35afb2",  # Test Org
    eval_llm="gpt-4",
    name="Test ChatBot 10",
    description="Test Dataset 10",
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

# alternatively, you can create test cases directly using the TestCaseClient
# ivy.TestCase.create(dataset_id=test_dataset["id"], input=...)

# can also load test existing datasets by ID
# test_dataset = ivy.TestDataset.load("ad240403-d8f2-4473-a949-b2acf9b9a54b")

# Create an Evaluator object for a given test dataset with an optional segments filter
evaluator = test_dataset.evaluate()
# evaluator = Evaluator.create(
#     ivy,
#     test_dataset_id=test_dataset.id,
#     evaluator_description="ChatBot Evaluation 1",
# )

for test_case, evaluate in evaluator.test_case_iterator():
    # Custom logic to execute the test case using the test case's properties
    user_input = test_case["input"]["user_input"]

    # Implement test case execution and response generation
    response = "Sorry, I don't know how to help with that. But I can help you with other things. Bro!"

    # Evaluate the response using the evaluate function provided by the iterator
    evaluate(response)
