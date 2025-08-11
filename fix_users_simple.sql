-- =====================================================
-- SCRIPT SIMPLES PARA CRIAR USUÁRIOS DE TESTE
-- =====================================================

USE poker_academy;

-- Primeiro, vamos ver a estrutura atual da tabela
DESCRIBE users;

-- Ver usuários existentes
SELECT * FROM users;

-- Tentar criar admin com a estrutura atual
-- (usando o nome da coluna que existe no seu banco)
INSERT INTO users (name, email, password, type, register_date) VALUES 
('admin', 'admin@pokeracademy.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', NOW())
ON DUPLICATE KEY UPDATE 
email = VALUES(email);

-- Tentar criar aluno de teste
INSERT INTO users (name, email, password, type, register_date) VALUES 
('aluno_teste', 'aluno@pokeracademy.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'student', NOW())
ON DUPLICATE KEY UPDATE 
email = VALUES(email);

-- Ver resultado final
SELECT 'USUÁRIOS CRIADOS:' as resultado;
SELECT id, name, email, type, register_date FROM users;

-- =====================================================
-- Se o script acima der erro, execute este alternativo:
-- =====================================================

-- ALTERNATIVA 1: Se a coluna se chama password_hash
-- INSERT INTO users (name, email, password_hash, type, register_date) VALUES 
-- ('admin', 'admin@pokeracademy.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', NOW());

-- ALTERNATIVA 2: Se não tem coluna register_date
-- INSERT INTO users (name, email, password, type) VALUES 
-- ('admin', 'admin@pokeracademy.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin');

-- =====================================================
-- CREDENCIAIS:
-- Email: admin@pokeracademy.com
-- Senha: admin123
-- 
-- Email: aluno@pokeracademy.com  
-- Senha: aluno123
-- =====================================================
