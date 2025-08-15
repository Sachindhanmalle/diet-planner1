document.addEventListener('DOMContentLoaded', () => {
    const mealForm = document.getElementById('meal-form');
    const mealResults = document.getElementById('meal-results');

    mealForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(mealForm);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/predict-meal-plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            displayMealPlan(result);
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to generate meal plan. Please try again.');
        }
    });

    function displayMealPlan(mealPlan) {
        const calorieInfo = document.getElementById('calorie-info');
        const breakfastDiv = document.getElementById('breakfast');
        const lunchDiv = document.getElementById('lunch');
        const dinnerDiv = document.getElementById('dinner');
        const snacksDiv = document.getElementById('snacks');

        calorieInfo.innerHTML = `<p>Recommended Daily Calories: ${mealPlan.total_calories} kcal</p>`;
        breakfastDiv.innerHTML = `<h3>Breakfast (${mealPlan.breakfast.calories} kcal)</h3>${formatMealItems(mealPlan.breakfast.items)}`;
        lunchDiv.innerHTML = `<h3>Lunch (${mealPlan.lunch.calories} kcal)</h3>${formatMealItems(mealPlan.lunch.items)}`;
        dinnerDiv.innerHTML = `<h3>Dinner (${mealPlan.dinner.calories} kcal)</h3>${formatMealItems(mealPlan.dinner.items)}`;
        snacksDiv.innerHTML = `<h3>Snacks (${mealPlan.snacks.calories} kcal)</h3>${formatMealItems(mealPlan.snacks.items)}`;

        mealResults.classList.remove('hidden');
    }

    function formatMealItems(items) {
        return items.map(item => `<p>${item.food} (${item.calories} kcal)</p>`).join('');
    }
});