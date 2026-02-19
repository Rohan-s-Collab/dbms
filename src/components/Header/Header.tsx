import React from 'react';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="header-container">
      <div className="logo">
        <span role="img" aria-label="location pin">📍</span>
        <span>FindBack</span>
      </div>
      <nav className="nav-links">
        <ul>
          <li><a href="#features">Features</a></li>
          <li><a href="#how-it-works">How It Works</a></li>
          <li><a href="#about">About</a></li>
        </ul>
      </nav>
      <button className="get-started-btn">Get Started</button>
    </header>
  );
};

export default Header;