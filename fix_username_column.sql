-- =====================================================
-- SCRIPT PARA CORRIGIR PROBLEMA DA COLUNA USERNAME
-- =====================================================

USE poker_academy;

-- Ver estrutura atual
DESCRIBE users;

-- Ver dados existentes
SELECT id, name, email, type FROM users;

-- SOLUÇÃO 1: Se a coluna username existir e estiver causando problema
-- Vamos removê-la completamente (recomendado)
ALTER TABLE users DROP COLUMN IF EXISTS username;

-- SOLUÇÃO 2: Se não conseguir remover, vamos torná-la nullable e preenchê-la
-- ALTER TABLE users MODIFY COLUMN username VARCHAR(100) NULL;
-- UPDATE users SET username = name WHERE username IS NULL OR username = '';

-- Ver estrutura após correção
DESCRIBE users;

-- Testar inserção de um usuário de teste
INSERT INTO users (name, email, password_hash, type, register_date) VALUES 
('teste_usuario', 'teste@email.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'student', NOW());

-- Ver se funcionou
SELECT * FROM users WHERE email = 'teste@email.com';

-- Remover o usuário de teste
DELETE FROM users WHERE email = 'teste@email.com';

-- =====================================================
-- RESULTADO ESPERADO:
-- - Coluna username removida ou corrigida
-- - Inserção de usuários funcionando normalmente
-- =====================================================
