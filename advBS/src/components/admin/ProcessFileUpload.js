// src/components/admin/ProcessFileUpload.js
import React, { useState, useEffect } from 'react';
import { Upload, FileText, Download, Trash2, User } from 'lucide-react';
import api from '../../services/api';

const ProcessFileUpload = () => {
  const [clients, setClients] = useState([]);
  const [cases, setCases] = useState([]);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [searchingClients, setSearchingClients] = useState(false);
  const [clientSearch, setClientSearch] = useState('');
  const [selectedClient, setSelectedClient] = useState(null);
  const [clientsCache, setClientsCache] = useState({}); // Cache para nomes de clientes
  const [formData, setFormData] = useState({
    client_id: '',
    case_id: '',
    description: '',
    file: null
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      // Só carrega arquivos inicialmente, não todos os clientes
      const response = await api.get('/api/admin/process-files');
      console.log('📁 Resposta dos arquivos:', response);

      // A API retorna { data: [...] }, então precisamos acessar response.data
      const filesData = response.data || [];
      console.log('📁 Arquivos carregados:', filesData);

      setUploadedFiles(filesData);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      setUploadedFiles([]);
    } finally {
      setLoading(false);
    }
  };

  // Nova função para buscar clientes dinamicamente
  const searchClients = async (searchTerm) => {
    if (!searchTerm || searchTerm.length < 2) {
      setClients([]);
      return;
    }

    try {
      setSearchingClients(true);
      // Implementar busca com limite
      const response = await api.get(`/api/admin/clients/search?q=${encodeURIComponent(searchTerm)}&limit=10`);
      console.log('🔍 Resposta da busca de clientes:', response);

      // A API retorna { data: [...] }, então precisamos acessar response.data
      const clientsData = response.data || [];
      console.log('👥 Clientes encontrados:', clientsData);

      setClients(clientsData);
    } catch (error) {
      console.error('Erro ao buscar clientes:', error);
      setClients([]);
    } finally {
      setSearchingClients(false);
    }
  };

  // Buscar casos do cliente selecionado
  const fetchClientCases = async (clientId) => {
    try {
      const response = await api.get(`/api/admin/clients/${clientId}/cases`);
      console.log('📋 Resposta dos casos:', response);

      // A API retorna { data: [...] }, então precisamos acessar response.data
      const casesData = response.data || [];
      console.log('📋 Casos carregados:', casesData);

      setCases(casesData);
    } catch (error) {
      console.error('Erro ao buscar casos do cliente:', error);
      setCases([]);
    }
  };

  // Handler para mudança na busca de cliente
  const handleClientSearchChange = (e) => {
    const value = e.target.value;
    setClientSearch(value);
    searchClients(value);
  };

  // Handler para seleção de cliente
  const handleClientSelect = (client) => {
    setSelectedClient(client);
    setFormData({ ...formData, client_id: client.id, case_id: '' });
    setClientSearch(client.name);
    setClients([]); // Limpa a lista de busca
    fetchClientCases(client.id); // Carrega casos do cliente
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();

    console.log('🚀 Iniciando upload...', {
      client_id: formData.client_id,
      case_id: formData.case_id,
      file: formData.file?.name,
      description: formData.description
    });

    // Validações específicas
    if (!formData.client_id) {
      alert('Por favor, selecione um cliente da lista de busca');
      return;
    }

    if (!formData.file) {
      alert('Por favor, selecione um arquivo para enviar');
      return;
    }

    try {
      setUploading(true);
      const uploadFormData = new FormData();
      uploadFormData.append('file', formData.file);
      uploadFormData.append('client_id', formData.client_id);
      uploadFormData.append('case_id', formData.case_id || '');
      uploadFormData.append('description', formData.description || '');

      console.log('📤 Enviando dados:', {
        file: formData.file.name,
        client_id: formData.client_id,
        case_id: formData.case_id || 'vazio',
        description: formData.description || 'vazio'
      });

      // Upload usando fetch diretamente para multipart/form-data
      const token = localStorage.getItem('advbs_token');
      console.log('🔑 Token:', token ? 'presente' : 'ausente');

      const response = await fetch('http://localhost:8000/api/admin/process-files', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: uploadFormData
      });

      console.log('📥 Resposta:', response.status, response.statusText);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ Erro na resposta:', errorText);
        throw new Error(`Erro no upload: ${response.status} - ${errorText}`);
      }

      const result = await response.json();
      console.log('✅ Upload bem-sucedido:', result);

      alert('Arquivo enviado com sucesso!');

      // Reset form
      setFormData({
        client_id: '',
        case_id: '',
        description: '',
        file: null
      });
      setSelectedClient(null);
      setClientSearch('');
      setCases([]);

      // Refresh files list
      fetchData();
    } catch (error) {
      console.error('❌ Erro ao enviar arquivo:', error);
      alert(`Erro ao enviar arquivo: ${error.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteFile = async (fileId) => {
    if (window.confirm('Tem certeza que deseja excluir este arquivo?')) {
      try {
        await api.delete(`/api/admin/process-files/${fileId}`);
        fetchData();
      } catch (error) {
        console.error('Erro ao excluir arquivo:', error);
      }
    }
  };

  const handleDownloadFile = async (fileId, filename) => {
    try {
      console.log(`🔽 Iniciando download do arquivo ID: ${fileId}`);

      const token = sessionStorage.getItem('advbs_token');
      const response = await fetch(`http://localhost:5000/api/admin/process-files/${fileId}/download`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      console.log(`📥 Resposta do download: ${response.status}`);

      if (!response.ok) {
        throw new Error(`Erro no download: ${response.status}`);
      }

      // Converter resposta para blob
      const blob = await response.blob();
      console.log(`📦 Blob criado, tamanho: ${blob.size} bytes`);

      // Criar URL temporária e fazer download
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();

      // Limpar
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      console.log(`✅ Download concluído: ${filename}`);

    } catch (error) {
      console.error('❌ Erro ao fazer download:', error);
      alert(`Erro ao fazer download: ${error.message}`);
    }
  };

  // Buscar nome do cliente por ID (com cache)
  const fetchClientName = async (clientId) => {
    if (clientsCache[clientId]) {
      return clientsCache[clientId];
    }

    try {
      const response = await api.get(`/api/admin/clients/${clientId}`);
      console.log('👤 Resposta do cliente:', response);

      // A API retorna { data: {...} }, então precisamos acessar response.data
      const clientData = response.data || {};
      const clientName = clientData.name || 'Nome não informado';

      setClientsCache(prev => ({ ...prev, [clientId]: clientName }));
      return clientName;
    } catch (error) {
      console.error('Erro ao buscar cliente:', error);
      return 'Cliente não encontrado';
    }
  };

  const getClientName = (clientId) => {
    if (clientsCache[clientId]) {
      return clientsCache[clientId];
    }

    // Se não está no cache, buscar e retornar placeholder temporário
    fetchClientName(clientId);
    return `Carregando...`;
  };

  const getCaseTitle = (caseId) => {
    if (!cases || !Array.isArray(cases) || !caseId) return 'Caso geral';
    const case_ = cases.find(c => c && c.id === caseId);
    return case_ ? (case_.title || 'Título não informado') : 'Caso geral';
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'pendente': { color: 'bg-yellow-500', text: 'Pendente' },
      'em_andamento': { color: 'bg-blue-500', text: 'Em Andamento' },
      'parado_na_justica': { color: 'bg-orange-500', text: 'Parado na Justiça' },
      'concluido': { color: 'bg-green-500', text: 'Concluído' }
    };
    
    const config = statusConfig[status] || { color: 'bg-gray-500', text: status };
    return (
      <span className={`px-2 py-1 rounded-full text-xs text-white ${config.color}`}>
        {config.text}
      </span>
    );
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
        <h1 className="text-3xl font-bold text-white">Upload de Arquivos de Processo</h1>
      </div>

      {/* Formulário de Upload */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <h2 className="text-xl font-semibold text-white mb-4">Enviar Novo Arquivo</h2>
        <form onSubmit={handleFileUpload} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="relative">
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Cliente *
              </label>
              <input
                type="text"
                value={clientSearch}
                onChange={handleClientSearchChange}
                placeholder={selectedClient ? "Cliente selecionado" : "Digite o nome ou email do cliente..."}
                disabled={selectedClient}
                className={`w-full px-3 py-2 border rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                  selectedClient
                    ? 'bg-green-700 border-green-600 cursor-not-allowed'
                    : 'bg-gray-700 border-gray-600'
                }`}
              />

              {/* Campo hidden para validação */}
              <input
                type="hidden"
                required
                value={formData.client_id}
                onChange={() => {}} // Não faz nada, só para validação
              />

              {/* Lista de resultados da busca */}
              {clients.length > 0 && (
                <div className="absolute z-10 w-full mt-1 bg-gray-700 border border-gray-600 rounded-lg shadow-lg max-h-60 overflow-y-auto">
                  {clients.map((client) => (
                    <div
                      key={client.id}
                      onClick={() => handleClientSelect(client)}
                      className="px-3 py-2 hover:bg-gray-600 cursor-pointer text-white border-b border-gray-600 last:border-b-0"
                    >
                      <div className="font-medium">{client.name}</div>
                      <div className="text-sm text-gray-400">{client.email}</div>
                    </div>
                  ))}
                </div>
              )}

              {/* Indicador de busca */}
              {searchingClients && (
                <div className="absolute right-3 top-9 text-gray-400">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500"></div>
                </div>
              )}

              {/* Cliente selecionado */}
              {selectedClient && (
                <div className="mt-2 p-2 bg-green-900 rounded border border-green-700 flex justify-between items-center">
                  <div className="text-sm text-green-200">
                    <strong>✓ Cliente selecionado:</strong> {selectedClient.name} - {selectedClient.email}
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      setSelectedClient(null);
                      setFormData({ ...formData, client_id: '', case_id: '' });
                      setClientSearch('');
                      setCases([]);
                    }}
                    className="text-green-300 hover:text-green-100 text-sm underline"
                  >
                    Alterar
                  </button>
                </div>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-1">
                Caso (Opcional)
              </label>
              <select
                value={formData.case_id}
                onChange={(e) => setFormData({ ...formData, case_id: e.target.value })}
                disabled={!selectedClient}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              >
                <option value="">
                  {selectedClient ? 'Caso geral' : 'Selecione um cliente primeiro'}
                </option>
                {cases && Array.isArray(cases) && cases.map((case_) => (
                  <option key={case_.id} value={case_.id}>
                    {case_.title || 'Título não informado'}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">
              Descrição
            </label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Descreva o conteúdo do arquivo..."
              rows={3}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">
              Arquivo *
            </label>
            <input
              type="file"
              required
              onChange={(e) => {
                console.log('📁 Arquivo selecionado:', e.target.files[0]);
                setFormData({ ...formData, file: e.target.files[0] });
              }}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <button
            type="submit"
            disabled={uploading}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-800 text-white px-6 py-2 rounded-lg flex items-center gap-2"
          >
            <Upload className="h-4 w-4" />
            {uploading ? 'Enviando...' : 'Enviar Arquivo'}
          </button>
        </form>
      </div>

      {/* Lista de Arquivos */}
      <div className="bg-gray-800 rounded-lg border border-gray-700">
        <div className="p-6 border-b border-gray-700">
          <h2 className="text-xl font-semibold text-white">Arquivos Enviados</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Arquivo
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Cliente
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Caso
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Data
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-700">
              {uploadedFiles && Array.isArray(uploadedFiles) && uploadedFiles.length > 0 ? (
                uploadedFiles.map((file) => {
                  if (!file) return null;

                  return (
                    <tr key={file.id} className="hover:bg-gray-700">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center">
                          <FileText className="h-5 w-5 text-blue-400 mr-3" />
                          <div>
                            <div className="text-sm font-medium text-white">
                              {file.original_filename || 'Nome do arquivo não disponível'}
                            </div>
                            {file.description && (
                              <div className="text-sm text-gray-400">{file.description}</div>
                            )}
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        <div className="flex items-center">
                          <User className="h-4 w-4 mr-2" />
                          {getClientName(file.user_id)}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {getCaseTitle(file.case_id)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">
                        {file.created_at ? new Date(file.created_at).toLocaleDateString('pt-BR') : '-'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        <div className="flex space-x-2">
                          <button
                            onClick={() => handleDownloadFile(file.id, file.original_filename)}
                            className="text-blue-400 hover:text-blue-300"
                            title="Fazer download do arquivo"
                          >
                            <Download className="h-4 w-4" />
                          </button>
                          <button
                            onClick={() => handleDeleteFile(file.id)}
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
                  <td colSpan="5" className="px-6 py-4 text-center text-gray-400">
                    {loading ? 'Carregando arquivos...' : 'Nenhum arquivo encontrado'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ProcessFileUpload;
