// src/components/shared/DojoLogo.js
import React from 'react';

const DojoLogo = ({ size = 48, className = "" }) => {
  return (
    <div className={`relative ${className}`} style={{ width: size, height: size }}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 200 200"
        className="drop-shadow-lg"
      >
        {/* Círculo vermelho de fundo */}
        <circle
          cx="100"
          cy="100"
          r="85"
          fill="#E53E3E"
        />

        {/* Círculo branco principal */}
        <circle cx="100" cy="95" r="55" fill="white" />

        {/* Estrutura do Torii em laranja/dourado */}
        <g fill="#FF8C00">
          {/* Travessa horizontal superior (mais larga) */}
          <rect x="50" y="70" width="100" height="8" rx="2" />

          {/* Travessa horizontal inferior */}
          <rect x="55" y="85" width="90" height="6" rx="1" />

          {/* Pilares verticais principais */}
          <rect x="65" y="70" width="6" height="45" />
          <rect x="129" y="70" width="6" height="45" />

          {/* Detalhes horizontais menores nas laterais */}
          <rect x="45" y="95" width="15" height="3" />
          <rect x="140" y="95" width="15" height="3" />

          {/* Elemento central vertical */}
          <rect x="97" y="100" width="6" height="20" />
        </g>

        {/* Elementos vermelhos triangulares */}
        <g fill="#E53E3E">
          {/* Triângulo central vermelho */}
          <path d="M90 105 L100 125 L110 105 Z" />
        </g>

        {/* Pilares brancos inferiores */}
        <g fill="white">
          <rect x="67" y="150" width="8" height="30" />
          <rect x="125" y="150" width="8" height="30" />
        </g>

        {/* Texto DOJO */}
        <text
          x="100"
          y="170"
          textAnchor="middle"
          fill="white"
          fontSize="16"
          fontWeight="bold"
          fontFamily="Arial, sans-serif"
          letterSpacing="4"
        >
          DOJO
        </text>

        {/* Linha decorativa */}
        <line
          x1="65"
          y1="175"
          x2="135"
          y2="175"
          stroke="white"
          strokeWidth="2"
        />

        {/* Texto POKER */}
        <text
          x="100"
          y="188"
          textAnchor="middle"
          fill="white"
          fontSize="12"
          fontFamily="Arial, sans-serif"
          letterSpacing="3"
        >
          POKER
        </text>
      </svg>
    </div>
  );
};

export default DojoLogo;
