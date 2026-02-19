import React from 'react';
import CountUp from 'react-countup';
import { useInView } from 'react-intersection-observer';
import './Stats.css';

interface StatItemProps {
  value: number;
  label: string;
  suffix?: string;
}

const StatItem: React.FC<StatItemProps> = ({ value, label, suffix = '' }) => {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.5 });

  return (
    <div className="stat-card" ref={ref}>
      <h3 className="stat-value">
        {inView ? (
          <CountUp start={0} end={value} duration={2.5} separator="," />
        ) : (
          '0'
        )}
        {suffix}
      </h3>
      <p className="stat-label">{label}</p>
    </div>
  );
};

const Stats: React.FC = () => {
  return (
    <section id="stats" className="stats-container">
      <div className="stats-grid">
        <StatItem value={18.6} suffix="K+" label="Successful Deliveries" />
        <StatItem value={3.2} suffix="M+" label="Kilometers Covered" />
        <StatItem value={96} suffix="%" label="On-Time Delivery Rate" />
        <StatItem value={24} suffix="/7" label="Operations Monitoring" />
      </div>
    </section>
  );
};

export default Stats;
