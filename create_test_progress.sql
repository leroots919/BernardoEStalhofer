-- =====================================================
-- SCRIPT PARA CRIAR DADOS DE TESTE DE PROGRESSO
-- =====================================================

USE poker_academy;

-- Ver usuários e aulas existentes
SELECT 'USUÁRIOS:' as info;
SELECT id, name, username, email, type FROM users;

SELECT 'AULAS:' as info;
SELECT id, name, instructor, category FROM classes;

-- Criar algumas aulas de teste se não existirem
INSERT IGNORE INTO classes (name, instructor, date, category, video_type, video_url, priority, views) VALUES
('Fundamentos do Pré-Flop', 'Daniel Negreanu', '2024-01-15', 'preflop', 'youtube', 'https://youtube.com/watch?v=example1', 5, 0),
('Estratégias Pós-Flop', 'Phil Ivey', '2024-01-20', 'postflop', 'youtube', 'https://youtube.com/watch?v=example2', 5, 0),
('Psicologia do Poker', 'Vanessa Selbst', '2024-01-25', 'mental', 'youtube', 'https://youtube.com/watch?v=example3', 5, 0),
('Torneios: Estrutura e Estratégia', 'Chris Moneymaker', '2024-02-01', 'torneos', 'youtube', 'https://youtube.com/watch?v=example4', 5, 0),
('Cash Game Avançado', 'Tom Dwan', '2024-02-05', 'cash', 'youtube', 'https://youtube.com/watch?v=example5', 5, 0);

-- Buscar ID do primeiro usuário student
SET @student_id = (SELECT id FROM users WHERE type = 'student' LIMIT 1);

-- Criar progresso de teste para o estudante
INSERT IGNORE INTO user_progress (user_id, class_id, progress, watched, last_watched) VALUES
(@student_id, 1, 75, true, DATE_SUB(NOW(), INTERVAL 1 DAY)),
(@student_id, 2, 40, false, DATE_SUB(NOW(), INTERVAL 3 DAY)),
(@student_id, 3, 100, true, DATE_SUB(NOW(), INTERVAL 7 DAY)),
(@student_id, 4, 15, false, DATE_SUB(NOW(), INTERVAL 30 DAY)),
(@student_id, 5, 60, false, DATE_SUB(NOW(), INTERVAL 2 DAY));

-- Ver resultado
SELECT 'PROGRESSO CRIADO:' as info;
SELECT 
    u.name as usuario,
    c.name as aula,
    up.progress,
    up.watched,
    up.last_watched
FROM user_progress up
JOIN users u ON up.user_id = u.id
JOIN classes c ON up.class_id = c.id
WHERE u.type = 'student';

-- =====================================================
-- RESULTADO ESPERADO:
-- - Usuário student terá histórico de 5 aulas
-- - Diferentes níveis de progresso (15%, 40%, 60%, 75%, 100%)
-- - Datas variadas de último acesso
-- =====================================================
