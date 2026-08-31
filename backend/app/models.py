from enum import Enum
from typing import Optional, List
from pydantic import BaseModel

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class OrbitalObject(BaseModel):
    norad_id: Optional[str] = None
    name: Optional[str] = None
    object_type: Optional[str] = None # PAYLOAD, DEBRIS, ROCKET_BODY
    tle_line1: Optional[str] = None
    tle_line2: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude_km: Optional[float] = None
    velocity_km_s: Optional[float] = None

class OrbitPoint(BaseModel):
    timestamp: str
    latitude: float
    longitude: float
    altitude_km: float

class Conjunction(BaseModel):
    id: str
    primary: OrbitalObject
    secondary: OrbitalObject
    tca: str
    miss_distance_km: float
    relative_velocity_km_s: float
    risk_score: float
    risk_level: RiskLevel
    time_to_tca_seconds: float

class ManeuverOption(BaseModel):
    id: str
    name: str
    description: str
    delta_v_m_s: float
    burn_direction: str
    fuel_cost_kg: float
    resulting_miss_distance_km: float
    execution_window: str
    risk_reduction: str

class AIRecommendation(BaseModel):
    recommended_maneuver_id: str
    confidence: float
    reasoning: str
    risk_factors: List[str]
    trade_off_analysis: str
    secondary_risks: str
    operator_briefing: str

class AnalysisResponse(BaseModel):
    conjunction_id: str
    maneuvers: List[ManeuverOption]
    ai_recommendation: AIRecommendation

class ApprovalRequest(BaseModel):
    maneuver_id: str

class ApprovalResponse(BaseModel):
    status: str
    conjunction_id: str
    maneuver_id: str
    message: str

class SystemStatus(BaseModel):
    status: str
    tracked_objects: int
    active_conjunctions: int
    highest_risk: str
