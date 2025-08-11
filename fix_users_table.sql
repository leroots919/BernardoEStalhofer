-- =====================================================
-- SCRIPT PARA CORRIGIR A TABELA USERS
-- =====================================================

USE poker_academy;

-- Ver estrutura atual da tabela
DESCRIBE users;

-- Ver dados existentes
SELECT * FROM users;

-- Se existir coluna username, vamos removê-la ou ajustá-la
-- PRIMEIRO: Verificar se existe a coluna username
-- Se existir, execute os comandos abaixo:

-- Opção 1: Remover a coluna username (se não for necessária)
-- ALTER TABLE users DROP COLUMN username;

-- Opção 2: Se a coluna username for necessária, vamos preenchê-la
-- UPDATE users SET username = name WHERE username IS NULL OR username = '';

-- Opção 3: Tornar a coluna username nullable (se existir)
-- ALTER TABLE users MODIFY COLUMN username VARCHAR(100) NULL;

-- Ver estrutura após correção
DESCRIBE users;

-- =====================================================
-- INSTRUÇÕES:
-- 1. Execute este script para ver a estrutura
-- 2. Se houver coluna username, descomente uma das opções acima
-- 3. Execute novamente para verificar se foi corrigido
-- =====================================================
