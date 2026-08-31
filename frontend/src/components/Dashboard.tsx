'use client';

import React, { useState } from 'react';
import { Conjunction, AnalysisResponse } from '../lib/types';
import ConjunctionAlert from './ConjunctionAlert';
import AIAdvisorPanel from './AIAdvisorPanel';
import ManeuverPanel from './ManeuverPanel';

interface DashboardProps {
  conjunctions: Conjunction[];
  activeAnalysis: AnalysisResponse | null;
  onAnalyze: (id: string) => void;
  isAnalyzing: boolean;
  onApproveManeuver: (conjunctionId: string, maneuverId: string) => Promise<void>;
}

export default function Dashboard({ 
  conjunctions, 
  activeAnalysis, 
  onAnalyze, 
  isAnalyzing,
  onApproveManeuver
}: DashboardProps) {
  const [activeTab, setActiveTab] = useState<'alerts' | 'analysis' | 'operations'>('alerts');

  // Switch to analysis tab automatically when analysis is complete
  React.useEffect(() => {
    if (activeAnalysis) {
      setActiveTab('analysis');
    }
  }, [activeAnalysis]);

  return (
    <div className="h-full flex flex-col bg-[#0a0e27] border-l border-slate-800">
      {/* Tabs */}
      <div className="flex border-b border-slate-800">
        <button 
          onClick={() => setActiveTab('alerts')}
          className={`flex-1 py-3 text-sm font-medium transition-colors ${activeTab === 'alerts' ? 'text-cyan-400 border-b-2 border-cyan-400 bg-slate-800/30' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/20'}`}
        >
          Active Alerts
          {conjunctions.length > 0 && (
            <span className="ml-2 bg-red-500 text-white text-[10px] px-1.5 py-0.5 rounded-full">{conjunctions.length}</span>
          )}
        </button>
        <button 
          onClick={() => setActiveTab('analysis')}
          className={`flex-1 py-3 text-sm font-medium transition-colors ${activeTab === 'analysis' ? 'text-cyan-400 border-b-2 border-cyan-400 bg-slate-800/30' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/20'}`}
        >
          AI Analysis
        </button>
        <button 
          onClick={() => setActiveTab('operations')}
          className={`flex-1 py-3 text-sm font-medium transition-colors ${activeTab === 'operations' ? 'text-cyan-400 border-b-2 border-cyan-400 bg-slate-800/30' : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/20'}`}
        >
          Operations
        </button>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-y-auto p-4 custom-scrollbar">
        {activeTab === 'alerts' && (
          <div className="space-y-4">
            {conjunctions.length === 0 ? (
              <div className="text-center p-8 text-slate-500">No active conjunction alerts.</div>
            ) : (
              conjunctions.map(conj => (
                <ConjunctionAlert 
                  key={conj.id} 
                  conjunction={conj} 
                  onAnalyze={onAnalyze} 
                  isAnalyzing={isAnalyzing} 
                />
              ))
            )}
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="space-y-6">
            {!activeAnalysis ? (
              <div className="text-center p-8 text-slate-500">
                Select an alert and click "AI Analysis" to generate a maneuver recommendation.
              </div>
            ) : (
              <>
                <AIAdvisorPanel recommendation={activeAnalysis.aiRecommendation} />
                <div className="border-t border-slate-800 my-4"></div>
                <ManeuverPanel 
                  options={activeAnalysis.maneuverOptions} 
                  recommendedId={activeAnalysis.aiRecommendation.recommendedManeuverId}
                  onApprove={(mId) => onApproveManeuver(activeAnalysis.conjunctionId, mId)}
                />
              </>
            )}
          </div>
        )}

        {activeTab === 'operations' && (
          <div className="text-center p-8 text-slate-500">
            Operations log and scheduled maneuvers would appear here.
          </div>
        )}
      </div>
    </div>
  );
}
