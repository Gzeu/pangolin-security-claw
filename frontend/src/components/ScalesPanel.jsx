import React, { useState } from 'react';

export default function ScalesPanel() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setStatus("");
  };

  const handleAction = async (action) => {
    if (!file) {
      setStatus("Please select a file first.");
      return;
    }

    setLoading(true);
    setStatus(`Processing ${action}...`);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const endpoint = action === 'encrypt' ? '/api/scales/encrypt' : '/api/scales/decrypt';
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      
      if (data.status === "ERROR") {
          setStatus(`Error: ${data.message}`);
      } else {
          setStatus(`Success! File ${action === 'encrypt' ? 'Armored (.pangolin)' : 'Unrolled'}. Check the backend 'uploads' directory.`);
      }
    } catch (error) {
      setStatus(`Failed to connect to backend: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glassmorphism p-6 mt-8 border border-[#a88a75]/30 rounded-lg">
      <h2 className="text-2xl font-bold text-[#a88a75] mb-4">Scales Module (Crypto)</h2>
      <p className="text-sm text-gray-400 mb-4">
        Encrypt files into armored chunks (Scales) using AES-256 GCM, or unroll them back to their original state.
      </p>

      <div className="flex flex-col items-start gap-4">
        <input 
          type="file" 
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-400
            file:mr-4 file:py-2 file:px-4
            file:rounded-md file:border-0
            file:text-sm file:font-semibold
            file:bg-[#3d2b1f] file:text-[#cbb8a9]
            hover:file:bg-[#5a4231] transition-colors"
        />

        <div className="flex gap-4 w-full">
          <button 
            onClick={() => handleAction('encrypt')}
            disabled={loading || !file}
            className="flex-1 bg-green-900/30 hover:bg-green-900/50 text-green-400 border border-green-800 p-3 rounded font-mono transition-colors disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'ARMOR FILE (Encrypt)'}
          </button>
          
          <button 
            onClick={() => handleAction('decrypt')}
            disabled={loading || !file}
            className="flex-1 bg-yellow-900/30 hover:bg-yellow-900/50 text-yellow-400 border border-yellow-800 p-3 rounded font-mono transition-colors disabled:opacity-50"
          >
            {loading ? 'Processing...' : 'UNROLL FILE (Decrypt)'}
          </button>
        </div>

        {status && (
          <div className="w-full mt-2 p-3 bg-black/40 rounded border border-gray-700">
            <span className="font-mono text-sm text-gray-300">{status}</span>
          </div>
        )}
      </div>
    </div>
  );
}