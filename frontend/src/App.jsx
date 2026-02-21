import React, { useState, useEffect } from 'react';
import './index.css';

export default function App() {
  const [stealthMode, setStealthMode] = useState(false);
  const [devices, setDevices] = useState([]);

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
      console.error("Nu s-a putut contacta Pangolin API:", err);
    }
  };

  const triggerCurlUp = async () => {
    try {
      await fetch('http://localhost:8000/api/curl-up/activate', { method: 'POST' });
      alert("CURL-UP ACTIVAT: Watchdog-ul CPU protejeaza sistemul.");
    } catch (err) {
      console.error("Eroare la activarea Curl-Up:", err);
    }
  };

  return (
    <div className={`min-h-screen text-gray-300 p-8 transition-opacity duration-500 ${stealthMode ? 'opacity-10' : 'opacity-100'}`}>
      {!stealthMode && (
        <header className="mb-10 border-b border-[#3d2b1f] pb-4">
          <h1 className="text-5xl font-bold tracking-wider text-[#a88a75]">Pangolin-Guard OS</h1>
          <p className="text-sm text-gray-500 mt-2">Apasati Shift+S pentru modul Stealth</p>
        </header>
      )}

      <div className="flex gap-6 mb-12">
        <button onClick={triggerScent} className="hex-button glassmorphism px-8 py-4 font-semibold text-[#cbb8a9]">
          [ Modul Scent ] Scanare Retea
        </button>
        <button onClick={triggerCurlUp} className="hex-button glassmorphism px-8 py-4 font-semibold text-red-400 border border-red-900/30">
          [ Modul Curl-Up ] Armare Defensiva
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {devices.map((dev, index) => {
          const dangerColor = dev.scent_level > 70 ? 'rgba(239, 68, 68, 0.2)' : 'rgba(34, 197, 94, 0.1)';
          return (
            <div key={index} className="scale-card glassmorphism p-6 relative overflow-hidden" style={{ backgroundColor: dangerColor }}>
              <div className="absolute top-0 right-0 p-2 opacity-50 text-6xl">⬡</div>
              <h3 className="text-xl font-bold text-white mb-2">{dev.ip}</h3>
              <p className="text-sm text-gray-400 font-mono mb-4">{dev.mac}</p>
              <div className="mt-4">
                <span className="text-xs uppercase tracking-widest text-gray-500">Nivel Miros</span>
                <div className="w-full bg-black/40 h-2 rounded-full mt-1">
                  <div className={`h-full rounded-full ${dev.scent_level > 70 ? 'bg-red-500' : 'bg-[#a88a75]'}`} style={{ width: `${dev.scent_level}%` }}></div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}