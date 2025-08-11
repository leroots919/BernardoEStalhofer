// src/services/api.js
const API_BASE_URL = 'http://localhost:8000';

// Variável global para armazenar o token temporariamente
let currentToken = null;

// Função para definir o token
export const setApiToken = (token) => {
  currentToken = token;
  // Persistir no localStorage para manter entre sessões e refreshes
  if (token) {
    localStorage.setItem('advbs_token', token);
  } else {
    localStorage.removeItem('advbs_token');
  }
};

// Função para obter o token
export const getToken = () => {
  // Se não temos token na memória, tentar recuperar do localStorage
  if (!currentToken) {
    currentToken = localStorage.getItem('advbs_token');
  }
  return currentToken;
};

// Função para fazer requisições autenticadas
const apiRequest = async (endpoint, options = {}) => {
  const token = getToken();
  const url = `${API_BASE_URL}${endpoint}`;

  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  };

  try {
    console.log(`🌐 API Request: ${config.method || 'GET'} ${url}`);
    const response = await fetch(url, config);

    if (!response.ok) {
      console.error(`❌ HTTP Error: ${response.status} ${response.statusText}`);
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    console.log(`✅ API Response: ${endpoint}`, data);
    return { data };
  } catch (error) {
    console.error('❌ Erro na API:', error);
    throw error;
  }
};

// Serviços de Classes
export const classService = {
  // Listar todas as aulas
  getAll: () => apiRequest('/api/classes'),
  
  // Obter detalhes de uma aula
  getById: (id) => apiRequest(`/api/classes/${id}`),
  
  // Criar nova aula (admin)
  create: (classData) => apiRequest('/api/classes', {
    method: 'POST',
    body: JSON.stringify(classData),
  }),
  
  // Atualizar aula (admin)
  update: (id, classData) => apiRequest(`/api/classes/${id}`, {
    method: 'PUT',
    body: JSON.stringify(classData),
  }),
  
  // Deletar aula (admin)
  delete: (id) => apiRequest(`/api/classes/${id}`, {
    method: 'DELETE',
  }),
  
  // Obter progresso da aula
  getProgress: (id) => apiRequest(`/api/classes/${id}/progress`),

  // Atualizar progresso da aula
  updateProgress: (id, progressData) => apiRequest(`/api/classes/${id}/progress`, {
    method: 'POST',
    body: JSON.stringify(progressData),
  }),

  // Registrar visualização da aula
  registerView: (id) => apiRequest(`/api/classes/${id}/view`, {
    method: 'POST',
  }),

  // Obter estatísticas de visualizações (admin)
  getViewStats: (id) => apiRequest(`/api/classes/${id}/views`),

  // Obter histórico de aulas assistidas
  getHistory: () => apiRequest('/api/classes/history'),

  // Obter lista de instrutores (admins)
  getInstructors: () => apiRequest('/api/instructors'),
};

// Serviços de Analytics
export const analyticsService = {
  // Obter estatísticas do painel (admin)
  getStats: () => apiRequest('/api/analytics/stats'),
};

// Serviços de Usuários
export const userService = {
  // Listar todos os usuários (admin)
  getAll: () => apiRequest('/api/users'),
  
  // Criar novo usuário (admin)
  create: (userData) => apiRequest('/api/users', {
    method: 'POST',
    body: JSON.stringify(userData),
  }),
  
  // Atualizar usuário (admin)
  update: (id, userData) => apiRequest(`/api/users/${id}`, {
    method: 'PUT',
    body: JSON.stringify(userData),
  }),
  
  // Deletar usuário (admin)
  delete: (id) => apiRequest(`/api/users/${id}`, {
    method: 'DELETE',
  }),
};

// Serviços de Favoritos
export const favoritesService = {
  // Listar favoritos do usuário
  getAll: () => apiRequest('/api/favorites'),
  
  // Adicionar aos favoritos
  add: (classId) => apiRequest(`/api/favorites/${classId}`, {
    method: 'POST',
  }),
  
  // Remover dos favoritos
  remove: (classId) => apiRequest(`/api/favorites/${classId}`, {
    method: 'DELETE',
  }),
  
  // Verificar se está nos favoritos
  check: (classId) => apiRequest(`/api/favorites/${classId}/check`),
};

