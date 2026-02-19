import React from 'react';
import { Link } from 'react-router-dom'; // Import Link
import './Navbar.css';

const Navbar: React.FC = () => {
  return (
    <header className="navbar-container">
      <Link to="/" className="logo">
        <span role="img" aria-label="package icon" style={{ marginRight: '8px' }}>📦</span>
        <span>LogiSphere </span><span className="beta-badge">v1.0</span>
      </Link>
      <nav className="nav-links">
        <ul>
          <li><a href="/#features">Features</a></li>
          <li><a href="/#how-it-works">How It Works</a></li>
          {/* Corrected structure: Link inside the li */}
          <li><Link to="/timeline">What's New</Link></li>
        </ul>
      </nav>
    </header>
  );
};

export default Navbar;