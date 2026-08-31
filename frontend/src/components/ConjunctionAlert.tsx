'use client';

import React, { useEffect, useState } from 'react';
import { Conjunction } from '../lib/types';
import { Clock, Target, Activity, ChevronRight } from 'lucide-react';

interface ConjunctionAlertProps {
  conjunction: Conjunction;
  onAnalyze: (id: string) => void;
  isAnalyzing: boolean;
}

export default function ConjunctionAlert({ conjunction, onAnalyze, isAnalyzing }: ConjunctionAlertProps) {
  const [timeLeft, setTimeLeft] = useState<string>('');

  useEffect(() => {
    const tcaTime = new Date(conjunction.tca).getTime();

    const updateTimer = () => {
      const now = new Date().getTime();
      const diff = tcaTime - now;

      if (diff <= 0) {
        setTimeLeft('TCA PASSED');
        return;
      }

      const h = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const s = Math.floor((diff % (1000 * 60)) / 1000);
      
      setTimeLeft(`T-${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`);
    };

    updateTimer();
    const interval = setInterval(updateTimer, 1000);
    return () => clearInterval(interval);
  }, [conjunction.tca]);

  const riskColor = conjunction.riskScore > 80 ? 'border-red-500 bg-red-500/10' : 
                   conjunction.riskScore > 50 ? 'border-orange-500 bg-orange-500/10' : 
                   'border-yellow-500 bg-yellow-500/10';
                   
  const textColor = conjunction.riskScore > 80 ? 'text-red-400' : 
                   conjunction.riskScore > 50 ? 'text-orange-400' : 
                   'text-yellow-400';

  return (
    <div className={`border-l-4 rounded-r-lg p-4 mb-4 bg-slate-900 border border-t-slate-800 border-r-slate-800 border-b-slate-800 ${riskColor}`}>
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            {conjunction.primaryObjectName}
            <span className="text-slate-500 text-sm font-normal">vs</span>
            {conjunction.secondaryObjectName}
          </h3>
          <div className="text-xs text-slate-400 mt-1">ID: {conjunction.id}</div>
        </div>
        <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${riskColor.split(' ')[0]} font-mono font-bold ${textColor}`}>
          {conjunction.riskScore}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="flex items-center gap-2 text-slate-300 bg-slate-800/50 p-2 rounded">
          <Target className="w-4 h-4 text-cyan-400" />
          <div className="flex flex-col">
            <span className="text-xs text-slate-500">Miss Distance</span>
            <span className="font-mono text-sm">{conjunction.missDistanceKm.toFixed(2)} km</span>
          </div>
        </div>
        <div className="flex items-center gap-2 text-slate-300 bg-slate-800/50 p-2 rounded">
          <Activity className="w-4 h-4 text-cyan-400" />
          <div className="flex flex-col">
            <span className="text-xs text-slate-500">Relative Vel.</span>
            <span className="font-mono text-sm">{conjunction.relativeVelocityKmS.toFixed(1)} km/s</span>
          </div>
        </div>
      </div>

      <div className="flex items-center justify-between mt-4 border-t border-slate-700/50 pt-3">
        <div className="flex items-center gap-2 text-red-400 animate-pulse">
          <Clock className="w-5 h-5" />
          <span className="font-mono font-bold text-lg">{timeLeft}</span>
        </div>
        
        <button 
          onClick={() => onAnalyze(conjunction.id)}
          disabled={isAnalyzing}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 text-white rounded-md font-medium text-sm flex items-center transition-colors"
        >
          {isAnalyzing ? 'Analyzing...' : 'AI Analysis'}
          {!isAnalyzing && <ChevronRight className="w-4 h-4 ml-1" />}
        </button>
      </div>
    </div>
  );
}
