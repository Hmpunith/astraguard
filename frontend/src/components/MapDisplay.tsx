'use client';

import React from 'react';
import { OrbitalObject, Conjunction } from '../lib/types';

interface MapDisplayProps {
  satellites: OrbitalObject[];
  conjunctions: Conjunction[];
}

export default function MapDisplay({ satellites, conjunctions }: MapDisplayProps) {
  // Simple equirectangular projection mapping lat/lon to percentage
  const getX = (lon: number) => ((lon + 180) / 360) * 100;
  const getY = (lat: number) => ((-lat + 90) / 180) * 100;

  return (
    <div className="relative w-full h-full bg-[#0a0e27] overflow-hidden rounded-l-2xl border-r border-slate-800">
      <div className="absolute top-0 left-0 w-full p-4 z-10 flex justify-between items-center bg-gradient-to-b from-[#0a0e27] to-transparent">
        <h2 className="text-cyan-400 font-mono tracking-widest font-bold text-sm">ORBITAL TRACKING DISPLAY</h2>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span className="text-xs text-green-500 font-mono">LIVE</span>
        </div>
      </div>

      {/* Grid Overlay */}
      <div className="absolute inset-0 z-0 opacity-20 pointer-events-none" 
           style={{
             backgroundImage: 'linear-gradient(to right, #38bdf8 1px, transparent 1px), linear-gradient(to bottom, #38bdf8 1px, transparent 1px)',
             backgroundSize: '10% 10%'
           }}>
      </div>

      {/* Simple Map Background (Stylized) */}
      <div className="absolute inset-0 opacity-10 flex items-center justify-center pointer-events-none">
        <svg viewBox="0 0 1000 500" className="w-full h-full fill-none stroke-cyan-500 stroke-1">
          {/* A very basic representation of continents for effect */}
          <path d="M 200 100 Q 250 50 300 100 T 400 150 Q 300 300 250 400 Z" />
          <path d="M 600 50 Q 700 100 800 50 T 900 150 Q 800 400 650 350 Z" />
          <path d="M 450 200 Q 550 250 500 350 T 400 300 Z" />
        </svg>
      </div>

      {/* Satellites */}
      {satellites.map(sat => (
        <div 
          key={sat.id}
          className="absolute transform -translate-x-1/2 -translate-y-1/2 group cursor-pointer"
          style={{ left: `${getX(sat.longitude)}%`, top: `${getY(sat.latitude)}%` }}
        >
          <div className={`w-2 h-2 rounded-full ${sat.type === 'satellite' ? 'bg-cyan-400' : 'bg-orange-500'} shadow-[0_0_10px_rgba(56,189,248,0.8)]`}></div>
          {/* Orbit line mock */}
          <div className="absolute top-1 left-1 w-32 h-px bg-gradient-to-r from-cyan-400/50 to-transparent transform -rotate-12 origin-left -z-10"></div>
          
          {/* Tooltip */}
          <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 hidden group-hover:block w-32 bg-slate-900/90 border border-slate-700 text-xs p-2 rounded pointer-events-none z-20">
            <div className="font-bold text-white truncate">{sat.name}</div>
            <div className="text-slate-400 capitalize">{sat.type}</div>
            <div className="text-slate-500 font-mono mt-1">Alt: {sat.altitude}km</div>
          </div>
        </div>
      ))}

      {/* Conjunction Warning Zones */}
      {conjunctions.map(conj => {
        // Find primary sat to center the warning
        const primary = satellites.find(s => s.id === conj.primaryObjectId);
        if (!primary) return null;
        
        return (
          <div 
            key={conj.id}
            className="absolute transform -translate-x-1/2 -translate-y-1/2 pointer-events-none z-10"
            style={{ left: `${getX(primary.longitude)}%`, top: `${getY(primary.latitude)}%` }}
          >
            <div className="w-16 h-16 rounded-full border border-red-500 bg-red-500/20 animate-pulse-fast flex items-center justify-center">
              <div className="w-8 h-8 rounded-full border border-red-400 bg-red-500/40"></div>
            </div>
            {/* Target line to secondary object */}
            {(() => {
              const sec = satellites.find(s => s.id === conj.secondaryObjectId);
              if (!sec) return null;
              // Very basic SVG line
              return (
                 <svg className="absolute top-1/2 left-1/2 overflow-visible" style={{ width: 1, height: 1 }}>
                   <line 
                     x1="0" y1="0" 
                     x2={(getX(sec.longitude) - getX(primary.longitude)) * 10} 
                     y2={(getY(sec.latitude) - getY(primary.latitude)) * 5} 
                     stroke="red" strokeWidth="1" strokeDasharray="4"
                   />
                 </svg>
              );
            })()}
          </div>
        );
      })}
    </div>
  );
}
