import os
from ivycheck.ivy_client import IvyClient

# Set up your API key and base URL
ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])


# Create a new test case dataset inside an existing project
test_dataset = ivy.TestDataset.create(
    project_id="7a89104c-0d07-4396-a144-21c0c096622a",  # Admin Org
    # project_id="12caf8c1-5bc9-4fb6-827e-ffecff35afb2",  # Test Org
    eval_llm="gpt-4",
    name="Test ChatBot",
    description="Our standard test cases for ChatBot evaluation",
    rubrics=[
        {
            "name": "Politeness",
            "instruction": "Is the response polite?",
        },
        {
            "name": "Humour",
            "instruction": "Is the response funny or entertaining?",
        },
    ],
)

test_dataset.add_rubric(name="New Rubric", instruction="New Rubric Instruction")


# Add test cases to the dataset
test_dataset.add_test_case(
    input={"user_input": "How can I cancel my subscription online?"},
    segments={"customer": "ChatBotUser", "difficulty": "easy"},
    golden_answer="You can cancel your subscription online by going to the 'My Account' page and clicking on the 'Cancel Subscription' button.",
)

test_dataset.add_test_case(
    input={"user_input": "How much is the Premium Plan?"},
    segments={"customer": "ChatBotUser", "difficulty": "hard"},
)
