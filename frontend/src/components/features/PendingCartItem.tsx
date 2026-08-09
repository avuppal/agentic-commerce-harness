import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

interface PendingCartItemProps {
  order: {
    id: string;
    original_prompt: string;
    flagged_reason: string;
    cart_total: string;
    submitted_at: string;
  };
}

const PendingCartItem: React.FC<PendingCartItemProps> = ({ order }) => {
  const router = useRouter();

  return (
    <Link href={`/admin/approvals/${order.id}`}>
      <div className="border rounded-lg p-4 hover:bg-slate-100 dark:hover:bg-slate-700 cursor-pointer transition-colors duration-200">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1">
            <div>
              <span className="text-sm text-secondary-light dark:text-secondary-dark font-medium">Original Prompt</span>
              <p className="text-sm line-clamp-2">{order.original_prompt}</p>
            </div>
            <div className="mt-2">
              <span className="text-sm text-secondary-light dark:text-secondary-dark font-medium">Flagged Reason</span>
              <p className="text-sm font-semibold text-orange-500 dark:text-orange-400 line-clamp-2">
                {order.flagged_reason}
              </p>
            </div>
          </div>
          <div className="text-right md:text-left lg:text-right space-y-1">
            <div>
              <span className="text-sm text-secondary-light dark:text-secondary-dark font-medium">Cart Total</span>
              <p className="font-semibold text-lg">{order.cart_total}</p>
            </div>
            <div className="mt-2">
              <span className="text-sm text-secondary-light dark:text-secondary-dark font-medium">Submitted</span>
              <p className="text-sm text-secondary-light dark:text-secondary-dark">{order.submitted_at}</p>
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
};

export default PendingCartItem;
