# Design do MVP: Sistema Bernardo & Stahlhöfer Advocacia de Trânsito
Data: 2026-04-07

## 1. Objetivo e Visão Geral
Construir um MVP simplificado para gestão de processos de multas de trânsito, focando em custo zero de infraestrutura e simplicidade de manutenção.

### Critérios de Sucesso
- Custo de infraestrutura zero (Vercel + Supabase).
- Fluxo funcional de upload e download de documentos entre cliente e advogado.
- Notificações automatizadas via WhatsApp sobre mudanças de status.
- Experiência de usuário fluida e responsiva.

---

## 2. Stack Técnica (Unificada)
A arquitetura migra de um modelo desacoplado (React + FastAPI) para um modelo fullstack unificado.

| Camada | Tecnologia | Motivação |
| :--- | :--- | :--- |
| **Framework** | Next.js 15 (App Router) | Sinergia com Vercel, deploy único, TypeScript unificado. |
| **Linguagem** | TypeScript | Segurança de tipos e manutenção simplificada. |
| **Banco de Dados** | Supabase (PostgreSQL) | Camada gratuita generosa, fácil escalabilidade. |
| **Autenticação** | Supabase Auth | Gestão de usuários e sessões nativa e segura. |
| **Storage** | Supabase Storage | Armazenamento de documentos com permissões RLS. |
| **Hospedagem** | Vercel | Deploy automatizado e custo zero para MVP. |
| **Notificações** | API WhatsApp via Next.js Route | Integração direta com a API existente. |

---

## 3. Estrutura de Componentes e Páginas

### Páginas Públicas
- `Landing Page`: Apresentação dos serviços, SEO e CTA para contato.

### Portal do Cliente (Privado)
- `Dashboard`: Visualização do status do processo.
- `Central de Arquivos`: Interface de upload (envio para advogado) e download (recebimento do advogado).

### Painel do Advogado (Admin - Privado)
- `Gestão de Processos`: CRUD de processos, alteração de status e observações.
- `Gestão de Arquivos`: Visualização e upload de documentos para o cliente.
- `Log de Notificações`: Verificação de envios de WhatsApp.

---

## 4. Fluxos de Dados e Lógica

### Fluxo de Arquivos
`Cliente` $\rightarrow$ `Next.js Component` $\rightarrow$ `Supabase Storage` $\rightarrow$ `Supabase DB (Referência)`.

### Fluxo de Notificações
`Advogado altera Status` $\rightarrow$ `Supabase DB` $\rightarrow$ `Next.js API Route` $\rightarrow$ `API WhatsApp` $\rightarrow$ `Cliente`.

### Segurança (RLS)
Utilização de Row Level Security no Supabase para garantir que:
- Clientes acessem apenas seus próprios processos e arquivos.
- Advogados acessem todos os processos da clínica.

---

## 5. Estratégia de Migração (Reaproveitamento)
Para evitar retrabalho, será adotado o seguinte plano de reaproveitamento:
- **Frontend:** Migração do HTML/CSS e estrutura de componentes da pasta `advBS`.
- **Backend:** Tradução da lógica de negócio e rotas do `advBS-backend` (FastAPI) para TypeScript/Next.js.
- **Banco de Dados:** Mapeamento do schema MySQL (`database_schema.sql`) para PostgreSQL no Supabase.

---

## 6. Qualidade e Verificação
- **Metodologia:** Test-Driven Development (TDD).
- **Foco:** Testes unitários e de integração para fluxos críticos (Auth, Upload, Notificações).
- **E2E:** Não priorizado para a fase inicial do MVP.
