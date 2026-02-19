import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./Hero.css";

const Hero: React.FC = () => {
  const fullText = "Logistics, Reimagined.";
  const [typedText, setTypedText] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (typedText.length < fullText.length) {
      const timer = setTimeout(() => {
        setTypedText(fullText.slice(0, typedText.length + 1));
      }, 70);
      return () => clearTimeout(timer);
    }
  }, [typedText, fullText]);

  return (
    <main className="hero-section">
      {/* LEFT CONTENT */}
      <div className="hero-content">
        <h1>
          {typedText}
          <span className="cursor">|</span>
        </h1>

        <p>
          Centralize shipments, automate fleet operations, and gain real-time
          visibility across your entire logistics network.
        </p>

        <div className="hero-buttons">
          <button
            className="primary-btn"
            onClick={() => navigate("/register")}
          >
            Get Started
          </button>

          
        </div>
      </div>

      {/* RIGHT GRAPHICS */}
      <div className="hero-graphic">
        <div className="glass-card main-card">
          <div className="icon">📦</div>
          <div className="card-content">
            <h4>Shipment In Transit</h4>
            <p>DEL-45892 · Chennai → Mumbai</p>

            <div className="progress">
              <span className="progress-fill"></span>
            </div>
          </div>
        </div>

        <div className="glass-card progress-card">
          <div className="progress-header">
            <span>🚚 Delivery Progress</span>
            <span className="percent">72%</span>
          </div>

          <div className="progress large">
            <span className="progress-fill"></span>
          </div>

          <div className="progress-steps">
            <span className="active">Picked</span>
            <span className="active">In Transit</span>
            <span>Out for Delivery</span>
            <span>Delivered</span>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Hero;
