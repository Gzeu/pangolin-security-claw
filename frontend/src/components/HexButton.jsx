import React from 'react';

export default function HexButton({ onClick, label, className = "", colorClass = "text-[#cbb8a9]", borderClass = "" }) {
  return (
    <button 
      onClick={onClick} 
      className={`hex-button glassmorphism px-8 py-4 font-semibold ${colorClass} ${borderClass} ${className}`}
    >
      {label}
    </button>
  );
}