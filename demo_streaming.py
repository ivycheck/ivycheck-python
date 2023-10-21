import os, json
from ivycheck.ivy_client import IvyClient

# set your API key as an environment variable
# export IVYCHECK_API_KEY=<your API key> or pass to constructor
ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])

chat_response = ivy.complete(
    slug="translation-2",
    field_values={"user_input": "would"},
    # stage="production",
    version=7,  # specify stage or version
    stream=True,
    raw_response=False,
)

for line in chat_response.iter_lines():
    print(line)
