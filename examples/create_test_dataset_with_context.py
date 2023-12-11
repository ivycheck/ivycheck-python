import os
from ivycheck.ivy_client import IvyClient

# Set up your API key and base URL
ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])


# Create a new test case dataset inside an existing project
test_dataset = ivy.TestDataset.create(
    project_id="<your-project-id>",  # Admin Org
    eval_llm="gpt-4",
    name="Test ChatBot with context",
    description="Our standard test cases for ChatBot evaluation",
)

test_dataset.add_rubric(
    name="Precision",
    instruction="Does the response provide only information that is given in the golden answer?",
)

test_dataset.add_rubric(
    name="Completeness",
    instruction="Does the response contain all information provided in the golden answer?",
)

# Add test cases to the dataset
test_dataset.add_test_case(
    input={"user_input": "How can I cancel my subscription online?"},
    segments={"customer": "ChatBotUser", "difficulty": "easy"},
    golden_answer="You can cancel your subscription online by going to the 'My Account' page and clicking on the 'Cancel Subscription' button.",
)

evaluator = test_dataset.evaluate("ChatBot Evaluation")

for test_case, evaluate in evaluator.test_case_iterator():
    # Custom logic to execute the test case using the test case's properties
    response = (
        "You can cancel your subscription by calling a customer service representative."
    )

    evaluate(response, run_in_background=True)
