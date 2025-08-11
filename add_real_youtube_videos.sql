-- =====================================================
-- ADICIONAR AULAS COM VÍDEOS REAIS DO YOUTUBE
-- =====================================================

USE poker_academy;

-- Limpar aulas existentes (opcional)
-- DELETE FROM classes;

-- Adicionar aulas com vídeos reais de poker do YouTube
INSERT INTO classes (name, instructor, date, category, video_type, video_url, priority, views) VALUES
('Fundamentos do Poker - Como Jogar', 'PokerStars', '2024-01-15', 'preflop', 'youtube', 'https://www.youtube.com/watch?v=GAoR9ji8D6A', 5, 0),
('Estratégias Básicas de Poker', 'PokerNews', '2024-01-20', 'postflop', 'youtube', 'https://www.youtube.com/watch?v=v3QzLjFLzd4', 5, 0),
('Psicologia no Poker', 'Daniel Negreanu', '2024-01-25', 'mental', 'youtube', 'https://www.youtube.com/watch?v=8wqw2H5U7Qs', 5, 0),
('Torneios de Poker - Guia Completo', 'WSOP', '2024-02-01', 'torneos', 'youtube', 'https://www.youtube.com/watch?v=ZJJ4PZ3eoNs', 5, 0),
('Cash Game Estratégias', 'Upswing Poker', '2024-02-05', 'cash', 'youtube', 'https://www.youtube.com/watch?v=50Bda5VKw-A', 5, 0);

-- Atualizar aulas existentes para usar vídeos reais (se preferir)
UPDATE classes SET 
    video_type = 'youtube',
    video_url = CASE 
        WHEN category = 'preflop' THEN 'https://www.youtube.com/watch?v=GAoR9ji8D6A'
        WHEN category = 'postflop' THEN 'https://www.youtube.com/watch?v=v3QzLjFzd4'
        WHEN category = 'mental' THEN 'https://www.youtube.com/watch?v=8wqw2H5U7Qs'
        WHEN category = 'torneos' THEN 'https://www.youtube.com/watch?v=ZJJ4PZ3eoNs'
        WHEN category = 'cash' THEN 'https://www.youtube.com/watch?v=50Bda5VKw-A'
        ELSE video_url
    END
WHERE video_url IS NULL OR video_url = '';

-- Ver resultado
SELECT id, name, instructor, category, video_type, video_url, views FROM classes;

-- =====================================================
-- RESULTADO ESPERADO:
-- - Aulas com vídeos reais do YouTube sobre poker
-- - URLs funcionais que podem ser testadas
-- - Diferentes categorias representadas
-- =====================================================
