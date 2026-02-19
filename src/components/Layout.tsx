import React from 'react';
import { Outlet } from 'react-router-dom';
import Navbar from './Navbar/Navbar';

const Layout: React.FC = () => {
  return (
    <div>
      <Navbar />
      <main>
        <Outlet /> {/* This is where the page content will be rendered */}
      </main>
    </div>
  );
};

export default Layout;