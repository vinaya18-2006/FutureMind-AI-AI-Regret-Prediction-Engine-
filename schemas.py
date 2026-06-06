from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

class DecisionCreate(BaseModel):
    input_text: str
    stress_level: Optional[float] = 50.0
    financial_cost: Optional[float] = 50.0
    emotional_risk: Optional[float] = 50.0
    confidence_level: Optional[float] = 50.0

class DecisionResolve(BaseModel):
    actual_regret_status: str  # "happy", "neutral", "regret"

class Milestone(BaseModel):
    time: str
    description: str
    stress: float
    satisfaction: float

class TimelineSimulation(BaseModel):
    name: str
    milestones: List[Milestone]

class PersonalityInsights(BaseModel):
    impulsiveness: float
    overthinking: float
    risk_tolerance: float

class SwotAnalysis(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]

class DecisionAnalysisResponse(BaseModel):
    title: str
    regret_probability: float
    emotional_stability: str
    stress_prediction: str
    satisfaction_score: float
    emotion_analysis: Dict[str, float]
    personality_insights: PersonalityInsights
    timeline_a: TimelineSimulation
    timeline_b: TimelineSimulation
    swot_analysis: SwotAnalysis
    summary_recommendation: str

class DecisionResponse(BaseModel):
    id: int
    title: str
    input_text: str
    emotion_analysis: Dict[str, Any]
    regret_probability: float
    satisfaction_score: float
    stress_prediction: str
    emotional_stability: str
    personality_insights: Dict[str, Any]
    timeline_a: Dict[str, Any]
    timeline_b: Dict[str, Any]
    swot_analysis: Dict[str, Any]
    summary_recommendation: str
    created_at: datetime
    actual_regret_status: str

    class Config:
        from_attributes = True
        # SQLite returns datetime objects and JSON strings. We'll handle conversion in routes.
