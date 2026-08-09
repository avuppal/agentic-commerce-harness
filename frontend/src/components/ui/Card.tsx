import React from 'react';
import clsx from 'clsx';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  interactive?: boolean;
  children: React.ReactNode;
}

/**
 * Card Component
 * 
 * A versatile, styled container component for panels and list items.
 * It provides a base styling for backgrounds, borders, and padding.
 * An optional `interactive` prop can be added to enable hover effects for clickable items.
 */
export const Card: React.FC<CardProps> = ({
  interactive = false,
  children,
  className,
  ...props
}) => {
  const cardClasses = clsx(
    'border rounded-lg shadow-sm',
    'bg-white dark:bg-slate-800',
    'border-slate-200 dark:border-slate-700',
    'p-6',
    interactive && [
      'hover:bg-slate-50 dark:hover:bg-slate-700/50', // Light and dark mode hover states
      'cursor-pointer',                             // Indicate interactivity
      'transition-colors duration-150'              // Smooth transition for hover effect
    ],
    className // Allow additional classes to be passed in
  );

  return (
    <div className={cardClasses} {...props}>
      {children}
    </div>
  );
};

export default Card;
