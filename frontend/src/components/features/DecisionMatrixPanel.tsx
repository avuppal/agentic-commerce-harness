// frontend/src/components/features/DecisionMatrixPanel.tsx

import React, { useState } from 'react';
import { Button } from '../ui/Button';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { approveOrder, rejectOrder } from '../../lib/api';

interface DecisionMatrixPanelProps {
  orderId: string;
}

export const DecisionMatrixPanel: React.FC<DecisionMatrixPanelProps> = ({ orderId }) => {
  const [notes, setNotes] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  const [isDecisionMade, setIsDecisionMade] = useState(false);

  const handleDecision = async (action: 'approve' | 'reject') => {
    setIsLoading(true);
    setFeedback(null);
    try {
      const apiCall = action === 'approve' ? approveOrder : rejectOrder;
      const response = await apiCall(orderId, notes);
      
      setFeedback({ type: 'success', message: `Order successfully ${action}d.` });
      setIsDecisionMade(true);
    } catch (error) {
      console.error(`Failed to ${action} order:`, error);
      setFeedback({ type: 'error', message: `Failed to ${action} the order. Please try again.` });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Decision</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <div>
          <label htmlFor="notes" className="block text-sm font-medium text-text-secondary-light dark:text-text-secondary-dark mb-2">
            Add optional notes for the agent:
          </label>
          <textarea
            id="notes"
            rows={4}
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            disabled={isLoading || isDecisionMade}
            className="w-full rounded-md border border-border-light dark:border-border-dark bg-background-light dark:bg-slate-700 p-2 text-sm placeholder:text-text-secondary-light dark:placeholder:text-text-secondary-dark focus:ring-2 focus:ring-primary-500"
            placeholder="e.g., 'Approved, but find a cheaper organic option next time.'"
          />
        </div>

        {feedback && (
          <div
            className={`p-3 rounded-lg text-sm ${
              feedback.type === 'success'
                ? 'bg-success-bg-light dark:bg-success-bg-dark text-green-800 dark:text-green-200'
                : 'bg-error-bg-light dark:bg-error-bg-dark text-red-800 dark:text-red-200'
            }`}
          >
            {feedback.message}
          </div>
        )}

        <div className="mt-2 grid grid-cols-2 gap-4">
          <Button
            variant="outline"
            onClick={() => handleDecision('reject')}
            disabled={isLoading || isDecisionMade}
          >
            Reject
          </Button>
          <Button
            variant="success"
            onClick={() => handleDecision('approve')}
            disabled={isLoading || isDecisionMade}
          >
            {isLoading ? 'Submitting...' : 'Approve & Execute'}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};
