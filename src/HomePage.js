import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const [showIntro, setShowIntro] = useState(true);
  const [name, setName] = useState('');
  const [dob, setDob] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowIntro(false);
    }, 3000);
    return () => clearTimeout(timer);
  }, []);

  const handleShowHoroscope = () => {
    if (name && dob) {
      navigate('/horoscope', { state: { name, dob } });
    } else {
      alert('Please enter your name and date of birth!');
    }
  };

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

      {/* Intro Screen */}
      {showIntro && (
        <div className="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-md flex items-center justify-center z-10">
          <div className="bg-white bg-opacity-20 backdrop-blur-sm rounded-full px-8 py-6 border border-white border-opacity-30">
            <p className="text-white text-xl font-semibold animate-flash text-center">
              Let's ask Crystal ball our horoscope. 🔮
            </p>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex items-center justify-center min-h-screen p-4">
        <div className="bg-white bg-opacity-20 backdrop-blur-md rounded-3xl p-8 shadow-2xl border border-white border-opacity-30 max-w-md w-full">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">Cloud Horoscope</h1>
            <div className="text-6xl mb-4">🔮</div>
            <p className="text-white text-opacity-90">Discover your cosmic destiny</p>
          </div>

          <div className="space-y-6">
            <div>
              <label className="block text-white text-sm font-medium mb-2">Your Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-white bg-opacity-20 border border-white border-opacity-30 text-white placeholder-white placeholder-opacity-70 focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
                placeholder="Enter your name"
              />
            </div>

            <div>
              <label className="block text-white text-sm font-medium mb-2">Date of Birth</label>
              <input
                type="date"
                value={dob}
                onChange={(e) => setDob(e.target.value)}
                className="w-full px-4 py-3 rounded-xl bg-white bg-opacity-20 border border-white border-opacity-30 text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
              />
            </div>

            <button
              onClick={handleShowHoroscope}
              className="w-full bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white font-semibold py-3 px-6 rounded-xl transition duration-300 transform hover:scale-105 shadow-lg"
            >
              Show Horoscope ✨
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;