from typing import Optional, Dict
from uuid import UUID
from pydantic import BaseModel


class TestCaseDatasetCreate(BaseModel):
    prompt_id: Optional[str] = None
    test_config: Optional[Dict] = None
    name: Optional[str] = None
    description: Optional[str] = None
