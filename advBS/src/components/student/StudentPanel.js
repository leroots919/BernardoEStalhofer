import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from '../shared/Sidebar';
import Catalog from './Catalog';
import Favorites from './Favorites';
// import Playlists from './Playlists'; // Oculto temporariamente
import History from './History';

const StudentPanel = () => {
  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      <Sidebar type="student" />
      <main className="flex-1 ml-64 p-8 overflow-y-auto">
        <div className="max-w-7xl mx-auto">
          <Routes>
            <Route index element={<Navigate to="catalog" replace />} />
            <Route path="catalog" element={<Catalog />} />
            <Route path="favorites" element={<Favorites />} />
            {/* <Route path="playlists" element={<Playlists />} /> */}
            <Route path="history" element={<History />} />
            <Route path="*" element={<Navigate to="catalog" replace />} />
          </Routes>
        </div>
      </main>
    </div>
  );
};

export default StudentPanel;