// Serviços de Playlists
export const playlistService = {
  // Listar playlists do usuário
  getAll: () => apiRequest('/api/playlists'),
  
  // Obter detalhes de uma playlist
  getById: (id) => apiRequest(`/api/playlists/${id}`),
  
  // Criar nova playlist
  create: (playlistData) => apiRequest('/api/playlists', {
    method: 'POST',
    body: JSON.stringify(playlistData),
  }),
  
  // Deletar playlist
  delete: (id) => apiRequest(`/api/playlists/${id}`, {
    method: 'DELETE',
  }),
  
  // Adicionar aula à playlist
  addClass: (playlistId, classId) => apiRequest(`/api/playlists/${playlistId}/classes/${classId}`, {
    method: 'POST',
  }),
  
  // Remover aula da playlist
  removeClass: (playlistId, classId) => apiRequest(`/api/playlists/${playlistId}/classes/${classId}`, {
    method: 'DELETE',
  }),
};

// Serviços de Autenticação
export const authService = {
  // Login
  login: async (email, password) => {
    try {
      const response = await apiRequest('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });

      // Salvar token no localStorage e na memória
      if (response.data && response.data.access_token) {
        const token = response.data.access_token;
        setApiToken(token);
        console.log('✅ Token salvo com sucesso!');
      }

      return response;
    } catch (error) {
      console.error('❌ Erro no login:', error);
      throw error;
    }
  },

  // Registro
  register: (userData) => apiRequest('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  }),

  // Verificar token
  verify: () => apiRequest('/api/auth/verify'),

  // Logout
  logout: () => apiRequest('/api/auth/logout', {
    method: 'POST',
  }),
};

// Serviços de Cliente
export const clientService = {
  // Perfil do cliente
  getProfile: () => apiRequest('/api/client/profile'),
  updateProfile: (profileData) => apiRequest('/api/client/profile', {
    method: 'PUT',
    body: JSON.stringify(profileData),
  }),

  // Casos do cliente
  getCases: () => apiRequest('/api/client/cases'),
  getCase: (caseId) => apiRequest(`/api/client/cases/${caseId}`),

  // Download de arquivo
  downloadFile: async (fileId) => {
    const token = getToken();
    const url = `${API_BASE_URL}/api/client/files/${fileId}/download`;

    try {
      console.log(`🌐 Download Request: GET ${url}`);
      console.log(`🔑 Token: ${token ? 'Presente' : 'Ausente'}`);

      const response = await fetch(url, {
        headers: {
          ...(token && { 'Authorization': `Bearer ${token}` }),
        },
      });

      console.log(`📡 Response Status: ${response.status}`);
      console.log(`📡 Response Headers:`, [...response.headers.entries()]);

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ Download Error: ${response.status} ${response.statusText}`);
        console.error(`❌ Error Body:`, errorText);
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      // Obter headers importantes
      const contentDisposition = response.headers.get('Content-Disposition');
      const contentType = response.headers.get('Content-Type');
      console.log(`📄 Content-Disposition RAW: "${contentDisposition}"`);
      console.log(`📄 Content-Type RAW: "${contentType}"`);

      // Estratégia mais robusta para extrair filename
      let filename = null;

      if (contentDisposition) {
        console.log(`🔍 Analisando Content-Disposition...`);

        // Tentar vários padrões
        const patterns = [
          /filename\*=UTF-8''([^;]+)/,  // RFC 5987
          /filename="([^"]+)"/,         // Com aspas
          /filename=([^;]+)/            // Sem aspas
        ];

        for (const pattern of patterns) {
          const match = contentDisposition.match(pattern);
          if (match && match[1]) {
            filename = match[1].trim();

            // Se tem encoding UTF-8, decodificar
            if (pattern.source.includes('UTF-8')) {
              try {
                filename = decodeURIComponent(filename);
              } catch (e) {
                console.log(`⚠️ Erro ao decodificar: ${e.message}`);
              }
            }

            console.log(`✅ Filename encontrado: "${filename}"`);
            break;
          }
        }
      }

      // Fallback: gerar nome baseado no tipo de arquivo
      if (!filename) {
        console.log(`🔄 Gerando filename baseado no Content-Type...`);

        const extensionMap = {
          'image/png': '.png',
          'image/jpeg': '.jpg',
          'image/jpg': '.jpg',
          'application/pdf': '.pdf',
          'application/msword': '.doc',
          'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
          'text/plain': '.txt',
          'application/zip': '.zip',
          'application/x-rar-compressed': '.rar'
        };

        const extension = extensionMap[contentType] || '';
        filename = `arquivo_${fileId}${extension}`;
        console.log(`📄 Filename gerado: "${filename}"`);
      }

      // Converter resposta para blob
      const blob = await response.blob();
      console.log(`📦 Blob size: ${blob.size} bytes`);
      console.log(`📦 Blob type: ${blob.type}`);

      // Criar URL temporária e fazer download
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();

      // Aguardar um pouco antes de limpar
      setTimeout(() => {
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);
      }, 100);

      console.log(`✅ Download completed: "${filename}"`);
      return { success: true, filename };
    } catch (error) {
      console.error('❌ Erro no download:', error);
      throw error;
    }
  },
};

// Serviços de Admin
export const adminService = {
  // Métodos genéricos
  get: (endpoint) => apiRequest(endpoint),
  post: (endpoint, data) => apiRequest(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  put: (endpoint, data) => apiRequest(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  delete: (endpoint) => apiRequest(endpoint, {
    method: 'DELETE',
  }),

  // Clientes
  getClients: () => apiRequest('/api/admin/clients'),
  createClient: (clientData) => apiRequest('/api/admin/clients', {
    method: 'POST',
    body: JSON.stringify(clientData),
  }),
  updateClient: (id, clientData) => apiRequest(`/api/admin/clients/${id}`, {
    method: 'PUT',
    body: JSON.stringify(clientData),
  }),
  deleteClient: (id) => apiRequest(`/api/admin/clients/${id}`, {
    method: 'DELETE',
  }),

  // Casos
  getCases: () => apiRequest('/api/admin/cases'),
  getClientCases: (clientId) => apiRequest(`/api/admin/clients/${clientId}/cases`),
  createClientCase: async (clientId, caseData) => {
    console.log(`🔍 Tentando criar caso para cliente ${clientId}:`, caseData);

    // Tentar diferentes rotas até encontrar uma que funcione
    const routes = [
      `/api/admin/clients/${clientId}/cases`,
      `/api/admin/create-case`,
      `/api/create-case-public`
    ];

    for (const route of routes) {
      try {
        console.log(`🌐 Tentando rota: ${route}`);

        const requestData = route.includes('create-case') ?
          { ...caseData, client_id: clientId } :
          caseData;

        const response = await apiRequest(route, {
          method: 'POST',
          body: JSON.stringify(requestData),
        });

        console.log(`✅ Sucesso na rota: ${route}`, response);
        return response;

      } catch (error) {
        console.log(`❌ Erro na rota ${route}:`, error.message);

        // Se não é a última rota, continuar tentando
        if (route !== routes[routes.length - 1]) {
          continue;
        }

        // Se chegou aqui, todas as rotas falharam
        throw error;
      }
    }
  },

  // Arquivos de processo
  getProcessFiles: () => apiRequest('/api/admin/process-files'),
  deleteProcessFile: (fileId) => apiRequest(`/api/admin/process-files/${fileId}`, {
    method: 'DELETE',
  }),

  // Serviços
  getServices: () => apiRequest('/api/services'),
};

// Funções genéricas para HTTP
const get = (endpoint) => apiRequest(endpoint);
const post = (endpoint, data) => apiRequest(endpoint, {
  method: 'POST',
  body: JSON.stringify(data),
});
const put = (endpoint, data) => apiRequest(endpoint, {
  method: 'PUT',
  body: JSON.stringify(data),
});
const del = (endpoint) => apiRequest(endpoint, {
  method: 'DELETE',
});

export default {
  get,
  post,
  put,
  delete: del,
  classService,
  userService,
  favoritesService,
  playlistService,
  authService,
  analyticsService,
  clientService,
  adminService,
};
