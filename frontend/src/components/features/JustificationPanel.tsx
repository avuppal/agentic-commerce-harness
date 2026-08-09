import React from 'react';

interface JustificationPanelProps {
  originalPrompt: string;
  groundedIntent: string;
  policyFlagReason: string;
}

const JustificationPanel: React.FC<JustificationPanelProps> = ({
  originalPrompt,
  groundedIntent,
  policyFlagReason,
}) => {
  return (
    <div className="border rounded-lg bg-surface p-6 shadow-sm">
      <div className="border-b pb-4 mb-6">
        <h2 className="text-xl font-semibold text-text-primary">Justification & Policy Flag</h2>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h3 className="text-lg font-medium text-text-primary mb-2">Original Prompt</h3>
          <blockquote className="text-text-secondary text-base italic p-4 border-l-4 border-primary-500 bg-background-light dark:bg-surface-dark rounded-r-md">
            {originalPrompt}
          </blockquote>

          <h3 className="text-lg font-medium text-text-primary mt-6 mb-2">Grounded Intent</h3>
          <pre className="text-sm font-mono bg-slate-100 dark:bg-slate-800 p-3 rounded-md whitespace-pre-wrap break-words">
            <code>{groundedIntent}</code>
          </pre>
        </div>
        <div>
          <div className="bg-warning-bg-light dark:bg-warning-bg-dark p-4 rounded-lg flex items-start gap-3 border border-warning-500">
            <svg className="w-6 h-6 text-warning-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
            <div>
              <p className="font-semibold text-warning-500">Flagged: {policyFlagReason.split(':')[0].trim()}</p>
              <p className="text-secondary text-sm mt-1 break-words">
                {policyFlagReason.split(':')[1] ? policyFlagReason.split(':')[1].trim() : policyFlagReason}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JustificationPanel;
