// src/context/AuthContext.js
import React, { createContext, useState, useContext, useEffect } from 'react';
import { setApiToken, getToken } from '../services/api';

const API_BASE_URL = 'http://localhost:8000';

// Criando o contexto de autenticação
export const AuthContext = createContext();

// Hook personalizado para usar o contexto de autenticação
export const useAuth = () => useContext(AuthContext);

// Provedor do contexto de autenticação
export const AuthProvider = ({ children }) => {
  // Estado para armazenar informações do usuário e status de autenticação
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true); // Iniciar como true para verificar token salvo
  const [error, setError] = useState('');

  // Verificar se há token salvo ao inicializar
  useEffect(() => {
    const checkSavedToken = async () => {
      const savedToken = getToken();
      console.log('🔍 Verificando token salvo:', savedToken ? 'Token encontrado' : 'Nenhum token');

      if (savedToken) {
        try {
          console.log('🔄 Verificando validade do token...');
          // Verificar se o token é válido
          const response = await fetch(`${API_BASE_URL}/api/auth/verify`, {
            headers: {
              'Authorization': `Bearer ${savedToken}`
            }
          });

          if (response.ok) {
            const userData = await response.json();
            console.log('✅ Token válido, restaurando sessão:', userData);
            setApiToken(savedToken);
            setUser(userData.user);
            setIsAuthenticated(true);
          } else {
            console.log('❌ Token inválido, removendo...');
            setApiToken(null);
          }
        } catch (error) {
          console.error('❌ Erro ao verificar token salvo:', error);
          setApiToken(null);
        }
      } else {
        console.log('ℹ️ Nenhum token encontrado, usuário não autenticado');
      }

      setLoading(false);
      console.log('🏁 Verificação de token concluída');
    };

    checkSavedToken();
  }, []);



  // Função para realizar login
  const login = async (email, password) => {
    setLoading(true);
    setError('');

    try {
      console.log('🔄 Tentando login para:', email);
      console.log('🌐 URL da API:', `${API_BASE_URL}/api/auth/login`);

      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      console.log('📡 Resposta recebida:', response.status, response.statusText);

      const data = await response.json();

      if (response.ok) {
        // Definir o token para uso nas requisições da API
        console.log('Token recebido no login:', data.access_token);
        setApiToken(data.access_token);
        console.log('Token definido, verificando:', getToken());
        console.log('Login realizado com sucesso:', data);
        console.log('Tipo de usuário:', data.user?.type);
        setUser(data.user);
        setIsAuthenticated(true);
        return true;
      } else {
        setError(data.error || 'Erro ao fazer login');
        return false;
      }
    } catch (err) {
      console.error('❌ Erro no login:', err);
      console.error('❌ Tipo do erro:', err.name);
      console.error('❌ Mensagem:', err.message);
      setError(`Erro ao conectar com o servidor: ${err.message}`);
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Função para realizar logout
  const logout = () => {
    console.log('🚪 Realizando logout...');
    // Limpar o token da API
    setApiToken(null);
    setUser(null);
    setIsAuthenticated(false);
    console.log('✅ Logout concluído');
  };

  // Valores e funções expostos pelo contexto
  const value = {
    user,
    isAuthenticated,
    loading,
    error,
    login,
    logout
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
