import { notFound } from 'next/navigation';

import { JustificationPanel } from '@/components/features/JustificationPanel';
import { TrustLedgerPanel } from '@/components/features/TrustLedgerPanel';
import { DecisionMatrixPanel } from '@/components/features/DecisionMatrixPanel';
import { getOrderDetails } from '@/lib/api'; // Assuming this function exists and fetches data
import { PendingOrder } from '@/lib/types';

// Ensure this page is a Server Component
export default async function OrderDetailPage({ params }: { params: { order_id: string } }) {
  const orderId = params.order_id;

  let orderDetails: PendingOrder;
  try {
    // Fetch order details on the server
    // Assuming getOrderDetails is an async function that fetches data from your API
    orderDetails = await getOrderDetails(orderId);
  } catch (error) {
    // If order not found or an error occurs during fetch, show a 404 page
    console.error(`Failed to fetch order details for order ${orderId}:`, error);
    notFound();
  }

  // Handle the case where the order might exist but has no details (unlikely but good practice)
  if (!orderDetails) {
    notFound();
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Review Order #{orderId}</h1>

      {/* Justification Panel */} 
      <div className="mb-6">
        <JustificationPanel
          justification={orderDetails.justification}
          policyFlag={orderDetails.policyFlag}
        />
      </div>

      {/* Trust Ledger and Decision Matrix Panels */} 
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <TrustLedgerPanel 
            items={orderDetails.items}
            cartTotal={orderDetails.cartTotal}
          />
        </div>
        <div className="lg:col-span-1">
          <DecisionMatrixPanel 
            orderId={orderId}
            // These handlers will be implemented within DecisionMatrixPanel itself
            // The parent passes down the orderId and expects the child to handle its own state and actions
            onApprove={async (notes: string) => {
              // This placeholder will be removed as DecisionMatrixPanel handles its own API calls
              console.log('Approve called with notes:', notes);
            }}
            onReject={async (notes: string) => {
              // This placeholder will be removed as DecisionMatrixPanel handles its own API calls
              console.log('Reject called with notes:', notes);
            }}
            isSubmitting={false} // This will be managed by DecisionMatrixPanel
          />
        </div>
      </div>
    </div>
  );
}
