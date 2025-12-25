import os
os.chdir(r'D:\HKUST\5054_Statistical_Machine_Learning\Assignments\HW1')

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import summary_table
import warnings
warnings.filterwarnings('ignore')

## Load the data
df = pd.read_csv('Life Expectancy Data.csv')
# print(df.head())

## Data Preprocessing
# Drop 'Country' as instructed
df = df.drop(columns=['Country'], errors='ignore')

# Convert 'Status' to dummy variables (0 for Developing, 1 for Developed)
df['Status'] = df['Status'].map({'Developing': 0, 'Developed': 1})

# Check column names for any trailing spaces!!!
print(df.columns.tolist()) 

# Check for missing values and drop rows with any missing values
print(f"\nMissing values number before dropping:")
print(df.isnull().sum())
df = df.dropna()
print(f"Shape of Dataframe after dropping NA: {df.shape}")

# Define y as 'Life expectancy' and X as all other predictors
predictors = [col for col in df.columns if col != 'Life expectancy '] #'Life expectancy ' has a trailing space
X = df[predictors]
y = df['Life expectancy ']

# Add a constant term for the intercept
X = sm.add_constant(X)

## Fit the full linear model
full_model = sm.OLS(y, X).fit()

## Question 1
print(f"\nQuestion 1: Full Model Summary")
print(full_model.summary())

# To identify significant predicting variables, we look for which variables p-values < 0.05
significant_vars = full_model.pvalues[full_model.pvalues < 0.05].index.tolist()
print(f"\nSignificant predicting variables (p < 0.05): {significant_vars}")

## Question 2
print(f"\nQuestion 2: 95% CI for 'Adult Mortality' and 'HIV/AIDS'")

# Get 95% confidence intervals for all coefficients
conf_int_95 = full_model.conf_int(alpha=0.05) # alpha=0.05 for 95% CI

adult_mort_ci = conf_int_95.loc['Adult Mortality']
hiv_aids_ci = conf_int_95.loc[' HIV/AIDS'] # Note the leading space in ' HIV/AIDS'

print(f"Adult Mortality 95% CI: [{adult_mort_ci[0]:.4f}, {adult_mort_ci[1]:.4f}]")
print(f"HIV/AIDS 95% CI: [{hiv_aids_ci[0]:.4f}, {hiv_aids_ci[1]:.4f}]")

# Check if the entire CI is negative
# If the upper bound of the CI is less than 0, we can be confident that the predictor has a negative impact
if adult_mort_ci[1] < 0:
    print("Yes, we are confident Adult Mortality has a negative impact (CI entirely negative).")
else:
    print("No, we cannot be fully confident (CI includes zero or positive values).")

if hiv_aids_ci[1] < 0:
    print("Yes, we are confident HIV/AIDS has a negative impact (CI entirely negative).")
else:
    print("No, we cannot be fully confident (CI includes zero or positive values).")

## Question 3
print("\nQuestion 3: 97% CI for 'Schooling' and 'Alcohol'")

# 97% confidence intervals (alpha=0.03)
conf_int_97 = full_model.conf_int(alpha=0.03)

schooling_ci = conf_int_97.loc['Schooling']
alcohol_ci = conf_int_97.loc['Alcohol']

print(f"Schooling 97% CI: [{schooling_ci[0]:.4f}, {schooling_ci[1]:.4f}]")
print(f"Alcohol 97% CI: [{alcohol_ci[0]:.4f}, {alcohol_ci[1]:.4f}]")

# Interpretation
# If the entire CI is positive, we can be confident the predictor has a positive impact
# If the entire CI is negative, we can be confident the predictor has a negative impact
# If the CI includes zero, we cannot be confident about the direction of the impact
if schooling_ci[0] > 0:
    print("Schooling has a positive impact on life expectancy (CI entirely positive).")
elif schooling_ci[1] < 0:
    print("Schooling has a negative impact on life expectancy (CI entirely negative).")
else:
    print("The impact of Schooling is not statistically clear at 97% confidence (CI includes zero).")

if alcohol_ci[0] > 0:
    print("Alcohol has a positive impact on life expectancy (CI entirely positive).")
elif alcohol_ci[1] < 0:
    print("Alcohol has a negative impact on life expectancy (CI entirely negative).")
else:
    print("The impact of Alcohol is not statistically clear at 97% confidence (CI includes zero).")

## Question 4
print("\nQuestion 4: Top 7 predictors by p-value")

# Get p-values for all predictors and drop the intercept
p_values = full_model.pvalues.drop('const').sort_values()

