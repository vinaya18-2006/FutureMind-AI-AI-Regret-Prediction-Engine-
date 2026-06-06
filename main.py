import json
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.config import settings
from backend.database import engine, Base, get_db
from backend.models import Decision
from backend.schemas import DecisionCreate, DecisionResolve, DecisionResponse, DecisionAnalysisResponse
from backend.services.ai_service import analyze_decision_with_ai

# Initialize SQLite database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FutureMind AI — Regret Prediction Engine")

# CORS middleware configuration to allow React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development Capstone
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def serialize_decision_db_to_response(db_dec: Decision) -> dict:
    """Helper to convert stored JSON strings in SQLite into Python dicts for Pydantic response validation."""
    return {
        "id": db_dec.id,
        "title": db_dec.title,
        "input_text": db_dec.input_text,
        "emotion_analysis": json.loads(db_dec.emotion_analysis) if db_dec.emotion_analysis else {},
        "regret_probability": db_dec.regret_probability,
        "satisfaction_score": db_dec.satisfaction_score,
        "stress_prediction": db_dec.stress_prediction,
        "emotional_stability": db_dec.emotional_stability,
        "personality_insights": json.loads(db_dec.personality_insights) if db_dec.personality_insights else {},
        "timeline_a": json.loads(db_dec.timeline_a_json) if db_dec.timeline_a_json else {},
        "timeline_b": json.loads(db_dec.timeline_b_json) if db_dec.timeline_b_json else {},
        "swot_analysis": json.loads(db_dec.swot_analysis) if db_dec.swot_analysis else {},
        "summary_recommendation": db_dec.summary_recommendation,
        "created_at": db_dec.created_at,
        "actual_regret_status": db_dec.actual_regret_status
    }

@app.post("/api/analyze", response_model=DecisionResponse)
def analyze_decision(
    payload: DecisionCreate, 
    db: Session = Depends(get_db),
    x_gemini_key: Optional[str] = Header(None),
    x_mock_mode: Optional[str] = Header(None)
):
    # Run AI Analysis
    analysis = analyze_decision_with_ai(
        payload.input_text,
        payload.stress_level,
        payload.financial_cost,
        payload.emotional_risk,
        payload.confidence_level,
        api_key=x_gemini_key,
        use_mock=(x_mock_mode == "true")
    )

    try:
        validated_analysis = DecisionAnalysisResponse(**analysis)
    except ValidationError as exc:
        print(f"AI analysis validation failed: {exc}")
        raise HTTPException(status_code=500, detail=f"Invalid AI response format: {exc}")
    
    # Create DB Record
    db_decision = Decision(
        title=validated_analysis.title,
        input_text=payload.input_text,
        emotion_analysis=json.dumps(validated_analysis.emotion_analysis),
        regret_probability=validated_analysis.regret_probability,
        satisfaction_score=validated_analysis.satisfaction_score,
        stress_prediction=validated_analysis.stress_prediction,
        emotional_stability=validated_analysis.emotional_stability,
        personality_insights=json.dumps(validated_analysis.personality_insights.dict()),
        timeline_a_json=json.dumps(validated_analysis.timeline_a.dict()),
        timeline_b_json=json.dumps(validated_analysis.timeline_b.dict()),
        swot_analysis=json.dumps(validated_analysis.swot_analysis.dict()),
        summary_recommendation=validated_analysis.summary_recommendation
    )
    
    db.add(db_decision)
    db.commit()
    db.refresh(db_decision)
    
    return serialize_decision_db_to_response(db_decision)


@app.post("/api/analyze/mock", response_model=DecisionResponse)
def analyze_decision_mock(
    payload: DecisionCreate,
    db: Session = Depends(get_db)
):
    """Fast path that always uses local mock analysis regardless of API key.
    Use this when the Gemini API is slow or unavailable to provide immediate results.
    """
    analysis = analyze_decision_with_ai(
        payload.input_text,
        payload.stress_level,
        payload.financial_cost,
        payload.emotional_risk,
        payload.confidence_level,
        use_mock=True,
    )

    try:
        validated_analysis = DecisionAnalysisResponse(**analysis)
    except ValidationError as exc:
        print(f"AI analysis validation failed (mock): {exc}")
        raise HTTPException(status_code=500, detail=f"Invalid AI response format: {exc}")

    db_decision = Decision(
        title=validated_analysis.title,
        input_text=payload.input_text,
        emotion_analysis=json.dumps(validated_analysis.emotion_analysis),
        regret_probability=validated_analysis.regret_probability,
        satisfaction_score=validated_analysis.satisfaction_score,
        stress_prediction=validated_analysis.stress_prediction,
        emotional_stability=validated_analysis.emotional_stability,
        personality_insights=json.dumps(validated_analysis.personality_insights.dict()),
        timeline_a_json=json.dumps(validated_analysis.timeline_a.dict()),
        timeline_b_json=json.dumps(validated_analysis.timeline_b.dict()),
        swot_analysis=json.dumps(validated_analysis.swot_analysis.dict()),
        summary_recommendation=validated_analysis.summary_recommendation
    )

    db.add(db_decision)
    db.commit()
    db.refresh(db_decision)

    return serialize_decision_db_to_response(db_decision)

@app.get("/api/decisions", response_model=List[DecisionResponse])
def list_decisions(db: Session = Depends(get_db)):
    decisions = db.query(Decision).order_by(Decision.created_at.desc()).all()
    return [serialize_decision_db_to_response(d) for d in decisions]

@app.delete("/api/decisions/{decision_id}")
def delete_decision(decision_id: int, db: Session = Depends(get_db)):
    db_dec = db.query(Decision).filter(Decision.id == decision_id).first()
    if not db_dec:
        raise HTTPException(status_code=404, detail="Decision not found")
    db.delete(db_dec)
    db.commit()
    return {"detail": "Decision deleted successfully"}

@app.post("/api/decisions/{decision_id}/resolve", response_model=DecisionResponse)
def resolve_decision(decision_id: int, payload: DecisionResolve, db: Session = Depends(get_db)):
    db_dec = db.query(Decision).filter(Decision.id == decision_id).first()
    if not db_dec:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    db_dec.actual_regret_status = payload.actual_regret_status
    db.commit()
    db.refresh(db_dec)
    
    return serialize_decision_db_to_response(db_dec)

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "engine": "FutureMind AI Regret Prediction Engine"}
