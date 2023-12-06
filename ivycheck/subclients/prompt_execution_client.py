from typing import Optional
from ..schemas import PromptExecutionCreate


class PromptExecutionClient:
    """
    Provides an interface to create prompt executions.
    """

    def __init__(self, client):
        self.client = client

    def create(
        self,
        project_id: str,
        input: Optional[dict] = None,
        output: Optional[str] = None,
        messages: Optional[list] = None,
        context: Optional[list] = None,
        llm_model_params: Optional[dict] = None,
        segments: Optional[dict] = None,
        metrics: Optional[dict] = None,
        info: Optional[dict] = None,
        auto_eval: Optional[bool] = False,
        run_eval_in_background: Optional[bool] = True,
    ):
        """
        Create a new prompt execution in the log.

        Example:
        ```python
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
        )
        ```

        :param project_id: The ID of the project to add the prompt execution to.
        :param input: The input to the model. Example: `{"user_input": "How can I cancel my subscription online?"}`
        :param messages: The message history of the conversation. Example: `[{"role": "system", "content": "You are a helpful assistant."}]`
        :param context: Additional context of the conversation. Can contain retrieved documents provided as list of dictionaries. Example: `[{"title": "How to cancel your subscription", "url": "https://example.com/cancel-subscription"}]`
        :param output: The output of the LLM.
        :param llm_model_params: The parameters of the LLM. Example: `{"model": "gpt-4", "temperature": 1.0, "maxLength": 1024}`
        :param segments: A dictionary of segments for filtering and analytics. Example: `{"customer": "Amazon"}`
        :param metrics: Metrics for analytics. Example: `{"response_time": 0.5}`
        :param into: Additional information to store with the prompt execution.
        """

        prompt_execution_data = PromptExecutionCreate(
            prompt_id=project_id,
            input=input,
            output=output,
            messages=messages,
            context=context,
            llm_model_params=llm_model_params,
            segments=segments,
            metrics=metrics,
            info=info,
        )
        validated_data = prompt_execution_data.model_dump(exclude_none=True)
        response = self.client._make_request(
            "POST",
            "/prompt_executions/",
            json=validated_data,
            params={
                "auto_eval": auto_eval,
                "run_eval_in_background": run_eval_in_background,
            },
        )

        # self.project_id = project_id
        # self.id = response["id"]
        # self.name = response.get("name")
        # self.description = response.get("description")
        # self.test_config = response.get("test_config")

        # return self
