import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const HoroscopePage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { name, dob } = location.state || {};

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 relative overflow-hidden">
      {/* Watermark Doodles */}
      <div className="absolute inset-0 opacity-10 pointer-events-none">
        <div className="absolute top-10 left-10 text-6xl animate-float">🔮</div>
        <div className="absolute top-20 right-20 text-5xl animate-float" style={{animationDelay: '1s'}}>🪄</div>
        <div className="absolute bottom-20 left-20 text-4xl animate-float" style={{animationDelay: '2s'}}>⭐</div>
        <div className="absolute bottom-10 right-10 text-5xl animate-float" style={{animationDelay: '0.5s'}}>🌙</div>
        <div className="absolute top-1/2 left-5 text-4xl animate-float" style={{animationDelay: '1.5s'}}>✨</div>
        <div className="absolute top-1/3 right-5 text-4xl animate-float" style={{animationDelay: '2.5s'}}>🌟</div>
      </div>

      <div className="flex items-center justify-center min-h-screen p-4">
        <div className="bg-white bg-opacity-20 backdrop-blur-md rounded-3xl p-8 shadow-2xl border border-white border-opacity-30 max-w-2xl w-full">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-4">Your Horoscope</h1>
            <div className="text-6xl mb-4">🔮</div>
            <h2 className="text-2xl font-semibold text-white mb-2">Hello, {name}!</h2>
            <p className="text-white text-opacity-90">Born on {new Date(dob).toLocaleDateString()}</p>
          </div>

          <div className="bg-white bg-opacity-10 rounded-2xl p-6 mb-6">
            <div className="text-center">
              <p className="text-white text-lg leading-relaxed">
                The crystal ball is preparing your cosmic reading... ✨
              </p>
            </div>
          </div>

          <div className="text-center">
            <button
              onClick={() => navigate('/')}
              className="bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white font-semibold py-3 px-8 rounded-xl transition duration-300 transform hover:scale-105 shadow-lg"
            >
              ← Back to Home
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HoroscopePage;