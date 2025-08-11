// src/App.js
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LandingPage from './components/LandingPage';
import Login from './components/auth/Login';
import AdminPanel from './components/admin/AdminPanel';
import ClientPanel from './components/client/ClientPanel';
import Loading from './components/shared/Loading';

// Componente para rotas protegidas
const ProtectedRoute = ({ children, requiredRole = null }) => {
  const { isAuthenticated, user, loading } = useAuth();
  
  // Mostrar loading enquanto verifica autenticação
  if (loading) {
    return <Loading show={true} />;
  }
  
  // Verificar autenticação
  if (!isAuthenticated) {
    console.log('🚫 Usuário não autenticado, redirecionando para landing page');
    return <Navigate to="/" replace />;
  }
  
  // Verificar papel/tipo de usuário se necessário
  if (requiredRole && user.type !== requiredRole) {
    return <Navigate to={`/${user.type}`} />;
  }
  
  return children;
};

// Componente para redirecionar usuários autenticados
const AuthenticatedRedirect = () => {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) {
    return <Loading show={true} />;
  }

  if (isAuthenticated && user) {
    // Redirecionar para o painel correto baseado no tipo de usuário
    console.log('🔄 Usuário autenticado, redirecionando para:', user.type);
    return <Navigate to={`/${user.type}`} replace />;
  }

  return <LandingPage />;
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Rota de login */}
          <Route path="/login" element={<Login />} />
          
          {/* Rotas do administrador */}
          <Route path="/admin/*" element={
            <ProtectedRoute requiredRole="admin">
              <AdminPanel />
            </ProtectedRoute>
          } />
          
          {/* Rotas do cliente */}
          <Route path="/cliente/*" element={
            <ProtectedRoute requiredRole="cliente">
              <ClientPanel />
            </ProtectedRoute>
          } />
          
          {/* Redirecionamento da raiz */}
          <Route path="/" element={<AuthenticatedRedirect />} />
          
          {/* Rota para qualquer outro caminho */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
