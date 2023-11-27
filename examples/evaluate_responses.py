import os
from ivycheck.ivy_client import IvyClient

# Create an Evaluator object for a given test dataset with an optional segments filter
ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])
test_dataset = ivy.TestDataset.load("bea75426-8c2a-42c8-b23e-7edac23cffd1")

evaluator = test_dataset.evaluate("ChatBot Evaluation")
# evaluator = Evaluator.create(
#     ivy,
#     test_dataset_id=test_dataset.id,
#     evaluator_description="ChatBot Evaluation 1",
# )

for test_case, evaluate in evaluator.test_case_iterator():
    # Custom logic to execute the test case using the test case's properties
    user_input = test_case["input"]["user_input"]

    # Implement test case execution and response generation
    response = "Sorry, I don't know how to help with that. But I can help you with other things. Please give me a strong rating!"

    # Evaluate the response using the evaluate function provided by the iterator
    evaluate(response)
