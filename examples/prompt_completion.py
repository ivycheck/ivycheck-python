import os
from ivycheck.ivy_client import IvyClient

ivy = IvyClient(
    api_key=os.environ["IVYCHECK_API_KEY"], base_url="http://localhost:8000"
)

chat_response = ivy.Prompt.complete(
    project_id="7af0b776-12e6-4fac-8526-d95c121664de",
    prompt_version=2,
    field_values={"user_input": "It's raining cats and dogs!"},
    stream=True,  # get streaming response
)

assert type(chat_response) is str
print(chat_response)

# streamin response
# for i, response in enumerate(chat_response):
#     print(f"Response {i}: {response}")
