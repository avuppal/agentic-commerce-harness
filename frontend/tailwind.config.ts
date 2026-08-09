import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: 'class',
  content: [
    './frontend/**/*.html',
    './frontend/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['monospace'],
      },
      colors: {
        // As defined in HUMAN_UI_PRD.md
        brand: {
          primary: '#3b82f6', // blue-500
          'primary-hover': '#2563eb', // blue-600
        },
        ui: {
          // You can use these in your HTML like:
          // <div class="bg-ui-background dark:bg-ui-background-dark">
          
          // Backgrounds
          background: '#f8fafc',      // light: slate-50
          'background-dark': '#0f172a', // dark: slate-900
          surface: '#ffffff',         // light: white
          'surface-dark': '#1e293b',   // dark: slate-800
          
          // Borders
          border: '#e2e8f0',           // light: slate-200
          'border-dark': '#334155',    // dark: slate-700
          
          // Text
          'text-primary': '#0f172a',      // light: slate-900
          'text-primary-dark': '#f8fafc', // dark: slate-50
          'text-secondary': '#64748b',    // light: slate-500
          'text-secondary-dark': '#94a3b8', // dark: slate-400
        },
        semantic: {
          // Success
          success: '#22c55e',          // green-500
          'success-bg': '#f0fdf4',      // light: green-50
          'success-bg-dark': '#14532d', // dark: green-900
          
          // Error
          error: '#ef4444',            // red-500
          'error-bg': '#fef2f2',        // light: red-50
          'error-bg-dark': '#7f1d1d',   // dark: red-900
          
          // Warning
          warning: '#f97316',          // orange-500
          'warning-bg': '#fff7ed',      // light: orange-50
          'warning-bg-dark': '#7c2d12', // dark: orange-900
        },
      },
    },
  },
  plugins: [],
}
export default config
