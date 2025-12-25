import os
os.chdir(r'D:\HKUST\5054_Statistical_Machine_Learning\Assignments\HW1')

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import time

train_df = pd.read_csv('boston_housing_train.csv')
test_df = pd.read_csv('boston_housing_test.csv')
print(train_df.head())
print(train_df.columns.tolist)
X_train = train_df.drop(columns=['medv'])
y_train = train_df['medv']
X_test = test_df.drop(columns=['medv'])
y_test = test_df['medv']

# Define the KNN Regressor class
class KNNRegressor:
    def __init__(self, k=5):
        self.k = k
        self.X_train = None
        self.y_train = None

    def fit(self, X_train, y_train):
        """
        Save the training data.
        """
        self.X_train = np.array(X_train)
        self.y_train = np.array(y_train)
    
    def euclidean_distance(self, x1, x2):
        """
        Calculate the Euclidean distance between two points.
        """
        return np.sqrt(np.sum((x1 - x2) ** 2))
    
    def predict_single(self, x):
        """
        Forecast the target value for a single sample x.
        """
        # Calculate distances from x to all training samples
        distances = [self.euclidean_distance(x, x_train) for x_train in self.X_train]        
        # Find the indices of the k nearest neighbors
        k_indices = np.argsort(distances)[:self.k]        
        # Get the labels of the k nearest neighbors
        k_nearest_labels = self.y_train[k_indices]        
        # Return the mean of the k nearest labels
        return np.mean(k_nearest_labels)
    
    def predict(self, X_test):
        """
        Predict the target values for the test set.
        """
        X_test = np.array(X_test)
        predictions = [self.predict_single(x) for x in X_test]
        return np.array(predictions)
    
## Question 1 
print("Question 1: KNN Regression without Standardization\n")
results = []
# Fit and evaluate KNN for K from 1 to 20
for k in range(1, 21): 
    knn = KNNRegressor(k=k)
    
    start_time = time.time()
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    end_time = time.time()
    
    mse = mean_squared_error(y_test, y_pred)
    running_time = end_time - start_time
    
    results.append({
        'K': k,
        'MSE': mse,
        'Running Time (s)': running_time
    })
    
    print(f"K={k:2d} | MSE: {mse:.4f} | Time: {running_time:.4f}s")

# Find the best K (the one with the lowest MSE)
best_k_no_std = min(results, key=lambda x: x['MSE'])['K']
print(f"Best K (without standardization): {best_k_no_std}\n")

## Question 2
# Standardize the features
print("Question 2: KNN Regression with Standardization\n")
X_train_mean = X_train.mean()
X_train_std = X_train.std()

X_train_scaled = (X_train - X_train_mean) / X_train_std
X_test_scaled = (X_test - X_train_mean) / X_train_std

# repeat the Question 1 process with standardized data
results_scaled = []

for k in range(1, 21):
    knn = KNNRegressor(k=k)
    
    start_time = time.time()
    knn.fit(X_train_scaled, y_train)
    y_pred_scaled = knn.predict(X_test_scaled)
    end_time = time.time()
    
    mse = mean_squared_error(y_test, y_pred_scaled)
    running_time = end_time - start_time
    
    results_scaled.append({
        'K': k,
        'MSE': mse,
        'Running Time (s)': running_time
    })
    
    print(f"K={k:2d} | MSE: {mse:.4f} | Time: {running_time:.4f}s")

# Find the best K 
best_k_with_std = min(results_scaled, key=lambda x: x['MSE'])['K']
print(f"Best K (with standardization): {best_k_with_std}\n")

## Question 3
print("Question 3: Comparison of Standardization Effect\n")
# Does standardization improve performance?
best_mse_no_std = min(results, key=lambda x: x['MSE'])['MSE']
best_mse_with_std = min(results_scaled, key=lambda x: x['MSE'])['MSE']
print(f"Best MSE without standardization: {best_mse_no_std:.4f}")
print(f"Best MSE with standardization: {best_mse_with_std:.4f}")

if best_mse_with_std < best_mse_no_std:
    print("\nYes, standardization improves performance.")
else:
    print("\nNo, standardization does not improve performance.")
