import React from 'react';
import Hero from '../../components/Hero/Hero';
import Stats from '../../components/Stats/Stats';
import Features from '../../components/Features/Features';
import HowItWorks from '../../components/HowItWorks/HowItWorks';

const HomePage: React.FC = () => {
  return (
    <div>
      <Hero />
      <Stats />
      <Features />
      <HowItWorks />
    </div>
  );
};

export default HomePage;