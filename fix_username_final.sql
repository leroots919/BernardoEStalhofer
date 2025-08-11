-- =====================================================
-- SCRIPT FINAL PARA RESOLVER PROBLEMA DA COLUNA USERNAME
-- =====================================================

USE poker_academy;

-- Ver estrutura atual
DESCRIBE users;

-- PASSO 1: Verificar se a coluna username existe
SELECT COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_SCHEMA = 'poker_academy' 
  AND TABLE_NAME = 'users' 
  AND COLUMN_NAME = 'username';

-- PASSO 2: Se a coluna username existir, vamos removê-la
-- Execute este comando apenas se a consulta acima retornar resultado
ALTER TABLE users DROP COLUMN IF EXISTS username;

-- PASSO 3: Verificar se ainda existe alguma constraint relacionada
SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE 
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS 
WHERE TABLE_SCHEMA = 'poker_academy' 
  AND TABLE_NAME = 'users';

-- PASSO 4: Ver estrutura final
DESCRIBE users;

-- PASSO 5: Testar inserção
INSERT INTO users (name, email, password_hash, type, register_date) VALUES 
('teste_final', 'teste_final@email.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'student', NOW());

-- PASSO 6: Verificar se funcionou
SELECT * FROM users WHERE email = 'teste_final@email.com';

-- PASSO 7: Limpar teste
DELETE FROM users WHERE email = 'teste_final@email.com';

-- =====================================================
-- SE AINDA DER ERRO, EXECUTE ESTE COMANDO ALTERNATIVO:
-- =====================================================
-- DROP TABLE users;
-- 
-- CREATE TABLE users (
--   id INT AUTO_INCREMENT PRIMARY KEY,
--   name VARCHAR(100) NOT NULL,
--   email VARCHAR(100) NOT NULL UNIQUE,
--   password_hash VARCHAR(255) NOT NULL,
--   type ENUM('admin', 'student') NOT NULL DEFAULT 'student',
--   register_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   last_login DATETIME NULL
-- );
-- 
-- -- Recriar usuário admin
-- INSERT INTO users (name, email, password_hash, type, register_date) VALUES 
-- ('admin', 'Lekolesny@hotmail.com', '$2b$12$dOmIj2KnNKo1cAirC.FAguG/LZlpnwVVE8ZnZ.XyDx9ZdD36O4b9C', 'admin', NOW());
-- =====================================================
