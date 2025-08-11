// src/components/client/ClientProfile.js
import React, { useState, useEffect } from 'react';
import { User, Save, Edit } from 'lucide-react';
import api from '../../services/api';

const ClientProfile = () => {
  const [profile, setProfile] = useState({
    name: '',
    email: '',
    cpf: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip_code: ''
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editing, setEditing] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      const response = await api.clientService.getProfile();
      setProfile(response.data);
    } catch (error) {
      console.error('Erro ao carregar perfil:', error);
      setMessage('Erro ao carregar perfil');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setSaving(true);
      await api.clientService.updateProfile(profile);
      setMessage('Perfil atualizado com sucesso!');
      setEditing(false);
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      console.error('Erro ao atualizar perfil:', error);
      setMessage('Erro ao atualizar perfil');
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile(prev => ({
      ...prev,
      [name]: value
    }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-white">Meus Dados</h1>
        <button
          onClick={() => setEditing(!editing)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
        >
          <Edit className="h-4 w-4" />
          {editing ? 'Cancelar' : 'Editar'}
        </button>
      </div>

      {message && (
        <div className={`p-4 rounded-lg ${
          message.includes('sucesso') 
            ? 'bg-green-800 text-green-200' 
            : 'bg-red-800 text-red-200'
        }`}>
          {message}
        </div>
      )}

      <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <div className="flex items-center mb-6">
          <User className="h-8 w-8 text-blue-400 mr-3" />
          <h2 className="text-xl font-semibold text-white">Informações Pessoais</h2>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Nome Completo *
              </label>
              <input
                type="text"
                name="name"
                required
                value={profile.name}
                onChange={handleChange}
                disabled={!editing}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Email *
              </label>
              <input
                type="email"
                name="email"
                required
                value={profile.email}
                onChange={handleChange}
                disabled={!editing}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                CPF
              </label>
              <input
                type="text"
                name="cpf"
                value={profile.cpf || ''}
                onChange={handleChange}
                disabled={!editing}
                placeholder="000.000.000-00"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Telefone
              </label>
              <input
                type="text"
                name="phone"
                value={profile.phone || ''}
                onChange={handleChange}
                disabled={!editing}
                placeholder="(11) 99999-9999"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">
              Endereço
            </label>
            <input
              type="text"
              name="address"
              value={profile.address || ''}
              onChange={handleChange}
              disabled={!editing}
              placeholder="Rua, número, complemento"
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Cidade
              </label>
              <input
                type="text"
                name="city"
                value={profile.city || ''}
                onChange={handleChange}
                disabled={!editing}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Estado
              </label>
              <input
                type="text"
                name="state"
                value={profile.state || ''}
                onChange={handleChange}
                disabled={!editing}
                placeholder="SP"
                maxLength={2}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                CEP
              </label>
              <input
                type="text"
                name="zip_code"
                value={profile.zip_code || ''}
                onChange={handleChange}
                disabled={!editing}
                placeholder="00000-000"
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              />
            </div>
          </div>

          {editing && (
            <div className="flex justify-end">
              <button
                type="submit"
                disabled={saving}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white px-6 py-2 rounded-lg flex items-center gap-2"
              >
                <Save className="h-4 w-4" />
                {saving ? 'Salvando...' : 'Salvar Alterações'}
              </button>
            </div>
          )}
        </form>
      </div>

      {/* Informações de Cadastro */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <h3 className="text-lg font-semibold text-white mb-4">Informações de Cadastro</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-400">Data de Cadastro:</span>
            <span className="text-white ml-2">
              {profile.register_date ? new Date(profile.register_date).toLocaleDateString('pt-BR') : '-'}
            </span>
          </div>
          <div>
            <span className="text-gray-400">Último Login:</span>
            <span className="text-white ml-2">
              {profile.last_login ? new Date(profile.last_login).toLocaleDateString('pt-BR') : 'Nunca'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClientProfile;
