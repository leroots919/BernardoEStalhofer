import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner, faChartBar, faUsers, faVideo, faTrophy } from '@fortawesome/free-solid-svg-icons';
import { analyticsService } from '../../services/api';
import PageHeader from '../shared/PageHeader';
import Card from '../shared/Card';

const Analytics = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Carregar estatísticas ao montar o componente
  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const data = await analyticsService.getStats();
        setAnalyticsData(data);
      } catch (err) {
        console.error('Erro ao carregar estatísticas:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <>
        <PageHeader
          title="Painel de Analytics"
          subtitle="Estatísticas e métricas do sistema"
          icon={faChartBar}
        />
        <Card>
          <div className="flex justify-center items-center py-12">
            <FontAwesomeIcon icon={faSpinner} spin size="3x" className="text-red-400" />
            <span className="ml-4 text-xl text-white">Carregando estatísticas...</span>
          </div>
        </Card>
      </>
    );
  }

  if (error) {
    return (
      <>
        <PageHeader
          title="Painel de Analytics"
          subtitle="Estatísticas e métricas do sistema"
          icon={faChartBar}
        />
        <Card>
          <div className="bg-red-900 bg-opacity-50 border border-red-600 p-4 rounded-modern">
            <p className="text-red-400">❌ Erro ao carregar estatísticas: {error}</p>
          </div>
        </Card>
      </>
    );
  }
  return (
    <>
      <PageHeader
        title="Painel de Analytics"
        subtitle="Estatísticas e métricas do sistema"
        icon={faChartBar}
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {/* Card Total de Alunos */}
        <Card hover className="group">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Total de Alunos</h3>
              <p className="text-4xl font-bold text-red-400">{analyticsData.total_students}</p>
              <p className="text-sm text-gray-300 mt-1">Estudantes cadastrados</p>
            </div>
            <div className="bg-red-400 bg-opacity-20 p-4 rounded-modern group-hover:bg-opacity-30 transition-all duration-200">
              <FontAwesomeIcon icon={faUsers} className="w-8 h-8 text-red-400" />
            </div>
          </div>
        </Card>

        {/* Card Total de Aulas */}
        <Card hover className="group">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-white mb-2">Total de Aulas</h3>
              <p className="text-4xl font-bold text-blue-300">{analyticsData.total_classes}</p>
              <p className="text-sm text-gray-300 mt-1">Aulas disponíveis</p>
            </div>
            <div className="bg-blue-300 bg-opacity-20 p-4 rounded-modern group-hover:bg-opacity-30 transition-all duration-200">
              <FontAwesomeIcon icon={faVideo} className="w-8 h-8 text-blue-300" />
            </div>
          </div>
        </Card>

        {/* Card Aula Mais Visualizada */}
        <Card hover className="group">
          <div className="flex items-center justify-between">
            <div className="flex-1 min-w-0">
              <h3 className="text-lg font-semibold text-white mb-2">Aula Mais Visualizada</h3>
              <p className="text-lg font-bold text-yellow-300 truncate" title={analyticsData.most_popular_class}>
                {analyticsData.most_popular_class}
              </p>
              <p className="text-sm text-gray-300 mt-1">{analyticsData.most_popular_class_views} visualizações</p>
            </div>
            <div className="bg-yellow-300 bg-opacity-20 p-4 rounded-modern group-hover:bg-opacity-30 transition-all duration-200 ml-4">
              <FontAwesomeIcon icon={faTrophy} className="w-8 h-8 text-yellow-300" />
            </div>
          </div>
        </Card>
      </div>

      {/* Informação adicional */}
      <Card className="text-center">
        <p className="text-sm text-gray-300">
          📊 Dados atualizados em tempo real do banco de dados
        </p>
      </Card>
    </>
  );
};

export default Analytics;
