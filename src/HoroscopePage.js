import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const HoroscopePage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { name, dob } = location.state || {};
  
  const [horoscopeData, setHoroscopeData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Your Lambda API endpoint
  const API_ENDPOINT = 'https://rud7r2puae.execute-api.us-east-1.amazonaws.com/horoscope/horoscope';

  // Function to format date from YYYY-MM-DD to DD/MM/YYYY
  const formatDateForAPI = (dateString) => {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  };

  // Function to call your horoscope API
  const fetchHoroscope = async () => {
    try {
      setLoading(true);
      setError(null);

      const formattedDob = formatDateForAPI(dob);
      
      const response = await fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: name,
          dob: formattedDob
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setHoroscopeData(data);
    } catch (err) {
      console.error('Error fetching horoscope:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Fetch horoscope when component mounts
  useEffect(() => {
    if (name && dob) {
      fetchHoroscope();
    } else {
      setError('Missing name or date of birth');
      setLoading(false);
    }
  }, [name, dob]);

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
            <h1 className="text-4xl font-bold text-white mb-4">Your Cloud Horoscope</h1>
            <div className="text-6xl mb-4">☁️</div>
            <h2 className="text-2xl font-semibold text-white mb-2">Hello, {name}!</h2>
            <p className="text-white text-opacity-90">Born on {dob ? new Date(dob).toLocaleDateString() : 'Unknown'}</p>
            {horoscopeData && (
              <div className="mt-4">
                <span className="inline-block bg-gradient-to-r from-yellow-400 to-orange-500 text-white px-4 py-2 rounded-full text-lg font-semibold">
                  {horoscopeData.sign}
                </span>
              </div>
            )}
          </div>

          <div className="bg-white bg-opacity-10 rounded-2xl p-6 mb-6">
            <div className="text-center">
              {loading && (
                <div className="flex flex-col items-center">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mb-4"></div>
                  <p className="text-white text-lg leading-relaxed">
                    The AWS crystal ball is preparing your cosmic reading... ✨
                  </p>
                </div>
              )}
              
              {error && (
                <div className="text-center">
                  <div className="text-4xl mb-4">❌</div>
                  <p className="text-red-200 text-lg mb-4">
                    Oops! Something went wrong with your cosmic reading.
                  </p>
                  <p className="text-white text-sm opacity-75 mb-4">
                    Error: {error}
                  </p>
                  <button
                    onClick={fetchHoroscope}
                    className="bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600 text-white font-semibold py-2 px-6 rounded-xl transition duration-300 transform hover:scale-105"
                  >
                    Try Again
                  </button>
                </div>
              )}
              
              {horoscopeData && !loading && !error && (
                <div className="text-left">
                  <div className="flex items-center justify-center mb-4">
                    <div className="text-3xl mr-2">🚀</div>
                    <h3 className="text-xl font-semibold text-white">Your AWS-Powered Horoscope</h3>
                    <div className="text-3xl ml-2">☁️</div>
                  </div>
                  <div className="bg-white bg-opacity-20 rounded-xl p-4 mb-4">
                    <p className="text-white text-lg leading-relaxed italic">
                      "{horoscopeData.horoscope}"
                    </p>
                  </div>
                  <div className="text-center text-sm text-white opacity-75">
                    <p>Generated by: {horoscopeData.project}</p>
                    <p>Powered by AWS Bedrock AI ⚡</p>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="text-center space-x-4">
            <button
              onClick={() => navigate('/')}
              className="bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white font-semibold py-3 px-8 rounded-xl transition duration-300 transform hover:scale-105 shadow-lg"
            >
              ← Back to Home
            </button>
            
            {horoscopeData && (
              <button
                onClick={fetchHoroscope}
                className="bg-gradient-to-r from-green-500 to-teal-500 hover:from-green-600 hover:to-teal-600 text-white font-semibold py-3 px-8 rounded-xl transition duration-300 transform hover:scale-105 shadow-lg"
              >
                🔮 Get New Reading
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HoroscopePage;