// src/components/admin/AdminPanel.js
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from '../shared/Sidebar';
import Dashboard from './Dashboard';
import ClientManagement from './ClientManagement';
import ProcessFileUpload from './ProcessFileUpload';
import ProcessManagement from './ProcessManagement';

const AdminPanel = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <Sidebar type="admin" />
      <main className="ml-64 p-8 min-h-screen overflow-y-auto">
        <div className="max-w-7xl mx-auto">
          <Routes>
            <Route index element={<Navigate to="dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="clients" element={<ClientManagement />} />
            <Route path="processes" element={<ProcessManagement />} />
            <Route path="files" element={<ProcessFileUpload />} />
            <Route path="*" element={<Navigate to="dashboard" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  );
};

export default AdminPanel;
