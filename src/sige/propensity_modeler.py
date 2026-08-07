class PropensityModeler:
    """Calculates the Propensity Score for a given product based on various factors."""

    def __init__(self, w1: float = 0.5, w2: float = 0.3, w3: float = 0.2):
        """Initializes the PropensityModeler with default weights."""
        self.weights = {
            'w1': w1,  # Clickstream weight
            'w2': w2,  # Velocity multiplier weight
            'w3': w3   # Friction multiplier weight
        }

    def calculate_score(self, C: float, V: float, F: float) -> float:
        """Calculates the Propensity Score using the formula: (w1 * C) + (w2 * V) - (w3 * F)."""
        return (self.weights['w1'] * C) + (self.weights['w2'] * V) - (self.weights['w3'] * F)

    def update_weights(self, w1: float = None, w2: float = None, w3: float = None):
        """Updates the model's weights. Unspecified weights remain unchanged."""
        if w1 is not None:
            self.weights['w1'] = w1
        if w2 is not None:
            self.weights['w2'] = w2
        if w3 is not None:
            self.weights['w3'] = w3


# Example Usage (optional, for demonstration)
if __name__ == '__main__':
    model = PropensityModeler()
    clickstream_data = 0.8
    velocity_data = 0.9
    friction_data = 0.3

    score = model.calculate_score(clickstream_data, velocity_data, friction_data)
    print(f"Initial Score: {score}")
