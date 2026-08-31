import math
from .models import RiskLevel

def score_risk(miss_distance_km: float, relative_velocity_km_s: float, primary_type: str, secondary_type: str) -> tuple[float, RiskLevel]:
    """
    Score conjunction risk on a 0-100 scale.
    """
    # 1. Distance factor (exponential decay)
    # Closer = much higher risk
    if miss_distance_km <= 0:
        dist_factor = 100.0
    else:
        dist_factor = 100.0 * math.exp(-0.1 * miss_distance_km)
        
    # 2. Velocity factor
    vel_factor = min(1.0, relative_velocity_km_s / 20.0)
    
    # 3. Size factor
    def type_weight(t: str) -> float:
        if t == "PAYLOAD": return 1.0
        if t == "ROCKET_BODY": return 0.8
        if t == "DEBRIS": return 0.5
        return 0.5
        
    size_factor = (type_weight(primary_type) + type_weight(secondary_type)) / 2.0
    
    # Combine (weighted)
    score = (dist_factor * 0.7) + (vel_factor * 100 * 0.15) + (size_factor * 100 * 0.15)
    score = max(0.0, min(100.0, score))
    
    # Map to level
    if score < 25:
        level = RiskLevel.LOW
    elif score < 50:
        level = RiskLevel.MEDIUM
    elif score < 75:
        level = RiskLevel.HIGH
    else:
        level = RiskLevel.CRITICAL
        
    return round(score, 1), level
