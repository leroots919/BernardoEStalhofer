import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import PageHeader from '../shared/PageHeader';
import Card from '../shared/Card';
import Button from '../shared/Button';

const Profile = () => {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    cpf: '',
    address: '',
    city: '',
    state: '',
    zipCode: ''
  });

  useEffect(() => {
    // Carregar dados do usuário
    if (user) {
      setFormData({
        name: user.name || '',
        email: user.email || '',
        phone: '',
        cpf: '',
        address: '',
        city: '',
        state: '',
        zipCode: ''
      });
    }
  }, [user]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = () => {
    // Aqui você implementaria a lógica para salvar os dados
    alert('Dados salvos com sucesso!');
    setIsEditing(false);
  };

  const handleCancel = () => {
    // Restaurar dados originais
    setFormData({
      name: user?.name || '',
      email: user?.email || '',
      phone: '',
      cpf: '',
      address: '',
      city: '',
      state: '',
      zipCode: ''
    });
    setIsEditing(false);
  };

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Meu Perfil" 
        subtitle="Gerencie suas informações pessoais"
      />
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Informações Pessoais */}
        <div className="lg:col-span-2">
          <Card className="p-6">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold text-white">Informações Pessoais</h3>
              {!isEditing ? (
                <Button 
                  onClick={() => setIsEditing(true)}
                  variant="outline"
                  size="sm"
                >
                  Editar
                </Button>
              ) : (
                <div className="flex gap-2">
                  <Button 
                    onClick={handleSave}
                    variant="primary"
                    size="sm"
                  >
                    Salvar
                  </Button>
                  <Button 
                    onClick={handleCancel}
                    variant="outline"
                    size="sm"
                  >
                    Cancelar
                  </Button>
                </div>
              )}
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Nome Completo
                </label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                />
              </div>
              
              <div>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Email
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                />
              </div>
              
              <div>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Telefone
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                  placeholder="(11) 99999-9999"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                />
              </div>
              
              <div>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  CPF
                </label>
                <input
                  type="text"
                  name="cpf"
                  value={formData.cpf}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                  placeholder="000.000.000-00"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                />
              </div>
              
              <div className="md:col-span-2">
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Endereço
                </label>
                <input
                  type="text"
                  name="address"
                  value={formData.address}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                  placeholder="Rua, número, complemento"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                />
              </div>
              
              <div>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Cidade
                </label>
                <input
                  type="text"
                  name="city"
                  value={formData.city}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                />
              </div>
              
              <div>
                <label className="block text-gray-300 text-sm font-medium mb-2">
                  Estado
                </label>
                <input
                  type="text"
                  name="state"
                  value={formData.state}
                  onChange={handleInputChange}
                  disabled={!isEditing}
                  placeholder="SP"
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                />
              </div>
            </div>
          </Card>
        </div>
        
        {/* Resumo da Conta */}
        <div className="space-y-6">
          <Card className="p-6">
            <h3 className="text-xl font-bold text-white mb-4">Resumo da Conta</h3>
            <div className="space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-300">Tipo de Conta:</span>
                <span className="text-blue-400 font-medium">Cliente</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-300">Membro desde:</span>
                <span className="text-white">Janeiro 2024</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-300">Casos ativos:</span>
                <span className="text-green-400 font-medium">2</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-300">Casos concluídos:</span>
                <span className="text-blue-400 font-medium">1</span>
              </div>
            </div>
          </Card>
          
          <Card className="p-6">
            <h3 className="text-xl font-bold text-white mb-4">Segurança</h3>
            <div className="space-y-3">
              <Button variant="outline" className="w-full">
                Alterar Senha
              </Button>
              <Button variant="outline" className="w-full">
                Configurar 2FA
              </Button>
            </div>
          </Card>
          
          <Card className="p-6">
            <h3 className="text-xl font-bold text-white mb-4">Suporte</h3>
            <div className="space-y-3">
              <Button variant="outline" className="w-full">
                Central de Ajuda
              </Button>
              <Button variant="primary" className="w-full">
                Falar com Suporte
              </Button>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default Profile;
