// src/components/student/Catalog.js
import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, faHeart, faPlus } from '@fortawesome/free-solid-svg-icons';
import { classService, favoritesService } from '../../services/api';
import VideoPlayer from '../shared/VideoPlayer';

const Catalog = () => {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedClass, setSelectedClass] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [favorites, setFavorites] = useState(new Set());
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        // Buscar aulas e favoritos em paralelo
        const [classesData, favoritesData] = await Promise.all([
          classService.getAll(),
          favoritesService.getAll().catch(() => []) // Se falhar, retorna array vazio
        ]);

        setClasses(classesData);

        // Criar Set com IDs dos favoritos para busca rápida
        const favoriteIds = new Set(favoritesData.map(fav => fav.id));
        setFavorites(favoriteIds);

      } catch (e) {
        console.error("Erro ao buscar dados:", e);
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleViewDetails = async (classId) => {
    try {
      const data = await classService.getById(classId);
      setSelectedClass(data);
      setIsModalOpen(true);
    } catch (e) {
      console.error("Erro ao buscar detalhes da aula:", e);
      setError("Não foi possível carregar os detalhes da aula. " + e.message);
      setSelectedClass(null);
      setIsModalOpen(false);
    }
  };

  const handleToggleFavorite = async (classId) => {
    try {
      if (favorites.has(classId)) {
        await favoritesService.remove(classId);
        setFavorites(prev => {
          const newSet = new Set(prev);
          newSet.delete(classId);
          return newSet;
        });
      } else {
        await favoritesService.add(classId);
        setFavorites(prev => new Set([...prev, classId]));
      }
    } catch (e) {
      console.error("Erro ao atualizar favoritos:", e);
      setError("Erro ao atualizar favoritos: " + e.message);
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedClass(null);
  };

  // Filtrar aulas baseado na busca e categoria
  const filteredClasses = classes.filter(cls => {
    const matchesSearch = cls.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         cls.instructor.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = categoryFilter === 'all' || cls.category === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  const categories = ['all', 'preflop', 'postflop', 'mental', 'torneos', 'cash'];

  const getCategoryDisplayName = (category) => {
    const categoryNames = {
      'all': 'Todas as Categorias',
      'preflop': 'Pré-Flop',
      'postflop': 'Pós-Flop',
      'mental': 'Mental Game',
      'torneos': 'Torneios',
      'cash': 'Cash Game'
    };
    return categoryNames[category] || category;
  };

  if (loading) {
    return <div className="p-6 text-white">Carregando catálogo de aulas...</div>;
  }

  // Exibe erro principal se houver, ou erro específico de modal se aplicável
  if (error && !isModalOpen) { // Só mostra erro principal se o modal não estiver tentando exibir algo
    return <div className="p-6 text-red-500">Erro ao carregar aulas: {error}</div>;
  }

  return (
    <div className="p-6 text-white min-h-screen">
      <h2 className="text-3xl font-bold mb-8 text-red-400">Catálogo de Aulas</h2>

      {/* Filtros */}
      <div className="mb-6 space-y-4">
        <div className="flex flex-col md:flex-row gap-4">
          <input
            type="text"
            placeholder="Buscar por nome da aula ou instrutor..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 bg-gray-500 text-white px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-300 placeholder-gray-300"
          />
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="bg-gray-500 text-white px-4 py-2 rounded focus:outline-none focus:ring-2 focus:ring-red-300"
          >
            {categories.map(category => (
              <option key={category} value={category}>
                {getCategoryDisplayName(category)}
              </option>
            ))}
          </select>
        </div>
      </div>

      {filteredClasses.length === 0 && !loading ? (
        <p className="text-gray-400">
          {searchTerm || categoryFilter !== 'all'
            ? 'Nenhuma aula encontrada com os filtros aplicados.'
            : 'Nenhuma aula disponível no momento.'}
        </p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredClasses.map(cls => (
            <div key={cls.id} className="bg-gray-700 p-4 rounded-lg shadow-md transform hover:bg-gray-600 transition-all duration-200 hover:scale-105 flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-semibold text-white truncate flex-1" title={cls.name}>{cls.name}</h3>
                  <button
                    onClick={() => handleToggleFavorite(cls.id)}
                    className={`ml-2 p-1 rounded transition-colors ${
                      favorites.has(cls.id)
                        ? 'text-red-500 hover:text-red-400'
                        : 'text-gray-400 hover:text-red-500'
                    }`}
                    title={favorites.has(cls.id) ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}
                  >
                    <FontAwesomeIcon icon={faHeart} />
                  </button>
                </div>
                <p className="text-sm text-gray-400 mb-1">Instrutor: {cls.instructor}</p>
                <p className="text-sm text-gray-400 mb-1">Categoria: {getCategoryDisplayName(cls.category)}</p>
                <p className="text-sm text-gray-400 mb-3">Data: {new Date(cls.date).toLocaleDateString()}</p>
              </div>
              <button
                onClick={() => handleViewDetails(cls.id)}
                className="w-full bg-red-400 hover:bg-red-500 text-white py-2 px-4 rounded transition-colors mt-2"
              >
                Ver Detalhes
              </button>
            </div>
          ))}
        </div>
      )}

      {isModalOpen && selectedClass && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <div className="bg-gray-800 p-6 rounded-lg w-full max-w-2xl shadow-xl transform transition-all relative">
            <button 
              onClick={closeModal} 
              className="absolute top-3 right-3 text-gray-400 hover:text-white transition-colors"
              aria-label="Fechar modal"
            >
              <FontAwesomeIcon icon={faTimes} size="lg" />
            </button>
            <h3 className="text-2xl font-semibold mb-4 text-red-400">{selectedClass.name}</h3>
            <p className="text-gray-300 mb-1"><span className="font-semibold">Instrutor:</span> {selectedClass.instructor}</p>
            <p className="text-gray-300 mb-1"><span className="font-semibold">Categoria:</span> {getCategoryDisplayName(selectedClass.category)}</p>
            <p className="text-gray-300 mb-3"><span className="font-semibold">Data:</span> {new Date(selectedClass.date).toLocaleDateString()}</p>

            {/* Player de vídeo com registro de visualização */}
            <VideoPlayer
              classData={selectedClass}
              onViewRegistered={(totalViews) => {
                console.log(`Visualização registrada. Total: ${totalViews}`);
                // Atualizar contador de views localmente
                setSelectedClass(prev => ({
                  ...prev,
                  views: totalViews
                }));
                // Atualizar também na lista principal
                setClasses(prev => prev.map(cls =>
                  cls.id === selectedClass.id
                    ? { ...cls, views: totalViews }
                    : cls
                ));
              }}
            />
            
            {/* Adicionar mais detalhes da aula aqui se necessário, como descrição, etc. */}
            
            <div className="mt-6 flex justify-end">
              <button 
                onClick={closeModal} 
                className="bg-gray-600 hover:bg-gray-500 text-gray-200 font-bold py-2 px-4 rounded transition-colors duration-150"
              >
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}
      {/* Exibe erro específico do modal, se houver, e o modal estiver fechado */}
      {error && selectedClass === null && !isModalOpen && (
         <div className="p-6 text-red-500">Erro ao carregar detalhes da aula: {error}</div>
      )}
    </div>
  );
};

export default Catalog;

