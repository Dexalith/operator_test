from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OperatorBase(BaseModel):
    name: str
    email: str
    is_active: bool = True
    max_leads: int = 10


class OperatorCreate(OperatorBase):
    pass


class Operator(OperatorBase):
    id: int
    current_leads: int = 0

    class Config:
        from_attributes = True


class SourceBase(BaseModel):
    name: str
    description: Optional[str] = None


class SourceCreate(SourceBase):
    pass


class Source(SourceBase):
    id: int

    class Config:
        from_attributes = True


class CompetencyBase(BaseModel):
    operator_id: int
    source_id: int
    weight: float = 1.0


class CompetencyCreate(CompetencyBase):
    pass


class Competency(CompetencyBase):
    id: int

    class Config:
        from_attributes = True


class LeadBase(BaseModel):
    source_id: int
    contact_info: str


class LeadCreate(LeadBase):
    pass


class Lead(LeadBase):
    id: str
    operator_id: Optional[int]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class LeadAssignment(BaseModel):
    lead_id: str
    operator_id: int