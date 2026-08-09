import React from 'react';
import * as TooltipPrimitive from '@radix-ui/react-tooltip';

interface TooltipProps {
  children: React.ReactNode;
  content: React.ReactNode;
  side?: 'top' | 'right' | 'bottom' | 'left';
  align?: 'start' | 'center' | 'end';
}

export const Tooltip: React.FC<TooltipProps> = ({
  children,
  content,
  side = 'top',
  align = 'center',
}) => {
  return (
    <TooltipPrimitive.Provider>
      <TooltipPrimitive.Root delayDuration={100}>
        <TooltipPrimitive.Trigger asChild>
          {children}
        </TooltipPrimitive.Trigger>
        <TooltipPrimitive.Portal>
          <TooltipPrimitive.Content
            side={side}
            align={align}
            className='z-50 px-2 py-1 bg-slate-900 text-white text-xs rounded-md shadow-lg will-change-transform data-[state=delayed-open]:data-[side=top]:animate-slideDown data-[state=delayed-open]:data-[side=right]:animate-slideLeft data-[state=delayed-open]:data-[side=bottom]:animate-slideUp data-[state=delayed-open]:data-[side=left]:animate-slideRight'
            sideOffset={4}
          >
            {content}
            <TooltipPrimitive.Arrow className='fill-current text-slate-900' />
          </TooltipPrimitive.Content>
        </TooltipPrimitive.Portal>
      </TooltipPrimitive.Root>
    </TooltipPrimitive.Provider>
  );
};
