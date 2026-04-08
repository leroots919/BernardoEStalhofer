import Link from 'next/link'
import { ArrowRight, CheckCircle2, Star, MessageCircle, Instagram, Facebook } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="flex flex-col min-h-screen bg-white text-slate-900 font-sans selection:bg-brand-primary/30">
      {/* Navbar */}
      <nav className="sticky top-0 z-50 bg-white/70 backdrop-blur-xl border-b border-slate-200/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-20 items-center">
            <div className="flex items-center gap-3">
              <div className="w-11 h-11 bg-brand-primary rounded-xl flex items-center justify-center text-white font-bold text-xl shadow-lg shadow-brand-primary/20 ring-4 ring-brand-primary/10">
                BS
              </div>
              <span className="font-serif font-bold text-2xl tracking-tight text-slate-900 hidden sm:block">
                Bernardo & Stahlhöfer
              </span>
            </div>

            <div className="hidden md:flex items-center gap-10 text-sm font-semibold text-slate-600">
              <a href="#services" className="hover:text-brand-primary transition-colors relative group">
                Serviços
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-brand-primary transition-all group-hover:w-full" />
              </a>
              <a href="#about" className="hover:text-brand-primary transition-colors relative group">
                Sobre
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-brand-primary transition-all group-hover:w-full" />
              </a>
              <a href="#specialization" className="hover:text-brand-primary transition-colors relative group">
                Especialização
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-brand-primary transition-all group-hover:w-full" />
              </a>
              <a href="#contact" className="hover:text-brand-primary transition-colors relative group">
                Contato
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-brand-primary transition-all group-hover:w-full" />
              </a>
            </div>

            <Link
              href="/login"
              className="bg-brand-primary text-white px-6 py-2.5 rounded-full text-sm font-bold hover:bg-brand-primary/90 transition-all shadow-lg shadow-brand-primary/20 hover:shadow-brand-primary/40 ring-2 ring-white"
            >
              Login
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-40 overflow-hidden bg-gradient-to-b from-blue-50/50 via-white to-white">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-10">
          <div className="absolute top-[-10%] left-[-10%] w-[50%] h-[50%] bg-brand-primary/10 rounded-full blur-[120px] opacity-60" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[50%] h-[50%] bg-blue-100 rounded-full blur-[120px] opacity-60" />
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white text-brand-primary text-xs font-bold uppercase tracking-widest mb-8 border border-brand-primary/20 shadow-sm animate-fade-in">
            <span className="flex h-2 w-2 rounded-full bg-brand-primary animate-pulse" />
            🏆 Especialistas em Direito de Trânsito
          </div>

          <h1 className="text-6xl md:text-8xl font-serif font-bold text-slate-900 mb-8 leading-[1.1] tracking-tight">
            Defendemos seus direitos com <br />
            <span className="text-brand-primary italic">excelência jurídica</span>
          </h1>

          <p className="max-w-2xl mx-auto text-xl text-slate-600 mb-12 leading-relaxed font-medium">
            Somos especialistas em reverter multas injustas, defender contra suspensão da CNH e oferecer consultoria jurídica completa com atendimento 100% personalizado.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mb-24">
            <a
              href="https://api.whatsapp.com/send/?phone=5551993577272&text=Ol%C3%A1%2C+gostaria+de+uma+avalia%C3%A7%C3%A3o+do+meu+caso"
              target="_blank"
              className="w-full sm:w-auto flex items-center justify-center gap-3 bg-brand-primary text-white px-10 py-5 rounded-2xl font-bold text-lg hover:bg-brand-primary/90 transition-all shadow-2xl shadow-brand-primary/40 group"
            >
              Fale com um especialista
              <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
            </a>
            <a
              href="#about"
              className="w-full sm:w-auto px-10 py-5 rounded-2xl font-bold text-lg text-slate-700 hover:bg-slate-100 transition-all border border-slate-200 shadow-sm"
            >
              Conheça nosso trabalho
            </a>
          </div>

          {/* Quick Stats - Premium Floating Box */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-12 max-w-5xl mx-auto p-10 bg-white/60 backdrop-blur-xl rounded-[40px] shadow-2xl shadow-slate-200/60 border border-white/80 ring-1 ring-slate-200/50">
            <div className="text-center group">
              <div className="text-4xl font-bold text-slate-900 mb-2 group-hover:text-brand-primary transition-colors">500+</div>
              <div className="text-sm text-slate-500 font-semibold uppercase tracking-wider">Casos Resolvidos</div>
            </div>
            <div className="text-center group border-x border-slate-100">
              <div className="text-4xl font-bold text-slate-900 mb-2 group-hover:text-brand-primary transition-colors">95%</div>
              <div className="text-sm text-slate-500 font-semibold uppercase tracking-wider">Taxa de Sucesso</div>
            </div>
            <div className="text-center group col-span-2 md:col-span-1">
              <div className="text-4xl font-bold text-slate-900 mb-2 group-hover:text-brand-primary transition-colors">24h</div>
              <div className="text-sm text-slate-500 font-semibold uppercase tracking-wider">Resposta Rápida</div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="py-32 bg-slate-50/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20">
            <h2 className="text-4xl md:text-5xl font-serif font-bold text-slate-900 mb-6">Nossos Serviços</h2>
            <div className="w-24 h-1.5 bg-brand-primary mx-auto rounded-full shadow-sm" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
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
              <div key={idx} className="p-10 rounded-[32px] border border-slate-200 bg-white hover:border-brand-primary/50 hover:shadow-2xl hover:-translate-y-2 transition-all duration-300 group shadow-sm">
                <div className="text-5xl mb-8 group-hover:scale-110 transition-transform duration-300">{service.icon}</div>
                <h3 className="text-2xl font-bold text-slate-900 mb-4">{service.title}</h3>
                <p className="text-slate-600 leading-relaxed text-lg">{service.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-32 bg-blue-50/30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
            <div className="space-y-10">
              <div>
                <h2 className="text-4xl md:text-5xl font-serif font-bold text-slate-900 mb-6">Sobre Nós</h2>
                <div className="w-24 h-1.5 bg-brand-primary rounded-full mb-8" />
              </div>

              <div className="space-y-8">
                <h3 className="text-3xl font-bold text-slate-800 leading-tight">
                  Referência em Direito de Trânsito no Rio Grande do Sul.
                </h3>
                <p className="text-xl text-slate-600 leading-relaxed font-medium">
                  Valorizamos a confiança que nossos clientes depositam em nós e nos esforçamos para superar suas expectativas em cada etapa do processo.
                </p>
                <p className="text-xl text-slate-600 leading-relaxed">
                  Garantimos a atenção que você merece, com o mais alto nível de transparência nas orientações jurídicas.
                </p>
              </div>

              <div className="flex items-center gap-5 p-8 bg-white rounded-3xl border border-slate-200 shadow-xl shadow-slate-200/50">
                <div className="flex-shrink-0 w-14 h-14 bg-brand-primary/10 rounded-2xl flex items-center justify-center text-brand-primary ring-4 ring-brand-primary/5">
                  <CheckCircle2 className="w-8 h-8" />
                </div>
                <div>
                  <p className="font-bold text-slate-900 text-lg">Transparência Total</p>
                  <p className="text-slate-500 leading-relaxed">Acompanhamento real e honesto de cada etapa do seu processo.</p>
                </div>
              </div>
            </div>

            <div className="bg-white p-10 rounded-[40px] shadow-2xl shadow-slate-200/60 border border-slate-100">
              <div className="flex items-center justify-between mb-10">
                <div className="flex items-center gap-4">
                  <img src="https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" alt="Google" className="w-24" />
                  <div className="text-sm font-bold text-slate-400 uppercase tracking-widest">Reviews</div>
                </div>
                <div className="flex items-center gap-1 text-yellow-400">
                  {[...Array(5)].map((_, i) => <Star key={i} className="w-5 h-5 fill-current" />)}
                </div>
              </div>

              <div className="mb-10">
                <span className="text-blue-600 font-extrabold text-xl uppercase tracking-wide">Excelente</span>
                <span className="ml-3 text-slate-500 text-sm font-medium">⭐⭐⭐⭐⭐ 239 avaliações no Google</span>
              </div>

              <div className="space-y-6">
                {[
                  {
                    name: 'Evandro Zalokar',
                    text: 'Ótimo atendimento, é bem surpreso. Consegui tirar profissionais sobre meu processo em relação ao Detran... consegui resolver meu problema e ainda fui atendendo com muita atenção e carinho.',
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
                  <div key={idx} className="p-6 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all">
                    <div className="flex items-center gap-4 mb-4">
                      <div className="w-10 h-10 rounded-full bg-brand-primary text-white flex items-center justify-center text-sm font-bold">
                        {review.initial}
                      </div>
                      <div className="text-sm font-bold text-slate-900">{review.name}</div>
                      <div className="flex items-center gap-0.5 text-yellow-400 ml-auto">
                        {[...Array(5)].map((_, i) => <Star key={i} className="w-4 h-4 fill-current" />)}
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
      <section className="py-32 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-20">
            <h2 className="text-4xl md:text-5xl font-serif font-bold text-slate-900 mb-6">Por que nos escolher?</h2>
            <div className="w-24 h-1.5 bg-brand-primary mx-auto rounded-full shadow-sm" />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
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
              <div key={idx} className="p-10 rounded-[32px] border border-slate-200 bg-slate-50 hover:bg-white hover:border-brand-primary/50 hover:shadow-2xl transition-all duration-300 group">
                <div className="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center text-4xl mb-8 group-hover:scale-110 transition-transform duration-300 ring-1 ring-slate-100">
                  {item.icon}
                </div>
                <h3 className="text-2xl font-bold text-slate-900 mb-4 uppercase tracking-tight">{item.title}</h3>
                <p className="text-slate-600 leading-relaxed text-lg">{item.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Specialization Section */}
      <section id="specialization" className="py-32 bg-slate-900 text-white relative overflow-hidden">
        <div className="absolute top-0 right-0 w-1/2 h-full bg-brand-primary/5 blur-[120px] rounded-full" />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="text-center mb-20">
            <h2 className="text-4xl md:text-5xl font-serif font-bold mb-6">Nossa Especialização</h2>
            <div className="w-24 h-1.5 bg-brand-primary mx-auto rounded-full" />
          </div>

          <div className="max-w-3xl mx-auto text-center mb-20">
            <h3 className="text-3xl font-bold mb-8 text-brand-primary/80">Escritório de Advocacia Especializado em Direito de Trânsito</h3>
            <p className="text-xl text-slate-300 leading-relaxed mb-8">
              Temos a Experiência para Resolver Casos Complexos, incluindo CNH Cassada, Suspensa, Bloqueada,
              além de Cancelamento de Multa por Dirigir com a CNH Suspensa.
            </p>
            <p className="text-xl text-slate-300 leading-relaxed mb-12">
              Atuamos há mais de 10 anos na Defesa do Direito de Dirigir, Ajudando Condutores a Manterem
              o Direito e a Liberdade de Dirigir.
            </p>
            <div className="inline-block px-10 py-5 rounded-full bg-brand-primary text-white font-bold text-xl animate-bounce shadow-2xl shadow-brand-primary/40 ring-4 ring-brand-primary/20">
              Conte com a Nossa Experiência e Continue Dirigindo!
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-10 max-w-4xl mx-auto">
            {[
              { name: 'Dr. Lucas Bernardo', oab: 'OAB/RS 102.336', icon: '👨‍💼' },
              { name: 'Dra. Sônia Stahlhöfer', oab: 'OAB/RS 110.390', icon: '👩‍💼' },
            ].map((lawyer, idx) => (
              <div key={idx} className="p-10 rounded-3xl bg-slate-800 border border-slate-700 flex items-center gap-8 hover:bg-slate-700 transition-all shadow-xl group">
                <div className="text-6xl group-hover:scale-110 transition-transform duration-300">{lawyer.icon}</div>
                <div>
                  <h4 className="text-2xl font-bold">{lawyer.name}</h4>
                  <p className="text-slate-400 font-medium text-lg">{lawyer.oab}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contact" className="py-20 bg-white border-t border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-16 mb-16">
            <div className="space-y-6">
              <div className="flex items-center gap-3">
                <div className="w-9 h-9 bg-brand-primary rounded-lg flex items-center justify-center text-white font-bold text-sm">BS</div>
                <span className="font-serif font-bold text-xl text-slate-900">Bernardo & Stahlhöfer</span>
              </div>
              <p className="text-slate-600 text-sm leading-relaxed">
                Advocacia de Trânsito é uma Sociedade de Advogados inscrita na OAB/RS. 9.012 e CNPJ sob o n° 34150.525000125
              </p>
            </div>

            <div className="space-y-6">
              <h4 className="font-bold text-slate-900 uppercase tracking-widest text-sm">Contatos</h4>
              <ul className="space-y-4 text-slate-600 text-sm font-medium">
                <li className="flex items-center gap-3 group cursor-pointer">
                  <MessageCircle className="w-5 h-5 text-brand-primary group-hover:scale-110 transition-transform" />
                  (51) 99357-7272
                </li>
                <li className="flex items-center gap-3 group cursor-pointer">
                  <div className="w-5 h-5 text-brand-primary font-bold group-hover:scale-110 transition-transform">@</div>
                  bernardostahlhofer@gmail.com
                </li>
                <li className="flex items-center gap-3 group cursor-pointer">
                  <div className="w-5 h-5 text-brand-primary font-bold group-hover:scale-110 transition-transform">📍</div>
                  Av. Assis Brasil, 3535/1307 - Porto Alegre/RS
                </li>
              </ul>
            </div>

            <div className="space-y-6">
              <h4 className="font-bold text-slate-900 uppercase tracking-widest text-sm">Redes Sociais</h4>
              <div className="flex gap-5">
                <a href="https://www.instagram.com/bernardostahlhofer.adv/#" target="_blank" className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 hover:bg-brand-primary hover:text-white transition-all shadow-sm hover:shadow-md">
                  <Instagram className="w-6 h-6" />
                </a>
                <a href="https://www.facebook.com/profile.php?id=100065278111661#" target="_blank" className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 hover:bg-brand-primary hover:text-white transition-all shadow-sm hover:shadow-md">
                  <Facebook className="w-6 h-6" />
                </a>
              </div>
            </div>
          </div>

          <div className="pt-10 border-t border-slate-100 text-center text-sm text-slate-500 font-medium">
            <p>&copy; 2024 Bernardo & Stahlhöfer. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>

      {/* Floating WhatsApp Button */}
      <a
        href="https://api.whatsapp.com/send/?phone=5551993577272&text=Ol%C3%A1%2C+envie+sua+mensagem+para+n%C3%B3s%21"
        target="_blank"
        rel="noopener noreferrer"
        className="fixed bottom-8 right-8 z-50 w-16 h-16 bg-green-500 text-white rounded-full flex items-center justify-center shadow-2xl hover:bg-green-600 transition-all hover:scale-110 animate-bounce ring-4 ring-white"
        aria-label="WhatsApp"
      >
        <MessageCircle className="w-8 h-8 fill-current" />
      </a>
    </div>
  )
}
