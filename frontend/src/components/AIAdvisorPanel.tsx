'use client';

import React, { useState, useEffect } from 'react';
import { AIRecommendation } from '../lib/types';
import { Bot } from 'lucide-react';

interface AIAdvisorPanelProps {
  recommendation: AIRecommendation;
}

export default function AIAdvisorPanel({ recommendation }: AIAdvisorPanelProps) {
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(true);

  useEffect(() => {
    let i = 0;
    setDisplayedText('');
    setIsTyping(true);
    
    const intervalId = setInterval(() => {
      if (i < recommendation.briefingText.length) {
        setDisplayedText((prev) => prev + recommendation.briefingText.charAt(i));
        i++;
      } else {
        clearInterval(intervalId);
        setIsTyping(false);
      }
    }, 15); // Fast typing effect

    return () => clearInterval(intervalId);
  }, [recommendation.briefingText]);

  return (
    <div className="bg-slate-900 border border-slate-700 rounded-lg overflow-hidden">
      <div className="bg-cyan-900/30 border-b border-slate-700 p-3 flex justify-between items-center">
        <div className="flex items-center gap-2">
          <Bot className="w-5 h-5 text-cyan-400" />
          <div>
            <h3 className="font-bold text-white tracking-wide">GRANITE AI ANALYSIS</h3>
            <p className="text-[10px] text-cyan-500/80 font-mono tracking-widest">Powered by IBM Granite</p>
          </div>
        </div>
        <div className="bg-cyan-500/20 px-2 py-1 rounded text-xs font-mono text-cyan-400 border border-cyan-500/30">
          CONFIDENCE: {recommendation.confidence}%
        </div>
      </div>
      
      <div className="p-4 space-y-4">
        <div>
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Recommendation</h4>
          <p className="text-sm text-slate-200">{recommendation.reasoning}</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Risk Factors</h4>
            <ul className="list-disc list-inside text-sm text-slate-300 space-y-1">
              {recommendation.riskFactors.map((factor, i) => (
                <li key={i}>{factor}</li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Secondary Risks</h4>
            <p className="text-sm text-slate-300">{recommendation.secondaryRisks}</p>
          </div>
        </div>

        <div>
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Trade-offs</h4>
          <p className="text-sm text-slate-300">{recommendation.tradeOffs}</p>
        </div>

        <div className="mt-4 border border-cyan-900 bg-black/40 rounded p-3 relative">
          <h4 className="text-[10px] text-cyan-500 absolute -top-2 left-2 bg-slate-900 px-1 font-mono">OPERATOR BRIEFING</h4>
          <p className="text-sm text-cyan-50 font-mono leading-relaxed mt-2 min-h-[100px]">
            {displayedText}
            {isTyping && <span className="inline-block w-2 h-4 bg-cyan-400 ml-1 animate-pulse"></span>}
          </p>
        </div>
      </div>
    </div>
  );
}
