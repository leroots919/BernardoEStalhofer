import React from 'react';

// Dados simulados de playlists
const playlistsData = [
  {
    id: 1,
    name: 'Trilha Completa de Desenvolvimento Web',
    courseCount: 5,
    courses: [
      { id: 10, title: 'HTML e CSS para Iniciantes', duration: '2h 30m' },
      { id: 11, title: 'JavaScript Essencial', duration: '4h 15m' },
      { id: 1, title: 'React Completo: Do Básico ao Avançado', duration: '10h' },
      { id: 2, title: 'Node.js para Backend de Alta Performance', duration: '8h' },
      { id: 12, title: 'Deploy de Aplicações Web', duration: '3h' },
    ],
    thumbnail: 'https://via.placeholder.com/350x200/8A2BE2/FFFFFF?text=Web+Dev+Trilha'
  },
  {
    id: 2,
    name: 'Especialização em UI/UX Design',
    courseCount: 3,
    courses: [
      { id: 20, title: 'Fundamentos do Design de Interface', duration: '5h' },
      { id: 21, title: 'Ferramentas de Prototipagem (Figma)', duration: '6h' },
      { id: 3, title: 'Dominando Tailwind CSS na Prática', duration: '4h' },
    ],
    thumbnail: 'https://via.placeholder.com/350x200/32CD32/FFFFFF?text=UI/UX+Design'
  },
];

const Playlists = () => {
  return (
    <div className="p-6 bg-dark-bg text-white min-h-screen">
      <h2 className="text-3xl font-bold mb-8 text-poker-red">Minhas Playlists de Estudo</h2>
      
      {playlistsData.length === 0 ? (
        <p className="text-gray-400">Você ainda não criou ou salvou nenhuma playlist.</p>
      ) : (
        <div className="space-y-8">
          {playlistsData.map(playlist => (
            <div key={playlist.id} className="bg-sidebar-bg p-5 rounded-lg shadow-lg flex flex-col md:flex-row items-start gap-5 transform hover:shadow-poker-red/50 transition-shadow duration-300">
              <img src={playlist.thumbnail} alt={`Thumbnail da playlist ${playlist.name}`} className="w-full md:w-1/3 h-auto md:h-48 object-cover rounded-md"/>
              <div className="flex-1">
                <h3 className="text-2xl font-semibold mb-2 text-poker-red truncate" title={playlist.name}>{playlist.name}</h3>
                <p className="text-sm text-gray-400 mb-1">{playlist.courseCount} aulas nesta playlist.</p>
                <div className="mb-3">
                  <h4 className="text-md font-medium text-gray-300 mb-1">Aulas incluídas:</h4>
                  <ul className="list-disc list-inside pl-1 text-sm text-gray-400 max-h-24 overflow-y-auto">
                    {playlist.courses.map(course => (
                      <li key={course.id} className="truncate" title={course.title}>{course.title} ({course.duration})</li>
                    ))}
                  </ul>
                </div>
                <button className="bg-poker-red text-white py-2 px-4 rounded hover:bg-red-700 transition-colors text-sm">
                  Ver Playlist Completa
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Playlists;
