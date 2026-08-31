'use client';

import React, { useState } from 'react';
import { ManeuverOption } from '../lib/types';
import { Fuel, Target, CheckCircle } from 'lucide-react';

interface ManeuverPanelProps {
  options: ManeuverOption[];
  recommendedId: string;
  onApprove: (id: string) => Promise<void>;
}

export default function ManeuverPanel({ options, recommendedId, onApprove }: ManeuverPanelProps) {
  const [approving, setApproving] = useState<string | null>(null);
  const [approved, setApproved] = useState<string | null>(null);

  const handleApprove = async (id: string) => {
    setApproving(id);
    await onApprove(id);
    setApproved(id);
    setApproving(null);
  };

  if (approved) {
    return (
      <div className="bg-green-900/20 border border-green-500/50 rounded-lg p-6 flex flex-col items-center justify-center text-center space-y-4">
        <CheckCircle className="w-16 h-16 text-green-500" />
        <h3 className="text-xl font-bold text-green-400">Maneuver Approved</h3>
        <p className="text-slate-300">Commands have been queued for transmission to the spacecraft.</p>
        <div className="font-mono text-sm bg-slate-900 p-2 rounded border border-slate-700 text-slate-400 w-full">
          STATUS: UPLINK_QUEUED | ID: {approved}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-bold text-white mb-2">Maneuver Options</h3>
      
      {options.map((option) => {
        const isRecommended = option.id === recommendedId;
        
        return (
          <div 
            key={option.id} 
            className={`p-4 rounded-lg border ${isRecommended ? 'border-green-500 bg-green-900/10' : 'border-slate-700 bg-slate-800'}`}
          >
            <div className="flex justify-between items-start mb-3">
              <div>
                <div className="flex items-center gap-2">
                  <h4 className="font-bold text-white">{option.name}</h4>
                  {isRecommended && (
                    <span className="text-[10px] font-bold bg-green-500/20 text-green-400 px-2 py-0.5 rounded border border-green-500/30 uppercase">
                      AI Recommended
                    </span>
                  )}
                </div>
                <div className="text-xs text-slate-400 mt-1">ID: {option.id}</div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3 mb-4">
              <div className="flex items-center gap-2 text-sm text-slate-300">
                <ActivityIcon className="w-4 h-4 text-cyan-400" />
                <span>ΔV: {option.deltaV} m/s</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-slate-300">
                <Fuel className="w-4 h-4 text-orange-400" />
                <span>Fuel: {option.fuelCost} kg</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-slate-300">
                <Target className="w-4 h-4 text-green-400" />
                <span>New Miss: {option.resultingMissDistanceKm} km</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-slate-300">
                <ShieldIcon className="w-4 h-4 text-blue-400" />
                <span>Risk: <span className="capitalize">{option.riskReductionLevel}</span> Reduction</span>
              </div>
            </div>

            <div className="flex gap-2">
              <button className="flex-1 px-3 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded text-sm font-medium transition-colors">
                Simulate
              </button>
              {isRecommended && (
                <button 
                  onClick={() => handleApprove(option.id)}
                  disabled={approving !== null}
                  className="flex-1 px-3 py-2 bg-green-600 hover:bg-green-500 text-white rounded text-sm font-bold transition-colors flex justify-center items-center"
                >
                  {approving === option.id ? 'Approving...' : 'AUTHORIZE EXECUTION'}
                </button>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}

// Simple icons for local use
const ActivityIcon = (props: any) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
);
const ShieldIcon = (props: any) => (
  <svg {...props} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
);
