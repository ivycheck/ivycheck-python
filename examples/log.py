import os
from ivycheck.ivy_client import IvyClient

ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])

# Log a prompt execution
ivy.PromptExecution.create(
    project_id="3b551e85-6806-49a3-98bb-b7b58e63111a",
    messages=[
        {
            "content": "Hi, I'm a chatbot. How can I help you?",
            "role": "assistant",
        },
        {
            "content": "I want to cancel my subscription.",
            "role": "user",
        },
    ],
    output="Call customer service.",
    metrics={"full_request": 0.5},
    auto_eval=True,
    run_eval_in_background=True,
)
