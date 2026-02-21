import React from 'react';

export default function ScaleCard({ ip, mac, scentLevel }) {
  const dangerColor = scentLevel > 70 ? 'rgba(239, 68, 68, 0.2)' : 'rgba(34, 197, 94, 0.1)';
  const barColor = scentLevel > 70 ? 'bg-red-500' : 'bg-[#a88a75]';

  return (
    <div className="scale-card glassmorphism p-6 relative overflow-hidden" style={{ backgroundColor: dangerColor }}>
      <div className="absolute top-0 right-0 p-2 opacity-50 text-6xl">⬡</div>
      <h3 className="text-xl font-bold text-white mb-2">{ip}</h3>
      <p className="text-sm text-gray-400 font-mono mb-4">{mac}</p>
      
      <div className="mt-4">
        <span className="text-xs uppercase tracking-widest text-gray-500">Scent Level</span>
        <div className="w-full bg-black/40 h-2 rounded-full mt-1">
          <div 
            className={`h-full rounded-full ${barColor}`}
            style={{ width: `${scentLevel}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
}