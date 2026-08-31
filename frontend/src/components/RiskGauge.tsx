'use client';

import React from 'react';

interface RiskGaugeProps {
  score: number;
}

export default function RiskGauge({ score }: RiskGaugeProps) {
  const radius = 36;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  const color = score > 75 ? 'text-red-500' : 
                score > 50 ? 'text-orange-500' : 
                score > 25 ? 'text-yellow-500' : 
                'text-green-500';

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg className="w-24 h-24 transform -rotate-90">
        <circle
          className="text-slate-800"
          strokeWidth="8"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="48"
          cy="48"
        />
        <circle
          className={`${color} transition-all duration-1000 ease-out`}
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="48"
          cy="48"
        />
      </svg>
      <div className="absolute flex flex-col items-center justify-center">
        <span className="text-2xl font-bold font-mono text-white">{score}</span>
        <span className="text-[10px] text-slate-400 uppercase">Risk</span>
      </div>
    </div>
  );
}
