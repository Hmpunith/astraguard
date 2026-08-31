import { OrbitalObject, Conjunction, AnalysisResponse, SystemStatus, ManeuverOption, AIRecommendation } from './types';

// ─── Mock Data (fallback when backend is unavailable) ───
const mockSatellites: OrbitalObject[] = [
  { id: '25544', name: 'ISS (ZARYA)', type: 'satellite', latitude: 35.0, longitude: -120.0, altitude: 408 },
  { id: '44713', name: 'STARLINK-1007', type: 'satellite', latitude: -10.0, longitude: 45.0, altitude: 550 },
  { id: '47913', name: 'STARLINK-2305', type: 'satellite', latitude: 20.0, longitude: 80.0, altitude: 550 },
  { id: '20580', name: 'HUBBLE SPACE TELESCOPE', type: 'satellite', latitude: 28.5, longitude: -70.0, altitude: 537 },
  { id: '48274', name: 'TIANGONG', type: 'satellite', latitude: 41.5, longitude: 95.0, altitude: 390 },
  { id: '46984', name: 'SENTINEL-6A', type: 'satellite', latitude: -5.0, longitude: 160.0, altitude: 1336 },
  { id: '49260', name: 'LANDSAT-9', type: 'satellite', latitude: 65.0, longitude: -45.0, altitude: 705 },
  { id: '43013', name: 'NOAA-20', type: 'satellite', latitude: -72.0, longitude: 120.0, altitude: 824 },
  { id: '33751', name: 'COSMOS 2251 DEB', type: 'debris', latitude: 40.0, longitude: -118.0, altitude: 780 },
  { id: '30000', name: 'FENGYUN 1C DEB', type: 'debris', latitude: -8.0, longitude: 47.0, altitude: 850 },
  { id: '33752', name: 'IRIDIUM 33 DEB', type: 'debris', latitude: 55.0, longitude: 30.0, altitude: 790 },
  { id: '20000', name: 'SL-8 R/B', type: 'debris', latitude: 22.0, longitude: 82.0, altitude: 500 },
];

const mockConjunctions: Conjunction[] = [
  {
    id: 'CJ-001',
    primaryObjectId: '25544',
    primaryObjectName: 'ISS (ZARYA)',
    secondaryObjectId: '33751',
    secondaryObjectName: 'COSMOS 2251 DEB',
    riskScore: 85,
    missDistanceKm: 1.8,
    relativeVelocityKmS: 14.5,
    tca: new Date(Date.now() + 1000 * 60 * 252).toISOString(),
  },
  {
    id: 'CJ-002',
    primaryObjectId: '44713',
    primaryObjectName: 'STARLINK-1007',
    secondaryObjectId: '30000',
    secondaryObjectName: 'FENGYUN 1C DEB',
    riskScore: 45,
    missDistanceKm: 5.2,
    relativeVelocityKmS: 11.2,
    tca: new Date(Date.now() + 1000 * 60 * 765).toISOString(),
  },
  {
    id: 'CJ-003',
    primaryObjectId: '20580',
    primaryObjectName: 'HUBBLE SPACE TELESCOPE',
    secondaryObjectId: '33752',
    secondaryObjectName: 'IRIDIUM 33 DEB',
    riskScore: 92,
    missDistanceKm: 0.4,
    relativeVelocityKmS: 15.2,
    tca: new Date(Date.now() + 1000 * 60 * 150).toISOString(),
  },
  {
    id: 'CJ-004',
    primaryObjectId: '47913',
    primaryObjectName: 'STARLINK-2305',
    secondaryObjectId: '20000',
    secondaryObjectName: 'SL-8 R/B',
    riskScore: 15,
    missDistanceKm: 22.0,
    relativeVelocityKmS: 9.8,
    tca: new Date(Date.now() + 1000 * 60 * 2190).toISOString(),
  }
];

const mockAnalysis: AnalysisResponse = {
  conjunctionId: 'CJ-001',  // default; overridden per conjunction at call time
  maneuverOptions: [
    {
      id: 'CJ-001-MNV-1',
      name: 'Conservative',
      deltaV: 2.0,
      fuelCost: 0.34,
      resultingMissDistanceKm: 55.0,
      riskReductionLevel: 'high',
    },
    {
      id: 'CJ-001-MNV-2',
      name: 'Balanced',
      deltaV: 0.8,
      fuelCost: 0.136,
      resultingMissDistanceKm: 25.0,
      riskReductionLevel: 'high',
    },
    {
      id: 'CJ-001-MNV-3',
      name: 'Minimal',
      deltaV: 0.2,
      fuelCost: 0.034,
      resultingMissDistanceKm: 12.0,
      riskReductionLevel: 'medium',
    }
  ],
  aiRecommendation: {
    recommendedManeuverId: 'CJ-001-MNV-2',
    confidence: 88,
    reasoning: 'The Balanced maneuver (0.8 m/s) provides an optimal trade-off. It achieves a 25.0 km miss distance, well above the 15 km safety threshold, while consuming only 0.136 kg of fuel — preserving delta-v reserves for future station-keeping.',
    riskFactors: [
      'High relative velocity of 14.5 km/s increases collision energy',
      'Secondary object (DEBRIS) presents an uncontrolled trajectory',
      'Time to closest approach is limited, requiring prompt action'
    ],
    tradeOffs: 'Conservative maneuver uses excessive fuel (0.34 kg) for marginal additional safety. Minimal maneuver leaves too little margin (12 km) given the orbital uncertainty.',
    secondaryRisks: 'Minimal risk of generating new conjunctions with nearby objects during the burn. Post-maneuver trajectory cleared for 7 days.',
    briefingText: 'OPERATOR BRIEFING — CONJUNCTION CJ-001\n\nBased on conjunction assessment analysis, IBM Granite AI recommends executing Balanced maneuver (MNV-2): retrograde burn of 0.8 m/s delta-v.\n\nThis maneuver requires 0.136 kg of propellant and will increase the miss distance from 1.8 km to a safe 25.0 km. Confidence score: 88%.\n\nRationale: The Balanced option provides the optimal trade-off between collision risk mitigation and fuel conservation. The Conservative option (MNV-1) would provide greater clearance but at 2.5x the fuel cost with diminishing safety returns. The Minimal option (MNV-3) provides insufficient margin given the 14.5 km/s relative velocity and debris trajectory uncertainty.\n\nSecondary collision screening: CLEAR. No new conjunctions projected in the post-maneuver orbital regime for 7 days.\n\nRecommendation: EXECUTE MNV-2. Awaiting operator authorization.'
  }
};

