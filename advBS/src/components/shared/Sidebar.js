// src/components/shared/Sidebar.js
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faUsers, faVideo, faChartBar, faBook,
  faHeart, faList, faHistory, faSignOutAlt,
  faGavel, faFileAlt, faCalendarAlt, faUser,
  faClipboardList
} from '@fortawesome/free-solid-svg-icons';
import { useAuth } from '../../context/AuthContext';
import BSLogo from './BSLogo';

const Sidebar = ({ type }) => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/'); // Vai para landing page
  };

  const isActive = (path) => {
    return location.pathname === path;
  };
  
  // Renderiza a sidebar do administrador
  const renderAdminSidebar = () => (
    <>
      <div className="header bg-gradient-to-b from-black to-gray-800 py-6 px-6">
        <div className="flex items-center space-x-3">
          <BSLogo size={36} className="opacity-95" />
          <div>
            <h3 className="text-white font-bold text-lg">Painel Admin</h3>
            <p className="text-gray-300 text-xs">Bernardo & Stahlhöfer</p>
          </div>
        </div>
      </div>
      <div className="px-4 py-2">
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/admin/dashboard')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/admin/dashboard')}
        >
          <FontAwesomeIcon icon={faChartBar} className="mr-3 w-5 h-5" />
          <span className="font-medium">Dashboard</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/admin/clients')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/admin/clients')}
        >
          <FontAwesomeIcon icon={faUsers} className="mr-3 w-5 h-5" />
          <span className="font-medium">Clientes</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/admin/processes')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/admin/processes')}
        >
          <FontAwesomeIcon icon={faClipboardList} className="mr-3 w-5 h-5" />
          <span className="font-medium">Processos</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/admin/files')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/admin/files')}
        >
          <FontAwesomeIcon icon={faFileAlt} className="mr-3 w-5 h-5" />
          <span className="font-medium">Arquivos</span>
        </div>
      </div>
    </>
  );
  
  // Renderiza a sidebar do aluno
  const renderStudentSidebar = () => (
    <>
      <div className="header bg-gradient-to-b from-black to-gray-800 py-6 px-6">
        <div className="flex items-center space-x-3">
          <BSLogo size={36} className="opacity-95" />
          <div>
            <h3 className="text-white font-bold text-lg">Portal do Cliente</h3>
            <p className="text-gray-300 text-xs">Bernardo & Stahlhöfer</p>
          </div>
        </div>
      </div>
      <div className="px-4 py-2">
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/student/catalog')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/student/catalog')}
        >
          <FontAwesomeIcon icon={faBook} className="mr-3 w-5 h-5" />
          <span className="font-medium">Catálogo de Aulas</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/student/favorites')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/student/favorites')}
        >
          <FontAwesomeIcon icon={faHeart} className="mr-3 w-5 h-5" />
          <span className="font-medium">Favoritos</span>
        </div>
        {/* Playlists temporariamente oculto */}
        {/* <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/student/playlists')
              ? 'bg-sidebar-active text-primary-red border-l-4 border-primary-red'
              : 'text-gray-700 hover:bg-sidebar-hover hover:text-primary-red'
          }`}
          onClick={() => navigate('/student/playlists')}
        >
          <FontAwesomeIcon icon={faList} className="mr-3 w-5 h-5" />
          <span className="font-medium">Playlists</span>
        </div> */}
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/student/history')
              ? 'bg-red-100 text-primary-red border-l-4 border-primary-red'
              : 'text-white hover:bg-gray-500 hover:text-red-200'
          }`}
          onClick={() => navigate('/student/history')}
        >
          <FontAwesomeIcon icon={faHistory} className="mr-3 w-5 h-5" />
          <span className="font-medium">Histórico</span>
        </div>
      </div>
    </>
  );

  // Renderiza a sidebar do cliente
  const renderClientSidebar = () => (
    <>
      <div className="header bg-gradient-to-b from-blue-900 to-blue-800 py-6 px-6">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 bg-blue-600 rounded-lg flex items-center justify-center">
            <FontAwesomeIcon icon={faGavel} className="text-white text-lg" />
          </div>
          <div>
            <h3 className="text-white font-bold text-lg">AdvTransito</h3>
            <p className="text-blue-200 text-xs">Portal do Cliente</p>
          </div>
        </div>
      </div>
      <div className="px-4 py-2">
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/cliente/profile')
              ? 'bg-blue-100 text-blue-800 border-l-4 border-blue-600'
              : 'text-white hover:bg-blue-700 hover:text-blue-200'
          }`}
          onClick={() => navigate('/cliente/profile')}
        >
          <FontAwesomeIcon icon={faUser} className="mr-3 w-5 h-5" />
          <span className="font-medium">Meus Dados</span>
        </div>
        <div
          className={`flex items-center px-4 py-3 rounded-modern cursor-pointer transition-all duration-200 ${
            isActive('/cliente/cases')
              ? 'bg-blue-100 text-blue-800 border-l-4 border-blue-600'
              : 'text-white hover:bg-blue-700 hover:text-blue-200'
          }`}
          onClick={() => navigate('/cliente/cases')}
        >
          <FontAwesomeIcon icon={faFileAlt} className="mr-3 w-5 h-5" />
          <span className="font-medium">Meus Processos</span>
        </div>
      </div>
    </>
  );

  const renderSidebar = () => {
    if (type === 'admin') return renderAdminSidebar();
    if (type === 'cliente') return renderClientSidebar();
    return renderStudentSidebar(); // fallback para student
  };

  return (
    <div className="bg-gray-800 w-64 h-screen flex flex-col shadow-lg fixed left-0 top-0 z-[9999] border-r border-gray-700">
      {renderSidebar()}

      {/* Botão de logout (comum para ambos os tipos) */}
      <div className="mt-auto p-4">
        <div
          className="flex items-center px-4 py-3 rounded-lg cursor-pointer transition-all duration-200 text-white hover:bg-red-100 hover:text-red-600 border border-gray-600 hover:border-red-400"
          onClick={handleLogout}
        >
          <FontAwesomeIcon icon={faSignOutAlt} className="mr-3 w-5 h-5" />
          <span className="font-medium">Sair</span>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
