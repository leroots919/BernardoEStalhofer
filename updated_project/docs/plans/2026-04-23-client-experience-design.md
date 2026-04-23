# Design: Experiência do Cliente e Rastreamento de Processos

## 1. Visão Geral e Objetivos
O objetivo deste módulo é transformar a comunicação entre o escritório Bernardo & Stahlhöfer e seus clientes, eliminando a ansiedade do cliente através de transparência total no status do processo e agilizando a troca de documentos.

### Critérios de Sucesso
- Redução de chamadas/mensagens de clientes perguntando "como está meu processo".
- Redução do tempo de coleta de documentos necessários.
- Experiência de usuário fluida, sem erros de navegação (404/406).

## 2. Jornada do Usuário

### Cliente
1. **Login:** Acesso seguro via Supabase Auth.
2. **Dashboard:** Visualização imediata do status do processo, documentos pendentes e notificações.
3. **Acompanhamento:** Consulta a uma linha do tempo visual e um log detalhado de eventos do processo.
4. **Gestão de Docs:** Upload de documentos solicitados pelo advogado com feedback de aprovação/recusa.

### Advogado
1. **Gestão de Casos:** Atualização de status do processo (gera evento automático).
2. **Solicitação de Docs:** Marcação de documentos como "pendentes" para um cliente específico.
3. **Validação:** Aprovação ou recusa de documentos enviados, com feedback para o cliente.
4. **Comunicação:** Disparo de alertas via WhatsApp (Evolution API) integrados aos eventos do sistema.

## 3. Arquitetura de Dados (Supabase)

### Tabelas Necessárias
- **`cases`**:
  - `id` (UUID, PK)
  - `client_id` (UUID, FK -> profiles)
  - `current_status` (Text)
  - `description` (Text)
  - `created_at` (Timestamp)

- **`case_events`**:
  - `id` (UUID, PK)
  - `case_id` (UUID, FK -> cases)
  - `event_description` (Text)
  - `status_label` (Text)
  - `created_at` (Timestamp)

- **`document_requests`**:
  - `id` (UUID, PK)
  - `case_id` (UUID, FK -> cases)
  - `document_name` (Text)
  - `status` (`pending` | `uploaded` | `approved` | `rejected`)
  - `lawyer_feedback` (Text, nullable)
  - `created_at` (Timestamp)

- **`documents`**:
  - `id` (UUID, PK)
  - `request_id` (UUID, FK -> document_requests)
  - `file_url` (Text)
  - `file_name` (Text)
  - `uploaded_at` (Timestamp)

## 4. Interface e UX (Frontend Next.js)

### Componentes Principais
- **ClientDashboard:** Grid de cards com resumo de status, alertas de documentos e notificações.
- **ProcessTimeline:** Stepper visual (estilo linha do tempo) + Lista de eventos datada.
- **DocumentCenter:** Lista de solicitações com estados visuais (Amarelo: Pendente, Azul: Análise, Verde: OK, Vermelho: Recusado).

### Fluxos de Lógica
- **Update Status:** `Adm Update Status` $\rightarrow$ `Insert case_events` $\rightarrow$ `Update cases.current_status` $\rightarrow$ `Notify Client (WhatsApp)`.
- **Doc Request:** `Adm Request Doc` $\rightarrow$ `Insert document_requests` $\rightarrow$ `Notify Client (WhatsApp)`.
- **Doc Upload:** `Client Upload` $\rightarrow$ `Upload to Storage` $\rightarrow$ `Update document_requests.status = 'uploaded'` $\rightarrow$ `Notify Lawyer`.

## 5. Tratamento de Erros e Segurança
- **Segurança:** Implementação de RLS (Row Level Security) no Supabase para que clientes vejam apenas seus próprios dados.
- **Resiliência:** Validação de tipos de arquivos no upload e tratamento de timeouts na API do WhatsApp.
- **Feedback:** Mensagens claras de erro (toasts) em vez de recarregamentos de página.
