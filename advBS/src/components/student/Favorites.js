// src/components/student/Favorites.js
import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, faHeart } from '@fortawesome/free-solid-svg-icons';
import { favoritesService, classService } from '../../services/api';

const Favorites = () => {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedClass, setSelectedClass] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    const fetchFavorites = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await favoritesService.getAll();
        setFavorites(data);
      } catch (e) {
        console.error("Erro ao buscar favoritos:", e);
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchFavorites();
  }, []);

  const handleViewDetails = async (classId) => {
    try {
      const data = await classService.getById(classId);
      setSelectedClass(data);
      setIsModalOpen(true);
    } catch (e) {
      console.error("Erro ao buscar detalhes da aula:", e);
      setError("Não foi possível carregar os detalhes da aula. " + e.message);
    }
  };

  const handleRemoveFavorite = async (classId) => {
    try {
      await favoritesService.remove(classId);
      setFavorites(prev => prev.filter(fav => fav.id !== classId));
    } catch (e) {
      console.error("Erro ao remover favorito:", e);
      setError("Erro ao remover dos favoritos: " + e.message);
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedClass(null);
  };

  if (loading) {
    return <div className="p-6 text-white">Carregando favoritos...</div>;
  }

  if (error) {
    return <div className="p-6 text-red-500">Erro ao carregar favoritos: {error}</div>;
  }

  return (
    <div className="p-6 text-white min-h-screen">
      <h2 className="text-3xl font-bold mb-8 text-red-400">Favoritos</h2>

      {favorites.length === 0 ? (
        <p className="text-gray-400">Você ainda não tem aulas favoritas. Adicione algumas aulas aos favoritos no catálogo!</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {favorites.map(cls => (
            <div key={cls.id} className="bg-gray-700 p-4 rounded-lg shadow-md transform hover:bg-gray-600 transition-all duration-200 hover:scale-105 flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-xl font-semibold text-white truncate flex-1" title={cls.name}>{cls.name}</h3>
                  <button
                    onClick={() => handleRemoveFavorite(cls.id)}
                    className="ml-2 p-1 rounded transition-colors text-red-500 hover:text-red-400"
                    title="Remover dos favoritos"
                  >
                    <FontAwesomeIcon icon={faHeart} />
                  </button>
                </div>
                <p className="text-sm text-gray-400 mb-1">Instrutor: {cls.instructor}</p>
                <p className="text-sm text-gray-400 mb-1">Categoria: {cls.category}</p>
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
    </div>
  );
};

export default Favorites;
