import os
from ivycheck.client import IvyClient

# set your API key as an environment variable
# export IVYCHECK_API_KEY=<your API key> or pass to constructor
ivy = IvyClient(api_key=os.environ['IVYCHECK_API_KEY'])

chat_response = ivy.complete(
    slug="translation-2",
    field_values={"user_input": "It's raining cats and dogs!"},
    # stage="production",
    version=2,  # specify stage or version
)

print(chat_response["message"])  # ¡Está lloviendo perros y gatos! ...