# Get the top 7 most significant (the lowest p-value the better)
top_7_predictors = p_values.head(7).index.tolist()
print(f"Top 7 most influential predictors by p-value: {top_7_predictors}")

## Fit a smaller model with top 7 predictors
X_small = df[top_7_predictors]
X_small = sm.add_constant(X_small) # Add intercept
small_model = sm.OLS(y, X_small).fit()

print("\nSmaller Model Summary:")
print(small_model.summary())
print(small_model.conf_int())
print(small_model.pvalues)
print(small_model.rsquared)
print(small_model.rsquared_adj)
print(small_model.tvalues)
print(small_model.fvalue)
print(small_model.mse_resid)
print(small_model.bse)

## Question 5
print("\nQuestion 5: Prediction with 99% CI")

# Create a new observation DataFrame
new_obs_data = {
    'Year': [2008],
    'Status': [1], # Developed
    'Adult Mortality': [125],
    'infant deaths': [94],
    'Alcohol': [4.1],
    'percentage expenditure': [100],
    'Hepatitis B': [20],
    'Measles': [13],
    'BMI': [55],
    'under-five deaths ': [2],
    'Polio': [12],
    'Total expenditure': [5.9],
    'Diphtheria': [12],
    ' HIV/AIDS': [0.5],
    'GDP': [5892],
    'Population': [1.34e6],
    'thinness  1-19 years': [0], # Assuming 0 because provided
    'thinness 5-9 years': [0],   # Assuming 0 because provided
    'Income composition of resources': [0.9],
    'Schooling': [18]
}

# Since our small model only uses the top 7 predictors, we must ensure the new_obs has the same columns as X_small (excluding 'const')
new_obs = pd.DataFrame(new_obs_data)
new_obs_small = new_obs[top_7_predictors] # Select only the top 7
new_obs_small = sm.add_constant(new_obs_small, has_constant='add') # Add intercept

# Make prediction
prediction = small_model.get_prediction(new_obs_small)
# Get 99% confidence interval (alpha=0.01)
pred_summary = prediction.summary_frame(alpha=0.01)
print(pred_summary.head())

print(f"Predicted Life Expectancy: {pred_summary['mean'].iloc[0]:.2f}")
print(f"99% Confidence Interval: [{pred_summary['mean_ci_lower'].iloc[0]:.2f}, {pred_summary['mean_ci_upper'].iloc[0]:.2f}]")

## Question 6
print("\n Question 6: AIC Comparison")

print(f"AIC of Full Model: {full_model.aic:.2f}")
print(f"AIC of Smaller Model: {small_model.aic:.2f}")
print(f"BIC of Full Model: {full_model.bic:.2f}")
print(f"BIC of Smaller Model: {small_model.bic:.2f}")
print(f"Adjusted R-squared of Full Model: {full_model.rsquared_adj:.4f}")
print(f"Adjusted R-squared of Smaller Model: {small_model.rsquared_adj:.4f}")

n = len(y)
p_full = full_model.params.shape[0]   
p_small = small_model.params.shape[0]
sigma2_full = full_model.mse_resid   
Cp_full = full_model.ssr / sigma2_full - (n - 2 * p_full)
Cp_small = small_model.ssr / sigma2_full - (n - 2 * p_small)
print("\nMallows' Cp:")
print(f"Cp (Full model): {Cp_full:.4f}")
print(f"Cp (Small model): {Cp_small:.4f}")

from sklearn.model_selection import KFold
def cv_mse(columns, X_df, y_series, k=5, random_state=42):
    kf = KFold(n_splits=k, shuffle=True, random_state=random_state)
    mses = []
    for train_idx, test_idx in kf.split(X_df):
        X_train = X_df.iloc[train_idx][columns]
        X_test = X_df.iloc[test_idx][columns]
        y_train = y_series.iloc[train_idx]
        y_test = y_series.iloc[test_idx]
        X_train_c = sm.add_constant(X_train, has_constant='add')
        X_test_c = sm.add_constant(X_test, has_constant='add')
        mdl = sm.OLS(y_train, X_train_c).fit()
        preds = mdl.predict(X_test_c)
        mses.append(np.mean((y_test - preds) ** 2))
    return np.mean(mses), np.std(mses)


full_columns = predictors  
mse_full_mean, mse_full_std = cv_mse(full_columns, df, y, k=5)
mse_small_mean, mse_small_std = cv_mse(top_7_predictors, df, y, k=5)

print("\n5-fold CV MSE:")
print(f"Full model CV MSE: {mse_full_mean:.4f} ± {mse_full_std:.4f}")
print(f"Small model CV MSE: {mse_small_mean:.4f} ± {mse_small_std:.4f}")

print("\n End of Problem 2")
