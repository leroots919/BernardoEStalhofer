// src/components/client/ClientCases.js
import React, { useState, useEffect } from 'react';
import { FileText, Download, Clock, CheckCircle, AlertCircle, BarChart3 } from 'lucide-react';
import api from '../../services/api';

const ClientCases = () => {
  const [cases, setCases] = useState([]);
  const [stats, setStats] = useState({
    total_cases: 0,
    pending_cases: 0,
    active_cases: 0,
    completed_cases: 0,
    total_files: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      console.log('🔍 Iniciando busca de dados...');

      const [casesResponse, statsResponse] = await Promise.all([
        api.get('/api/client/cases'),
        api.get('/api/client/stats')
      ]);

      console.log('✅ Dados recebidos:', { casesResponse, statsResponse });
      setCases(casesResponse.data || casesResponse);
      setStats(statsResponse.data || statsResponse);
    } catch (error) {
      console.error('❌ Erro ao carregar dados:', error);
      // Definir dados padrão em caso de erro
      setCases([]);
      setStats({
        total_cases: 0,
        pending_cases: 0,
        active_cases: 0,
        completed_cases: 0,
        total_files: 0
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (fileId, filename) => {
    try {
      const response = await api.get(`/api/client/files/${fileId}/download`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Erro ao fazer download:', error);
      alert('Erro ao fazer download do arquivo');
    }
  };

  const getStatusBadge = (status) => {
    if (!status) return null;

    const statusConfig = {
      'pendente': {
        color: 'bg-yellow-500',
        text: 'Pendente',
        icon: AlertCircle
      },
      'em_andamento': {
        color: 'bg-blue-500',
        text: 'Em Andamento',
        icon: Clock
      },
      'parado_na_justica': {
        color: 'bg-orange-500',
        text: 'Parado na Justiça',
        icon: AlertCircle
      },
      'concluido': {
        color: 'bg-green-500',
        text: 'Concluído',
        icon: CheckCircle
      }
    };

    const config = statusConfig[status] || {
      color: 'bg-gray-500',
      text: status || 'Desconhecido',
      icon: AlertCircle
    };

    const Icon = config.icon;

    return (
      <span className={`px-3 py-1 rounded-full text-xs text-white ${config.color} flex items-center gap-1`}>
        <Icon className="h-3 w-3" />
        {config.text}
      </span>
    );
  };

  const StatCard = ({ icon: Icon, title, value, color }) => (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-400 text-sm font-medium">{title}</p>
          <p className={`text-xl font-bold ${color}`}>{value}</p>
        </div>
        <Icon className={`h-6 w-6 ${color}`} />
      </div>
    </div>
  );

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
        <h1 className="text-3xl font-bold text-white">Meus Processos</h1>
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
        <StatCard
          icon={FileText}
          title="Total de Processos"
          value={stats.total_cases}
          color="text-blue-400"
        />
        <StatCard
          icon={AlertCircle}
          title="Pendentes"
          value={stats.pending_cases}
          color="text-yellow-400"
        />
        <StatCard
          icon={Clock}
          title="Em Andamento"
          value={stats.active_cases}
          color="text-blue-400"
        />
        <StatCard
          icon={CheckCircle}
          title="Concluídos"
          value={stats.completed_cases}
          color="text-green-400"
        />
        <StatCard
          icon={BarChart3}
          title="Arquivos"
          value={stats.total_files}
          color="text-purple-400"
        />
      </div>

      {/* Lista de Processos */}
      <div className="space-y-4">
        {!Array.isArray(cases) || cases.length === 0 ? (
          <div className="bg-gray-800 rounded-lg border border-gray-700 p-8 text-center">
            <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-white mb-2">Nenhum processo encontrado</h3>
            <p className="text-gray-400">Você ainda não possui processos cadastrados.</p>
          </div>
        ) : (
          cases.map((case_) => {
            if (!case_ || !case_.id) return null;

            return (
              <div key={case_.id} className="bg-gray-800 rounded-lg border border-gray-700 p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-semibold text-white mb-2">{case_.title || 'Título não informado'}</h3>
                    {case_.description && (
                      <p className="text-gray-400 mb-3">{case_.description}</p>
                    )}
                    <div className="flex items-center gap-4 text-sm text-gray-400">
                      <span>Criado em: {case_.created_at ? new Date(case_.created_at).toLocaleDateString('pt-BR') : 'N/A'}</span>
                      <span>Atualizado em: {case_.updated_at ? new Date(case_.updated_at).toLocaleDateString('pt-BR') : 'N/A'}</span>
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-2">
                    {getStatusBadge(case_.status)}
                  </div>
                </div>

                {/* Arquivos do Processo */}
                {Array.isArray(case_.files) && case_.files.length > 0 && (
                  <div className="border-t border-gray-700 pt-4">
                    <h4 className="text-lg font-medium text-white mb-3">Arquivos do Processo</h4>
                    <div className="space-y-2">
                      {case_.files.map((file) => {
                        if (!file || !file.id) return null;

                        return (
                          <div key={file.id} className="flex items-center justify-between p-3 bg-gray-700 rounded-lg">
                            <div className="flex items-center">
                              <FileText className="h-5 w-5 text-blue-400 mr-3" />
                              <div>
                                <div className="text-white font-medium">{file.original_filename || 'Arquivo sem nome'}</div>
                                {file.description && (
                                  <div className="text-sm text-gray-400">{file.description}</div>
                                )}
                                <div className="text-xs text-gray-500">
                                  Enviado em: {file.created_at ? new Date(file.created_at).toLocaleDateString('pt-BR') : 'N/A'}
                                </div>
                              </div>
                            </div>
                            <button
                              onClick={() => handleDownload(file.id, file.original_filename)}
                              className="text-blue-400 hover:text-blue-300 p-2 rounded-lg hover:bg-gray-600"
                              title="Fazer download"
                            >
                              <Download className="h-4 w-4" />
                            </button>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default ClientCases;
