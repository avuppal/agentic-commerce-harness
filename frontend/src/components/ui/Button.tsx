import React from 'react';
import clsx from 'clsx';

type ButtonVariant = 'approve' | 'reject' | 'default';
type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'default',
  size = 'md',
  className,
  ...props
}) => {
  const baseStyles = 'font-semibold rounded-lg focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors duration-150 ease-in-out';

  const variantStyles = {
    default: 'bg-primary-500 hover:bg-primary-600 focus:ring-primary-500 text-white',
    approve: 'bg-success-500 hover:bg-success-600 focus:ring-success-500 text-white',
    reject: 'bg-error-500 hover:bg-error-600 focus:ring-error-500 text-white',
  };

  const sizeStyles = {
    sm: 'py-2 px-4 text-sm',
    md: 'py-2 px-5 text-base',
    lg: 'py-3 px-6 text-lg',
  };

  const combinedClassName = clsx(
    baseStyles,
    variantStyles[variant],
    sizeStyles[size],
    className
  );

  return (
    <button className={combinedClassName} {...props}>
      {children}
    </button>
  );
};

export default Button;
