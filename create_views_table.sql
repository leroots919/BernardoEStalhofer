-- =====================================================
-- CRIAR TABELA DE VISUALIZAÇÕES
-- =====================================================

USE poker_academy;

-- Criar tabela para registrar cada visualização individual
CREATE TABLE IF NOT EXISTS class_views (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    class_id INT NOT NULL,
    viewed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    INDEX idx_user_class (user_id, class_id),
    INDEX idx_class_views (class_id),
    INDEX idx_viewed_at (viewed_at)
);

-- Atualizar contador de views nas aulas existentes baseado nos dados atuais
UPDATE classes c 
SET views = (
    SELECT COUNT(*) 
    FROM user_progress up 
    WHERE up.class_id = c.id AND up.watched = true
);

-- Ver estrutura criada
DESCRIBE class_views;

-- Ver contadores atualizados
SELECT id, name, views FROM classes ORDER BY views DESC;

-- =====================================================
-- RESULTADO ESPERADO:
-- - Tabela class_views criada para registrar visualizações
-- - Contador views atualizado baseado em progresso existente
-- - Índices para performance
-- =====================================================
