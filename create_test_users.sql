-- =====================================================
-- SCRIPT PARA CRIAR USUÁRIOS DE TESTE
-- =====================================================
-- Execute este script diretamente no MySQL
-- =====================================================

USE poker_academy;

-- Verificar se os usuários já existem
SELECT 'Usuários existentes:' as info;
SELECT id, name, email, type, register_date FROM users;

-- Inserir usuário administrador (se não existir)
INSERT IGNORE INTO users (name, email, password_hash, type, register_date) VALUES 
('admin', 'admin@pokeracademy.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', NOW());

-- Inserir usuário aluno de teste (se não existir)
INSERT IGNORE INTO users (name, email, password_hash, type, register_date) VALUES 
('aluno', 'aluno@pokeracademy.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'student', NOW());

-- Verificar se foram criados
SELECT 'Usuários após inserção:' as info;
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
