import time
from collections import defaultdict, deque

class PolicyEnforcer:
    def __init__(self):
        # REQ-SPGE-01: Spend Limits
        # Stores the total spent amount for each agent execution context.
        # Format: {agent_execution_id: total_spent}
        self.spend_limits = defaultdict(float)
        self.transaction_limits = {
            "default": 1000.0  # Default hard-stop financial transaction limit
            # Add more specific limits per agent context if needed
        }

        # REQ-SPGE-02: Velocity Controls
        # Stores purchase timestamps for rate limiting.
        # Format: {agent_execution_id: {category: deque([timestamp1, timestamp2]), ...}}
        self.purchase_history = defaultdict(lambda: defaultdict(deque))
        self.purchase_frequency_limits = {
            "default": {
                "time_window_seconds": 60,  # e.g., 1 minute
                "max_purchases": 5
            }
            # Add more specific limits per category, vendor, etc.
        }

        # For in-memory cleanup as per architect's guidance
        self.cleanup_interval_seconds = 300 # Clean up every 5 minutes
        self.last_cleanup_time = time.time()

    def _cleanup_old_records(self):
        """Cleans up old records from purchase_history to prevent unbounded memory growth."""
        current_time = time.time()
        if current_time - self.last_cleanup_time > self.cleanup_interval_seconds:
            # Define a cutoff time for records to keep (e.g., 24 hours)
            cutoff_time = current_time - (24 * 60 * 60)
            
            for agent_id in list(self.purchase_history.keys()):
                for category in list(self.purchase_history[agent_id].keys()):
                    # Remove timestamps older than cutoff_time
                    while self.purchase_history[agent_id][category] and self.purchase_history[agent_id][category][0] < cutoff_time:
                        self.purchase_history[agent_id][category].popleft()
                    
                    # If a category for an agent is now empty, remove it
                    if not self.purchase_history[agent_id][category]:
                        del self.purchase_history[agent_id][category]
                
                # If an agent has no more categories, remove the agent entry
                if not self.purchase_history[agent_id]:
                    del self.purchase_history[agent_id]
            
            self.last_cleanup_time = current_time

    def enforce_spend_limit(self, agent_execution_id: str, transaction_amount: float) -> bool:
        """Enforces hard-stop financial transaction limits.

        Args:
            agent_execution_id: Unique identifier for the agent's execution context.
            transaction_amount: The amount of the current transaction.

        Returns:
            True if the transaction is allowed, False otherwise.
        """
        self._cleanup_old_records() # Ensure cleanup happens before checking limits
        
        current_spend = self.spend_limits.get(agent_execution_id, 0.0)
        limit = self.transaction_limits.get("default", float('inf')) # Use default limit
        
        if current_spend + transaction_amount > limit:
            return False  # Exceeds limit
        
        # If allowed, update the spent amount for the next check
        self.spend_limits[agent_execution_id] = current_spend + transaction_amount
        return True

    def enforce_velocity_controls(self, agent_execution_id: str, purchase_category: str, vendor_domain: str) -> bool:
        """Enforces rate-limiting purchases by frequency, category, and vendor domain.

        Args:
            agent_execution_id: Unique identifier for the agent's execution context.
            purchase_category: The category of the purchased item.
            vendor_domain: The domain of the vendor.

        Returns:
            True if the purchase is allowed, False otherwise.
        """
        self._cleanup_old_records() # Ensure cleanup happens before checking limits

        current_time = time.time()
        
        # Check limits for the given category (can be extended to check vendor_domain too)
        # For simplicity, we'll use the 'default' category limits here.
        # In a real system, you'd have more granular checks based on `purchase_category` and `vendor_domain`.
        limit_config = self.purchase_frequency_limits.get("default", {"time_window_seconds": 60, "max_purchases": 5})
        time_window = limit_config["time_window_seconds"]
        max_purchases = limit_config["max_purchases"]

        # Get the deque for this agent and category
        timestamps = self.purchase_history[agent_execution_id][purchase_category]

        # Remove timestamps older than the current time window
        while timestamps and timestamps[0] < current_time - time_window:
            timestamps.popleft()

        # Check if the number of purchases within the window exceeds the limit
        if len(timestamps) >= max_purchases:
            return False  # Exceeds velocity limit

        # If allowed, add the current purchase timestamp
        timestamps.append(current_time)
        return True

    def reset_agent_spend(self, agent_execution_id: str):
        """Resets the spend limit for a given agent execution context."""
        if agent_execution_id in self.spend_limits:
            del self.spend_limits[agent_execution_id]

    def reset_agent_purchase_history(self, agent_execution_id: str):
        """Resets the purchase history for a given agent execution context."""
        if agent_execution_id in self.purchase_history:
            del self.purchase_history[agent_execution_id]

