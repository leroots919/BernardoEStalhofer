// src/components/shared/Loading.js
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

const Loading = ({ show }) => {
  if (!show) return null;
  
  return (
    <div className="fixed top-0 left-0 w-full h-full bg-black bg-opacity-70 flex justify-center items-center z-50">
      <div className="text-center">
        <FontAwesomeIcon 
          icon={faSpinner} 
          spin 
          className="text-poker-red text-4xl mb-2" 
        />
        <p className="text-white">Carregando...</p>
      </div>
    </div>
  );
};

export default Loading;
