// src/components/shared/BSLogo.js
import React, { useState } from 'react';

const BSLogo = ({ size = 200, className = "" }) => {
  const [imageError, setImageError] = useState(false);

  // Se a imagem falhar, mostra um texto temporário
  if (imageError) {
    return (
      <div className={`flex items-center ${className}`} style={{ height: `${size}px` }}>
        <div
          style={{
            background: '#3B4A6B',
            color: 'white',
            padding: '10px 20px',
            borderRadius: '8px',
            fontSize: `${size * 0.15}px`,
            fontWeight: 'bold',
            fontFamily: 'serif'
          }}
        >
          Bernardo & Stahlhöfer
        </div>
      </div>
    );
  }

  return (
    <div className={`flex items-center ${className}`}>
      <img
        src="/images/bs-logo.png"
        alt="Bernardo & Stahlhöfer - Advocacia de Trânsito"
        style={{
          height: `${size}px`,
          width: 'auto',
          objectFit: 'contain',
          borderRadius: '6px'
        }}
        onError={() => {
          console.log('❌ Erro ao carregar logo: /images/bs-logo.png não encontrado');
          setImageError(true);
        }}
        onLoad={() => {
          console.log('✅ Logo carregado com sucesso!');
        }}
      />
    </div>
  );
};

export default BSLogo;
