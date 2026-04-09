# Guia do Projeto - Bernardo & Stahlhöfer

Este arquivo serve como a fonte da verdade para o comportamento do assistente AI neste projeto. As instruções abaixo devem ser seguidas rigorosamente em todas as sessões.

## 🌐 Idioma e Comunicação
- **Idioma Obrigatório**: Pensar e responder EXCLUSIVAMENTE em português (Brasil). 
- **Tons**: Profissional, direto e conciso. Evite preâmbulos desnecessários.

## 🛠️ Execução Técnica
- **Ferramentas**: Para cada tarefa, deve-se proativamente analisar e utilizar a melhor combinação de:
  - **Skills**: Invocar a skill relevante antes de qualquer ação.
  - **MCPs**: Utilizar servidores MCP (como Puppeteer para análise visual ou outros integrados) sempre que trouxerem vantagem.
  - **CLIs**: Utilizar comandos de terminal (npm, git, gh, etc.) de forma eficiente.
- **Qualidade de Código**:
  - **TypeScript**: Proibido o uso de `any`. Definir interfaces e tipos precisos.
  - **Next.js**: Utilizar App Router. Diferenciar corretamente Server e Client Components (usar `'use client'` apenas quando necessário).
  - **Estilização**: Seguir a paleta de cores da marca (`brand-dark`, `brand-primary`).
  - **Supabase**: Manter as políticas de RLS (Row Level Security) rigorosas para proteção de dados jurídicos.

## 📁 Estrutura do Projeto
- `src/app`: Páginas e rotas (App Router).
- `src/lib`: Utilitários e configurações (ex: cliente do Supabase).
- `.env.local`: Variáveis de ambiente sensíveis (não commitadas).

## 🎯 Objetivos Atuais
1. Manter a landing page moderna e alinhada à identidade visual da marca.
2. Garantir que o fluxo de leads (Formulário -> Supabase) esteja operando perfeitamente.
3. Desenvolver e proteger a Área do Cliente (Login -> Dashboard).
