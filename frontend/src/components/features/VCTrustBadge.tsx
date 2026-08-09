import React from 'react';
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';

interface VCTrustBadgeProps {
  status: 'success' | 'error';
  labelText: string;
  tooltipContent: string;
}

const VCTrustBadge: React.FC<VCTrustBadgeProps> = ({
  status,
  labelText,
  tooltipContent,
}) => {
  const statusConfig = {
    success: {
      icon: CheckCircleIcon,
      textColor: 'text-success-500',
      labelColor: 'text-green-600',
      borderColor: 'border-green-300',
    },
    error: {
      icon: XCircleIcon,
      textColor: 'text-error-500',
      labelColor: 'text-red-600',
      borderColor: 'border-red-300',
    },
  };

  const config = statusConfig[status];

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div
            className={`flex items-center gap-1 cursor-pointer p-1 rounded-md ${config.borderColor}`}
          >
            <config.icon className={`w-5 h-5 ${config.textColor}`} />
            <span className={`font-medium text-sm ${config.labelColor}`}>{labelText}</span>
          </div>
        </TooltipTrigger>
        <TooltipContent>
          <p>{tooltipContent}</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  );
};

export default VCTrustBadge;
