// src/components/admin/ClientManagement.js
import React, { useState, useEffect } from 'react';
import { Plus, Search, Edit, Trash2, Eye } from 'lucide-react';
import { adminService } from '../../services/api';

const ClientManagement = () => {
  const [clients, setClients] = useState([]);
  const [filteredClients, setFilteredClients] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [showCaseModal, setShowCaseModal] = useState(false);
  const [selectedClient, setSelectedClient] = useState(null);
  const [selectedClientForCase, setSelectedClientForCase] = useState(null);
  const [clientCases, setClientCases] = useState({});
  const [services, setServices] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    cpf: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    zip_code: ''
  });
  const [caseFormData, setCaseFormData] = useState({
    title: '',
    description: '',
    status: 'pendente',
    service_id: 1 // ID padrão do primeiro serviço
  });

  useEffect(() => {
    fetchClients();
    fetchServices();
  }, []);

  useEffect(() => {
    if (!clients || !Array.isArray(clients)) {
      setFilteredClients([]);
      return;
    }

    const filtered = clients.filter(client => {
      if (!client) return false;

      const name = client.name || '';
      const email = client.email || '';
      const cpf = client.cpf || '';

      return (
        name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        cpf.includes(searchTerm)
      );
    });
    setFilteredClients(filtered);
  }, [clients, searchTerm]);

  const fetchClients = async () => {
    try {
      setLoading(true);
      const response = await adminService.getClients();
      console.log('Resposta completa da API:', response);

      // A resposta vem no formato { data: [...] }
      const clients = response.data || response || [];
      console.log('Clientes carregados:', clients);

      setClients(Array.isArray(clients) ? clients : []);

      // Buscar casos para cada cliente
      if (Array.isArray(clients)) {
        clients.forEach(client => {
          if (client && client.id) {
            fetchClientCases(client.id);
          }
        });
      }
    } catch (error) {
      console.error('Erro ao carregar clientes:', error);
      setClients([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchClientCases = async (clientId) => {
    try {
      const response = await adminService.getClientCases(clientId);
      console.log(`Casos do cliente ${clientId}:`, response);

      // A resposta vem no formato { data: [...] }
      const cases = response.data || response || [];

      setClientCases(prev => ({
        ...prev,
        [clientId]: Array.isArray(cases) ? cases : []
      }));
    } catch (error) {
      console.error('Erro ao buscar casos do cliente:', error);
      setClientCases(prev => ({
        ...prev,
        [clientId]: []
      }));
    }
  };

  const fetchServices = async () => {
    try {
      const response = await adminService.getServices();
      console.log('Serviços carregados:', response);

      // A resposta vem no formato { data: [...] }
      const services = response.data || response || [];

      if (Array.isArray(services) && services.length > 0) {
        setServices(services);
      } else {
        // Se não conseguir buscar serviços, usar valores padrão
        setServices([
          { id: 1, name: 'CNH', description: 'Questões relacionadas à CNH' },
          { id: 2, name: 'Acidentes', description: 'Acidentes de trânsito' },
          { id: 3, name: 'Consultoria', description: 'Consultoria jurídica' },
          { id: 4, name: 'Recursos', description: 'Recursos e defesas' }
        ]);
      }
    } catch (error) {
      console.error('Erro ao buscar serviços:', error);
      // Se não conseguir buscar serviços, usar valores padrão
      setServices([
        { id: 1, name: 'CNH', description: 'Questões relacionadas à CNH' },
        { id: 2, name: 'Acidentes', description: 'Acidentes de trânsito' },
        { id: 3, name: 'Consultoria', description: 'Consultoria jurídica' },
        { id: 4, name: 'Recursos', description: 'Recursos e defesas' }
      ]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (selectedClient) {
        await adminService.updateClient(selectedClient.id, formData);
      } else {
        await adminService.createClient(formData);
      }
      fetchClients();
      setShowModal(false);
      resetForm();
    } catch (error) {
      console.error('Erro ao salvar cliente:', error);
    }
  };

  const handleEdit = (client) => {
    setSelectedClient(client);
    setFormData({
      name: client.name || '',
      email: client.email || '',
      cpf: client.cpf || '',
      phone: client.phone || '',
      address: client.address || '',
      city: client.city || '',
      state: client.state || '',
      zip_code: client.zip_code || ''
    });
    setShowModal(true);
  };

  const handleDelete = async (clientId) => {
    if (window.confirm('Tem certeza que deseja excluir este cliente?')) {
      try {
        await adminService.deleteClient(clientId);
        fetchClients();
      } catch (error) {
        console.error('Erro ao excluir cliente:', error);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      email: '',
      cpf: '',
      phone: '',
      address: '',
      city: '',
      state: '',
      zip_code: ''
    });
    setSelectedClient(null);
  };

  const handleCreateCase = (client) => {
    setSelectedClientForCase(client);
    setCaseFormData({
      title: '',
      description: '',
      status: 'pendente',
      service_id: services.length > 0 ? services[0].id : 1
    });
    setShowCaseModal(true);
  };

  const handleCaseSubmit = async (e) => {
    e.preventDefault();
    try {
      // Usar a rota que funciona
      const caseData = {
        ...caseFormData,
        client_id: selectedClientForCase.id
      };

      console.log('Enviando dados do caso:', caseData);

      await adminService.createClientCase(selectedClientForCase.id, caseData);
      fetchClientCases(selectedClientForCase.id);
      setShowCaseModal(false);
      setCaseFormData({
        title: '',
        description: '',
        status: 'pendente',
        service_id: services.length > 0 ? services[0].id : 1
      });
      setSelectedClientForCase(null);
    } catch (error) {
      console.error('Erro ao criar caso:', error);
      alert('Erro ao criar caso. Tente novamente.');
    }
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
        <h1 className="text-3xl font-bold text-white">Gerenciar Clientes</h1>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2"
        >
          <Plus className="h-4 w-4" />
          Novo Cliente
        </button>
      </div>

      {/* Busca */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
        <input
          type="text"
          placeholder="Buscar por nome, email ou CPF..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {/* Lista de Clientes */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Cliente
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  CPF
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Telefone
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Processos
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Cadastro
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {filteredClients && filteredClients.length > 0 ? (
                filteredClients.map((client) => {
                  if (!client) return null;

                  return (
                    <tr key={client.id} className="hover:bg-gray-700">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div>
                          <div className="text-sm font-medium text-white">{client.name || 'Nome não informado'}</div>
                          <div className="text-sm text-gray-400">{client.email || 'Email não informado'}</div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {client.cpf || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {client.phone || '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        <div className="flex items-center gap-2">
                          <span className="bg-blue-600 text-white px-2 py-1 rounded text-xs">
                            {clientCases[client.id]?.length || 0} processo(s)
                          </span>
                          <button
                            onClick={() => handleCreateCase(client)}
                            className="text-green-400 hover:text-green-300 text-xs"
                            title="Criar novo processo"
                          >
                            + Novo
                          </button>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {client.register_date ? new Date(client.register_date).toLocaleDateString('pt-BR') : '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleEdit(client)}
                            className="text-blue-400 hover:text-blue-300"
                          >
                            <Edit className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleDelete(client.id)}
                            className="text-red-400 hover:text-red-300"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan="6" className="px-6 py-4 text-center text-gray-400">
                    {loading ? 'Carregando clientes...' : 'Nenhum cliente encontrado'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-white mb-4">
              {selectedClient ? 'Editar Cliente' : 'Novo Cliente'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Nome Completo
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Email
                </label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  CPF
                </label>
                <input
                  type="text"
                  value={formData.cpf}
                  onChange={(e) => setFormData({ ...formData, cpf: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Telefone
                </label>
                <input
                  type="text"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    resetForm();
                  }}
                  className="px-4 py-2 text-gray-300 hover:text-white"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
                >
                  {selectedClient ? 'Atualizar' : 'Criar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal para Criar Caso */}
      {showCaseModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold text-white mb-4">
              Novo Processo para {selectedClientForCase?.name}
            </h2>
            <form onSubmit={handleCaseSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Tipo de Serviço
                </label>
                <select
                  value={caseFormData.service_id}
                  onChange={(e) => setCaseFormData({ ...caseFormData, service_id: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                >
                  {services.map(service => (
                    <option key={service.id} value={service.id}>
                      {service.name} - {service.description}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Título do Processo
                </label>
                <input
                  type="text"
                  required
                  value={caseFormData.title}
                  onChange={(e) => setCaseFormData({ ...caseFormData, title: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Ex: Multa por excesso de velocidade"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Descrição
                </label>
                <textarea
                  required
                  value={caseFormData.description}
                  onChange={(e) => setCaseFormData({ ...caseFormData, description: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows="3"
                  placeholder="Descreva os detalhes do processo..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-1">
                  Status
                </label>
                <select
                  value={caseFormData.status}
                  onChange={(e) => setCaseFormData({ ...caseFormData, status: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="pendente">Pendente</option>
                  <option value="em_andamento">Em Andamento</option>
                  <option value="parado_na_justica">Parado na Justiça</option>
                  <option value="concluido">Concluído</option>
                </select>
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowCaseModal(false)}
                  className="px-4 py-2 text-gray-300 hover:text-white"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg"
                >
                  Criar Processo
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default ClientManagement;
