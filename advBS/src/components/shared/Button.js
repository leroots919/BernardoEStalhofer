// src/components/shared/Button.js
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  icon = null,
  iconPosition = 'left',
  loading = false,
  disabled = false,
  className = '',
  onClick = null,
  type = 'button',
  ...props
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-modern transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2';
  
  const variants = {
    primary: 'bg-primary-red text-white hover:bg-secondary-red focus:ring-primary-red shadow-modern',
    secondary: 'bg-gray-100 text-gray-700 hover:bg-gray-200 focus:ring-gray-500 border border-gray-300',
    outline: 'bg-transparent text-primary-red border border-primary-red hover:bg-primary-red hover:text-white focus:ring-primary-red',
    danger: 'bg-error text-white hover:bg-red-600 focus:ring-error shadow-modern',
    success: 'bg-success text-white hover:bg-green-600 focus:ring-success shadow-modern',
  };
  
  const sizes = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2.5 text-sm',
    lg: 'px-6 py-3 text-base',
    xl: 'px-8 py-4 text-lg',
  };
  
  const disabledClasses = disabled || loading ? 'opacity-50 cursor-not-allowed' : '';
  
  return (
    <button
      type={type}
      className={`${baseClasses} ${variants[variant]} ${sizes[size]} ${disabledClasses} ${className}`}
      onClick={onClick}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <FontAwesomeIcon icon="spinner" spin className="mr-2" />
      )}
      {icon && iconPosition === 'left' && !loading && (
        <FontAwesomeIcon icon={icon} className="mr-2" />
      )}
      {children}
      {icon && iconPosition === 'right' && !loading && (
        <FontAwesomeIcon icon={icon} className="ml-2" />
      )}
    </button>
  );
};

export default Button;
