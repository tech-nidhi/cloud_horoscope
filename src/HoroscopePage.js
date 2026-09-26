import React, { useState, useEffect, useCallback } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { getHoroscope, parseDob } from './horoscopeEngine';
import { downloadHoroscopeImage, downloadHoroscopeMarkdown } from './reportExporter';

const HoroscopePage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { name, dob } = location.state || {};

  const [horoscopeData, setHoroscopeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [variationOffset, setVariationOffset] = useState(0);
  const [copied, setCopied] = useState(false);
  const [showDownloadModal, setShowDownloadModal] = useState(false);
  const [downloadSuccess, setDownloadSuccess] = useState(null);

  // Fetch horoscope callback
  const fetchHoroscopeData = useCallback(async (offset = 0) => {
    if (!name || !dob) {
      setError('Missing name or date of birth. Please start from the homepage.');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await getHoroscope({
        name,
        dob,
        variationOffset: offset
      });
      setHoroscopeData(data);
    } catch (err) {
      console.error('Error fetching horoscope:', err);
      setError(err.message || 'Failed to generate cosmic reading.');
    } finally {
      setLoading(false);
    }
  }, [name, dob]);

  // Initial load
  useEffect(() => {
    fetchHoroscopeData(0);
  }, [fetchHoroscopeData]);

  // Handler for new reading
  const handleNewReading = () => {
    const nextOffset = variationOffset + 1;
    setVariationOffset(nextOffset);
    fetchHoroscopeData(nextOffset);
  };

  const parsedDate = parseDob(dob);
  const dobFormatted = parsedDate?.formatted || dob || 'Unknown';

  // Copy to clipboard safely
  const handleCopy = () => {
    if (!horoscopeData) return;
    const textToCopy = `🔮 Cloud Horoscope for ${name} (${horoscopeData.sign} ${horoscopeData.symbol}):\n"${horoscopeData.horoscope}"\n\n⚡ Lucky AWS Service: ${horoscopeData.luckyService}\n🌐 Lucky Region: ${horoscopeData.luckyRegion}\n🛡️ Architecture Resilience: ${horoscopeData.resilienceScore}%`;
    
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(textToCopy)
        .then(() => {
          setCopied(true);
          setTimeout(() => setCopied(false), 2500);
        })
        .catch(() => {
          fallbackCopy(textToCopy);
        });
    } else {
      fallbackCopy(textToCopy);
    }
  };

  const fallbackCopy = (text) => {
    try {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      document.execCommand('copy');
      textArea.remove();
      setCopied(true);
      setTimeout(() => setCopied(false), 2500);
    } catch (e) {
      console.error('Fallback copy failed:', e);
    }
  };

  const handleDownloadPng = () => {
    if (!horoscopeData) return;
    downloadHoroscopeImage({ name, dobFormatted, horoscopeData });
    setDownloadSuccess('Cosmic PNG Card downloaded!');
    setShowDownloadModal(false);
    setTimeout(() => setDownloadSuccess(null), 3000);
  };

  const handleDownloadMd = () => {
    if (!horoscopeData) return;
    downloadHoroscopeMarkdown({ name, dobFormatted, horoscopeData });
    setDownloadSuccess('Markdown Report downloaded!');
    setShowDownloadModal(false);
    setTimeout(() => setDownloadSuccess(null), 3000);
  };

  return (
    <div className="min-h-screen cosmic-bg flex flex-col justify-between relative overflow-hidden text-slate-100 font-sans">
      {/* Background Celestial Watermarks */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-30 select-none">
        <div className="absolute -top-20 -right-20 w-96 h-96 bg-purple-600/30 rounded-full blur-3xl animate-pulse-glow"></div>
        <div className="absolute bottom-10 -left-20 w-96 h-96 bg-indigo-600/30 rounded-full blur-3xl animate-pulse-glow" style={{ animationDelay: '2s' }}></div>
        
        <div className="absolute top-10 left-10 text-6xl animate-float">🔮</div>
        <div className="absolute top-20 right-20 text-5xl animate-float" style={{ animationDelay: '1s' }}>🪄</div>
        <div className="absolute bottom-20 left-20 text-4xl animate-float" style={{ animationDelay: '2s' }}>⭐</div>
        <div className="absolute bottom-10 right-10 text-5xl animate-float" style={{ animationDelay: '0.5s' }}>🌙</div>
        <div className="absolute top-1/2 left-5 text-4xl animate-float" style={{ animationDelay: '1.5s' }}>✨</div>
        <div className="absolute top-1/3 right-5 text-4xl animate-float" style={{ animationDelay: '2.5s' }}>🌟</div>
      </div>

      {/* Toast Notification */}
      {downloadSuccess && (
        <div className="fixed top-6 left-1/2 -translate-x-1/2 z-50 bg-emerald-600 text-white text-xs font-semibold px-5 py-2.5 rounded-full shadow-2xl border border-emerald-400 flex items-center gap-2 animate-bounce">
          <span>✓</span>
          <span>{downloadSuccess}</span>
        </div>
      )}

      {/* Top Navigation */}
      <header className="relative z-20 px-6 py-5 flex items-center justify-between max-w-6xl mx-auto w-full">
        <button
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-xs bg-slate-900/80 hover:bg-slate-800 border border-slate-700/80 px-4 py-2.5 rounded-xl text-slate-200 hover:text-white transition shadow-sm backdrop-blur group"
        >
          <span className="group-hover:-translate-x-1 transition-transform">←</span>
          <span>Back to Crystal Ball</span>
        </button>

        <div className="text-right">
          <span className="text-xs px-3 py-1 rounded-full bg-purple-500/20 border border-purple-400/30 text-purple-200">
            {horoscopeData?.source === 'aws-api' ? '☁️ AWS Gateway Live' : '⚡ AWS Bedrock AI Engine'}
          </span>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="relative z-10 flex items-center justify-center p-4 my-auto">
        <div className="glass-card rounded-3xl p-6 sm:p-10 max-w-2xl w-full border border-purple-500/30 shadow-2xl relative">
          
          {/* Header Profile */}
          <div className="text-center mb-6">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-gradient-to-tr from-purple-600 to-indigo-600 border border-purple-300/40 shadow-xl mb-3 text-4xl animate-float">
              {horoscopeData?.symbol || '🔮'}
            </div>
            
            <h1 className="text-3xl sm:text-4xl font-display font-bold bg-gradient-to-r from-white via-purple-100 to-pink-200 bg-clip-text text-transparent mb-1">
              {name ? `${name}'s Cosmic Reading` : 'Your Cloud Horoscope'}
            </h1>
            
            <p className="text-slate-400 text-xs sm:text-sm">
              Birthdate: <span className="text-purple-300 font-medium">{dobFormatted}</span>
            </p>

            {horoscopeData && (
              <div className="flex flex-wrap items-center justify-center gap-2 mt-4">
                <span className="inline-flex items-center gap-1.5 bg-gradient-to-r from-purple-500 to-indigo-600 text-white px-4 py-1.5 rounded-full text-sm font-semibold shadow-md shadow-purple-500/20 border border-purple-300/30">
                  <span>{horoscopeData.symbol}</span>
                  <span>{horoscopeData.sign}</span>
                  <span className="opacity-75 font-normal text-xs">({horoscopeData.dates})</span>
                </span>
                
                <span className="inline-flex items-center gap-1 bg-slate-800/90 text-slate-300 px-3 py-1.5 rounded-full text-xs font-medium border border-slate-700">
                  <span>🔥</span> Element: <strong className="text-white">{horoscopeData.element}</strong>
                </span>
              </div>
            )}
          </div>

          {/* Body content */}
          <div className="bg-slate-900/60 border border-slate-700/50 rounded-2xl p-5 sm:p-6 mb-6 relative overflow-hidden backdrop-blur-md shadow-inner">
            
            {/* Loading State */}
            {loading && (
              <div className="py-12 flex flex-col items-center justify-center text-center">
                <div className="relative w-16 h-16 mb-4">
                  <div className="absolute inset-0 rounded-full border-4 border-purple-500/20"></div>
                  <div className="absolute inset-0 rounded-full border-4 border-t-purple-400 border-r-pink-400 border-b-transparent border-l-transparent animate-spin"></div>
                  <div className="absolute inset-2 flex items-center justify-center text-xl animate-pulse">
                    🔮
                  </div>
                </div>
                <h3 className="text-lg font-semibold text-white mb-1">
                  Connecting to AWS Bedrock Constellations...
                </h3>
                <p className="text-slate-400 text-xs max-w-sm">
                  Computing serverless fortune, planetary lambdas, and architectural destiny ✨
                </p>
              </div>
            )}

            {/* Error State */}
            {error && !loading && (
              <div className="py-8 text-center">
                <div className="text-5xl mb-3">⚠️</div>
                <h3 className="text-lg font-bold text-red-300 mb-2">Cosmic Stream Interrupted</h3>
                <p className="text-slate-300 text-xs sm:text-sm mb-5 max-w-md mx-auto">
                  {error}
                </p>
                <button
                  onClick={() => fetchHoroscopeData(variationOffset)}
                  className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white text-xs font-semibold py-2.5 px-6 rounded-xl transition shadow-lg shadow-purple-600/30"
                >
                  Retry Reading
                </button>
              </div>
            )}

            {/* Horoscope Reading View */}
            {horoscopeData && !loading && !error && (
              <div className="space-y-5">
                
                {/* Main Horoscope Text Card */}
                <div className="bg-gradient-to-br from-purple-900/30 via-slate-900/50 to-indigo-900/30 rounded-2xl p-5 border border-purple-500/20 relative shadow-sm">
                  <div className="flex items-center justify-between mb-3 text-xs text-purple-300 font-medium border-b border-purple-500/20 pb-2">
                    <span className="flex items-center gap-1.5">
                      <span>🚀</span> Architectural Forecast
                    </span>
                    <span className="text-[11px] opacity-75">
                      Reading #{variationOffset + 1}
                    </span>
                  </div>

                  <p className="text-slate-100 text-base sm:text-lg leading-relaxed font-light italic">
                    "{horoscopeData.horoscope}"
                  </p>
                </div>

                {/* Cloud Horoscope Attributes Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-left">
                  <div className="bg-slate-800/70 border border-slate-700/60 rounded-xl p-3.5 flex flex-col justify-between">
                    <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                      ⚡ Lucky AWS Service
                    </span>
                    <span className="text-xs font-bold text-purple-200 mt-1">
                      {horoscopeData.luckyService}
                    </span>
                  </div>

                  <div className="bg-slate-800/70 border border-slate-700/60 rounded-xl p-3.5 flex flex-col justify-between">
                    <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                      🌐 Optimal Cloud Region
                    </span>
                    <span className="text-xs font-bold text-blue-200 mt-1">
                      {horoscopeData.luckyRegion}
                    </span>
                  </div>

                  <div className="bg-slate-800/70 border border-slate-700/60 rounded-xl p-3.5 flex flex-col justify-between">
                    <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                      🛡️ Serverless Resilience
                    </span>
                    <span className="text-xs font-bold text-emerald-300 mt-1 flex items-center gap-1">
                      <span>{horoscopeData.resilienceScore}%</span>
                      <span className="text-[10px] text-slate-400 font-normal">Uptime</span>
                    </span>
                  </div>
                </div>

                {/* Meta details footer */}
                <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800">
                  <span>Engine: {horoscopeData.author}</span>
                  <span>Project: {horoscopeData.project}</span>
                </div>
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex flex-wrap items-center justify-center gap-2.5 sm:gap-3">
            <button
              onClick={() => navigate('/')}
              className="w-full sm:w-auto px-5 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs uppercase tracking-wider transition border border-slate-700 shadow-sm"
            >
              ← Back
            </button>

            {horoscopeData && (
              <>
                <button
                  onClick={handleCopy}
                  className="w-full sm:w-auto px-4 py-3 rounded-xl bg-slate-800/90 hover:bg-purple-900/40 text-purple-200 font-semibold text-xs uppercase tracking-wider transition border border-purple-500/30 flex items-center justify-center gap-1.5"
                >
                  <span>{copied ? '✓ Copied' : '📋 Share'}</span>
                </button>

                <button
                  onClick={() => setShowDownloadModal(true)}
                  className="w-full sm:w-auto px-4 py-3 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-500 hover:to-emerald-500 text-white font-semibold text-xs uppercase tracking-wider transition shadow-md shadow-emerald-600/20 flex items-center justify-center gap-1.5"
                >
                  <span>📥 Download Report</span>
                </button>

                <button
                  onClick={handleNewReading}
                  disabled={loading}
                  className="w-full sm:w-auto px-5 py-3 rounded-xl bg-gradient-to-r from-purple-600 via-indigo-600 to-pink-600 hover:from-purple-500 hover:via-indigo-500 hover:to-pink-500 text-white font-semibold text-xs uppercase tracking-wider transition shadow-lg shadow-purple-600/30 flex items-center justify-center gap-1.5 group"
                >
                  <span className="group-hover:rotate-45 transition-transform">🔮</span>
                  <span>New Reading</span>
                </button>
              </>
            )}
          </div>
        </div>
      </main>

      {/* Download Modal */}
      {showDownloadModal && horoscopeData && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md flex items-center justify-center z-50 p-4 animate-fade-in">
          <div className="glass-card rounded-3xl p-6 sm:p-8 max-w-md w-full border border-purple-500/40 shadow-2xl relative">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <span>📥</span> Download Cosmic Report
              </h3>
              <button
                onClick={() => setShowDownloadModal(false)}
                className="text-slate-400 hover:text-white text-xl leading-none"
              >
                ✕
              </button>
            </div>

            <p className="text-xs text-slate-300 mb-5 leading-relaxed">
              Export your personalized Cloud Architecture reading as a high-resolution cosmic certificate or a technical markdown document.
            </p>

            <div className="space-y-3 mb-6">
              <button
                onClick={handleDownloadPng}
                className="w-full p-4 rounded-2xl bg-gradient-to-r from-purple-900/60 to-indigo-900/60 hover:from-purple-800/80 hover:to-indigo-800/80 border border-purple-500/40 text-left transition flex items-center justify-between group"
              >
                <div>
                  <h4 className="font-bold text-sm text-white flex items-center gap-2">
                    <span>🖼️</span> Cosmic Image Card (PNG)
                  </h4>
                  <p className="text-[11px] text-slate-300 mt-1">
                    High-resolution certificate with celestial artwork & AWS stats.
                  </p>
                </div>
                <span className="text-purple-300 group-hover:translate-x-1 transition-transform text-lg">
                  ↓
                </span>
              </button>

              <button
                onClick={handleDownloadMd}
                className="w-full p-4 rounded-2xl bg-gradient-to-r from-slate-800/80 to-slate-900/80 hover:bg-slate-800 border border-slate-700 text-left transition flex items-center justify-between group"
              >
                <div>
                  <h4 className="font-bold text-sm text-white flex items-center gap-2">
                    <span>📄</span> Architecture Report (Markdown)
                  </h4>
                  <p className="text-[11px] text-slate-300 mt-1">
                    Full structured technical document formatted with cloud specs.
                  </p>
                </div>
                <span className="text-slate-400 group-hover:translate-x-1 transition-transform text-lg">
                  ↓
                </span>
              </button>
            </div>

            <div className="flex justify-end">
              <button
                onClick={() => setShowDownloadModal(false)}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-medium text-slate-300"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="relative z-20 text-center py-6 text-xs text-slate-500">
        <p>
          Cloud Horoscope • Powered by Serverless Cloud Architecture & Bedrock AI
        </p>
      </footer>
    </div>
  );
};

export default HoroscopePage;