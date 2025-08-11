// src/components/admin/Dashboard.js
import React, { useState, useEffect } from 'react';
import { Users, FileText, Clock, CheckCircle } from 'lucide-react';
import api, { adminService } from '../../services/api';

console.log('📦 Dashboard.js carregado - API importado:', api);
console.log('🔧 adminService disponível:', adminService);
console.log('🔧 api.adminService disponível:', api.adminService);

const Dashboard = () => {
  console.log('🎯 Dashboard component renderizado!');

  const [stats, setStats] = useState({
    totalClients: 0,
    activeCases: 0,
    pendingCases: 0,
    completedCases: 0
  });
  const [recentClients, setRecentClients] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log('🔄 useEffect executado - chamando fetchDashboardData');
    console.log('🔑 Token atual:', localStorage.getItem('advbs_token'));
    console.log('🔑 Token antigo:', localStorage.getItem('token'));
    console.log('🔧 adminService:', adminService);
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      console.log('🚀 INICIANDO fetchDashboardData...');
      setLoading(true);

      console.log('📡 Fazendo requisições para API...');
      console.log('🔧 Usando adminService:', adminService);

      // Buscar estatísticas
      const [clientsResponse, casesResponse] = await Promise.all([
        adminService.getClients(),
        adminService.getCases()
      ]);

      console.log('📦 Response clientes:', clientsResponse);
      console.log('📦 Response casos:', casesResponse);

      // Extrair dados das respostas
      const clients = clientsResponse?.data || clientsResponse || [];
      const cases = casesResponse?.data || casesResponse || [];

      console.log('✅ Clientes recebidos:', clients);
      console.log('✅ Casos recebidos:', cases);
      console.log('🔍 Tipo de clients:', typeof clients, Array.isArray(clients));
      console.log('🔍 Tipo de cases:', typeof cases, Array.isArray(cases));

      const clientsArray = Array.isArray(clients) ? clients : [];
      const casesArray = Array.isArray(cases) ? cases : [];

      const newStats = {
        totalClients: clientsArray.length,
        activeCases: casesArray.filter(c => c && c.status === 'em_andamento').length,
        pendingCases: casesArray.filter(c => c && c.status === 'pendente').length,
        completedCases: casesArray.filter(c => c && c.status === 'concluido').length
      };

      console.log('📊 Stats calculadas:', newStats);
      setStats(newStats);

      // Últimos 5 clientes cadastrados
      const recentClientsData = clientsArray.slice(-5).reverse();
      console.log('👥 Clientes recentes:', recentClientsData);
      setRecentClients(recentClientsData);
      console.log('✅ Dashboard data carregado com sucesso!');

    } catch (error) {
      console.error('❌ Erro ao carregar dados do dashboard:', error);
      console.error('❌ Stack trace:', error.stack);
    } finally {
      setLoading(false);
      console.log('🏁 fetchDashboardData finalizado');
    }
  };

  const StatCard = ({ icon: Icon, title, value, color }) => (
    <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-400 text-sm font-medium">{title}</p>
          <p className={`text-2xl font-bold ${color}`}>{value}</p>
        </div>
        <Icon className={`h-8 w-8 ${color}`} />
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={Users}
          title="Total de Clientes"
          value={stats.totalClients}
          color="text-blue-400"
        />
        <StatCard
          icon={Clock}
          title="Casos em Andamento"
          value={stats.activeCases}
          color="text-yellow-400"
        />
        <StatCard
          icon={FileText}
          title="Casos Pendentes"
          value={stats.pendingCases}
          color="text-orange-400"
        />
        <StatCard
          icon={CheckCircle}
          title="Casos Concluídos"
          value={stats.completedCases}
          color="text-green-400"
        />
      </div>

      {/* Clientes Recentes */}
      <div className="bg-gray-800 rounded-lg border border-gray-700">
        <div className="p-6 border-b border-gray-700">
          <h2 className="text-xl font-semibold text-white">Clientes Recentes</h2>
        </div>
        <div className="p-6">
          {recentClients.length === 0 ? (
            <p className="text-gray-400 text-center py-4">Nenhum cliente cadastrado ainda</p>
          ) : (
            <div className="space-y-4">
              {recentClients.map((client) => {
                if (!client) return null;

                return (
                  <div key={client.id} className="flex items-center justify-between p-4 bg-gray-700 rounded-lg">
                    <div>
                      <h3 className="text-white font-medium">{client.name || 'Nome não informado'}</h3>
                      <p className="text-gray-400 text-sm">{client.email || 'Email não informado'}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-gray-400 text-sm">
                        {client.register_date ? new Date(client.register_date).toLocaleDateString('pt-BR') : '-'}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
