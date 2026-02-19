import React from 'react';
import './Features.css';

const Features: React.FC = () => (
  <section id="features" className="section-container">
    <h2 className="section-title">Smarter Logistics. Faster Deliveries.</h2>
    <p className="section-subtitle">
      Our platform combines intelligent automation, real-time tracking, and scalable architecture
      to streamline modern logistics operations end-to-end.
    </p>

    <div className="features-grid">
      {/* AI / Optimization Features */}
      <div className="feature-card">
        <div className="feature-icon">🧠</div>
        <h3>Intelligent Route Optimization</h3>
        <p>
          AI-driven algorithms analyze traffic, distance, and delivery priority to generate the
          most efficient routes, reducing fuel costs and delivery time.
        </p>
      </div>

      <div className="feature-card">
        <div className="feature-icon">📊</div>
        <h3>Predictive Delivery Insights</h3>
        <p>
          Machine learning models forecast delays, demand spikes, and delivery risks, helping
          logistics managers take proactive decisions.
        </p>
      </div>

      <div className="feature-card">
        <div className="feature-icon">📦</div>
        <h3>Smart Shipment Classification</h3>
        <p>
          Automatically categorize shipments based on size, priority, and destination to ensure
          optimal handling and resource allocation.
        </p>
      </div>

      <div className="feature-card">
        <div className="feature-icon">🔐</div>
        <h3>Secure Proof of Delivery</h3>
        <p>
          Digital verification using OTPs, QR codes, or signatures ensures secure and transparent
          handover of goods.
        </p>
      </div>

      {/* User / Operations Features */}
      <div className="feature-card">
        <div className="feature-icon">📍</div>
        <h3>Real-Time Vehicle Tracking</h3>
        <p>
          Track vehicles live with GPS integration, providing accurate ETAs and full shipment
          visibility to both operators and customers.
        </p>
      </div>

      <div className="feature-card">
        <div className="feature-icon">💬</div>
        <h3>Driver & Manager Communication</h3>
        <p>
          Secure in-app messaging enables seamless communication between drivers, warehouse staff,
          and logistics managers.
        </p>
      </div>

      {/* Technical Architecture */}
      <div className="feature-card">
        <div className="feature-icon">🎨</div>
        <h3>Responsive Logistics Dashboard</h3>
        <p>
          A modern, responsive dashboard built with React that works smoothly across desktops,
          tablets, and mobile devices.
        </p>
      </div>

    </div>
  </section>
);

export default Features;
