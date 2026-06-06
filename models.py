import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from backend.database import Base

class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    input_text = Column(Text)
    emotion_analysis = Column(Text)  # JSON string
    regret_probability = Column(Float)
    satisfaction_score = Column(Float)
    stress_prediction = Column(String)
    emotional_stability = Column(String)
    personality_insights = Column(Text)  # JSON string
    timeline_a_json = Column(Text)  # JSON string
    timeline_b_json = Column(Text)  # JSON string
    swot_analysis = Column(Text)  # JSON string
    summary_recommendation = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    actual_regret_status = Column(String, default="unresolved")  # "unresolved", "happy", "neutral", "regret"
