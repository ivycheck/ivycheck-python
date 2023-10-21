import os, json
from ivycheck.ivy_client import IvyClient

# set your API key as an environment variable
# export IVYCHECK_API_KEY=<your API key> or pass to constructor
ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])

chat_response = ivy.complete(
    slug="translation-2",
    field_values={"user_input": "It's raining cats and dogs."},
    # stage="production",
    version=7,  # specify stage or version
    stream=False,
    raw_response=False,
)

print(json.loads(chat_response.text))
