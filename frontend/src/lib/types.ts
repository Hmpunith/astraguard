export interface OrbitalObject {
  id: string;
  name: string;
  type: 'satellite' | 'debris';
  latitude: number;
  longitude: number;
  altitude: number;
}

export interface Conjunction {
  id: string;
  primaryObjectId: string;
  primaryObjectName: string;
  secondaryObjectId: string;
  secondaryObjectName: string;
  riskScore: number;
  missDistanceKm: number;
  relativeVelocityKmS: number;
  tca: string; // Time of Closest Approach (ISO string)
}

export interface ManeuverOption {
  id: string;
  name: string;
  deltaV: number;
  fuelCost: number;
  resultingMissDistanceKm: number;
  riskReductionLevel: 'low' | 'medium' | 'high';
}

export interface AIRecommendation {
  recommendedManeuverId: string;
  confidence: number;
  reasoning: string;
  riskFactors: string[];
  tradeOffs: string;
  secondaryRisks: string;
  briefingText: string;
}

export interface AnalysisResponse {
  conjunctionId: string;
  maneuverOptions: ManeuverOption[];
  aiRecommendation: AIRecommendation;
}

export interface SystemStatus {
  status: 'operational' | 'degraded' | 'offline';
  trackedObjectsCount: number;
  activeConjunctionsCount: number;
  highestRiskLevel: 'none' | 'low' | 'medium' | 'high' | 'critical';
}