const mockStatus: SystemStatus = {
  status: 'operational',
  trackedObjectsCount: 12,
  activeConjunctionsCount: 4,
  highestRiskLevel: 'critical',
};

// ─── Backend Response Transformers ───

function transformSatellite(raw: any): OrbitalObject {
  return {
    id: raw.norad_id || raw.id || '',
    name: raw.name || 'Unknown',
    type: raw.object_type === 'PAYLOAD' ? 'satellite' : 'debris',
    latitude: raw.latitude || 0,
    longitude: raw.longitude || 0,
    altitude: raw.altitude_km || 0,
  };
}

function transformConjunction(raw: any): Conjunction {
  return {
    id: raw.id,
    primaryObjectId: raw.primary?.norad_id || '',
    primaryObjectName: raw.primary?.name || 'Unknown',
    secondaryObjectId: raw.secondary?.norad_id || '',
    secondaryObjectName: raw.secondary?.name || 'Unknown',
    riskScore: raw.risk_score || 0,
    missDistanceKm: raw.miss_distance_km || 0,
    relativeVelocityKmS: raw.relative_velocity_km_s || 0,
    tca: raw.tca || '',
  };
}

function transformManeuver(raw: any): ManeuverOption {
  return {
    id: raw.id,
    name: raw.name,
    deltaV: raw.delta_v_m_s || 0,
    fuelCost: raw.fuel_cost_kg || 0,
    resultingMissDistanceKm: raw.resulting_miss_distance_km || 0,
    riskReductionLevel: raw.risk_reduction?.toLowerCase().includes('0%') ? 'high' 
      : raw.risk_reduction?.toLowerCase().includes('1%') ? 'high' 
      : 'medium',
  };
}

function transformAnalysis(raw: any): AnalysisResponse {
  const rec = raw.ai_recommendation || {};
  return {
    conjunctionId: raw.conjunction_id,
    maneuverOptions: (raw.maneuvers || []).map(transformManeuver),
    aiRecommendation: {
      recommendedManeuverId: rec.recommended_maneuver_id || '',
      confidence: Math.round((rec.confidence || 0) * 100),
      reasoning: rec.reasoning || '',
      riskFactors: rec.risk_factors || [],
      tradeOffs: rec.trade_off_analysis || '',
      secondaryRisks: rec.secondary_risks || '',
      briefingText: rec.operator_briefing || '',
    },
  };
}

function transformStatus(raw: any): SystemStatus {
  return {
    status: (raw.status || 'operational').toLowerCase() as any,
    trackedObjectsCount: raw.tracked_objects || 0,
    activeConjunctionsCount: raw.active_conjunctions || 0,
    highestRiskLevel: (raw.highest_risk || 'none').toLowerCase() as any,
  };
}

// ─── API Client ───

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function tryFetch<T>(url: string, options?: RequestInit): Promise<T | null> {
  try {
    const res = await fetch(url, { ...options, signal: AbortSignal.timeout(5000) });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch {
    return null;
  }
}

export async function fetchStatus(): Promise<SystemStatus> {
  const raw = await tryFetch(`${BASE_URL}/api/status`);
  if (raw) return transformStatus(raw);
  return mockStatus;
}

export async function fetchSatellites(): Promise<OrbitalObject[]> {
  const raw = await tryFetch<any[]>(`${BASE_URL}/api/satellites`);
  if (raw && Array.isArray(raw)) return raw.map(transformSatellite);
  return mockSatellites;
}

export async function fetchConjunctions(): Promise<Conjunction[]> {
  const raw = await tryFetch<any[]>(`${BASE_URL}/api/conjunctions`);
  if (raw && Array.isArray(raw)) return raw.map(transformConjunction);
  return mockConjunctions;
}

export async function analyzeConjunction(id: string): Promise<AnalysisResponse> {
  const raw = await tryFetch(`${BASE_URL}/api/conjunctions/${id}/analyze`, { method: 'POST' });
  if (raw) return transformAnalysis(raw);
  return { ...mockAnalysis, conjunctionId: id };
}

export async function approveManeuver(conjunctionId: string, maneuverId: string): Promise<{ success: boolean }> {
  const raw = await tryFetch(`${BASE_URL}/api/conjunctions/${conjunctionId}/approve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ maneuver_id: maneuverId }),
  });
  if (raw) return { success: true };
  // Mock fallback
  return new Promise(resolve => setTimeout(() => resolve({ success: true }), 1000));
}
