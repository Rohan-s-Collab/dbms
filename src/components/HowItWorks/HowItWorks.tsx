import React, { useState } from 'react';
import './HowItWorks.css';

const HowItWorks: React.FC = () => {
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState<null | 'success' | 'error'>(null);

  // Handle form submit as JSON
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus(null);

    try {
      const response = await fetch('https://formspree.io/f/mblplrlg', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });
      if (response.ok) {
        setStatus('success');
        setMessage('');
      } else {
        setStatus('error');
      }
    } catch {
      setStatus('error');
    }
  };

  return (
    <section id="how-it-works" className="section-container how-it-works-section">
      <h2 className="section-title">Deliver Smarter in 3 Simple Steps</h2>
      <p className="section-subtitle">
        Our streamlined logistics workflow ensures faster deliveries and complete visibility.
      </p>

      <div className="steps-container">
        <div className="step-card">
          <div className="step-number">1</div>
          <h3>Create a Shipment</h3>
          <p>
            Add shipment details including pickup location, destination, package type, and delivery
            priority in just a few clicks.
          </p>
        </div>

        <div className="step-arrow">→</div>

        <div className="step-card">
          <div className="step-number">2</div>
          <h3>Optimize & Assign</h3>
          <p>
            Our system automatically assigns the best vehicle and route using real-time traffic and
            AI-based optimization.
          </p>
        </div>

        <div className="step-arrow">→</div>

        <div className="step-card">
          <div className="step-number">3</div>
          <h3>Track & Deliver</h3>
          <p>
            Monitor shipments live, receive status updates, and confirm delivery securely with
            digital proof of delivery.
          </p>
        </div>
      </div>

      {/* Contact Section */}
      <section className="contact-section">
        <p className="footer-question">Need help with operations or onboarding? Reach out to us.</p>

        <form onSubmit={handleSubmit} style={{ display: 'inline' }}>
          <textarea
            className="contact-message-input"
            value={message}
            onChange={e => setMessage(e.target.value)}
            placeholder="Type your message here..."
            rows={3}
            required
            style={{
              resize: 'vertical',
              width: '270px',
              marginBottom: '1rem',
              borderRadius: '5px',
              padding: '0.5rem',
            }}
          />
          <br />
          <button type="submit" className="contact-us-button">
            Contact Us
          </button>
        </form>

        {status === 'success' && (
          <p style={{ color: '#237a46', marginTop: '1rem' }}>
            Message sent! Our logistics team will reach out shortly.
          </p>
        )}

        {status === 'error' && (
          <p style={{ color: '#b12134', marginTop: '1rem' }}>
            Something went wrong. Please try again later.
          </p>
        )}
      </section>
    </section>
  );
};

export default HowItWorks;
