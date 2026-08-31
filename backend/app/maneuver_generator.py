from datetime import datetime, timezone, timedelta
from .models import Conjunction, ManeuverOption

def generate_maneuvers(conjunction: Conjunction) -> list[ManeuverOption]:
    """Generate 3 avoidance maneuver options for a conjunction."""
    tca = datetime.fromisoformat(conjunction.tca)
    options = []
    
    mass_kg = 500.0
    isp_s = 300.0
    g0 = 9.80665
    
    def calc_fuel(dv: float) -> float:
        # Rocket equation approximation for small delta-v
        # m_fuel = m0 * (1 - exp(-dv / (Isp * g0)))
        import math
        return mass_kg * (1 - math.exp(-dv / (isp_s * g0)))

    # Option 1: Conservative
    dv1 = 2.0
    options.append(ManeuverOption(
        id=f"{conjunction.id}-MNV-1",
        name="Conservative",
        description="Maximum safety margin, high fuel cost.",
        delta_v_m_s=dv1,
        burn_direction="prograde",
        fuel_cost_kg=round(calc_fuel(dv1), 3),
        resulting_miss_distance_km=55.0,
        execution_window=(tca - timedelta(hours=2)).isoformat(),
        risk_reduction="Reduces risk to 0%"
    ))
    
    # Option 2: Balanced
    dv2 = 0.8
    options.append(ManeuverOption(
        id=f"{conjunction.id}-MNV-2",
        name="Balanced",
        description="Good safety/fuel trade-off.",
        delta_v_m_s=dv2,
        burn_direction="retrograde",
        fuel_cost_kg=round(calc_fuel(dv2), 3),
        resulting_miss_distance_km=25.0,
        execution_window=(tca - timedelta(minutes=90)).isoformat(),
        risk_reduction="Reduces risk to < 1%"
    ))
    
    # Option 3: Minimal
    dv3 = 0.2
    options.append(ManeuverOption(
        id=f"{conjunction.id}-MNV-3",
        name="Minimal",
        description="Minimum safe clearance, low fuel cost.",
        delta_v_m_s=dv3,
        burn_direction="normal",
        fuel_cost_kg=round(calc_fuel(dv3), 3),
        resulting_miss_distance_km=12.0,
        execution_window=(tca - timedelta(hours=1)).isoformat(),
        risk_reduction="Reduces risk to ~5%"
    ))
    
    return options
