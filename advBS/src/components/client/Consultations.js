import React, { useState, useEffect } from 'react';
import PageHeader from '../shared/PageHeader';
import Card from '../shared/Card';
import Button from '../shared/Button';

const Consultations = () => {
  const [consultations, setConsultations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showScheduleModal, setShowScheduleModal] = useState(false);

  // Mock data para demonstração
  useEffect(() => {
    setTimeout(() => {
      setConsultations([
        {
          id: 1,
          service: 'Consultoria Jurídica',
          scheduled_date: '2024-01-25T14:00:00',
          status: 'pendente',
          notes: 'Consulta sobre multa de trânsito'
        },
        {
          id: 2,
          service: 'Defesa CNH',
          scheduled_date: '2024-01-20T10:00:00',
          status: 'concluido',
          notes: 'Orientação sobre processo de defesa da CNH'
        }
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const getStatusColor = (status) => {
    const colors = {
      pendente: 'bg-yellow-100 text-yellow-800',
      em_andamento: 'bg-blue-100 text-blue-800',
      concluido: 'bg-green-100 text-green-800',
      cancelado: 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  };

  const getStatusText = (status) => {
    const texts = {
      pendente: 'Agendada',
      em_andamento: 'Em Andamento',
      concluido: 'Concluída',
      cancelado: 'Cancelada'
    };
    return texts[status] || status;
  };

  const formatDateTime = (dateString) => {
    const date = new Date(dateString);
    return {
      date: date.toLocaleDateString('pt-BR'),
      time: date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    };
  };

  const handleScheduleConsultation = () => {
    setShowScheduleModal(true);
  };

  const handleCancelConsultation = (consultationId) => {
    if (window.confirm('Tem certeza que deseja cancelar esta consulta?')) {
      alert(`Consulta ${consultationId} cancelada`);
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <PageHeader 
          title="Consultas" 
          subtitle="Agende e acompanhe suas consultas jurídicas"
        />
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <PageHeader 
          title="Consultas" 
          subtitle="Agende e acompanhe suas consultas jurídicas"
        />
        <Button 
          onClick={handleScheduleConsultation}
          variant="primary"
        >
          Agendar Consulta
        </Button>
      </div>
      
      {consultations.length === 0 ? (
        <Card className="text-center py-12">
          <div className="text-6xl mb-4">📅</div>
          <h3 className="text-xl font-bold text-white mb-2">Nenhuma consulta agendada</h3>
          <p className="text-gray-300 mb-6">
            Agende uma consulta com nossos especialistas para esclarecer suas dúvidas.
          </p>
          <Button 
            onClick={handleScheduleConsultation}
            variant="primary"
          >
            Agendar Primeira Consulta
          </Button>
        </Card>
      ) : (
        <div className="space-y-4">
          {consultations.map((consultation) => {
            const { date, time } = formatDateTime(consultation.scheduled_date);
            return (
              <Card key={consultation.id} className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-2xl">📅</span>
                      <h3 className="text-xl font-bold text-white">{consultation.service}</h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(consultation.status)}`}>
                        {getStatusText(consultation.status)}
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                      <div>
                        <span className="text-gray-400 text-sm">Data:</span>
                        <p className="text-blue-400 font-medium">{date}</p>
                      </div>
                      <div>
                        <span className="text-gray-400 text-sm">Horário:</span>
                        <p className="text-blue-400 font-medium">{time}</p>
                      </div>
                    </div>
                    
                    {consultation.notes && (
                      <div>
                        <span className="text-gray-400 text-sm">Observações:</span>
                        <p className="text-gray-300">{consultation.notes}</p>
                      </div>
                    )}
                  </div>
                  
                  <div className="ml-4 flex flex-col gap-2">
                    {consultation.status === 'pendente' && (
                      <>
                        <Button variant="outline" size="sm">
                          Reagendar
                        </Button>
                        <Button 
                          onClick={() => handleCancelConsultation(consultation.id)}
                          variant="danger" 
                          size="sm"
                        >
                          Cancelar
                        </Button>
                      </>
                    )}
                    {consultation.status === 'concluido' && (
                      <Button variant="outline" size="sm">
                        Ver Relatório
                      </Button>
                    )}
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      )}
      
      <div className="mt-8 p-6 bg-blue-800/30 rounded-lg border border-blue-700">
        <h3 className="text-xl font-bold text-white mb-2">Como funcionam as consultas?</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-300">
          <div>
            <h4 className="font-semibold text-white mb-1">📞 Online ou Presencial</h4>
            <p>Escolha a modalidade que melhor se adequa à sua necessidade.</p>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-1">⏰ Duração</h4>
            <p>Consultas têm duração média de 30 a 60 minutos.</p>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-1">📋 Preparação</h4>
            <p>Tenha em mãos todos os documentos relacionados ao seu caso.</p>
          </div>
          <div>
            <h4 className="font-semibold text-white mb-1">📄 Relatório</h4>
            <p>Após a consulta, você receberá um relatório com as orientações.</p>
          </div>
        </div>
      </div>

      {/* Modal de Agendamento (simplificado) */}
      {showScheduleModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-gray-800 p-6 rounded-lg max-w-md w-full mx-4">
            <h3 className="text-xl font-bold text-white mb-4">Agendar Consulta</h3>
            <p className="text-gray-300 mb-4">
              Entre em contato conosco para agendar sua consulta:
            </p>
            <div className="space-y-3 mb-6">
              <Button variant="outline" className="w-full">
                📞 (11) 99999-9999
              </Button>
              <Button variant="outline" className="w-full">
                📧 contato@advtransito.com
              </Button>
              <Button variant="primary" className="w-full">
                💬 WhatsApp
              </Button>
            </div>
            <Button 
              onClick={() => setShowScheduleModal(false)}
              variant="outline" 
              className="w-full"
            >
              Fechar
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Consultations;
