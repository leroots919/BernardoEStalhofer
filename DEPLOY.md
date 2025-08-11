# Deploy no Railway - Bernardo & Stahlhöfer

## 🚀 SOLUÇÃO RADICAL: HEALTHCHECK REMOVIDO

Este projeto foi configurado para deploy no Railway **SEM HEALTHCHECK** para evitar problemas de timeout.

## 📋 Arquivos de Deploy Criados

1. **railway.json** - Configuração principal do Railway (sem healthcheck)
2. **Procfile** - Comando de inicialização alternativo
3. **requirements.txt** - Dependências Python na raiz
4. **start.py** - Script de inicialização robusto
5. **.env.example** - Exemplo de variáveis de ambiente

## 🔧 Configuração no Railway

### 1. Variáveis de Ambiente Necessárias:

```
DB_HOST=seu-host-mysql
DB_PORT=3306
DB_USER=seu-usuario
DB_PASSWORD=sua-senha
DB_NAME=BS
SECRET_KEY=sua-chave-secreta
```

### 2. Comando de Deploy:

O Railway executará automaticamente: `python start.py`

### 3. Porta:

A aplicação usa a variável `PORT` do Railway automaticamente.

## 🗄️ Banco de Dados

Configure um banco MySQL no Railway ou use um serviço externo como:
- PlanetScale
- Railway MySQL
- AWS RDS

## 🔍 Verificação

Após o deploy, acesse:
- `https://seu-app.railway.app/api/health` - Status da API
- `https://seu-app.railway.app/docs` - Documentação Swagger

## 🚨 Importante

- **HEALTHCHECK REMOVIDO**: Não há verificação de saúde automática
- **Restart Policy**: Configurado para reiniciar em caso de falha (máx. 10 tentativas)
- **Ambiente**: Detecta automaticamente se está no Railway

## 📝 Logs

Para verificar logs no Railway:
```bash
railway logs
```

## 🔄 Redeploy

Para fazer redeploy:
```bash
git push origin main
```

O Railway fará deploy automaticamente.
