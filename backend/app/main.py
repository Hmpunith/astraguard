import os
import uuid
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

from .models import (
    SystemStatus, OrbitalObject, Conjunction, ManeuverOption,
    AnalysisResponse, ApprovalRequest, ApprovalResponse, AIRecommendation
)
from .tle_fetcher import fetch_tle_data
from .orbit_propagator import get_current_position, propagate_orbit
from .conjunction_detector import detect_conjunctions
from .maneuver_generator import generate_maneuvers
from .granite_advisor import GraniteAdvisor

app = FastAPI(title="AstraGuard Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# State
tracked_objects: List[OrbitalObject] = []
active_conjunctions: List[Conjunction] = []
advisor = GraniteAdvisor()

@app.on_event("startup")
def startup_event():
    global tracked_objects, active_conjunctions
    
    # 1. Fetch TLE data
    tle_data = fetch_tle_data()
    for name, line1, line2, obj_type in tle_data:
        lat, lon, alt, vel = get_current_position(line1, line2)
        norad_id = line2.split()[1] if len(line2.split()) > 1 else str(uuid.uuid4().hex[:5])
        tracked_objects.append(OrbitalObject(
            norad_id=norad_id,
            name=name,
            object_type=obj_type,
            tle_line1=line1,
            tle_line2=line2,
            latitude=lat,
            longitude=lon,
            altitude_km=alt,
            velocity_km_s=vel
        ))
        
    # 2. Detect Conjunctions
    active_conjunctions = detect_conjunctions(tracked_objects)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/status", response_model=SystemStatus)
def get_status():
    highest = "LOW"
    if active_conjunctions:
        # Simple risk level ordering
        levels = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
        highest_cj = max(active_conjunctions, key=lambda c: levels.get(c.risk_level.value, 0))
        highest = highest_cj.risk_level.value
        
    return SystemStatus(
        status="OPERATIONAL",
        tracked_objects=len(tracked_objects),
        active_conjunctions=len(active_conjunctions),
        highest_risk=highest
    )

@app.get("/api/satellites")
def get_satellites():
    # Return objects with short propagated paths
    result = []
    now = datetime.now(timezone.utc)
    for obj in tracked_objects:
        path = propagate_orbit(obj.tle_line1, obj.tle_line2, now, 90, 1)
        obj_dict = obj.model_dump()
        obj_dict["path"] = [p.model_dump() for p in path]
        result.append(obj_dict)
    return result

@app.get("/api/conjunctions", response_model=List[Conjunction])
def get_conjunctions():
    # Update time_to_tca_seconds dynamically
    now = datetime.now(timezone.utc)
    for cj in active_conjunctions:
        tca = datetime.fromisoformat(cj.tca)
        cj.time_to_tca_seconds = max(0.0, (tca - now).total_seconds())
    return active_conjunctions

@app.get("/api/conjunctions/{conjunction_id}", response_model=Conjunction)
def get_conjunction(conjunction_id: str):
    now = datetime.now(timezone.utc)
    for cj in active_conjunctions:
        if cj.id == conjunction_id:
            tca = datetime.fromisoformat(cj.tca)
            cj.time_to_tca_seconds = max(0.0, (tca - now).total_seconds())
            return cj
    raise HTTPException(status_code=404, detail="Conjunction not found")

@app.post("/api/conjunctions/{conjunction_id}/analyze", response_model=AnalysisResponse)
def analyze_conjunction(conjunction_id: str):
    cj = None
    for c in active_conjunctions:
        if c.id == conjunction_id:
            cj = c
            break
            
    if not cj:
        raise HTTPException(status_code=404, detail="Conjunction not found")
        
    maneuvers = generate_maneuvers(cj)
    recommendation = advisor.analyze_conjunction(cj, maneuvers)
    
    return AnalysisResponse(
        conjunction_id=cj.id,
        maneuvers=maneuvers,
        ai_recommendation=recommendation
    )

@app.post("/api/conjunctions/{conjunction_id}/approve", response_model=ApprovalResponse)
def approve_maneuver(conjunction_id: str, request: ApprovalRequest):
    # In a real app we'd dispatch commands to the satellite
    # Here we just remove the conjunction from active tracking
    global active_conjunctions
    active_conjunctions = [c for c in active_conjunctions if c.id != conjunction_id]
    
    return ApprovalResponse(
        status="APPROVED",
        conjunction_id=conjunction_id,
        maneuver_id=request.maneuver_id,
        message=f"Maneuver {request.maneuver_id} approved and execution scheduled."
    )
