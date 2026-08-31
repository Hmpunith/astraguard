import os
import uuid
from datetime import datetime, timezone, timedelta
from typing import List
from .models import Conjunction, OrbitalObject, RiskLevel
from .orbit_propagator import propagate_pair
from .risk_scorer import score_risk

def detect_conjunctions(objects: List[OrbitalObject], time_window_hours: int = 72, distance_threshold_km: float = 50.0) -> List[Conjunction]:
    """Detect conjunctions between tracked objects."""
    demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
    if demo_mode:
        return generate_demo_conjunctions(objects)

    conjunctions = []
    now = datetime.now(timezone.utc)
    
    # Simple N^2 search for small catalogues
    for i in range(len(objects)):
        for j in range(i + 1, len(objects)):
            obj1 = objects[i]
            obj2 = objects[j]
            
            # Propagate pair
            results = propagate_pair(
                obj1.tle_line1, obj1.tle_line2,
                obj2.tle_line1, obj2.tle_line2,
                now, time_window_hours, 60
            )
            
            if not results:
                continue
                
            # Find min distance
            min_dist_entry = min(results, key=lambda x: x[1])
            tca, min_dist, r1, r2, v1, v2 = min_dist_entry
            
            if min_dist < distance_threshold_km:
                # Calc relative velocity
                rel_v = ((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2 + (v1[2]-v2[2])**2)**0.5
                score, level = score_risk(min_dist, rel_v, obj1.object_type, obj2.object_type)
                
                cj = Conjunction(
                    id=f"CJ-{uuid.uuid4().hex[:6].upper()}",
                    primary=obj1,
                    secondary=obj2,
                    tca=tca.isoformat(),
                    miss_distance_km=round(min_dist, 2),
                    relative_velocity_km_s=round(rel_v, 2),
                    risk_score=score,
                    risk_level=level,
                    time_to_tca_seconds=(tca - now).total_seconds()
                )
                conjunctions.append(cj)
                
    return conjunctions

def generate_demo_conjunctions(objects: List[OrbitalObject]) -> List[Conjunction]:
    """Generate 4 realistic synthetic conjunctions for demo mode."""
    now = datetime.now(timezone.utc)
    
    def find_obj(name_part):
        for o in objects:
            if name_part in (o.name or ""):
                return o
        return objects[0] if objects else None

    iss = find_obj("ISS")
    cosmos = find_obj("COSMOS")
    starlink1 = find_obj("STARLINK-1007")
    fengyun = find_obj("FENGYUN")
    starlink2 = find_obj("STARLINK-2305")
    sl8 = find_obj("SL-8")
    hubble = find_obj("HUBBLE")
    iridium = find_obj("IRIDIUM")
    
    conjunctions = []
    
    # CJ-001: ISS vs COSMOS (HIGH Risk)
    if iss and cosmos:
        tca1 = now + timedelta(hours=4, minutes=12)
        conjunctions.append(Conjunction(
            id="CJ-001",
            primary=iss,
            secondary=cosmos,
            tca=tca1.isoformat(),
            miss_distance_km=1.8,
            relative_velocity_km_s=14.5,
            risk_score=85.0,
            risk_level=RiskLevel.HIGH,
            time_to_tca_seconds=(tca1 - now).total_seconds()
        ))
        
    # CJ-002: STARLINK-1007 vs FENGYUN (MEDIUM Risk)
    if starlink1 and fengyun:
        tca2 = now + timedelta(hours=12, minutes=45)
        conjunctions.append(Conjunction(
            id="CJ-002",
            primary=starlink1,
            secondary=fengyun,
            tca=tca2.isoformat(),
            miss_distance_km=5.2,
            relative_velocity_km_s=11.2,
            risk_score=45.0,
            risk_level=RiskLevel.MEDIUM,
            time_to_tca_seconds=(tca2 - now).total_seconds()
        ))

    # CJ-003: HUBBLE vs IRIDIUM DEB (CRITICAL Risk — new demo scenario)
    if hubble and iridium:
        tca3 = now + timedelta(hours=2, minutes=30)
        conjunctions.append(Conjunction(
            id="CJ-003",
            primary=hubble,
            secondary=iridium,
            tca=tca3.isoformat(),
            miss_distance_km=0.4,
            relative_velocity_km_s=15.2,
            risk_score=92.0,
            risk_level=RiskLevel.CRITICAL,
            time_to_tca_seconds=(tca3 - now).total_seconds()
        ))
        
    # CJ-004: STARLINK-2305 vs SL-8 R/B (LOW Risk)
    if starlink2 and sl8:
        tca4 = now + timedelta(hours=36, minutes=30)
        conjunctions.append(Conjunction(
            id="CJ-004",
            primary=starlink2,
            secondary=sl8,
            tca=tca4.isoformat(),
            miss_distance_km=22.0,
            relative_velocity_km_s=9.8,
            risk_score=15.0,
            risk_level=RiskLevel.LOW,
            time_to_tca_seconds=(tca4 - now).total_seconds()
        ))
        
    return conjunctions
