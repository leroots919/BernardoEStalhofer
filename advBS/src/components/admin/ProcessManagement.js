import React, { useState, useEffect, useCallback } from 'react';
import { adminService } from '../../services/api';
import './ProcessManagement.css';

const ProcessManagement = () => {
  const [processes, setProcesses] = useState([]);
  const [clients, setClients] = useState([]);
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [filters, setFilters] = useState({
    clientId: '',
    status: '',
    search: ''
  });
  const [editingProcess, setEditingProcess] = useState(null);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [processToDelete, setProcessToDelete] = useState(null);

  const itemsPerPage = 10;

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError('');

      // Buscar casos (que são os "processos")
      const casesResponse = await adminService.get('/api/admin/cases');
      console.log('📋 Casos carregados:', casesResponse);

      // Os casos vêm com duplo data do axios
      let allCases = casesResponse?.data?.data || casesResponse?.data || [];
      console.log('🔍 Tipo de allCases:', typeof allCases, Array.isArray(allCases));
      console.log('🔍 allCases:', allCases);

      // DEBUG: Verificar se service_name está presente
      if (allCases.length > 0) {
        console.log('🔍 PRIMEIRO CASO COMPLETO:', allCases[0]);
        console.log('🔍 SERVICE_NAME do primeiro caso:', allCases[0].service_name);
        console.log('🔍 Todas as propriedades do primeiro caso:', Object.keys(allCases[0]));
      }

      // Garantir que é array
      if (!Array.isArray(allCases)) {
        console.log('❌ allCases não é array, convertendo...');
        allCases = [];
      }

      // Aplicar filtros localmente
      let filteredCases = allCases;

      if (filters.clientId) {
        filteredCases = filteredCases.filter(caso => caso.client_id === filters.clientId);
      }

      if (filters.status) {
        filteredCases = filteredCases.filter(caso => caso.status === filters.status);
      }

      if (filters.search) {
        const searchLower = filters.search.toLowerCase();
        filteredCases = filteredCases.filter(caso =>
          caso.description?.toLowerCase().includes(searchLower) ||
          caso.client_name?.toLowerCase().includes(searchLower)
        );
      }

      // Aplicar paginação
      const startIndex = (currentPage - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;
      const paginatedCases = filteredCases.slice(startIndex, endIndex);

      setProcesses(paginatedCases);
      setTotalPages(Math.ceil(filteredCases.length / itemsPerPage));

      // Buscar clientes para o filtro
      if (clients.length === 0) {
        const clientsResponse = await adminService.get('/api/admin/clients');
        setClients(clientsResponse?.data?.data || clientsResponse?.data || []);
      }

      // Buscar serviços para o modal de edição
      if (services.length === 0) {
        console.log('🔍 Carregando serviços...');
        const servicesResponse = await adminService.get('/api/services');
        const servicesData = servicesResponse?.data?.data || servicesResponse?.data || [];
        console.log('📋 Serviços carregados:', servicesData.length, servicesData);
        setServices(servicesData);
      }
    } catch (error) {
      console.error('❌ Erro ao carregar dados:', error);
      setError('Erro ao carregar dados');
    } finally {
      setLoading(false);
    }
  }, [currentPage, filters, clients.length, services.length]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  // const handleStatusChange = async (processId, newStatus) => {
  //   try {
  //     // Por enquanto, vamos usar a rota de casos
  //     await adminService.put(`/api/admin/cases/${processId}`, {
  //       status: newStatus
  //     });

  //     console.log(`✅ Status do caso ${processId} alterado para: ${newStatus}`);
  //     fetchData(); // Recarregar dados
  //   } catch (error) {
  //     console.error('❌ Erro ao alterar status:', error);
  //     setError('Erro ao alterar status do processo');
  //   }
  // };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'pendente': { color: 'bg-orange-100 text-orange-800', text: 'Pendente' },
      'em_andamento': { color: 'bg-blue-100 text-blue-800', text: 'Em Andamento' },
      'concluido': { color: 'bg-green-100 text-green-800', text: 'Concluído' },
      'arquivado': { color: 'bg-gray-100 text-gray-800', text: 'Arquivado' }
    };

    // Tratar status vazio ou inválido
    const normalizedStatus = status || 'pendente';
    const config = statusConfig[normalizedStatus] || { color: 'bg-gray-100 text-gray-800', text: normalizedStatus || 'Sem Status' };

    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.color}`}>
        {config.text}
      </span>
    );
  };

  const formatDate = (dateString) => {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const handleEditProcess = async (process) => {
    console.log('🔍 Editando processo:', process);
    console.log('📋 Serviços disponíveis:', services.length, services);

    // SEMPRE carregar serviços quando abrir modal (para debug)
    console.log('🔄 FORÇANDO carregamento de serviços...');
    try {
      const servicesResponse = await adminService.get('/api/services');
      const servicesData = servicesResponse?.data?.data || servicesResponse?.data || [];
      console.log('📋 Serviços carregados para modal:', servicesData.length, servicesData);
      setServices(servicesData);
    } catch (error) {
      console.error('❌ Erro ao carregar serviços:', error);
    }

    setEditingProcess({
      id: process.id,
      description: process.description || '',
      status: process.status || 'em_andamento',
      service_id: process.service_id || ''
    });
    setShowEditModal(true);
  };

  const handleSaveEdit = async () => {
    try {
      await adminService.put(`/api/admin/processes/${editingProcess.id}`, {
        description: editingProcess.description,
        status: editingProcess.status,
        service_id: editingProcess.service_id
      });
      setShowEditModal(false);
      setEditingProcess(null);
      fetchData();
    } catch (error) {
      console.error('Erro ao editar processo:', error);
      setError('Erro ao editar processo');
    }
  };

  const handleDeleteProcess = (process) => {
    setProcessToDelete(process);
    setShowDeleteModal(true);
  };

  const confirmDelete = async () => {
    try {
      await adminService.delete(`/api/admin/processes/${processToDelete.id}`);
      setShowDeleteModal(false);
      setProcessToDelete(null);
      fetchData();
    } catch (error) {
      console.error('Erro ao deletar processo:', error);
      setError('Erro ao deletar processo');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-red"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Gerenciamento de Processos</h1>
        <p className="text-gray-600">Visualize e gerencie todos os processos dos clientes</p>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* Filtros */}
      <div className="mb-6 bg-white p-4 rounded-lg shadow">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Cliente
            </label>
            <select
              value={filters.clientId}
              onChange={(e) => setFilters({...filters, clientId: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-red"
            >
              <option value="">Todos os clientes</option>
              {clients.map(client => (
                <option key={client.id} value={client.id}>
                  {client.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={filters.status}
              onChange={(e) => setFilters({...filters, status: e.target.value})}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-red"
            >
              <option value="">Todos os status</option>
              <option value="em_andamento">Em Andamento</option>
              <option value="parado_na_justica">Parado na Justiça</option>
              <option value="concluido">Concluído</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Buscar
            </label>
            <input
              type="text"
              value={filters.search}
              onChange={(e) => setFilters({...filters, search: e.target.value})}
              placeholder="Buscar por descrição..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-red"
            />
          </div>
        </div>
      </div>

      {/* Lista de Processos - Estilo Moderno */}
      <div className="modern-table-container">
        <div className="search-header">
          <input
            type="text"
            value={filters.search}
            onChange={(e) => setFilters({...filters, search: e.target.value})}
            placeholder="Buscar processo por nome, descrição ou email..."
            className="search-input-modern"
          />
        </div>

        <div className="table-wrapper">
          <table className="modern-data-table">
            <thead>
              <tr>
                <th>NOME</th>
                <th>DESCRIÇÃO</th>
                <th>TIPO DE SERVIÇO</th>
                <th>EMAIL</th>
                <th>STATUS</th>
                <th>DATA DE CADASTRO</th>
                <th>ÚLTIMO LOGIN</th>
                <th>AÇÕES</th>
              </tr>
            </thead>
            <tbody>
              {processes.length === 0 ? (
                <tr>
                  <td colSpan="8" className="no-data-row">
                    Nenhum processo encontrado
                  </td>
                </tr>
              ) : (
                processes.map((process) => (
                  <tr key={process.id}>
                    <td className="name-cell">
                      <div className="client-info">
                        <span className="client-name">
                          {process.client_name || 'Cliente não encontrado'}
                        </span>
                        <span className="client-username">
                          {process.client_username || `ID: ${process.client_id}`}
                        </span>
                      </div>
                    </td>
                    <td className="description-cell">
                      {process.description || 'Sem descrição'}
                    </td>
                    <td className="service-cell">
                      {process.service_name || 'Não informado'}
                    </td>
                    <td className="email-cell">
                      {process.client_email || 'Não informado'}
                    </td>
                    <td className="status-cell">
                      {getStatusBadge(process.status)}
                    </td>
                    <td className="date-cell">
                      {formatDate(process.created_at)}
                    </td>
                    <td className="date-cell">
                      {formatDate(process.updated_at) || 'Nunca'}
                    </td>
                    <td className="actions-cell">
                      <div className="action-buttons-modern">
                        <button
                          className="action-btn edit-btn"
                          onClick={() => handleEditProcess(process)}
                          title="Editar"
                        >
                          ✏️
                        </button>
                        <button
                          className="action-btn delete-btn"
                          onClick={() => handleDeleteProcess(process)}
                          title="Excluir"
                        >
                          🗑️
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Paginação */}
        {totalPages > 1 && (
          <div className="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200">
            <div className="flex-1 flex justify-between sm:hidden">
              <button
                onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                disabled={currentPage === 1}
                className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                Anterior
              </button>
              <button
                onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                disabled={currentPage === totalPages}
                className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
              >
                Próximo
              </button>
            </div>
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700">
                  Página <span className="font-medium">{currentPage}</span> de{' '}
                  <span className="font-medium">{totalPages}</span>
                </p>
              </div>
              <div>
                <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px">
                  <button
                    onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                    disabled={currentPage === 1}
                    className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                  >
                    Anterior
                  </button>
                  <button
                    onClick={() => setCurrentPage(Math.min(totalPages, currentPage + 1))}
                    disabled={currentPage === totalPages}
                    className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                  >
                    Próximo
                  </button>
                </nav>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Modal de Edição */}
      {showEditModal && (
        <div className="modal-overlay">
          <div className="modal-content" key={`edit-modal-${editingProcess?.id}-${Date.now()}`}>
            <h3>Editar Processo</h3>
            <div className="form-group">
              <label>Descrição:</label>
              <textarea
                value={editingProcess?.description || ''}
                onChange={(e) => setEditingProcess({...editingProcess, description: e.target.value})}
                rows="4"
                className="form-input"
              />
            </div>

            {/* DEBUG VISUAL */}
            <div style={{background: '#ffeb3b', padding: '10px', margin: '10px 0', border: '2px solid red'}}>
              <strong>🔍 DEBUG CAMPO TIPO DE SERVIÇO:</strong><br/>
              - Services length: {services.length}<br/>
              - Services data: {JSON.stringify(services.slice(0, 2))}<br/>
              - EditingProcess: {JSON.stringify(editingProcess)}<br/>
              - ShowEditModal: {showEditModal ? 'true' : 'false'}
            </div>

            <div className="form-group">
              <label>Tipo de Serviço:</label>
              <select
                value={editingProcess?.service_id || ''}
                onChange={(e) => setEditingProcess({...editingProcess, service_id: e.target.value})}
                className="form-select"
              >
                <option value="">Selecione um serviço</option>
                {services.length > 0 ? (
                  services.map(service => (
                    <option key={service.id} value={service.id}>
                      {service.name}
                    </option>
                  ))
                ) : (
                  <option value="" disabled>Carregando serviços...</option>
                )}
              </select>
              {/* Debug info */}
              <small style={{color: '#666', fontSize: '12px'}}>
                Debug: {services.length} serviços carregados
              </small>
            </div>
            <div className="form-group">
              <label>Status:</label>
              <select
                value={editingProcess?.status || ''}
                onChange={(e) => setEditingProcess({...editingProcess, status: e.target.value})}
                className="form-select"
              >
                <option value="pendente">Pendente</option>
                <option value="em_andamento">Em Andamento</option>
                <option value="concluido">Concluído</option>
                <option value="arquivado">Arquivado</option>
              </select>
            </div>
            <div className="modal-actions">
              <button onClick={() => setShowEditModal(false)} className="btn-cancel">
                Cancelar
              </button>
              <button onClick={handleSaveEdit} className="btn-save">
                Salvar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Confirmação de Exclusão */}
      {showDeleteModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h3>Confirmar Exclusão</h3>
            <p>Tem certeza que deseja excluir este processo?</p>
            <p><strong>Cliente:</strong> {processToDelete?.client_name}</p>
            <p><strong>Descrição:</strong> {processToDelete?.description}</p>
            <div className="modal-actions">
              <button onClick={() => setShowDeleteModal(false)} className="btn-cancel">
                Cancelar
              </button>
              <button onClick={confirmDelete} className="btn-delete">
                Excluir
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProcessManagement;
