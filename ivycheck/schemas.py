from typing import Optional, Dict, List
from uuid import UUID
from pydantic import BaseModel


class TestCaseDatasetCreate(BaseModel):
    prompt_id: str
    test_config: Optional[Dict] = {}
    name: Optional[str] = None
    description: Optional[str] = None


class TestCaseDatasetUpdate(BaseModel):
    test_config: Optional[dict]
    name: Optional[str]
    description: Optional[str]


# Define Pydantic models for validation
class TestCaseCreate(BaseModel):
    input: Dict
    message_history: Optional[List] = None
    context: Optional[List] = None
    golden_answer: Optional[str] = None
    golden_context: Optional[List] = None
    segments: Optional[Dict] = None
    info: Optional[Dict] = None
    dataset_id: str


class TestCaseUpdate(TestCaseCreate):
    pass


# Pydantic models based on the backend models
class EvaluationBase(BaseModel):
    config: Optional[Dict] = None
    evaluation_result: Optional[
        Dict
    ] = None  # maybe remove here. This should be filled by ivycheck
    output: Dict
    test_case_id: str
    evaluation_dataset_id: str


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationUpdate(EvaluationBase):
    pass


class EvaluationDatasetBase(BaseModel):
    description: Optional[str] = None
    aggregate_results: Optional[Dict] = None
    config: Optional[Dict] = None
    test_case_dataset_id: str


class EvaluationDatasetCreate(EvaluationDatasetBase):
    pass


class EvaluationDatasetUpdate(EvaluationDatasetBase):
    pass


class PromptExecutionBase(BaseModel):
    prompt_id: Optional[str] = None
    prompt_version_id: Optional[str] = None
    input: Optional[Dict] = None
    messages: Optional[list] = None
    context: Optional[list] = None
    segments: Optional[dict] = None
    llm_model_params: Optional[Dict] = None
    output: Optional[str] = None
    metrics: Optional[Dict] = None
    info: Optional[dict] = None


class PromptExecutionCreate(PromptExecutionBase):
    pass
