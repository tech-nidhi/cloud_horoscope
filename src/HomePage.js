import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getZodiacSign, ZODIAC_DATA, parseDob } from './horoscopeEngine';

const HomePage = () => {
  const [showIntro, setShowIntro] = useState(true);
  const [name, setName] = useState('');
  const [dob, setDob] = useState('1998-07-15');
  const [showApiModal, setShowApiModal] = useState(false);
  const [customEndpoint, setCustomEndpoint] = useState(
    localStorage.getItem('custom_horoscope_api_endpoint') || ''
  );
  const [previewSign, setPreviewSign] = useState(null);
  const navigate = useNavigate();

  // Intro fade timer
  useEffect(() => {
    const timer = setTimeout(() => {
      setShowIntro(false);
    }, 2400);
    return () => clearTimeout(timer);
  }, []);

  // Update preview sign on date change
  useEffect(() => {
    const parsed = parseDob(dob);
    if (parsed && !isNaN(parsed.day) && !isNaN(parsed.month)) {
      const sign = getZodiacSign(parsed.day, parsed.month);
      setPreviewSign(sign);
    } else {
      setPreviewSign(null);
    }
  }, [dob]);

  const handleShowHoroscope = (e) => {
    if (e) e.preventDefault();
    if (!name.trim()) {
      alert('Please enter your name!');
      return;
    }
    if (!dob) {
      alert('Please select your date of birth!');
      return;
    }

    navigate('/horoscope', { state: { name: name.trim(), dob } });
  };

  const handleQuickDemo = (demoName, demoDob) => {
    setName(demoName);
    setDob(demoDob);
  };

  const saveApiEndpoint = () => {
    if (customEndpoint.trim()) {
      localStorage.setItem('custom_horoscope_api_endpoint', customEndpoint.trim());
    } else {
      localStorage.removeItem('custom_horoscope_api_endpoint');
    }
    setShowApiModal(false);
  };

  const signInfo = previewSign ? ZODIAC_DATA[previewSign] : null;

  return (
    <div className="min-h-screen cosmic-bg flex flex-col justify-between relative overflow-hidden text-slate-100 font-sans">
      {/* Background Celestial Watermarks */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-30 select-none">
        <div className="absolute -top-10 -left-10 w-96 h-96 bg-purple-600/30 rounded-full blur-3xl animate-pulse-glow"></div>
        <div className="absolute top-1/2 -right-20 w-80 h-80 bg-blue-600/30 rounded-full blur-3xl animate-pulse-glow" style={{ animationDelay: '1.5s' }}></div>
        <div className="absolute -bottom-20 left-1/3 w-96 h-96 bg-pink-600/20 rounded-full blur-3xl animate-pulse-glow" style={{ animationDelay: '3s' }}></div>
        
        {/* Floating Zodiac Doodles */}
        <div className="absolute top-12 left-10 text-5xl animate-float">🔮</div>
        <div className="absolute top-24 right-16 text-4xl animate-float-slow" style={{ animationDelay: '1s' }}>☁️</div>
        <div className="absolute bottom-24 left-14 text-4xl animate-float" style={{ animationDelay: '2s' }}>⚡</div>
        <div className="absolute bottom-16 right-12 text-5xl animate-float-slow" style={{ animationDelay: '0.7s' }}>✨</div>
        <div className="absolute top-1/2 left-6 text-3xl animate-float" style={{ animationDelay: '1.8s' }}>🪐</div>
        <div className="absolute top-1/3 right-8 text-3xl animate-float-slow" style={{ animationDelay: '2.5s' }}>🚀</div>
      </div>

      {/* Intro Splash Modal */}
      {showIntro && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md flex items-center justify-center z-50 transition-opacity duration-500">
          <div className="glass-card rounded-3xl p-8 max-w-md mx-4 text-center border border-purple-500/30 shadow-2xl animate-pulse-glow">
            <div className="text-7xl mb-4 animate-float">🔮</div>
            <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-400 via-pink-300 to-blue-400 bg-clip-text text-transparent mb-2">
              Cosmic Gateway Initializing...
            </h2>
            <p className="text-slate-300 text-sm mb-4">
              Aligning AWS Cloud constellations with your zodiac destiny ✨
            </p>
            <button
              onClick={() => setShowIntro(false)}
              className="px-5 py-2 rounded-xl bg-purple-600/60 hover:bg-purple-600 text-xs font-semibold uppercase tracking-wider text-white transition-all"
            >
              Enter Now
            </button>
          </div>
        </div>
      )}

      {/* Top Navbar */}
      <header className="relative z-20 px-6 py-5 flex items-center justify-between max-w-6xl mx-auto w-full">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center text-xl shadow-lg shadow-purple-500/30 border border-purple-300/30">
            🔮
          </div>
          <div>
            <h1 className="font-display font-bold text-xl tracking-tight text-white flex items-center gap-2">
              Cloud Horoscope <span className="text-xs px-2 py-0.5 rounded-full bg-purple-500/30 border border-purple-400/40 text-purple-200">v2.0</span>
            </h1>
            <p className="text-xs text-slate-400">AWS Bedrock & Serverless Astrological Intelligence</p>
          </div>
        </div>

        <button
          onClick={() => setShowApiModal(true)}
          className="flex items-center space-x-2 text-xs bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/80 px-3.5 py-2 rounded-xl text-slate-300 hover:text-white transition shadow-sm backdrop-blur"
          title="Configure AWS Lambda Gateway"
        >
          <span>⚙️</span>
          <span className="hidden sm:inline">
            {customEndpoint ? 'Custom AWS API' : 'Cosmic Engine: Active'}
          </span>
        </button>
      </header>

      {/* Main Content Area */}
      <main className="relative z-10 flex items-center justify-center p-4 my-auto">
        <div className="glass-card rounded-3xl p-6 sm:p-10 max-w-lg w-full border border-purple-500/20 shadow-2xl relative">
          
          {/* Header Banner */}
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center p-3 rounded-2xl bg-gradient-to-tr from-purple-500/20 to-blue-500/20 border border-purple-500/30 mb-4 shadow-inner">
              <span className="text-5xl animate-float">🔮</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-display font-bold bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent">
              Discover Your Cosmic Cloud Destiny
            </h2>
            <p className="text-slate-300 text-sm mt-2">
              Reveal your architectural horoscope, lucky AWS services, and serverless alignment.
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleShowHoroscope} className="space-y-5">
            <div>
              <label className="block text-slate-200 text-xs font-semibold uppercase tracking-wider mb-2">
                Your Full Name / Alias
              </label>
              <div className="relative">
                <input
                  type="text"
                  required
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-4 py-3.5 rounded-xl cosmic-input text-white placeholder-slate-400 focus:outline-none"
                  placeholder="e.g. Satoshi Nakamoto, Alice, Alex"
                />
                <span className="absolute right-3.5 top-3.5 text-lg opacity-60">👤</span>
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-slate-200 text-xs font-semibold uppercase tracking-wider">
                  Date of Birth
                </label>
                {signInfo && (
                  <span className="text-xs px-2 py-0.5 rounded-md bg-purple-500/20 border border-purple-400/40 text-purple-200 flex items-center gap-1 font-medium">
                    <span>{signInfo.symbol}</span>
                    <span>{previewSign} ({signInfo.dates})</span>
                  </span>
                )}
              </div>
              <div className="relative">
                <input
                  type="date"
                  required
                  value={dob}
                  onChange={(e) => setDob(e.target.value)}
                  className="w-full px-4 py-3.5 rounded-xl cosmic-input text-white focus:outline-none [color-scheme:dark]"
                />
              </div>
            </div>

            {/* Quick Demo Shortcuts */}
            <div>
              <p className="text-slate-400 text-xs mb-2">⚡ Quick demo profiles:</p>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={() => handleQuickDemo('Maya Cloudsmith', '1996-03-25')}
                  className="text-xs px-2.5 py-1.5 rounded-lg bg-slate-800/80 hover:bg-purple-900/40 border border-slate-700/60 text-slate-300 hover:text-white transition"
                >
                  ♈ Maya (Aries)
                </button>
                <button
                  type="button"
                  onClick={() => handleQuickDemo('David Serverless', '1993-08-10')}
                  className="text-xs px-2.5 py-1.5 rounded-lg bg-slate-800/80 hover:bg-purple-900/40 border border-slate-700/60 text-slate-300 hover:text-white transition"
                >
                  ♌ David (Leo)
                </button>
                <button
                  type="button"
                  onClick={() => handleQuickDemo('Nora Quantum', '2000-11-05')}
                  className="text-xs px-2.5 py-1.5 rounded-lg bg-slate-800/80 hover:bg-purple-900/40 border border-slate-700/60 text-slate-300 hover:text-white transition"
                >
                  ♏ Nora (Scorpio)
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full bg-gradient-to-r from-purple-600 via-indigo-600 to-pink-600 hover:from-purple-500 hover:via-indigo-500 hover:to-pink-500 text-white font-semibold py-4 px-6 rounded-xl transition duration-300 transform hover:scale-[1.02] active:scale-[0.98] shadow-lg shadow-purple-600/30 flex items-center justify-center gap-2 group"
            >
              <span>Consult The Crystal Ball</span>
              <span className="text-xl group-hover:rotate-12 transition-transform">✨</span>
            </button>
          </form>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-20 text-center py-6 text-xs text-slate-500">
        <p>
          Cloud Horoscope • Powered by Serverless Cloud Architecture & Bedrock AI • {new Date().getFullYear()}
        </p>
      </footer>

      {/* Settings Modal */}
      {showApiModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md flex items-center justify-center z-50 p-4">
          <div className="glass-card rounded-3xl p-6 sm:p-8 max-w-md w-full border border-purple-500/40 shadow-2xl">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <span>⚙️</span> API Gateway Settings
              </h3>
              <button
                onClick={() => setShowApiModal(false)}
                className="text-slate-400 hover:text-white text-xl leading-none"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-slate-300 mb-4 leading-relaxed">
              By default, the application uses its built-in resilient Bedrock AI Cosmic Engine. You can optionally paste your live AWS API Gateway endpoint URL below:
            </p>

            <div className="mb-5">
              <label className="block text-slate-300 text-xs font-semibold mb-1">
                Custom AWS API Gateway URL (POST)
              </label>
              <input
                type="url"
                value={customEndpoint}
                onChange={(e) => setCustomEndpoint(e.target.value)}
                placeholder="https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/horoscope"
                className="w-full px-3.5 py-2.5 rounded-xl cosmic-input text-xs text-white placeholder-slate-500 focus:outline-none"
              />
              <p className="text-[11px] text-slate-400 mt-1.5">
                Leave empty to use the built-in offline-resilient Bedrock Cosmic Engine.
              </p>
            </div>

            <div className="flex justify-end gap-3">
              <button
                onClick={() => {
                  setCustomEndpoint('');
                  localStorage.removeItem('custom_horoscope_api_endpoint');
                  setShowApiModal(false);
                }}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300"
              >
                Reset to Default
              </button>
              <button
                onClick={saveApiEndpoint}
                className="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-xs font-semibold text-white shadow-md shadow-purple-600/30"
              >
                Save Settings
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HomePage;