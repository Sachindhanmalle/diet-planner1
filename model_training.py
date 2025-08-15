import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Simulate data generation for BMR prediction
np.random.seed(42)

def generate_synthetic_data(n_samples=1000):
    # Generate synthetic training data
    ages = np.random.randint(18, 65, n_samples)
    weights = np.random.uniform(50, 100, n_samples)
    heights = np.random.uniform(1.5, 2.0, n_samples)
    genders = np.random.choice(['male', 'female'], n_samples)
    
    def calculate_bmr(age, weight, height, gender):
        if gender == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height * 100) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height * 100) - (4.330 * age)
        return bmr * 1.55  # Moderate activity level
    
    calories = [calculate_bmr(age, weight, height, gender) 
                for age, weight, height, gender in zip(ages, weights, heights, genders)]
    
    data = pd.DataFrame({
        'age': ages,
        'weight': weights,
        'height': heights,
        'gender': genders,
        'calories': calories
    })
    
    return data

# Generate and split data
data = generate_synthetic_data()
X = data[['age', 'weight', 'height']]
X = pd.get_dummies(pd.concat([X, pd.get_dummies(data['gender'], prefix='gender')], axis=1))
y = data['calories']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, 'calorie_predictor.pkl')
print("Model trained and saved successfully!")