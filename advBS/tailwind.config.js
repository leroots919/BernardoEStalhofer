/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Cores principais do time
        'primary-red': '#E53E3E',
        'primary-white': '#FFFFFF',
        'secondary-red': '#C53030',
        'accent-red': '#FC8181',

        // Tons de cinza modernos
        'gray-50': '#F9FAFB',
        'gray-100': '#F3F4F6',
        'gray-200': '#E5E7EB',
        'gray-300': '#D1D5DB',
        'gray-400': '#9CA3AF',
        'gray-500': '#6B7280',
        'gray-600': '#4B5563',
        'gray-700': '#374151',
        'gray-800': '#1F2937',
        'gray-900': '#111827',

        // Backgrounds modernos
        'bg-primary': '#FFFFFF',
        'bg-secondary': '#F9FAFB',
        'bg-dark': '#1F2937',
        'sidebar-bg': '#FFFFFF',
        'sidebar-hover': '#F3F4F6',
        'sidebar-active': '#FEF2F2',

        // Estados
        'success': '#10B981',
        'warning': '#F59E0B',
        'error': '#EF4444',
        'info': '#3B82F6',
      },
      boxShadow: {
        'modern': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'modern-lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
        'modern-xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
      },
      borderRadius: {
        'modern': '12px',
        'modern-lg': '16px',
      },
    },
  },
  plugins: [],
}
