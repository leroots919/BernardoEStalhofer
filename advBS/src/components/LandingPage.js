import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import BSLogo from './shared/BSLogo';
import './LandingPage.css';

const LandingPage = () => {
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showContactModal, setShowContactModal] = useState(false);
  const [contactForm, setContactForm] = useState({
    nome: '',
    email: '',
    whatsapp: '',
    assunto: ''
  });
  const navigate = useNavigate();

  const handleLoginClick = () => {
    setShowLoginModal(true);
  };

  const handleContactClick = () => {
    setShowContactModal(true);
  };

  const handleContactFormChange = (e) => {
    const { name, value } = e.target;
    setContactForm(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleContactFormSubmit = (e) => {
    e.preventDefault();
    // Aqui será implementada a lógica de envio
    console.log('Dados do formulário:', contactForm);
    // Por enquanto apenas fecha o modal
    setShowContactModal(false);
  };

  const handleCloseModal = () => {
    setShowLoginModal(false);
  };

  const handleLoginSuccess = () => {
    setShowLoginModal(false);
    // Redirecionamento será feito pelo componente de login
  };

  return (
    <div className="landing-page">
      {/* Header */}
      <header className="header">
        <div className="container">
          <div className="logo">
            <BSLogo size={50} />
          </div>
          <nav className="nav">
            <a href="#services">Serviços</a>
            <a href="#about">Sobre</a>
            <a href="#specialization">Especialização</a>
            <a href="#contact">Contato</a>
            <button className="login-btn" onClick={handleLoginClick}>
              Login
            </button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <div className="hero-content">
            <div className="hero-badge">
              <span>🏆 Especialistas em Direito de Trânsito</span>
            </div>
            <h1>Defendemos seus direitos com <span className="highlight">excelência jurídica</span></h1>
            <p className="hero-subtitle">
              Somos especialistas em reverter multas injustas, defender contra suspensão da CNH e oferecer consultoria jurídica completa com atendimento 100% personalizado.
            </p>

            <div className="hero-stats">
              <div className="stat-item">
                <div className="stat-number">500+</div>
                <div className="stat-label">Casos Resolvidos</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">95%</div>
                <div className="stat-label">Taxa de Sucesso</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">24h</div>
                <div className="stat-label">Resposta Rápida</div>
              </div>
            </div>

            <div className="hero-services">
              <div className="service-item">
                <div className="service-icon">⚖️</div>
                <span>Reversão de multas injustas</span>
              </div>
              <div className="service-item">
                <div className="service-icon">🚗</div>
                <span>Defesa contra suspensão da CNH</span>
              </div>
              <div className="service-item">
                <div className="service-icon">📋</div>
                <span>Consultoria jurídica completa</span>
              </div>
              <div className="service-item">
                <div className="service-icon">💻</div>
                <span>Atendimento 100% online</span>
              </div>
            </div>

            <div className="hero-cta">
              <button className="cta-button primary" onClick={handleContactClick}>
                Fale com um especialista
              </button>
              <button className="cta-button secondary" onClick={() => document.getElementById('about').scrollIntoView()}>
                Conheça nosso trabalho
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="services">
        <div className="container">
          <h2>Nossos Serviços</h2>
          <div className="services-grid">
            <div className="service-card">
              <div className="service-icon">🚗</div>
              <h3>Recursos de Multas</h3>
              <p>Contestamos multas indevidas e defendemos seus direitos no trânsito com base na legislação vigente.</p>
            </div>
            <div className="service-card">
              <div className="service-icon">📋</div>
              <h3>Defesa Administrativa</h3>
              <p>Representação em processos administrativos junto aos órgãos de trânsito competentes.</p>
            </div>
            <div className="service-card">
              <div className="service-icon">🆔</div>
              <h3>CNH - Suspensão/Cassação</h3>
              <p>Defesa contra suspensão ou cassação da CNH, mantendo seu direito de dirigir.</p>
            </div>
            <div className="service-card">
              <div className="service-icon">⚖️</div>
              <h3>Assessoria em Acidentes</h3>
              <p>Orientação jurídica completa em casos de acidentes de trânsito e suas consequências.</p>
            </div>
          </div>
        </div>
      </section>



      {/* About Section */}
      <section id="about" className="about">
        <div className="container">
          <div className="about-content">
            <div className="about-text">
              <h2>Sobre Nós</h2>
              <div className="about-intro">
                <h3>Somos um Escritório de Advocacia Especializado em Direito de Trânsito considerado uma Referência no Estado do Rio Grande do Sul.</h3>
                <p>
                  Valorizamos a confiança que nossos clientes depositam em nós e nos esforçamos para superar suas expectativas em cada etapa do processo.
                </p>
                <p>
                  Garantimos que você receberá a atenção que merece, com o mais alto nível de transparência nas orientações que lhe daremos.
                </p>
              </div>

              {/* Google Reviews Section */}
              <div className="google-reviews">
                <div className="google-header">
                  <img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" alt="Google" style={{width: '80px', marginBottom: '5px'}} />
                  <div className="reviews-title">
                    <span style={{color: '#666', fontSize: '18px'}}>Reviews</span>
                    <div className="stars">⭐⭐⭐⭐⭐</div>
                  </div>
                </div>

                <div className="review-summary">
                  <span style={{color: '#1a73e8', fontWeight: 'bold'}}>EXCELENTE</span>
                  <span style={{color: '#666', marginLeft: '10px'}}>⭐⭐⭐⭐⭐ 239 avaliações em Google</span>
                </div>

                <div className="reviews-list">
                  <div className="review-item">
                    <div className="review-header">
                      <span className="reviewer-initial">E</span>
                      <div className="reviewer-info">
                        <strong>Evandro Zalokar</strong>
                        <div className="stars">⭐⭐⭐⭐⭐</div>
                      </div>
                    </div>
                    <p className="review-text">
                      Ótimo atendimento, é bem surpreso. Consegui tirar profissionais sobre meu processo em relação ao Detran, e todos me acompanharam que não haveria possibilidade. Porém, eles me deram uma luz no fim do túnel, consegui resolver meu problema e ainda fui atendido com muita atenção e carinho. Desta forma, só tenho a agradecer pelos ótimos profissionais e sucesso no Detran do meu caso.
                    </p>
                  </div>

                  <div className="review-item">
                    <div className="review-header">
                      <span className="reviewer-initial">G</span>
                      <div className="reviewer-info">
                        <strong>Guilherme Peretti</strong>
                        <div className="stars">⭐⭐⭐⭐⭐</div>
                      </div>
                    </div>
                    <p className="review-text">
                      Só tenho elogios com muita organização e competência técnica no auxílio que necessitei, agilizou sucesso no prazo estabelecido, com muita seriedade, transparência e agilidade em todas as etapas do processo. Destaco a excelência no atendimento, desde o primeiro contato até a conclusão do trabalho onde o escritório foi uma constante parceria.
                    </p>
                  </div>

                  <div className="review-item">
                    <div className="review-header">
                      <span className="reviewer-initial">I</span>
                      <div className="reviewer-info">
                        <strong>Iverson Medas</strong>
                        <div className="stars">⭐⭐⭐⭐⭐</div>
                      </div>
                    </div>
                    <p className="review-text">
                      Ótimo serviço, serviços realizados no prazo exato! Ótimo atendimento, de toda equipe!
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section id="why-choose-us" className="why-choose-us">
        <div className="container">
          <div className="why-choose-grid">
            <div className="why-choose-card">
              <div className="why-choose-icon">
                <div className="icon-circle">
                  <span>🎯</span>
                </div>
              </div>
              <h3>EXPERIÊNCIA E CONFIANÇA</h3>
              <p>
                Contamos com <strong>+10 anos de Experiência</strong> Comprovada em
                <strong> Resolução de Casos que Envolvem CNH Suspensa</strong>.
              </p>
              <p>
                <strong>Confie a Solução</strong> do seu Problema a quem realmente é
                um <strong>Advogado Especialista em Suspensão de CNH</strong>.
              </p>
            </div>

            <div className="why-choose-card">
              <div className="why-choose-icon">
                <div className="icon-circle">
                  <span>🏆</span>
                </div>
              </div>
              <h3>ALTA TAXA DE RESULTADOS POSITIVOS</h3>
              <p>
                Nosso <strong>histórico de resultados positivos</strong> é a prova do nosso compromisso
                em <strong>fornecer um serviço jurídico de alta qualidade</strong> que atenda às
                <strong>necessidades de nossos clientes</strong>.
              </p>
              <p>
                <strong>Trabalhamos incansavelmente</strong> para garantir que cada caso seja
                tratado com a devida atenção e cuidado, a fim de <strong>alcançar os melhores
                resultados possíveis</strong>.
              </p>
            </div>

            <div className="why-choose-card">
              <div className="why-choose-icon">
                <div className="icon-circle">
                  <span>💳</span>
                </div>
              </div>
              <h3>HONORÁRIOS JUSTOS!</h3>
              <p>
                Entendemos que <strong>cada cliente tem realidades financeiras distintas</strong> e, por
                isso, <strong>trabalhamos com formatos de pagamento ajustados à sua realidade</strong>.
              </p>
              <p>
                Nossa missão é facilitar o acesso à justiça, <strong>oferecendo um serviço de qualidade
                a um método de pagamento acessível</strong>.
              </p>
              <p>
                <strong>Juntos, podemos encontrar a melhor solução para o seu caso!</strong>
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Specialization Section */}
      <section id="specialization" className="specialization">
        <div className="container">
          <div className="specialization-content">
            <h2>Nossa Especialização</h2>

            <div className="specialization-intro">
              <h3>Escritório de Advocacia Especializado em Direito de Trânsito</h3>
              <p>
                Temos a Experiência para Resolver Casos Complexos, incluindo CNH Cassada, Suspensa, Bloqueada,
                além de Cancelamento de Multa por Dirigir com a CNH Suspensa.
              </p>
              <p>
                Atuamos há mais de 10 anos na Defesa do Direito de Dirigir, Ajudando Condutores a Manterem
                o Direito e a Liberdade de Dirigir.
              </p>
              <p className="call-to-action">
                <strong>Conte com a Nossa Experiência e Continue Dirigindo!</strong>
              </p>
            </div>

            <div className="lawyers-info">
              <div className="lawyer-card">
                <div className="lawyer-icon">👨‍💼</div>
                <h4>Dr. Lucas Bernardo</h4>
                <p>OAB/RS 102.336</p>
              </div>
              <div className="lawyer-card">
                <div className="lawyer-icon">👩‍💼</div>
                <h4>Dra. Sônia Stahlhöfer</h4>
                <p>OAB/RS 110.390</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contact" className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-section">
              <h3>Bernardo & Stahlhöfer</h3>
              <p>Advocacia de Trânsito é uma Sociedade de Advogados inscrita na OAB/RS. 9.012 e CNPJ sob o n° 34150.525000125</p>
            </div>
            <div className="footer-section">
              <h4>Contatos</h4>
              <p>📱 (51) 99357-7272</p>
              <p>📧 bernardostahlhofer@gmail.com</p>
              <p>📍 Av. Assis Brasil, 3535/1307 - Jardim Lindóia - Porto Alegre/RS - CEP: 91110-000</p>
            </div>
            <div className="footer-section">
              <h4>Redes Sociais</h4>
              <div className="social-links">
                <a href="https://www.instagram.com/bernardostahlhofer.adv/#" target="_blank" rel="noopener noreferrer" aria-label="Instagram">📷 Instagram</a>
                <a href="https://www.facebook.com/profile.php?id=100065278111661#" target="_blank" rel="noopener noreferrer" aria-label="Facebook">📘 Facebook</a>
                <a href="https://api.whatsapp.com/send/?phone=5551993577272&text=Ol%C3%A1%2C+envie+sua+mensagem+para+n%C3%B3s%21&type=phone_number&app_absent=0" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">💬 WhatsApp</a>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2024 Bernardo & Stahlhöfer. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>

      {/* Login Modal */}
      {showLoginModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={handleCloseModal}>×</button>
            <LoginModal onSuccess={handleLoginSuccess} />
          </div>
        </div>
      )}

      {/* Contact Modal */}
      {showContactModal && (
        <div className="modal-overlay" onClick={() => setShowContactModal(false)}>
          <div className="contact-modal-content" onClick={(e) => e.stopPropagation()}>
            <button
              className="modal-close"
              onClick={() => setShowContactModal(false)}
            >
              ×
            </button>

            <div className="contact-modal-header">
              <h2>Preencha o Formulário Abaixo</h2>
              <p>Nós Entraremos em Contato com Você pelo WhatsApp!</p>
            </div>

            <form onSubmit={handleContactFormSubmit} className="contact-form">
              <div className="form-row">
                <input
                  type="text"
                  name="nome"
                  placeholder="Nome"
                  value={contactForm.nome}
                  onChange={handleContactFormChange}
                  required
                />
                <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  value={contactForm.email}
                  onChange={handleContactFormChange}
                  required
                />
                <input
                  type="tel"
                  name="whatsapp"
                  placeholder="Whatsapp"
                  value={contactForm.whatsapp}
                  onChange={handleContactFormChange}
                  required
                />
              </div>

              <textarea
                name="assunto"
                placeholder="Assunto"
                value={contactForm.assunto}
                onChange={handleContactFormChange}
                rows="4"
                required
              ></textarea>

              <button type="submit" className="contact-submit-btn">
                Enviar Mensagem para Receber uma Avaliação via WhatsApp
              </button>
            </form>
          </div>
        </div>
      )}

      {/* WhatsApp Floating Button */}
      <a
        href="https://api.whatsapp.com/send/?phone=5551993577272&text=Ol%C3%A1%2C+envie+sua+mensagem+para+n%C3%B3s%21&type=phone_number&app_absent=0"
        target="_blank"
        rel="noopener noreferrer"
        className="whatsapp-float"
        aria-label="Falar no WhatsApp"
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.465 3.488"/>
        </svg>
      </a>
    </div>
  );
};

// Componente de Login Modal integrado com o sistema de autenticação
const LoginModal = ({ onSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, loading, error } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const success = await login(email, password);

    if (success) {
      onSuccess();
      // O redirecionamento será feito automaticamente pelo AuthContext
    }
  };

  return (
    <div className="login-modal">
      <h2>Acesso ao Portal</h2>
      <p className="text-gray-600 mb-4 text-center">
        Entre com suas credenciais para acessar sua conta
      </p>

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <input
            type="text"
            placeholder="Email ou Username"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="mb-4">
          <input
            type="password"
            placeholder="Senha"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-3 py-2 rounded mb-4 text-sm">
            {error}
          </div>
        )}

        <button type="submit" disabled={loading}>
          {loading ? 'Entrando...' : 'Entrar'}
        </button>
      </form>

      <div className="text-center mt-4">
        <p className="text-sm text-gray-600">
          Não tem uma conta? Entre em contato conosco para criar sua conta.
        </p>
      </div>
    </div>
  );
};

export default LandingPage;
