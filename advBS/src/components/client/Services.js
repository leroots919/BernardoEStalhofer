import React, { useState, useEffect } from 'react';
import PageHeader from '../shared/PageHeader';
import Card from '../shared/Card';
import Button from '../shared/Button';

const Services = () => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  // Mock data para demonstração
  useEffect(() => {
    // Simular carregamento de dados
    setTimeout(() => {
      setServices([
        {
          id: 1,
          name: 'Recurso de Multa',
          description: 'Contestação de multas de trânsito indevidas com base na legislação vigente.',
          category: 'multas',
          price: 150.00,
          duration_days: 30,
          active: true
        },
        {
          id: 2,
          name: 'Defesa CNH - Suspensão',
          description: 'Defesa contra suspensão da CNH por pontuação ou infrações graves.',
          category: 'cnh',
          price: 300.00,
          duration_days: 45,
          active: true
        },
        {
          id: 3,
          name: 'Assessoria em Acidentes',
          description: 'Orientação jurídica completa em casos de acidentes de trânsito.',
          category: 'acidentes',
          price: 250.00,
          duration_days: 60,
          active: true
        },
        {
          id: 4,
          name: 'Consultoria Jurídica',
          description: 'Consultoria especializada em direito de trânsito.',
          category: 'consultoria',
          price: 100.00,
          duration_days: 7,
          active: true
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleRequestService = (serviceId) => {
    alert(`Solicitação de serviço ${serviceId} enviada! Entraremos em contato em breve.`);
  };

  const getCategoryIcon = (category) => {
    const icons = {
      multas: '🚗',
      cnh: '🆔',
      acidentes: '⚠️',
      consultoria: '⚖️',
      recursos: '📋'
    };
    return icons[category] || '📄';
  };

  const getCategoryColor = (category) => {
    const colors = {
      multas: 'bg-red-100 text-red-800',
      cnh: 'bg-blue-100 text-blue-800',
      acidentes: 'bg-yellow-100 text-yellow-800',
      consultoria: 'bg-green-100 text-green-800',
      recursos: 'bg-purple-100 text-purple-800'
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <PageHeader 
          title="Nossos Serviços" 
          subtitle="Conheça nossos serviços especializados em direito de trânsito"
        />
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Nossos Serviços" 
        subtitle="Conheça nossos serviços especializados em direito de trânsito"
      />
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {services.map((service) => (
          <Card key={service.id} className="h-full flex flex-col">
            <div className="flex-1">
              <div className="flex items-center justify-between mb-4">
                <div className="text-3xl">{getCategoryIcon(service.category)}</div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(service.category)}`}>
                  {service.category.charAt(0).toUpperCase() + service.category.slice(1)}
                </span>
              </div>
              
              <h3 className="text-xl font-bold text-white mb-2">{service.name}</h3>
              <p className="text-gray-300 mb-4 flex-1">{service.description}</p>
              
              <div className="space-y-2 mb-4">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Preço:</span>
                  <span className="text-green-400 font-semibold">
                    R$ {service.price.toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Prazo:</span>
                  <span className="text-blue-400">
                    {service.duration_days} dias
                  </span>
                </div>
              </div>
            </div>
            
            <Button 
              onClick={() => handleRequestService(service.id)}
              className="w-full mt-4"
              variant="primary"
            >
              Solicitar Serviço
            </Button>
          </Card>
        ))}
      </div>
      
      <div className="mt-8 p-6 bg-blue-800/30 rounded-lg border border-blue-700">
        <h3 className="text-xl font-bold text-white mb-2">Precisa de ajuda?</h3>
        <p className="text-gray-300 mb-4">
          Nossa equipe está pronta para atendê-lo. Entre em contato conosco para uma consulta personalizada.
        </p>
        <div className="flex flex-wrap gap-4">
          <Button variant="outline">
            📞 (11) 99999-9999
          </Button>
          <Button variant="outline">
            📧 contato@advtransito.com
          </Button>
          <Button variant="primary">
            💬 WhatsApp
          </Button>
        </div>
      </div>
    </div>
  );
};

export default Services;
