'use client';

import React from 'react';
import { Activity, Radio, AlertTriangle, Shield } from 'lucide-react';
import { SystemStatus } from '../lib/types';

interface StatsBarProps {
  status: SystemStatus;
}

export default function StatsBar({ status }: StatsBarProps) {
  return (
    <div className="flex gap-4 p-4 bg-slate-900/50 border-b border-slate-800 backdrop-blur-sm items-center">
      {/* Brand identifier */}
      <div className="flex items-center gap-2 pr-4 border-r border-slate-700">
        <span className="text-cyan-400 text-lg">🛰️</span>
        <div>
          <div className="text-xs font-bold text-white tracking-widest font-mono">ASTRAGUARD</div>
          <div className="text-[10px] text-slate-500 font-mono">SPACE TRAFFIC MGMT</div>
        </div>
      </div>

      <div className="flex-1 bg-slate-800/50 rounded-lg p-3 flex items-center gap-3 border border-slate-700/50">
        <div className="p-2 bg-blue-500/20 rounded-md">
          <Activity className="w-5 h-5 text-blue-400" />
        </div>
        <div>
          <div className="text-xs text-slate-400">Tracked Objects</div>
          <div className="text-lg font-bold font-mono text-white">{status.trackedObjectsCount.toLocaleString()}</div>
        </div>
      </div>

      <div className="flex-1 bg-slate-800/50 rounded-lg p-3 flex items-center gap-3 border border-slate-700/50">
        <div className="p-2 bg-orange-500/20 rounded-md">
          <AlertTriangle className="w-5 h-5 text-orange-400" />
        </div>
        <div>
          <div className="text-xs text-slate-400">Conjunctions</div>
          <div className="text-lg font-bold font-mono text-white">{status.activeConjunctionsCount}</div>
        </div>
      </div>

      <div className="flex-1 bg-slate-800/50 rounded-lg p-3 flex items-center gap-3 border border-slate-700/50">
        <div className="p-2 bg-red-500/20 rounded-md">
          <Shield className="w-5 h-5 text-red-400" />
        </div>
        <div>
          <div className="text-xs text-slate-400">Highest Risk</div>
          <div className="text-lg font-bold font-mono text-red-400 uppercase">{status.highestRiskLevel}</div>
        </div>
      </div>
      
      <div className="flex-1 bg-slate-800/50 rounded-lg p-3 flex items-center gap-3 border border-slate-700/50">
        <div className="p-2 bg-green-500/20 rounded-md">
          <Radio className="w-5 h-5 text-green-400" />
        </div>
        <div>
          <div className="text-xs text-slate-400">System</div>
          <div className="text-lg font-bold font-mono text-green-400 uppercase">{status.status}</div>
        </div>
      </div>
    </div>
  );
}
