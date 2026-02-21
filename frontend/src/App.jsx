import React, { useState, useEffect } from 'react';
import HexButton from './components/HexButton';
import ScaleCard from './components/ScaleCard';
import './index.css';

export default function App() {
  const [stealthMode, setStealthMode] = useState(false);
  const [devices, setDevices] = useState([]);
  const [leaks, setLeaks] = useState([]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.shiftKey && e.key.toLowerCase() === 's') {
        setStealthMode(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const triggerScent = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/scent/scan');
      const data = await res.json();
      setDevices(data.devices);
    } catch (err) {
      console.error("Could not contact Pangolin API:", err);
    }
  };

  const triggerCurlUp = async () => {
    try {
      await fetch('http://localhost:8000/api/curl-up/activate', { method: 'POST' });
      alert("CURL-UP ACTIVATED: CPU Watchdog is protecting the system.");
    } catch (err) {
      console.error("Error activating Curl-Up:", err);
    }
  };

  const triggerLongTongue = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/long-tongue/search?query=secrets');
      const data = await res.json();
      setLeaks(data.leaks);
    } catch (err) {
      console.error("Error activating Long Tongue:", err);
    }
  };

  return (
    <div className={`min-h-screen text-gray-300 p-8 transition-opacity duration-500 ${stealthMode ? 'opacity-10' : 'opacity-100'}`}>
      {!stealthMode && (
        <header className="mb-10 border-b border-[#3d2b1f] pb-4">
          <h1 className="text-5xl font-bold tracking-wider text-[#a88a75]">Pangolin-Guard OS</h1>
          <p className="text-sm text-gray-500 mt-2">Press Shift+S for Stealth Mode</p>
        </header>
      )}

      <div className="flex flex-wrap gap-6 mb-12">
        <HexButton 
          onClick={triggerScent} 
          label="[ Scent Module ] Network Scan" 
        />
        <HexButton 
          onClick={triggerCurlUp} 
          label="[ Curl-Up Module ] Defensive Arming" 
          colorClass="text-red-400" 
          borderClass="border border-red-900/30" 
        />
        <HexButton 
          onClick={triggerLongTongue} 
          label="[ Long Tongue ] Deep Search" 
          colorClass="text-blue-400" 
          borderClass="border border-blue-900/30" 
        />
      </div>

      {leaks.length > 0 && (
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-[#a88a75] mb-4">Data Leaks Detected</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {leaks.map((leak, i) => (
              <div key={i} className="glassmorphism p-4 border border-red-900/50">
                <p className="text-red-400 font-mono text-sm">{leak.file}</p>
                <p className="text-white mt-2">Type: {leak.leak_type}</p>
                <p className="text-xs text-gray-500 mt-1">Confidence: {(leak.confidence_score * 100).toFixed(0)}%</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <h2 className="text-2xl font-bold text-[#a88a75] mb-4">Network Radar (Scent)</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {devices.map((dev, index) => (
          <ScaleCard 
            key={index}
            ip={dev.ip} 
            mac={dev.mac} 
            scentLevel={dev.scent_level} 
          />
        ))}
      </div>
    </div>
  );
}