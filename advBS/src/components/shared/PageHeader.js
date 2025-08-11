// src/components/shared/PageHeader.js
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

const PageHeader = ({ 
  title, 
  subtitle, 
  icon, 
  children, 
  className = "" 
}) => {
  return (
    <div className={`bg-gray-700 rounded-modern-lg shadow-modern p-6 mb-6 border border-gray-600 ${className}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {icon && (
            <div className="bg-red-400 text-white p-3 rounded-modern">
              <FontAwesomeIcon icon={icon} className="w-6 h-6" />
            </div>
          )}
          <div>
            <h1 className="text-2xl font-bold text-white">{title}</h1>
            {subtitle && (
              <p className="text-gray-300 mt-1">{subtitle}</p>
            )}
          </div>
        </div>
        {children && (
          <div className="flex items-center space-x-3">
            {children}
          </div>
        )}
      </div>
    </div>
  );
};

export default PageHeader;
