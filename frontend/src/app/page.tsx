'use client';

import React, { useEffect, useState } from 'react';
import { fetchStatus, fetchSatellites, fetchConjunctions, analyzeConjunction, approveManeuver } from '../lib/api';
import { SystemStatus, OrbitalObject, Conjunction, AnalysisResponse } from '../lib/types';
import MapDisplay from '../components/MapDisplay';
import StatsBar from '../components/StatsBar';
import Dashboard from '../components/Dashboard';

export default function Home() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [satellites, setSatellites] = useState<OrbitalObject[]>([]);
  const [conjunctions, setConjunctions] = useState<Conjunction[]>([]);
  const [activeAnalysis, setActiveAnalysis] = useState<AnalysisResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [stat, sats, conjs] = await Promise.all([
          fetchStatus(),
          fetchSatellites(),
          fetchConjunctions()
        ]);
        setStatus(stat);
        setSatellites(sats);
        setConjunctions(conjs);
      } catch (error) {
        console.error("Failed to load data", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleAnalyze = async (id: string) => {
    setIsAnalyzing(true);
    try {
      // Simulate network delay for demo
      await new Promise(resolve => setTimeout(resolve, 1500));
      const result = await analyzeConjunction(id);
      setActiveAnalysis(result);
    } catch (error) {
      console.error("Analysis failed", error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleApproveManeuver = async (conjunctionId: string, maneuverId: string) => {
    try {
      await approveManeuver(conjunctionId, maneuverId);
      // In a real app, we would refresh the state here to remove the conjunction
    } catch (error) {
      console.error("Failed to approve maneuver", error);
    }
  };

  if (loading || !status) {
    return (
      <div className="flex items-center justify-center w-full h-full bg-[#0a0e27] text-cyan-400">
        <div className="flex flex-col items-center">
          <div className="w-12 h-12 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="font-mono tracking-widest text-sm">INITIALIZING ASTRAGUARD SYSTEMS...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-[#0a0e27]">
      <StatsBar status={status} />
      
      <div className="flex flex-1 overflow-hidden">
        {/* Left Side: Map View (60%) */}
        <div className="w-[60%] h-full relative">
          <MapDisplay satellites={satellites} conjunctions={conjunctions} />
        </div>
        
        {/* Right Side: Dashboard (40%) */}
        <div className="w-[40%] h-full">
          <Dashboard 
            conjunctions={conjunctions} 
            activeAnalysis={activeAnalysis} 
            onAnalyze={handleAnalyze} 
            isAnalyzing={isAnalyzing}
            onApproveManeuver={handleApproveManeuver}
          />
        </div>
      </div>
    </div>
  );
}
