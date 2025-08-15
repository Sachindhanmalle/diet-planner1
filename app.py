import os
import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

# Load pre-trained model and food data
model = joblib.load('calorie_predictor.pkl')
# food_data = pd.read_csv('D:\predict\Food and Calories - Sheet1.csv')
 
food_data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'Food and Calories - Sheet1.csv'))


def calculate_bmr(age, weight, height, gender):
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height * 100) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height * 100) - (4.330 * age)
    return bmr * 1.55  # Moderate activity level

def create_meal_plan(total_calories):
    breakfast_percent = 0.25
    lunch_percent = 0.30
    dinner_percent = 0.30
    snacks_percent = 0.15
    print(type(total_calories),total_calories)
    total_calories=int(total_calories)

    meal_plan = {
        'total_calories': int(total_calories),
        'breakfast': create_meal_subset(total_calories * breakfast_percent),
        'lunch': create_meal_subset(total_calories * lunch_percent),
        'dinner': create_meal_subset(total_calories * dinner_percent),
        'snacks': create_meal_subset(total_calories * snacks_percent)
    }
    return meal_plan


def create_meal_subset(target_calories):
    # Ensure 'Calories' column is cleaned and converted to numeric
    food_data['Calories'] = food_data['Calories'].astype(str)  # Convert all to string
    food_data['Calories'] = food_data['Calories'].str.replace('cal', '', regex=False).str.strip()
    food_data['Calories'] = pd.to_numeric(food_data['Calories'], errors='coerce')  # Convert to float, handle invalid entries
    
    # Drop rows with invalid or NaN calorie values
    food_data_cleaned = food_data.dropna(subset=['Calories'])
    
    # Filter subset where calories are less than or equal to 80% of target calories
    subset = food_data_cleaned[food_data_cleaned['Calories'] <= target_calories * 0.8]
    
    # If there are not enough items to sample, handle it gracefully
    if len(subset) < 3:
        selected_items = subset.sample(n=len(subset))  # Sample as many as available
    else:
        selected_items = subset.sample(n=3)
    
    # Calculate total calories and prepare the list of selected items
    calories = selected_items['Calories'].sum()
    items = [{'food': row['Food'], 'calories': row['Calories']} for _, row in selected_items.iterrows()]
    
    return {
        'calories': int(calories),
        'items': items
    }




@app.route('/')
def serve_index():
    return send_from_directory('.', 'app.html')

@app.route('/predict-meal-plan', methods=['POST'])
def predict_meal_plan():
    data = request.json
    print(data)
    
    try:
        total_calories = calculate_bmr(
            int(data['age']), 
            float(data['weight']), 
            float(data['height']), 
            data['gender']
        )
        meal_plan = create_meal_plan(total_calories)
        return jsonify(meal_plan)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
