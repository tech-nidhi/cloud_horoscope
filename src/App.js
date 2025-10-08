import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './HomePage';
import HoroscopePage from './HoroscopePage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/horoscope" element={<HoroscopePage />} />
      </Routes>
    </Router>
  );
};

export default App;