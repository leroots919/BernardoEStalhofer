import React, { useState, useRef, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay } from '@fortawesome/free-solid-svg-icons';
import { classService } from '../../services/api';
import { getToken } from '../../services/api';

const VideoPlayer = ({ classData, onViewRegistered }) => {
  const [isWatching, setIsWatching] = useState(false);
  const [viewRegistered, setViewRegistered] = useState(false);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const videoRef = useRef(null);

  // Carregar progresso da aula ao montar o componente
  useEffect(() => {
    const loadProgress = async () => {
      try {
        const progressData = await classService.getProgress(classData.id);
        setProgress(progressData);
        console.log('Progresso carregado:', progressData);
      } catch (error) {
        console.error('Erro ao carregar progresso:', error);
        setProgress({ progress: 0, watched: false, last_watched: null });
      } finally {
        setLoading(false);
      }
    };

    if (classData.id) {
      loadProgress();
    }
  }, [classData.id]);

  // Função para registrar visualização
  const registerView = async () => {
    if (viewRegistered) return; // Evitar registrar múltiplas vezes

    try {
      const response = await classService.registerView(classData.id);
      setViewRegistered(true);

      if (onViewRegistered) {
        onViewRegistered(response.total_views);
      }

      console.log('Visualização registrada:', response);
    } catch (error) {
      console.error('Erro ao registrar visualização:', error);
    }
  };

  // Função para salvar progresso do vídeo
  const saveProgress = async (currentTime, duration) => {
    if (!duration || duration === 0) return;

    const progressPercent = Math.round((currentTime / duration) * 100);
    const watched = progressPercent >= 90; // Considera assistido se passou de 90%

    try {
      await classService.updateProgress(classData.id, {
        progress: progressPercent,
        watched: watched,
        current_time: currentTime
      });

      setProgress(prev => ({
        ...prev,
        progress: progressPercent,
        watched: watched,
        current_time: currentTime
      }));

      console.log(`Progresso salvo: ${progressPercent}% (${currentTime}s)`);
    } catch (error) {
      console.error('Erro ao salvar progresso:', error);
    }
  };

  // Função para iniciar assistir
  const handleStartWatching = () => {
    setIsWatching(true);
    registerView();
  };

  // Função para quando o vídeo carrega
  const handleVideoLoaded = () => {
    if (videoRef.current && progress && progress.current_time) {
      // Retomar de onde parou
      videoRef.current.currentTime = progress.current_time;
      console.log(`Retomando vídeo em ${progress.current_time}s (${progress.progress}%)`);
    }
  };

  // Função para salvar progresso periodicamente
  const handleTimeUpdate = () => {
    if (videoRef.current) {
      const currentTime = videoRef.current.currentTime;
      const duration = videoRef.current.duration;

      // Salvar progresso a cada 10 segundos
      if (Math.floor(currentTime) % 10 === 0) {
        saveProgress(currentTime, duration);
      }
    }
  };

  // Função para salvar progresso quando pausar
  const handlePause = () => {
    if (videoRef.current) {
      const currentTime = videoRef.current.currentTime;
      const duration = videoRef.current.duration;
      saveProgress(currentTime, duration);
    }
  };

  // Renderizar player para vídeos locais
  if (!isWatching) {
    if (loading) {
      return (
        <div className="my-4">
          <div className="bg-gray-800 rounded-lg p-8 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-poker-red mx-auto mb-4"></div>
            <p className="text-gray-400">Carregando...</p>
          </div>
        </div>
      );
    }

    return (
      <div className="my-4">
        <div className="bg-gray-800 rounded-lg p-8 text-center">
          <div className="mb-4">
            <FontAwesomeIcon icon={faPlay} size="3x" className="text-poker-red" />
          </div>
          <h3 className="text-xl font-semibold mb-2">
            {progress && progress.progress > 0 ? 'Continuar assistindo?' : 'Pronto para assistir?'}
          </h3>
          <p className="text-gray-400 mb-4">
            {progress && progress.progress > 0
              ? `Você parou em ${progress.progress}% da aula`
              : 'Vídeo local disponível'
            }
          </p>
          {progress && progress.progress > 0 && (
            <div className="w-full bg-gray-700 rounded-full h-2 mb-4">
              <div
                className="bg-poker-red h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress.progress}%` }}
              ></div>
            </div>
          )}
          <button
            onClick={handleStartWatching}
            className="bg-poker-red hover:bg-red-700 text-white font-bold py-3 px-6 rounded-lg transition-colors"
          >
            <FontAwesomeIcon icon={faPlay} className="mr-2" />
            {progress && progress.progress > 0 ? 'Continuar Aula' : 'Assistir Aula'}
          </button>
        </div>
      </div>
    );
  }

  // Player para vídeos locais
  if (classData.video_path) {
    // Usar rota com token para autenticação
    const token = getToken();
    const videoUrl = `http://localhost:5000/api/videos/${classData.video_path}?token=${token}`;
    console.log('URL do vídeo:', videoUrl);

    return (
      <div className="my-4">
        <div className="bg-gray-900 rounded-lg p-4">
          <div className="mb-4">
            <h4 className="text-lg font-semibold text-white mb-2">{classData.name}</h4>
            <p className="text-gray-400 text-sm mb-4">Instrutor: {classData.instructor}</p>
          </div>

          <div className="aspect-w-16 aspect-h-9 mb-4">
            <video
              ref={videoRef}
              controls
              className="w-full h-96 rounded bg-black"
              preload="metadata"
              onLoadedData={handleVideoLoaded}
              onTimeUpdate={handleTimeUpdate}
              onPause={handlePause}
              onEnded={() => saveProgress(videoRef.current?.duration || 0, videoRef.current?.duration || 0)}
            >
              <source src={videoUrl} type="video/mp4" />
              <source src={videoUrl} type="video/webm" />
              <source src={videoUrl} type="video/ogg" />
              Seu navegador não suporta o elemento de vídeo.
            </video>
          </div>

          {/* Barra de progresso visual */}
          {progress && progress.progress > 0 && (
            <div className="mb-4">
              <div className="flex justify-between text-sm text-gray-400 mb-1">
                <span>Progresso da aula</span>
                <span>{progress.progress}%</span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-2">
                <div
                  className="bg-poker-red h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress.progress}%` }}
                ></div>
              </div>
            </div>
          )}

          {viewRegistered && (
            <div className="text-center bg-green-900 bg-opacity-50 p-3 rounded">
              <p className="text-green-400 text-sm">✓ Visualização registrada com sucesso!</p>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Fallback se nenhum vídeo for encontrado
  return (
    <div className="my-4">
      <div className="bg-gray-800 rounded-lg p-8 text-center">
        <p className="text-gray-400">Nenhum vídeo disponível para esta aula</p>
        <p className="text-gray-500 text-sm mt-2">Entre em contato com o administrador</p>
      </div>
    </div>
  );
};

export default VideoPlayer;
