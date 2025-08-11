import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from '../shared/Sidebar';
import ClientProfile from './ClientProfile';
import MyCases from './MyCases';

const ClientPanel = () => {
  return (
    <div className="flex h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900">
      <Sidebar type="cliente" />
      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <div className="max-w-7xl mx-auto">
          <Routes>
            <Route index element={<Navigate to="profile" replace />} />
            <Route path="profile" element={<ClientProfile />} />
            <Route path="cases" element={<MyCases />} />
            <Route path="*" element={<Navigate to="profile" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  );
};

export default ClientPanel;
