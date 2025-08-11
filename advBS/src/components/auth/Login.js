// src/components/auth/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';
import { faGavel } from '@fortawesome/free-solid-svg-icons';
import BSLogo from '../shared/BSLogo';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, loading, error } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const success = await login(email, password);

    if (success) {
      // O redirecionamento será feito automaticamente pelo AuthContext
      console.log('Login bem-sucedido');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 flex items-center justify-center p-4">
      <div className="bg-gray-800 p-8 rounded-lg shadow-xl w-full max-w-md border border-gray-700">
        {/* Header com Logo e Título */}
        <div className="text-center mb-8">
          <div className="mx-auto mb-4">
            <BSLogo size={120} />
          </div>
          <p className="text-gray-300 text-sm mt-1">Acesso ao Portal</p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-white font-medium mb-2">
              Email ou Username
            </label>
            <input
              type="text"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-gray-700 border border-gray-600 text-white px-4 py-3 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 placeholder-gray-400"
              placeholder="Digite seu email ou username"
              required
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-white font-medium mb-2">
              Senha
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-gray-700 border border-gray-600 text-white px-4 py-3 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 placeholder-gray-400"
              placeholder="Digite sua senha"
              required
            />
          </div>

          {error && (
            <div className="bg-red-900/20 border border-red-500/50 text-red-300 px-4 py-3 rounded-md text-sm">
              {error}
            </div>
          )}

          <div>
            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 transition-all duration-200 flex items-center justify-center font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading}
            >
              {loading ? (
                <>
                  <FontAwesomeIcon icon={faSpinner} spin className="mr-2" />
                  Processando...
                </>
              ) : 'Entrar'}
            </button>
          </div>

          <div className="text-center">
            <a href="#" className="text-gray-400 hover:text-blue-400 transition-colors duration-200 text-sm">
              Esqueceu sua senha?
            </a>
          </div>

          <div className="text-center mt-4">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="text-gray-400 hover:text-blue-400 transition-colors duration-200 text-sm"
            >
              ← Voltar ao site
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Login;
