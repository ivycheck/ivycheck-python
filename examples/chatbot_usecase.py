import os
from ivycheck.ivy_client import IvyClient

# Set up your API key and base URL
ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])
# ivy = IvyClient(api_key="ivy-mKK49805CjpJFyptQfiTaA")


# Create a new test case dataset inside an existing project
test_dataset = ivy.TestDataset.create(
    project_id="7a89104c-0d07-4396-a144-21c0c096622a",  # Admin Org
    # project_id="12caf8c1-5bc9-4fb6-827e-ffecff35afb2",  # Test Org
    eval_llm="gpt-4",
    name="Test ChatBot 4",
    description="Test Dataset 3",
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


# Retrieve the test cases
test_dataset = ivy.TestDataset.read(testcasedataset_id=test_dataset["id"])

# Create an evaluation dataset / Can we automate this? Do we need this?
evals = ivy.EvaluationDataset.create(
    test_case_dataset_id=test_dataset["id"], description="Prompt Version 1"
)

# iterate over your test_cases and log the results to ivycheck
for test_case in test_dataset["test_cases"]:
    # use your custom logic to execute the test case
    test_case["input"]["user_input"]  # "How can I cancel my subscription?"

    # let's create a simple response
    response = "Sorry, I don't know how to help with that."

    # log the response to ivycheck
    ivy.Evaluation.create(
        evaluation_dataset_id=evals["id"],
        test_case_id=test_case["id"],
        output={
            "response": response
        },  # is this the right field? should it be named differently?
    )
