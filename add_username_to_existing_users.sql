-- =====================================================
-- SCRIPT PARA ADICIONAR USERNAME AOS USUÁRIOS EXISTENTES
-- =====================================================

USE poker_academy;

-- Ver usuários existentes
SELECT id, name, email, type FROM users;

-- Adicionar username baseado no email (parte antes do @)
UPDATE users 
SET username = CONCAT(
  SUBSTRING_INDEX(email, '@', 1), 
  '_', 
  id
) 
WHERE username IS NULL OR username = '';

-- Ver resultado
SELECT id, name, username, email, type FROM users;

-- =====================================================
-- RESULTADO ESPERADO:
-- - Usuário admin terá username: Lekolesny_1 (ou similar)
-- - Todos os usuários terão username único
-- =====================================================
