-- =====================================================
-- SCRIPT CORRIGIDO PARA CRIAR USUÁRIOS DE TESTE
-- =====================================================

USE poker_academy;

-- Ver estrutura atual
DESCRIBE users;

-- Ver usuários existentes
SELECT * FROM users;

-- Criar admin com password_hash (nome correto da coluna)
INSERT INTO users (name, email, password_hash, type, register_date) VALUES 
('admin', 'admin@pokeracademy.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', NOW());

-- Criar aluno de teste
INSERT INTO users (name, email, password_hash, type, register_date) VALUES 
('aluno', 'aluno@pokeracademy.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'student', NOW());

-- Ver resultado final
SELECT 'USUÁRIOS APÓS CRIAÇÃO:' as status;
SELECT id, name, email, type, register_date FROM users;

-- =====================================================
-- CREDENCIAIS DE TESTE:
-- =====================================================
-- ADMIN:
--   Email: admin@pokeracademy.com
--   Senha: admin123
--
-- ALUNO:
--   Email: aluno@pokeracademy.com
--   Senha: aluno123
-- =====================================================
