import React, { useState, useEffect } from 'react';
import PageHeader from '../shared/PageHeader';
import Card from '../shared/Card';
import Button from '../shared/Button';
import DocumentUpload from './DocumentUpload';
import api from '../../services/api';

const MyCases = () => {
  console.log('🔍 MyCases component rendered!');

  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showUpload, setShowUpload] = useState(false);
  const [selectedCaseId, setSelectedCaseId] = useState(null);
  const [showDetails, setShowDetails] = useState(false);
  const [selectedCase, setSelectedCase] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log('🔍 MyCases useEffect triggered - calling fetchCases');
    fetchCases();
  }, []);

  const fetchCases = async () => {
    console.log('🚀 fetchCases called - starting API request');
    try {
      setLoading(true);
      setError(null);
      console.log('📡 Making API call to api.clientService.getCases()');
      const response = await api.clientService.getCases();
      console.log('✅ API response received:', response);
      console.log('📊 Response data:', response.data);
      setCases(response.data || []);
      console.log('✅ Cases set in state:', response.data || []);
    } catch (error) {
      console.error('❌ Erro ao carregar casos:', error);
      setError('Erro ao carregar casos. Tente novamente.');
      setCases([]);
    } finally {
      setLoading(false);
      console.log('🏁 fetchCases completed');
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      pendente: 'bg-yellow-100 text-yellow-800',
      em_andamento: 'bg-blue-100 text-blue-800',
      concluido: 'bg-green-100 text-green-800',
      arquivado: 'bg-gray-100 text-gray-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getStatusText = (status) => {
    const texts = {
      pendente: 'Pendente',
      em_andamento: 'Em Andamento',
      concluido: 'Concluído',
      arquivado: 'Arquivado'
    };
    return texts[status] || status;
  };

  const getStatusIcon = (status) => {
    const icons = {
      pendente: '⏳',
      em_andamento: '⚡',
      concluido: '✅',
      arquivado: '📁'
    };
    return icons[status] || '📄';
  };

  const handleViewDetails = (caseId) => {
    const caseData = cases.find(c => c.id === caseId);
    if (caseData) {
      setSelectedCase(caseData);
      setShowDetails(true);
    }
  };

  const handleUploadDocument = (caseId) => {
    setSelectedCaseId(caseId);
    setShowUpload(true);
  };

  const handleUploadSuccess = (uploadData) => {
    console.log('Upload realizado:', uploadData);
    setShowUpload(false);
    setSelectedCaseId(null);
  };

  const handleDownloadFile = async (fileId, filename) => {
    try {
      console.log(`🔽 Iniciando download do arquivo ID: ${fileId}`);
      await api.clientService.downloadFile(fileId);
      console.log(`✅ Download concluído: ${filename}`);
    } catch (error) {
      console.error('❌ Erro ao baixar arquivo:', error);
      alert('Erro ao baixar arquivo. Tente novamente.');
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <PageHeader 
          title="Meus Casos" 
          subtitle="Acompanhe o andamento dos seus processos jurídicos"
        />
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Meus Casos" 
        subtitle="Acompanhe o andamento dos seus processos jurídicos"
      />
      
      {cases.length === 0 ? (
        <Card className="text-center py-12">
          <div className="text-6xl mb-4">📋</div>
          <h3 className="text-xl font-bold text-white mb-2">Nenhum caso encontrado</h3>
          <p className="text-gray-300 mb-6">
            Você ainda não possui casos em andamento. Solicite um de nossos serviços para começar.
          </p>
          <Button variant="primary">
            Ver Serviços
          </Button>
        </Card>
      ) : (
        <div className="space-y-4">
          {cases.map((case_item) => (
            <Card key={case_item.id} className="p-6">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className="text-2xl">{getStatusIcon(case_item.status)}</span>
                    <h3 className="text-xl font-bold text-white">{case_item.title}</h3>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(case_item.status)}`}>
                      {getStatusText(case_item.status)}
                    </span>
                  </div>
                  
                  <p className="text-gray-300 mb-3">{case_item.description}</p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                    <div>
                      <span className="text-gray-400">Serviço:</span>
                      <p className="text-blue-400 font-medium">{case_item.service}</p>
                    </div>
                    <div>
                      <span className="text-gray-400">Criado em:</span>
                      <p className="text-white">{formatDate(case_item.created_at)}</p>
                    </div>
                    <div>
                      <span className="text-gray-400">Última atualização:</span>
                      <p className="text-white">{formatDate(case_item.updated_at)}</p>
                    </div>
                  </div>
                </div>
                
                <div className="ml-4 flex flex-col gap-2">
                  <Button
                    onClick={() => handleViewDetails(case_item.id)}
                    variant="outline"
                    size="sm"
                  >
                    Ver Detalhes
                  </Button>
                  <Button
                    onClick={() => handleUploadDocument(case_item.id)}
                    variant="primary"
                    size="sm"
                  >
                    📎 Enviar Documento
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
      
      <div className="mt-8 p-6 bg-blue-800/30 rounded-lg border border-blue-700">
        <h3 className="text-xl font-bold text-white mb-2">Dúvidas sobre seus casos?</h3>
        <p className="text-gray-300 mb-4">
          Nossa equipe está disponível para esclarecer qualquer dúvida sobre o andamento dos seus processos.
        </p>
        <Button variant="primary">
          Entrar em Contato
        </Button>
      </div>

      {/* Modal de Detalhes */}
      {showDetails && selectedCase && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-2xl font-bold text-white">
                  Detalhes do Caso
                </h3>
                <button
                  onClick={() => setShowDetails(false)}
                  className="text-gray-400 hover:text-white text-2xl"
                >
                  ×
                </button>
              </div>

              <div className="space-y-6">
                {/* Informações Básicas */}
                <div className="bg-gray-700 rounded-lg p-4">
                  <div className="flex items-center gap-3 mb-4">
                    <span className="text-3xl">{getStatusIcon(selectedCase.status)}</span>
                    <div>
                      <h4 className="text-xl font-bold text-white">{selectedCase.title}</h4>
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(selectedCase.status)}`}>
                        {getStatusText(selectedCase.status)}
                      </span>
                    </div>
                  </div>

                  <p className="text-gray-300 mb-4">{selectedCase.description}</p>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <span className="text-gray-400 text-sm">Serviço:</span>
                      <p className="text-blue-400 font-medium">{selectedCase.service}</p>
                    </div>
                    <div>
                      <span className="text-gray-400 text-sm">Data de Criação:</span>
                      <p className="text-white">{formatDate(selectedCase.created_at)}</p>
                    </div>
                    <div>
                      <span className="text-gray-400 text-sm">Última Atualização:</span>
                      <p className="text-white">{formatDate(selectedCase.updated_at)}</p>
                    </div>
                    <div>
                      <span className="text-gray-400 text-sm">ID do Caso:</span>
                      <p className="text-white">#{selectedCase.id}</p>
                    </div>
                  </div>
                </div>

                {/* Arquivos */}
                <div className="bg-gray-700 rounded-lg p-4">
                  <h5 className="text-lg font-bold text-white mb-4">📎 Documentos</h5>
                  {selectedCase.files && selectedCase.files.length > 0 ? (
                    <div className="space-y-2">
                      {selectedCase.files.map((file, index) => (
                        <div key={index} className="flex items-center justify-between p-3 bg-gray-600 rounded">
                          <div className="flex items-center gap-3">
                            <span className="text-blue-400">📄</span>
                            <div>
                              <p className="text-white font-medium">{file.original_filename || `Documento ${index + 1}`}</p>
                              <p className="text-gray-400 text-sm">
                                Enviado em: {file.created_at ? formatDate(file.created_at) : 'Data não disponível'}
                              </p>
                            </div>
                          </div>
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleDownloadFile(file.id, file.original_filename)}
                          >
                            📥 Download
                          </Button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-400 text-center py-4">
                      Nenhum documento enviado ainda.
                    </p>
                  )}

                  <div className="mt-4 pt-4 border-t border-gray-600">
                    <Button
                      onClick={() => {
                        setShowDetails(false);
                        handleUploadDocument(selectedCase.id);
                      }}
                      variant="primary"
                      className="w-full"
                    >
                      📎 Enviar Novo Documento
                    </Button>
                  </div>
                </div>

                {/* Ações */}
                <div className="flex gap-3">
                  <Button
                    onClick={() => setShowDetails(false)}
                    variant="outline"
                    className="flex-1"
                  >
                    Fechar
                  </Button>
                  <Button
                    onClick={() => {
                      setShowDetails(false);
                      handleUploadDocument(selectedCase.id);
                    }}
                    variant="primary"
                    className="flex-1"
                  >
                    📎 Enviar Documento
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Upload */}
      {showUpload && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold text-white">
                  Enviar Documento - Caso #{selectedCaseId}
                </h3>
                <button
                  onClick={() => setShowUpload(false)}
                  className="text-gray-400 hover:text-white text-2xl"
                >
                  ×
                </button>
              </div>
              <DocumentUpload
                caseId={selectedCaseId}
                onUploadSuccess={handleUploadSuccess}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MyCases;
