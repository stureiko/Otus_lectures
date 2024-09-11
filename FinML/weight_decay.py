import numpy as np
import matplotlib.pyplot as plt


class LinearRegressionWithWeightDecay:
    def __init__(self, alpha=0.01, lambda_val=0.1, epochs=1000):
        self.alpha = alpha  # learning rate
        self.lambda_val = lambda_val  # weight decay parameter
        self.epochs = epochs  # number of iterations for gradient descent
        self.weights = None  # weights for linear regression

    def fit(self, X, y):
        # Initialize weights with zeros
        self.weights = np.zeros(X.shape[1])
        m = len(y)  # number of training examples
        
        for _ in range(self.epochs):
            # Compute predictions
            y_pred = np.dot(X, self.weights)
            
            # Compute error and gradient
            error = y_pred - y
            gradient = np.dot(X.T, error) / m
            
            # Update weights with gradient descent and weight decay
            self.weights -= self.alpha * (gradient + self.lambda_val * self.weights)  # update rule with weight decay

    def predict(self, X):
        return np.dot(X, self.weights)

# Example usage:
X_train = np.array([[1, 2], [2, 3], [3, 4]])
y_train = np.array([3, 4, 5])

# Instantiate and train the model with weight decay
model = LinearRegressionWithWeightDecay(alpha=0.01, lambda_val=0.1, epochs=1000)
model.fit(X_train, y_train)

# Print learned weights
print("Learned weights:", model.weights)


# Define different weight decay hyperparameters to test
lambda_values = [0, 0.01, 0.1, 1]

# Train linear regression models with different weight decay values
weights_history = []
for lambda_val in lambda_values:
    model = LinearRegressionWithWeightDecay(alpha=0.01, lambda_val=lambda_val, epochs=1000)
    model.fit(X_train, y_train)
    weights_history.append(model.weights)

# Plot the impact of different weight decay hyperparameters on model performance
plt.figure(figsize=(10, 6))
for i, weights in enumerate(weights_history):
    plt.plot(range(len(weights)), weights, label=f"lambda={lambda_values[i]}")
plt.title("Impact of Weight Decay on Model Weights")
plt.xlabel("Iterations")
plt.ylabel("Weights")
plt.legend()
plt.grid(True)
plt.show()
