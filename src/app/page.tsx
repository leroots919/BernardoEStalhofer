import Link from 'next/link'
import { ArrowRight, CheckCircle2, Star, MessageCircle, Instagram, Facebook } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen bg-slate-50 text-slate-900 font-sans">
      {/* Navbar */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-brand-primary rounded-lg flex items-center justify-center text-white font-bold text-xl">
                BS
              </div>
              <span className="font-serif font-bold text-xl tracking-tight text-slate-900 hidden sm:block">
                Bernardo & Stahlhöfer
              </span>
            </div>

            <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-600">
              <a href="#services" className="hover:text-brand-primary transition-colors">Serviços</a>
              <a href="#about" className="hover:text-brand-primary transition-colors">Sobre</a>
              <a href="#specialization" className="hover:text-brand-primary transition-colors">Especialização</a>
              <a href="#contact" className="hover:text-brand-primary transition-colors">Contato</a>
            </div>

            <Link
              href="/login"
              className="bg-brand-primary text-white px-5 py-2 rounded-full text-sm font-semibold hover:bg-brand-primary transition-all shadow-sm hover:shadow-brand-primary/20"
            >
              Login
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-10">
          <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-brand-primary/20 rounded-full blur-3xl opacity-50" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-100 rounded-full blur-3xl opacity-50" />
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-primary/10 text-brand-primary text-xs font-bold uppercase tracking-wider mb-6 border border-brand-primary/20">
            <span className="flex h-2 w-2 rounded-full bg-brand-primary animate-pulse" />
            🏆 Especialistas em Direito de Trânsito
          </div>

          <h1 className="text-5xl md:text-7xl font-serif font-bold text-slate-900 mb-6 leading-tight">
            Defendemos seus direitos com <br />
            <span className="text-brand-primary">excelência jurídica</span>
          </h1>

          <p className="max-w-2xl mx-auto text-lg text-slate-600 mb-10 leading-relaxed">
            Somos especialistas em reverter multas injustas, defender contra suspensão da CNH e oferecer consultoria jurídica completa com atendimento 100% personalizado.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <a
              href="https://api.whatsapp.com/send/?phone=5551993577272&text=Ol%C3%A1%2C+gostaria+de+uma+avalia%C3%A7%C3%A3o+do+meu+caso"
              target="_blank"
              className="w-full sm:w-auto flex items-center justify-center gap-2 bg-brand-primary text-white px-8 py-4 rounded-xl font-bold text-lg hover:bg-brand-primary transition-all shadow-xl shadow-brand-primary/20 group"
            >
              Fale com um especialista
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </a>
            <a
              href="#about"
              className="w-full sm:w-auto px-8 py-4 rounded-xl font-bold text-lg text-slate-700 hover:bg-slate-100 transition-all"
            >
              Conheça nosso trabalho
            </a>
          </div>

          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-8 max-w-4xl mx-auto p-8 bg-white rounded-3xl shadow-xl border border-slate-100">
            <div className="text-center">
              <div className="text-3xl font-bold text-slate-900 mb-1">500+</div>
              <div className="text-sm text-slate-500 font-medium">Casos Resolvidos</div>
            </div>
            <div className="text-center border-x border-slate-100">
              <div className="text-3xl font-bold text-slate-900 mb-1">95%</div>
              <div className="text-sm text-slate-500 font-medium">Taxa de Sucesso</div>
            </div>
            <div className="text-center col-span-2 md:col-span-1">
              <div className="text-3xl font-bold text-slate-900 mb-1">24h</div>
              <div className="text-sm text-slate-500 font-medium">Resposta Rápida</div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-serif font-bold text-slate-900 mb-4">Nossos Serviços</h2>
            <div className="w-20 h-1.5 bg-brand-primary mx-auto rounded-full" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              {
                title: 'Recursos de Multas',
                desc: 'Contestamos multas indevidas e defendemos seus direitos no trânsito com base na legislação vigente.',
                icon: '🚗'
              },
              {
                title: 'Defesa Administrativa',
                desc: 'Representação em processos administrativos junto aos órgãos de trânsito competentes.',
                icon: '📋'
              },
              {
                title: 'CNH - Suspensão/Cassação',
                desc: 'Defesa contra suspensão ou cassação da CNH, mantendo seu direito de dirigir.',
                icon: '🆔'
              },
              {
                title: 'Assessoria em Acidentes',
                desc: 'Orientação jurídica completa em casos de acidentes de trânsito e suas consequências.',
                icon: '⚖️'
              },
            ].map((service, idx) => (
              <div key={idx} className="p-8 rounded-2xl border border-slate-100 bg-slate-50 hover:bg-white hover:shadow-xl transition-all group">
                <div className="text-4xl mb-6 group-hover:scale-110 transition-transform duration-300">{service.icon}</div>
                <h3 className="text-xl font-bold text-slate-900 mb-3">{service.title}</h3>
                <p className="text-slate-600 leading-relaxed">{service.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-24 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
              <div>
                <h2 className="text-3xl md:text-4xl font-serif font-bold text-slate-900 mb-4">Sobre Nós</h2>
                <div className="w-20 h-1.5 bg-brand-primary rounded-full mb-6" />
              </div>

              <div className="space-y-6">
                <h3 className="text-2xl font-bold text-slate-800 leading-tight">
                  Somos um Escritório de Advocacia Especializado em Direito de Trânsito considerado uma Referência no Estado do Rio Grande do Sul.
                </h3>
                <p className="text-lg text-slate-600 leading-relaxed">
                  Valorizamos a confiança que nossos clientes depositam em nós e nos esforçamos para superar suas expectativas em cada etapa do processo.
                </p>
                <p className="text-lg text-slate-600 leading-relaxed">
                  Garantimos que você receberá a atenção que merece, com o mais alto nível de transparência nas orientações que lhe daremos.
                </p>
              </div>

              <div className="flex items-center gap-4 p-6 bg-white rounded-2xl border border-slate-200 shadow-sm">
                <div className="flex-shrink-0 w-12 h-12 bg-brand-primary/20 rounded-full flex items-center justify-center text-brand-primary">
                  <CheckCircle2 className="w-6 h-6" />
                </div>
                <div>
                  <p className="font-bold text-slate-900">Transparência Total</p>
                  <p className="text-sm text-slate-500">Acompanhamento real e honesto de cada etapa do seu processo.</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-8 rounded-3xl shadow-xl border border-slate-100">
              <div className="flex items-center justify-between mb-8">
                <div className="flex items-center gap-3">
                  <img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" alt="Google" className="w-20" />
                  <div className="text-sm font-medium text-slate-500">Reviews</div>
                </div>
                <div className="flex items-center gap-1 text-yellow-400">
                  {[...Array(5)].map((_, i) => <Star key={i} className="w-4 h-4 fill-current" />)}
                </div>
              </div>

              <div className="mb-6">
                <span className="text-blue-600 font-bold text-lg uppercase tracking-wide">Excelente</span>
                <span className="ml-3 text-slate-500 text-sm">⭐⭐⭐⭐⭐ 239 avaliações no Google</span>
              </div>

              <div className="space-y-6">
                {[
                  {
                    name: 'Evandro Zalokar',
                    text: 'Ótimo atendimento, é bem surpreso. Consegui tirar profissionais sobre meu processo em relação ao Detran... consegui resolver meu problema e ainda fui atendido com muita atenção e carinho.',
                    initial: 'E'
                  },
                  {
                    name: 'Guilherme Peretti',
                    text: 'Só tenho elogios com muita organização e competência técnica no auxílio que necessitei, agilizou sucesso no prazo estabelecido.',
                    initial: 'G'
                  },
                  {
                    name: 'Iverson Medas',
                    text: 'Ótimo serviço, serviços realizados no prazo exato! Ótimo atendimento, de toda equipe!',
                    initial: 'I'
                  },
                ].map((review, idx) => (
                  <div key={idx} className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="w-8 h-8 rounded-full bg-brand-primary text-white flex items-center justify-center text-xs font-bold">
                        {review.initial}
                      </div>
                      <div className="text-sm font-bold text-slate-900">{review.name}</div>
                      <div className="flex items-center gap-0.5 text-yellow-400 ml-auto">
                        {[...Array(5)].map((_, i) => <Star key={i} className="w-3 h-3 fill-current" />)}
                      </div>
                    </div>
                    <p className="text-sm text-slate-600 italic leading-relaxed">"{review.text}"</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-serif font-bold text-slate-900 mb-4">Por que nos escolher?</h2>
            <div className="w-20 h-1.5 bg-brand-primary mx-auto rounded-full" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                title: 'Experiência e Confiança',
                text: 'Contamos com +10 anos de Experiência Comprovada em Resolução de Casos que Envolvem CNH Suspensa. Confie a Solução do seu Problema a quem realmente é um Advogado Especialista.',
                icon: '🎯'
              },
              {
                title: 'Alta Taxa de Resultados',
                text: 'Nosso histórico de resultados positivos é a prova do nosso compromisso em fornecer um serviço jurídico de alta qualidade que atenda às necessidades de nossos clientes.',
                icon: '🏆'
              },
              {
                title: 'Honorários Justos',
                text: 'Entendemos que cada cliente tem realidades financeiras distintas e trabalhamos com formatos de pagamento ajustados à sua realidade. Facilitamos o acesso à justiça.',
                icon: '💳'
              },
            ].map((item, idx) => (
              <div key={idx} className="p-8 rounded-3xl border border-slate-100 bg-slate-50 hover:bg-brand-primary/10 transition-colors group">
                <div className="w-14 h-14 bg-white rounded-2xl shadow-sm flex items-center justify-center text-3xl mb-6 group-hover:scale-110 transition-transform">
                  {item.icon}
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-4 uppercase tracking-tight">{item.title}</h3>
                <p className="text-slate-600 leading-relaxed">{item.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Specialization Section */}
      <section id="specialization" className="py-24 bg-slate-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-serif font-bold mb-4">Nossa Especialização</h2>
            <div className="w-20 h-1.5 bg-brand-primary/100 mx-auto rounded-full" />
          </div>

          <div className="max-w-3xl mx-auto text-center mb-16">
            <h3 className="text-2xl font-bold mb-6 text-brand-primary/50">Escritório de Advocacia Especializado em Direito de Trânsito</h3>
            <p className="text-lg text-slate-300 leading-relaxed mb-6">
              Temos a Experiência para Resolver Casos Complexos, incluindo CNH Cassada, Suspensa, Bloqueada,
              além de Cancelamento de Multa por Dirigir com a CNH Suspensa.
            </p>
            <p className="text-lg text-slate-300 leading-relaxed mb-8">
              Atuamos há mais de 10 anos na Defesa do Direito de Dirigir, Ajudando Condutores a Manterem
              o Direito e a Liberdade de Dirigir.
            </p>
            <div className="inline-block px-6 py-3 rounded-full bg-brand-primary text-white font-bold text-lg animate-bounce">
              Conte com a Nossa Experiência e Continue Dirigindo!
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {[
              { name: 'Dr. Lucas Bernardo', oab: 'OAB/RS 102.336', icon: '👨‍💼' },
              { name: 'Dra. Sônia Stahlhöfer', oab: 'OAB/RS 110.390', icon: '👩‍💼' },
            ].map((lawyer, idx) => (
              <div key={idx} className="p-8 rounded-2xl bg-slate-800 border border-slate-700 flex items-center gap-6 hover:bg-slate-700 transition-all">
                <div className="text-5xl">{lawyer.icon}</div>
                <div>
                  <h4 className="text-xl font-bold">{lawyer.name}</h4>
                  <p className="text-slate-400 font-medium">{lawyer.oab}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contact" className="py-16 bg-white border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
            <div className="space-y-4">
              <div className="flex items-center gap-2 mb-6">
                <div className="w-8 h-8 bg-brand-primary rounded flex items-center justify-center text-white font-bold text-sm">BS</div>
                <span className="font-serif font-bold text-lg text-slate-900">Bernardo & Stahlhöfer</span>
              </div>
              <p className="text-slate-600 text-sm leading-relaxed">
                Advocacia de Trânsito é uma Sociedade de Advogados inscrita na OAB/RS. 9.012 e CNPJ sob o n° 34150.525000125
              </p>
            </div>

            <div className="space-y-4">
              <h4 className="font-bold text-slate-900 uppercase tracking-wider text-sm">Contatos</h4>
              <ul className="space-y-3 text-slate-600 text-sm">
                <li className="flex items-center gap-3">
                  <MessageCircle className="w-4 h-4 text-brand-primary" />
                  (51) 99357-7272
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-4 h-4 text-brand-primary font-bold">@</div>
                  bernardostahlhofer@gmail.com
                </li>
                <li className="flex items-center gap-3">
                  <div className="w-4 h-4 text-brand-primary font-bold">📍</div>
                  Av. Assis Brasil, 3535/1307 - Porto Alegre/RS
                </li>
              </ul>
            </div>

            <div className="space-y-4">
              <h4 className="font-bold text-slate-900 uppercase tracking-wider text-sm">Redes Sociais</h4>
              <div className="flex gap-4">
                <a href="https://www.instagram.com/bernardostahlhofer.adv/#" target="_blank" className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 hover:bg-brand-primary hover:text-white transition-all">
                  <Instagram className="w-5 h-5" />
                </a>
                <a href="https://www.facebook.com/profile.php?id=100065278111661#" target="_blank" className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 hover:bg-brand-primary hover:text-white transition-all">
                  <Facebook className="w-5 h-5" />
                </a>
              </div>
            </div>
          </div>

          <div className="pt-8 border-t border-slate-100 text-center text-sm text-slate-500">
            <p>&copy; 2024 Bernardo & Stahlhöfer. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>

      {/* Floating WhatsApp Button */}
      <a
        href="https://api.whatsapp.com/send/?phone=5551993577272&text=Ol%C3%A1%2C+envie+sua+mensagem+para+n%C3%B3s%21"
        target="_blank"
        rel="noopener noreferrer"
        className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-green-500 text-white rounded-full flex items-center justify-center shadow-2xl hover:bg-green-600 transition-all hover:scale-110 animate-bounce"
        aria-label="WhatsApp"
      >
        <MessageCircle className="w-7 h-7 fill-current" />
      </a>
    </div>
  )
}
