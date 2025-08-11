// src/components/shared/Card.js
import React from 'react';

const Card = ({ 
  children, 
  className = "", 
  padding = "p-6",
  hover = false,
  onClick = null 
}) => {
  const baseClasses = `bg-gray-700 rounded-modern-lg shadow-modern border border-gray-600 ${padding}`;
  const hoverClasses = hover ? "hover:shadow-modern-lg transition-all duration-200 cursor-pointer" : "";
  const clickableClasses = onClick ? "cursor-pointer" : "";
  
  return (
    <div 
      className={`${baseClasses} ${hoverClasses} ${clickableClasses} ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  );
};

export default Card;
