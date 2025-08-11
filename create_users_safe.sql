-- =====================================================
-- SCRIPT SEGURO PARA CRIAR USUÁRIOS DE TESTE
-- =====================================================

USE poker_academy;

-- Ver usuários existentes primeiro
SELECT 'USUÁRIOS EXISTENTES:' as status;
SELECT id, name, email, type, register_date FROM users;

-- Criar admin apenas se não existir
INSERT INTO users (name, email, password_hash, type, register_date) 
SELECT 'admin_test', 'admin@pokeracademy.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', NOW()
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'admin@pokeracademy.com');

-- Criar aluno apenas se não existir
INSERT INTO users (name, email, password_hash, type, register_date) 
SELECT 'aluno_test', 'aluno@pokeracademy.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'student', NOW()
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'aluno@pokeracademy.com');

-- Ver resultado final
SELECT 'USUÁRIOS APÓS SCRIPT:' as status;
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
