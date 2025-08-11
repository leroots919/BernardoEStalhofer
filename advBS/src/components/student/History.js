import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner, faPlay, faRedo } from '@fortawesome/free-solid-svg-icons';
import { classService } from '../../services/api';

const History = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Buscar histórico de aulas
  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await classService.getHistory();
      setHistory(data);
    } catch (e) {
      console.error("Erro ao buscar histórico:", e);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  // Função para formatar data
  const formatLastWatched = (dateString) => {
    if (!dateString) return 'Nunca';

    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) return 'Ontem';
    if (diffDays <= 7) return `Há ${diffDays} dias`;
    if (diffDays <= 30) return `Há ${Math.ceil(diffDays / 7)} semanas`;
    return `Há ${Math.ceil(diffDays / 30)} meses`;
  };

  // Função para obter cor da categoria
  const getCategoryColor = (category) => {
    const colors = {
      'preflop': '#FF6B6B',
      'postflop': '#4ECDC4',
      'mental': '#45B7D1',
      'torneos': '#96CEB4',
      'cash': '#FFEAA7'
    };
    return colors[category] || '#6C5CE7';
  };

  if (loading) {
    return (
      <div className="p-6 text-white min-h-screen flex justify-center items-center">
        <FontAwesomeIcon icon={faSpinner} spin size="3x" />
        <span className="ml-4 text-xl">Carregando histórico...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-white min-h-screen">
        <h2 className="text-3xl font-bold mb-8 text-red-400">Meu Histórico de Aulas</h2>
        <div className="text-red-500 text-center">
          <p>Erro ao carregar histórico: {error}</p>
          <button
            onClick={fetchHistory}
            className="mt-4 bg-red-400 hover:bg-red-500 text-white py-2 px-4 rounded transition-colors"
          >
            Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 text-white min-h-screen">
      <h2 className="text-3xl font-bold mb-8 text-red-400">Meu Histórico de Aulas</h2>

      {history.length === 0 ? (
        <div className="text-center text-gray-400 py-12">
          <FontAwesomeIcon icon={faPlay} size="3x" className="mb-4 opacity-50" />
          <p className="text-xl">Você ainda não assistiu nenhuma aula.</p>
          <p className="text-sm mt-2">Comece explorando nosso catálogo de aulas!</p>
        </div>
      ) : (
        <div className="space-y-4">
          {history.map(item => (
            <div key={item.id} className="bg-gray-700 p-4 rounded-lg shadow-md flex items-center gap-4 transform hover:bg-gray-600 transition-colors duration-200">
              {/* Thumbnail com cor da categoria */}
              <div
                className="w-32 h-20 rounded flex items-center justify-center text-white font-bold text-sm"
                style={{ backgroundColor: getCategoryColor(item.category) }}
              >
                {item.category?.toUpperCase() || 'AULA'}
              </div>

              <div className="flex-1">
                <h3 className="text-lg font-semibold text-white truncate" title={item.name}>
                  {item.name}
                </h3>
                <p className="text-sm text-gray-400">
                  Instrutor: {item.instructor}
                </p>
                <p className="text-sm text-gray-400">
                  Última vez assistido: {formatLastWatched(item.last_watched)}
                </p>
                <div className="w-full bg-gray-600 rounded-full h-2.5 mt-2">
                  <div
                    className="bg-red-400 h-2.5 rounded-full transition-all duration-300"
                    style={{ width: `${item.progress}%` }}
                    aria-valuenow={item.progress}
                    aria-valuemin="0"
                    aria-valuemax="100"
                  ></div>
                </div>
                <p className="text-xs text-gray-400 mt-1">{item.progress}% completo</p>
              </div>

              <button className="bg-red-400 hover:bg-red-500 text-white py-2 px-4 rounded transition-colors text-sm whitespace-nowrap flex items-center gap-2">
                <FontAwesomeIcon icon={item.progress === 100 ? faRedo : faPlay} />
                {item.progress === 100 ? 'Rever Aula' : 'Continuar'}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;
