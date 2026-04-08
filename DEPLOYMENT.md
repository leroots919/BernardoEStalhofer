# Guia de Implantação - Sistema de Gestão Jurídica (MVP)

Este guia descreve os passos necessários para implantar o sistema de gestão para advogados de trânsito.

## 🚀 Stack Tecnológica
- **Frontend/Backend**: Next.js 15+ (App Router)
- **Banco de Dados & Auth**: Supabase (PostgreSQL)
- **Storage**: Supabase Storage
- **Hospedagem**: Vercel
- **Notificações**: WhatsApp API (via Evolution API ou similar)

## 🛠️ Configuração do Ambiente

Crie um arquivo `.env.local` na raiz do projeto com as seguintes variáveis:

```env
# Supabase (Obtido no painel do Supabase -> Settings -> API)
NEXT_PUBLIC_SUPABASE_URL=your-supabase-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# WhatsApp API (Configuração da instância de notificação)
WHATSAPP_BASE_URL=http://seu-servidor-whatsapp:8080
WHATSAPP_API_KEY=sua-chave-api-whatsapp
WHATSAPP_INSTANCE_ID=nome-da-sua-instancia
```

## 🗄️ Configuração do Banco de Dados

1.  **Executar Migrações**:
    - Aplique os arquivos em `supabase/migrations/` na ordem numérica:
      1. `001_initial_schema.sql` (Criação de tabelas e tipos)
      2. `002_enable_rls.sql` (Configuração de segurança RLS)
      3. `003_auth_profile_trigger.sql` (Automação de perfis)

2.  **Configurar Storage**:
    - Crie um bucket chamado `process-files` no painel do Supabase.
    - Defina o bucket como **público** ou configure as políticas de acesso conforme definido no arquivo `002_enable_rls.sql`.

## 📦 Implantação na Vercel

1.  Conecte seu repositório GitHub à Vercel.
2.  Adicione todas as variáveis de ambiente listadas acima nas configurações do projeto na Vercel.
3.  Execute o deploy.

## ✅ Checklist de Verificação Final

- [ ] **Autenticação**: Login e Registro funcionando.
- [ ] **Landing Page**: Acessível e responsiva.
- [ ] **Dashboard Advogado**:
    - [ ] Visão geral com estatísticas.
    - [ ] Gestão de Clientes (Listagem).
    - [ ] Gestão de Processos (Criação e Listagem).
    - [ ] Detalhes do Caso e Gerenciamento de Arquivos.
- [ ] **Fluxo do Cliente**:
    - [ ] Acesso aos seus próprios processos.
    - [ ] Upload de arquivos para o advogado.
- [ ] **Notificações**: Testar envio de WhatsApp ao alterar status de um processo.

## 🛠️ Manutenção
- Para adicionar novos serviços, insira registros na tabela `services`.
- Para ajustar as permissões de acesso, modifique as políticas de RLS no banco de dados.
