from datetime import date
from uuid import UUID

from pydantic import BaseModel, Field
from typing import Optional, List


class BudgetBreakdown(BaseModel):
    infrastructure: Optional[float] = Field(0, ge=0)
    training: Optional[float] = Field(0, ge=0)
    materials: Optional[float] = Field(0, ge=0)
    monitoring: Optional[float] = Field(0, ge=0)
    contingency: Optional[float] = Field(0, ge=0)


class ImpactMetrics(BaseModel):
    beneficiaries: int
    duration: str


class Milestone(BaseModel):
    title:            str
    description:      str
    duration_weeks:   int
    budget_allocated: float
    deliverables:     List[str]


class CampaignDraft(BaseModel):
    title:            str
    description:      str
    category:         str
    location:         str
    budget_inr:       int
    budget_breakdown:  BudgetBreakdown
    schedule_vii:      str
    sdg_alignment:     List[int]
    start_date:       date
    end_date:         date
    impact_metrics:    ImpactMetrics
    milestones:       List[Milestone]


class UpdateImpactMetrics(BaseModel):
    beneficiaries: Optional[int] = None
    duration: Optional[str] = None


class UpdateMilestone(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_weeks: Optional[int] = None
    budget_allocated: Optional[float] = None
    deliverables: Optional[List[str]] = None

 
class UpdateCampaignDraft(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    budget_inr: Optional[int] = None
    budget_breakdown: Optional[BudgetBreakdown] = None
    schedule_vii: Optional[str] = None
    sdg_alignment: Optional[List[int]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    impact_metrics: Optional[UpdateImpactMetrics] = None
    milestones: Optional[List[UpdateMilestone]] = None


class SelectedCampaignIn(BaseModel):
    campaign:   CampaignDraft
    company_id: int


class SelectedCampaignResponse(BaseModel):
    id:      str
    title:   str
    status:  str
    message: str

class UpdateSelectedCampaign(BaseModel):
    campaign: Optional[UpdateCampaignDraft] = None
    company_id: int
    campaign_id: UUID
