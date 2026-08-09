import React from 'react';
import { VCTrustBadge } from './VCTrustBadge'; // Assuming VCTrustBadge is in the same directory or accessible path
import { CartItem, VCCredential } from '../lib/types';

// Define the props for TrustLedgerPanel
interface TrustLedgerPanelProps {
  cartItems: CartItem[];
}

export const TrustLedgerPanel: React.FC<TrustLedgerPanelProps> = ({ cartItems }) => {
  return (
    <div className="p-6 border rounded-lg bg-surface shadow-sm">
      <h2 className="text-xl font-semibold text-text-primary mb-4">Trust Ledger</h2>
      {cartItems.length === 0 ? (
        <p className="text-text-secondary">No items in the cart.</p>
      ) : (
        <ul className="divide-y divide-border">
          {cartItems.map((item) => (
            <li key={item.id} className="py-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div className="flex-grow">
                <p className="font-medium text-text-primary">{item.name}</p>
                <p className="text-text-secondary text-sm">SKU: {item.id}</p>
              </div>
              
              <div className="flex items-center gap-4">
                <div className="flex flex-wrap gap-2">
                  {item.credentials.map((cred, index) => (
                    <VCTrustBadge key={index} credential={cred} />
                  ))}
                </div>
                <div className="text-right whitespace-nowrap">
                  <p className="text-secondary text-sm">{item.quantity} x ${item.price.toFixed(2)}</p>
                  <p className="font-semibold text-lg">${(item.quantity * item.price).toFixed(2)}</p>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
