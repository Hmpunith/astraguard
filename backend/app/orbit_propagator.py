import math
import numpy as np
from datetime import datetime, timezone, timedelta
from sgp4.api import Satrec, WGS84
from .models import OrbitPoint

def propagate_orbit(tle_line1: str, tle_line2: str, start_time: datetime, duration_minutes: int, step_minutes: int) -> list[OrbitPoint]:
    """Propagate orbit over a time window and return path points."""
    satellite = Satrec.twoline2rv(tle_line1, tle_line2)
    points = []
    
    current_time = start_time
    end_time = start_time + timedelta(minutes=duration_minutes)
    
    while current_time <= end_time:
        jd, fr = get_jd_fr(current_time)
        e, r, v = satellite.sgp4(jd, fr)
        if e == 0:
            lat, lon, alt = eci2lla(r, current_time)
            points.append(OrbitPoint(
                timestamp=current_time.isoformat(),
                latitude=lat,
                longitude=lon,
                altitude_km=alt
            ))
        current_time += timedelta(minutes=step_minutes)
        
    return points

def get_current_position(tle_line1: str, tle_line2: str) -> tuple[float, float, float, float]:
    """Get current lat, lon, alt, and velocity magnitude."""
    satellite = Satrec.twoline2rv(tle_line1, tle_line2)
    current_time = datetime.now(timezone.utc)
    jd, fr = get_jd_fr(current_time)
    e, r, v = satellite.sgp4(jd, fr)
    
    if e == 0:
        lat, lon, alt = eci2lla(r, current_time)
        velocity_km_s = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
        return lat, lon, alt, velocity_km_s
    return 0.0, 0.0, 0.0, 0.0

def propagate_pair(tle1_line1: str, tle1_line2: str, tle2_line1: str, tle2_line2: str, start_time: datetime, duration_hours: int, step_seconds: int) -> list:
    """Propagate two objects and return distance between them."""
    sat1 = Satrec.twoline2rv(tle1_line1, tle1_line2)
    sat2 = Satrec.twoline2rv(tle2_line1, tle2_line2)
    
    results = []
    current_time = start_time
    end_time = start_time + timedelta(hours=duration_hours)
    
    while current_time <= end_time:
        jd, fr = get_jd_fr(current_time)
        e1, r1, v1 = sat1.sgp4(jd, fr)
        e2, r2, v2 = sat2.sgp4(jd, fr)
        
        if e1 == 0 and e2 == 0:
            dist = math.sqrt((r1[0]-r2[0])**2 + (r1[1]-r2[1])**2 + (r1[2]-r2[2])**2)
            results.append((current_time, dist, r1, r2, v1, v2))
        
        current_time += timedelta(seconds=step_seconds)
        
    return results

def get_jd_fr(dt: datetime) -> tuple[float, float]:
    """Calculate Julian Date and fraction from datetime."""
    # SGP4 wants julian date
    # A simple conversion
    time_tuple = dt.utctimetuple()
    year = time_tuple.tm_year
    month = time_tuple.tm_mon
    day = time_tuple.tm_mday
    hour = time_tuple.tm_hour
    minute = time_tuple.tm_min
    sec = time_tuple.tm_sec
    
    if month <= 2:
        year -= 1
        month += 12
        
    A = year // 100
    B = 2 - A + (A // 4)
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    fr = (hour + minute / 60.0 + sec / 3600.0) / 24.0
    return jd, fr

def eci2lla(r: tuple, dt: datetime) -> tuple[float, float, float]:
    """Convert ECI to Lat/Lon/Alt."""
    # Simplified estimation
    # GMST estimation
    jd, fr = get_jd_fr(dt)
    jd_total = jd + fr
    d = jd_total - 2451545.0
    gmst = (18.697374558 + 24.06570982441908 * d) % 24.0
    gmst_rad = gmst * math.pi / 12.0
    
    x, y, z = r
    
    lon = math.atan2(y, x) - gmst_rad
    lon = (lon + math.pi) % (2 * math.pi) - math.pi
    
    r_eq = math.sqrt(x**2 + y**2)
    lat = math.atan2(z, r_eq)
    
    alt = math.sqrt(x**2 + y**2 + z**2) - 6371.0
    return math.degrees(lat), math.degrees(lon), alt
