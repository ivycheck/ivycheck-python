import os
from ivycheck.client import IvyClient

ivy = IvyClient(api_key=os.environ["IVYCHECK_API_KEY"])

chat_response = ivy.complete(
    slug="translation-2",
    field_values={"user_input": "It's raining cats and dogs!"},
    # stage="production",
    version=2,  # specify stage or version
    stream=False,  # get streaming response
    raw_response=False,  # get full model response or only the response message.
)

print(chat_response.text)  # ¡Está lloviendo perros y gatos! ...
