import random
import mysql.connector
from app.Calculator import calculate_macronutrients
from scipy.optimize import minimize
from flask import request, jsonify

# Database Connection
def get_db_connection():
    """Establishes a connection to the MySQL database using predefined credentials."""
    return mysql.connector.connect(
        host="",
        port="",
        user="",
        password="",
        database=""
    )

# Save user details to the database
def save_user_details(user_id, user_data):
    """
    Updates user details in the User table of the database.
    
    Args:
        user_id: Unique identifier for the user.
        user_data: Dictionary containing user details (age, weight, height, gender, activity, goal, diet).
    """
    conn = get_db_connection() # Get database connection
    cursor = conn.cursor() # Create cursor for executing SQL queries
    meal_variety = user_data.get('meal_variety')
    try:
        # Update user details in the User table
        cursor.execute("""
            UPDATE User 
            SET age = %s, weight = %s, height = %s, gender = %s, activity_level = %s, goal = %s, diet = %s, meal_variety = %s
            WHERE user_id = %s
        """, (
            user_data['age'],
            user_data['weight'],
            user_data['height'],
            1 if user_data['gender'] == 'male' else 0, # Convert gender to binary (1 for male, 0 for female)
            user_data['activity'],
            user_data['goal'],
            user_data['diet'],
            meal_variety,
            user_id
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Retrieve user details from the database
def get_user_details(user_id):
    """
    Retrieves user details from the User table for a given user ID.
    
    Args:
        user_id: Unique identifier for the user.
    
    Returns:
        Dictionary with user details or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT age, weight, height, gender, activity_level, goal, diet, meal_variety
        FROM User 
        WHERE user_id = %s
    """, (user_id,)) # Execute query with user_id parameter
    user_data = cursor.fetchone() # Fetch single row of user data
    conn.close()
    if user_data:
        # Transform data to match expected format
        user_data['gender'] = '' if user_data['gender'] is None else 'male' if user_data['gender'] == 1 else 'female' # Convert binary gender to string
        user_data['activity'] = user_data.pop('activity_level') # Rename activity_level to activity
        user_data['preferences'] = '' # Default empty preferences
        user_data['meal_variety'] = user_data.get('meal_variety') # Default to 50 if not set
    return user_data

# Save a meal plan to the database (overwrites previous plan)
def save_meal_plan(user_id, meal_plan):
    """
    Saves a 7-day meal plan to the Diet_Plan_Food table, overwriting any existing plan for the user.
    
    Args:
        user_id: Unique identifier for the user.
        meal_plan: List of dictionaries representing the 7-day meal plan.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete existing meal plan for the user to avoid duplicates
        cursor.execute("DELETE FROM Diet_Plan_Food WHERE user_id = %s", (user_id,))
        # Save new meal plan
        for day in meal_plan:
            for meal_type in ["Breakfast", "Lunch", "Dinner"]: # Iterate through meal types
                for ingredient, details in day[meal_type].items(): # Iterate through ingredients
                    # Find food_id for the ingredient
                    cursor.execute("SELECT food_id FROM Food WHERE food_item = %s", (ingredient,))
                    food_id_result = cursor.fetchone() # Fetch food_id
                    if not food_id_result:
                        print(f"Warning: Food item '{ingredient}' not found in Food table. Skipping.") # Log missing food item
                        continue
                    food_id = food_id_result[0] # Extract food_id
                    # Insert meal plan entry
                    cursor.execute("""
                        INSERT INTO Diet_Plan_Food (user_id, day, meal_type, food_id, quantity)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (user_id, day["Day"], meal_type, food_id, details["servings"])) # Insert meal data
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Update a specific day in the meal plan
def update_meal_plan_day(user_id, day_to_regenerate, regenerated_day):
    """
    Updates a specific day's meal plan in the Diet_Plan_Food table.
    
    Args:
        user_id: Unique identifier for the user.
        day_to_regenerate: Day number to update (1-7).
        regenerated_day: Dictionary containing the updated meal plan for the day.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete existing meals for the specified day
        cursor.execute("""
            DELETE FROM Diet_Plan_Food 
            WHERE user_id = %s AND day = %s
        """, (user_id, day_to_regenerate)) # Remove old meals
        # Insert new meals for the day
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            for ingredient, details in regenerated_day[meal_type].items():
                cursor.execute("SELECT food_id FROM Food WHERE food_item = %s", (ingredient,)) # Get food_id
                food_id_result = cursor.fetchone()
                if not food_id_result:
                    print(f"Warning: Food item '{ingredient}' not found in Food table. Skipping.") # Log missing food
                    continue
                food_id = food_id_result[0] # Extract food_id
                # Insert new meal plan entry
                cursor.execute("""
                    INSERT INTO Diet_Plan_Food (user_id, day, meal_type, food_id, quantity)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, day_to_regenerate, meal_type, food_id, details["servings"])) # Insert new meal
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# Retrieve the last meal plan for a user
def get_last_meal_plan(user_id):
    """
    Retrieves the most recent meal plan for a user from the database.
    
    Args:
        user_id: Unique identifier for the user.
    
    Returns:
        Tuple of (meal_plan, daily_requirements) or (None, None) if no plan exists.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Fetch meal plan foods with nutritional data
        cursor.execute("""
            SELECT d.day, d.meal_type, f.food_item, d.quantity, f.calories, f.protein, f.carbohydrates, f.fat
            FROM Diet_Plan_Food d
            JOIN Food f ON d.food_id = f.food_id
            WHERE d.user_id = %s
            ORDER BY d.day, FIELD(d.meal_type, 'Breakfast', 'Lunch', 'Dinner')
        """, (user_id,)) # Fetch meal plan data
        meals = cursor.fetchall() # Get all meal records
        if not meals:
            return None, None # Return None if no meal plan exists
        # Reconstruct the meal plan
        meal_plan = []
        for day in range(1, 8): # Iterate through 7 days
            day_meals = {"Day": day, "Breakfast": {}, "Lunch": {}, "Dinner": {}, "totals": {"Breakfast": {}, "Lunch": {}, "Dinner": {}, "daily": {}}} # Initialize day structure
            for meal in meals:
                if int(meal['day']) != day:
                    continue # Skip meals for other days
                meal_type = meal['meal_type'] # Get meal type
                ingredient = meal['food_item'] # Get food item
                # Add ingredient details to meal
                day_meals[meal_type][ingredient] = {
                    "servings": meal['quantity'], # Quantity of ingredient
                    "nutrition": {
                        "calories": meal['calories'] or 0, # Calories per serving
                        "protein": meal['protein'] or 0, # Protein per serving
                        "carbs": meal['carbohydrates'] or 0, # Carbs per serving
                        "fats": meal['fat'] or 0 # Fats per serving
                    }
                }
            # Calculate totals for each meal
            for meal_type in ["Breakfast", "Lunch", "Dinner"]:
                total_calories = 0
                total_protein = 0
                total_carbs = 0
                total_fats = 0
                for ingredient, details in day_meals[meal_type].items():
                    serving_size = details['servings'] # Get serving size
                    total_calories += serving_size * details['nutrition']['calories'] # Sum calories
                    total_protein += serving_size * details['nutrition']['protein'] # Sum protein
                    total_carbs += serving_size * details['nutrition']['carbs'] # Sum carbs
                    total_fats += serving_size * details['nutrition']['fats'] # Sum fats
                # Determine dominant macronutrient
                protein_calories = total_protein * 4 # Protein calories (4 kcal/g)
                carb_calories = total_carbs * 4 # Carb calories (4 kcal/g)
                fat_calories = total_fats * 9 # Fat calories (9 kcal/g)
                dominant_macro = "none" # Default dominant macro
                if total_calories > 0:
                    protein_percentage = (protein_calories / total_calories) * 100 # Protein percentage
                    carb_percentage = (carb_calories / total_calories) * 100 # Carb percentage
                    fat_percentage = (fat_calories / total_calories) * 100 # Fat percentage
                    if protein_percentage > carb_percentage and protein_percentage > fat_percentage:
                        dominant_macro = "protein" # Protein dominant
                    elif carb_percentage > protein_percentage and carb_percentage > fat_percentage:
                        dominant_macro = "carbs" # Carbs dominant
                    else:
                        dominant_macro = "fats" # Fats dominant
                # Store meal totals
                day_meals["totals"][meal_type] = {
                    "calories": round(total_calories, 2), # Rounded total calories
                    "protein": round(total_protein, 2), # Rounded total protein
                    "carbs": round(total_carbs, 2), # Rounded total carbs
                    "fats": round(total_fats, 2), # Rounded total fats
                    "dominant_macro": dominant_macro # Dominant macronutrient
                }
            # Calculate daily totals
            daily_totals = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0} # Initialize daily totals
            for meal_type in ["Breakfast", "Lunch", "Dinner"]:
                for macro in daily_totals:
                    daily_totals[macro] += day_meals["totals"][meal_type][macro] # Sum meal totals
            day_meals["totals"]["daily"] = daily_totals # Store daily totals
            meal_plan.append(day_meals) # Add day to meal plan
        # Calculate daily requirements
        user_data = get_user_details(user_id) # Fetch user details
        user_requirements = get_user_requirements(user_data)[0] # Get nutritional requirements
        daily_requirements = {
            "calories": round((user_requirements["calorie_min"] + user_requirements["calorie_max"]) / 2, 2), # Average calorie needs
            "protein": round((user_requirements["macros"]["protein"]["min"] + user_requirements["macros"]["protein"]["max"]) / 2, 2), # Average protein needs
            "carbs": round((user_requirements["macros"]["carbs"]["min"] + user_requirements["macros"]["carbs"]["max"]) / 2, 2), # Average carb needs
            "fats": round((user_requirements["macros"]["fats"]["min"] + user_requirements["macros"]["fats"]["max"]) / 2, 2) # Average fat needs
        }
        return meal_plan, daily_requirements
    finally:
        conn.close()

# Fetch food data from the database, filtered by preferences and diet
def fetch_food_data(preferences=None, diet=None):
    """
    Retrieves food items from the Food table, filtered by user preferences and diet.
    
    Args:
        preferences: String of comma-separated ingredients to exclude.
        diet: Dietary restriction (e.g., vegan, vegetarian).
    
    Returns:
        Tuple of (categorised_foods, food_dict) where categorised_foods maps meal types to food lists,
        and food_dict maps food items to their nutritional data.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM Food" # Base query for food items
    conditions = [] # List of SQL conditions
    if preferences:
        exclude_items = [item.strip().lower() for item in preferences.split(",")] # Parse preferences
        if exclude_items:
            exclude_clause = " AND ".join(
                [f"LOWER(food_item) NOT LIKE '%{item}%'" for item in exclude_items if item]
            ) # Build exclusion clause
            conditions.append(exclude_clause) # Add to conditions
    if diet:
        diet = diet.lower() # Normalize diet
        allowed_diets = [] # List of allowed diets
        if diet == "vegan":
            allowed_diets = ["vegan"] # Only vegan foods
        elif diet == "vegetarian":
            allowed_diets = ["vegan", "vegetarian"] # Vegan and vegetarian foods
        elif diet == "pescatarian":
            allowed_diets = ["vegan", "vegetarian", "pescatarian"] # Include pescatarian foods
        else:
            allowed_diets = None  # Omnivore includes all diets
        if allowed_diets:
            diet_clause = "LOWER(diet) IN (" + ", ".join([f"'{d}'" for d in allowed_diets]) + ")" # Build diet clause
            conditions.append(diet_clause) # Add to conditions
    if conditions:
        query += " WHERE " + " AND ".join(conditions) # Append conditions to query
    cursor.execute(query) # Execute food query
    food_items = cursor.fetchall() # Fetch all food items
    cursor.execute("SELECT food_id, high_type FROM Food_High") # Fetch high-macronutrient data
    high_macro_items = cursor.fetchall() # Get high-macronutrient records
    # Build food dictionary keyed by food_item
    food_dict = {}
    for food in food_items:
        food_dict[food['food_item']] = { # Key by food_item
            "name": food["food_item"], # Food name
            "calories": food["calories"] or 0, # Calories per serving
            "protein": food["protein"] or 0, # Protein per serving
            "carbs": food["carbohydrates"] or 0, # Carbs per serving
            "fats": food["fat"] or 0, # Fats per serving
            "categories": [], # List of high-macronutrient categories
            "category": food["category"].lower() # Meal type category
        }
    # Add high macronutrient categories
    for item in high_macro_items:
        # Find the food_item corresponding to food_id
        cursor.execute("SELECT food_item FROM Food WHERE food_id = %s", (item['food_id'],))
        food_item_result = cursor.fetchone()
        if food_item_result and food_item_result['food_item'] in food_dict:
            food_dict[food_item_result['food_item']]["categories"].append(item["high_type"]) # Add high-type category
    # Categorize foods by meal type
    categorised_foods = {"breakfast": [], "lunch": [], "dinner": []} # Initialize categorised foods
    for food in food_dict.values():
        category = food["category"] # Get food category
        if category in categorised_foods:
            categorised_foods[category].append(food) # Add to appropriate meal type
        else:
            print(f"Warning: Unknown category '{category}' for food item '{food['name']}'. Skipping.") # Log unknown category
    conn.close() # Close database connection
    return categorised_foods, food_dict # Return categorised foods and food dictionary

# Get user requirements from provided user_data or Flask request
def get_user_requirements(user_data=None):
    """
    Calculates nutritional requirements based on user data.
    
    Args:
        user_data: Dictionary with user details (optional, else uses Flask request).
    
    Returns:
        Tuple of (user_requirements, user_data) with nutritional needs and user data.
    """
    try:
        # Use provided user_data or request JSON
        data = user_data if user_data is not None else request.json # Select data source
        # Extract and validate user data
        weight = float(data['weight']) # User's weight
        height = float(data['height']) # User's height
        age = int(data['age']) # User's age
        gender = data['gender'] # User's gender
        activity_level = data['activity'] # User's activity level
        goal = data['goal'] # User's fitness goal
        diet = data['diet'] # User's dietary preference
        preferences = data['preferences'] # User's food exclusions
        # Use meal_variety if provided (from frontend), else default to 50
        meal_variety = data.get('meal_variety', data.get('meal_variety', 50)) # Meal variety factor
        # Calculate macronutrient requirements
        macros = calculate_macronutrients(weight, height, age, gender, activity_level, goal) # Compute macros
        # Define user requirements with min/max ranges
        user_requirements = {
            "calorie_min": macros["calories"] * 0.9, # Minimum calorie needs
            "calorie_max": macros["calories"] * 1.1, # Maximum calorie needs
            "macros": {
                "protein": {"min": macros["protein"], "max": macros["protein"] * 1.1}, # Protein range
                "carbs": {"min": macros["carbs"], "max": macros["carbs"] * 1.1}, # Carb range
                "fats": {"min": macros["fats"], "max": macros["fats"] * 1.1}, # Fat range
            },
        }
        # Construct user data dictionary
        user_data = {
            "weight": weight,
            "height": height,
            "age": age,
            "gender": gender,
            "activity_level": activity_level,
            "goal": goal,
            "diet": diet,
            "preferences": preferences,
            "meal_variety": meal_variety
        }
        return user_requirements, user_data # Return requirements and user data
    except Exception as e:
        raise ValueError(f"Error processing user data: {e}") # Raise error on invalid data

# Individual class
class Individual:
    """Represents a candidate meal plan in the genetic algorithm."""
    def __init__(self, categorised_foods):
        """
        Initializes an individual with a random 7-day meal plan.
        
        Args:
            categorised_foods: Dictionary mapping meal types to food lists.
        """
        self.meal_plan = [] # List to store 7-day meal plan
        self.fitness = 0 # Fitness score of the meal plan
        # Generate a 7-day meal plan with exactly 3 ingredients per meal
        for day in range(7):
            day_plan = {
                "Day": day + 1, # Day number (1-7)
                "Breakfast": self._create_meal("breakfast", categorised_foods), # Breakfast meal
                "Lunch": self._create_meal("lunch", categorised_foods), # Lunch meal
                "Dinner": self._create_meal("dinner", categorised_foods), # Dinner meal
                "totals": {"Breakfast": {}, "Lunch": {}, "Dinner": {}, "daily": {}} # Nutritional totals
            }
            self.meal_plan.append(day_plan) # Add day to meal plan

    def _create_meal(self, meal_type, categorised_foods, num_ingredients=3):
        """
        Creates a meal with a specified number of ingredients.
        
        Args:
            meal_type: Type of meal (breakfast, lunch, dinner).
            categorised_foods: Dictionary of categorised foods.
            num_ingredients: Number of ingredients to include (default 3).
        
        Returns:
            Dictionary representing the meal.
        """
        meal = {} # Initialize empty meal
        ingredients = categorised_foods.get(meal_type, []) # Get foods for meal type
        if not ingredients:
            all_foods = categorised_foods["breakfast"] + categorised_foods["lunch"] + categorised_foods["dinner"] # Fallback to all foods
            ingredients = all_foods
        if not ingredients:
            return meal # Return empty meal if no foods available
        # Select exactly num_ingredients (default 3)
        selected_ingredients = random.sample(ingredients, min(num_ingredients, len(ingredients))) # Randomly select ingredients
        for ingredient in selected_ingredients:
            meal[ingredient["name"]] = {
                "servings": random.uniform(0.5, 2.0), # Random serving size between 0.5 and 2
                "nutrition": {
                    "calories": ingredient.get("calories", 0), # Calories per serving
                    "protein": ingredient.get("protein", 0), # Protein per serving
                    "carbs": ingredient.get("carbs", 0), # Carbs per serving
                    "fats": ingredient.get("fats", 0) # Fats per serving
                }
            }
        return meal # Return constructed meal

# Crossover function
def crossover(parent1, parent2, categorised_foods):
    """
    Performs crossover between two parent meal plans to produce two children.
    
    Args:
        parent1: First parent Individual.
        parent2: Second parent Individual.
        categorised_foods: Dictionary of categorised foods.
    
    Returns:
        Tuple of two child Individuals.
    """
    child1 = Individual(categorised_foods) # Create first child
    child2 = Individual(categorised_foods) # Create second child
    for day in range(7):
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            parent1_meal = parent1.meal_plan[day][meal_type] # Get parent1 meal
            parent2_meal = parent2.meal_plan[day][meal_type] # Get parent2 meal
            # Combine ingredients from both parents
            combined_ingredients = {}
            for ing in parent1_meal:
                combined_ingredients[ing] = parent1_meal[ing].copy() # Copy parent1 ingredients
            for ing in parent2_meal:
                if ing not in combined_ingredients:
                    combined_ingredients[ing] = parent2_meal[ing].copy() # Add parent2 unique ingredients
                else:
                    # If ingredient exists in both, randomly choose servings
                    if random.random() < 0.5:
                        combined_ingredients[ing]["servings"] = parent2_meal[ing]["servings"] # Use parent2 servings
            # Split ingredients between children, ensuring max 3 ingredients
            all_ingredients = list(combined_ingredients.keys()) # List of all ingredients
            if len(all_ingredients) > 3:
                child1_ingredients = random.sample(all_ingredients, 3) # Select 3 for child1
                # Remaining ingredients for child2, ensuring no overlap
                remaining = [ing for ing in all_ingredients if ing not in child1_ingredients] # Get remaining ingredients
                child2_ingredients = random.sample(remaining, min(3, len(remaining))) # Select up to 3 for child2
            else:
                child1_ingredients = all_ingredients # Use all if <= 3
                child2_ingredients = all_ingredients # Use all if <= 3
            # Build meals for children
            child1_meal = {}
            child2_meal = {}
            for ing in child1_ingredients:
                child1_meal[ing] = combined_ingredients[ing].copy() # Assign to child1
            for ing in child2_ingredients:
                child2_meal[ing] = combined_ingredients[ing].copy() # Assign to child2
            child1.meal_plan[day][meal_type] = child1_meal # Set child1 meal
            child2.meal_plan[day][meal_type] = child2_meal # Set child2 meal
    return child1, child2 # Return children

# Mutation function
def mutate(ind, mut_rate, categorised_foods):
    """
    Mutates an individual's meal plan by altering serving sizes or replacing ingredients.
    
    Args:
        ind: Individual to mutate.
        mut_rate: Mutation probability.
        categorised_foods: Dictionary of categorised foods.
    """
    for day in range(7):
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            meal = ind.meal_plan[day][meal_type] # Get meal
            ingredients = list(meal.keys()) # List of ingredients
            # Mutate serving sizes
            for ingredient in ingredients:
                if random.random() < mut_rate:
                    meal[ingredient]["servings"] = random.uniform(0.5, 4.0) # Random new serving size
            # Replace an ingredient (maintaining exactly 3 ingredients)
            if random.random() < mut_rate and ingredients:
                # Remove one ingredient
                ingredient_to_remove = random.choice(ingredients) # Select random ingredient
                del meal[ingredient_to_remove] # Remove it
                # Add a new ingredient
                new_meal = ind._create_meal(meal_type, categorised_foods, num_ingredients=1) # Create new ingredient
                meal.update(new_meal) # Add new ingredient
                # If we exceed 3 ingredients, remove one randomly
                while len(meal) > 3:
                    ingredient_to_remove = random.choice(list(meal.keys())) # Select random excess ingredient
                    del meal[ingredient_to_remove] # Remove it

# Simplified fitness function (without optimization)
def evaluate_fitness_simple(ind, calorie_min, calorie_max, macros):
    """
    Evaluates the fitness of a meal plan based on nutritional targets and diversity.
    
    Args:
        ind: Individual meal plan.
        calorie_min: Minimum daily calorie requirement.
        calorie_max: Maximum daily calorie requirement.
        macros: Dictionary of macronutrient requirements.
    """
    penalty = 0 # Initialize penalty
    diversity = set() # Track unique ingredients for diversity
    daily_calories_target = (calorie_min + calorie_max) / 2 # Average calorie target
    daily_protein_target = (macros["protein"]["min"] + macros["protein"]["max"]) / 2 # Average protein target
    daily_carbs_target = (macros["carbs"]["min"] + macros["carbs"]["max"]) / 2 # Average carb target
    daily_fats_target = (macros["fats"]["min"] + macros["fats"]["max"]) / 2 # Average fat target

    for day in ind.meal_plan:
        daily_calories = 0 # Daily calorie total
        daily_macros = {"protein": 0, "carbs": 0, "fats": 0} # Daily macro totals
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            meal = day[meal_type] # Get meal
            if not meal:
                continue # Skip empty meals
            total_calories = 0
            total_protein = 0
            total_carbs = 0
            total_fats = 0
            for ing in meal:
                serving_size = meal[ing]["servings"] # Get serving size
                total_calories += serving_size * meal[ing]["nutrition"]["calories"] # Sum calories
                total_protein += serving_size * meal[ing]["nutrition"]["protein"] # Sum protein
                total_carbs += serving_size * meal[ing]["nutrition"]["carbs"] # Sum carbs
                total_fats += serving_size * meal[ing]["nutrition"]["fats"] # Sum fats
                diversity.add(ing) # Add ingredient to diversity set
            daily_calories += total_calories # Add to daily calories
            daily_macros["protein"] += total_protein # Add to daily protein
            daily_macros["carbs"] += total_carbs # Add to daily carbs
            daily_macros["fats"] += total_fats # Add to daily fats
            # Update totals (simplified)
            dominant_macro = "none" # Default dominant macro
            if total_calories > 0:
                protein_calories = total_protein * 4 # Protein calories
                carb_calories = total_carbs * 4 # Carb calories
                fat_calories = total_fats * 9 # Fat calories
                protein_percentage = (protein_calories / total_calories) * 100 # Protein percentage
                carb_percentage = (carb_calories / total_calories) * 100 # Carb percentage
                fat_percentage = (fat_calories / total_calories) * 100 # Fat percentage
                if protein_percentage > carb_percentage and protein_percentage > fat_percentage:
                    dominant_macro = "protein" # Protein dominant
                elif carb_percentage > protein_percentage and carb_percentage > fat_percentage:
                    dominant_macro = "carbs" # Carbs dominant
                else:
                    dominant_macro = "fats" # Fats dominant
            day["totals"][meal_type] = {
                "calories": round(total_calories, 2), # Rounded calories
                "protein": round(total_protein, 2), # Rounded protein
                "carbs": round(total_carbs, 2), # Rounded carbs
                "fats": round(total_fats, 2), # Rounded fats
                "dominant_macro": dominant_macro # Dominant macronutrient
            }
        # Calculate daily totals
        daily_totals = {"calories": daily_calories, "protein": daily_macros["protein"], "carbs": daily_macros["carbs"], "fats": daily_macros["fats"]} # Daily totals
        day["totals"]["daily"] = daily_totals # Store daily totals
        # Penalize deviations
        calorie_dev = abs(daily_calories - daily_calories_target) / daily_calories_target * 100 # Calorie deviation
        protein_dev = abs(daily_macros["protein"] - daily_protein_target) / daily_protein_target * 100 # Protein deviation
        carbs_dev = abs(daily_macros["carbs"] - daily_carbs_target) / daily_carbs_target * 100 # Carb deviation
        fats_dev = abs(daily_macros["fats"] - daily_fats_target) / daily_fats_target * 100 # Fat deviation
        penalty += 1.0 * calorie_dev + 2.0 * protein_dev + 2.0 * carbs_dev + 1.4 * fats_dev # Weighted penalty
    diversity_score = len(diversity) / (21 * 3) # Diversity score (ingredients used / max possible)
    penalty -= diversity_score * 10 # Reward diversity
    ind.fitness = 1 / (1 + penalty) # Set fitness (higher is better)

# Full fitness function with optimization (used sparingly)
def evaluate_fitness(ind, calorie_min, calorie_max, macros, food_dict):
    """
    Evaluates fitness with serving size optimization for better nutritional alignment.
    
    Args:
        ind: Individual meal plan.
        calorie_min: Minimum daily calorie requirement.
        calorie_max: Maximum daily calorie requirement.
        macros: Dictionary of macronutrient requirements.
        food_dict: Dictionary mapping ingredients to nutritional data.
    """
    daily_calories_target = (calorie_min + calorie_max) / 2 # Average daily calories
    daily_protein_target = (macros["protein"]["min"] + macros["protein"]["max"]) / 2 # Average daily protein
    daily_carbs_target = (macros["carbs"]["min"] + macros["carbs"]["max"]) / 2 # Average daily carbs
    daily_fats_target = (macros["fats"]["min"] + macros["fats"]["max"]) / 2 # Average daily fats
    meal_calories_target = daily_calories_target / 3 # Per-meal calorie target
    meal_protein_target = daily_protein_target / 3 # Per-meal protein target
    meal_carbs_target = daily_carbs_target / 3 # Per-meal carb target
    meal_fats_target = daily_fats_target / 3 # Per-meal fat target

    # First, compute simple fitness to get initial totals
    evaluate_fitness_simple(ind, calorie_min, calorie_max, macros) # Run simple fitness
    
    # Optimize serving sizes for each meal
    for day in ind.meal_plan:
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            meal = day[meal_type] # Get meal
            if not meal:
                continue # Skip empty meals
            ingredients = [] # List of ingredient data
            ingredient_names = [] # List of ingredient names
            for name in meal:
                if name in food_dict:
                    ingredients.append(food_dict[name]) # Add ingredient data
                    ingredient_names.append(name) # Add ingredient name
                else:
                    print(f"Warning: Ingredient '{name}' not found in food_dict. Skipping in fitness evaluation.") # Log missing ingredient
            if not ingredients:
                continue # Skip if no valid ingredients
            def objective(servings):
                """Objective function for serving size optimization."""
                total_calories = sum(servings[i] * (ingredients[i].get("calories", 0)) for i in range(len(ingredients))) # Total calories
                total_protein = sum(servings[i] * (ingredients[i].get("protein", 0)) for i in range(len(ingredients))) # Total protein
                total_carbs = sum(servings[i] * (ingredients[i].get("carbs", 0)) for i in range(len(ingredients))) # Total carbs
                total_fats = sum(servings[i] * (ingredients[i].get("fats", 0)) for i in range(len(ingredients))) # Total fats
                calorie_diff = (total_calories - meal_calories_target) ** 2 # Calorie deviation
                protein_diff = (total_protein - meal_protein_target) ** 2 # Protein deviation
                carbs_diff = (total_carbs - meal_carbs_target) ** 2 # Carb deviation
                fats_diff = (total_fats - meal_fats_target) ** 2 # Fat deviation
                return calorie_diff + protein_diff + carbs_diff + fats_diff # Sum of squared deviations
            initial_servings = [meal[ing]["servings"] for ing in ingredient_names] # Initial serving sizes
            bounds = [(0.5, 4) for _ in range(len(ingredients))] # Serving size bounds
            result = minimize(objective, initial_servings, bounds=bounds) # Optimize servings
            # Update serving sizes
            for i, ing in enumerate(ingredient_names):
                meal[ing]["servings"] = result.x[i] # Set optimized serving size
    
    # Recalculate fitness with optimized servings
    evaluate_fitness_simple(ind, calorie_min, calorie_max, macros) # Re-run simple fitness

# Genetic Algorithm
def genetic_algorithm(user_requirements, categorised_foods, food_dict):
    """
    Runs a genetic algorithm to generate an optimized 7-day meal plan.
    
    Args:
        user_requirements: Dictionary of nutritional requirements.
        categorised_foods: Dictionary mapping meal types to food lists.
        food_dict: Dictionary mapping ingredients to nutritional data.
    
    Returns:
        Optimized 7-day meal plan.
    """
    print("user_requirements in genetic_algorithm():", user_requirements) # Log requirements
    print("Categorised foods in genetic_algorithm:", {k: len(v) for k, v in categorised_foods.items()}) # Log food counts
    user_reqs = user_requirements # Alias for requirements
    calorie_min = user_reqs["calorie_min"] # Minimum calories
    calorie_max = user_reqs["calorie_max"] # Maximum calories
    macros = user_reqs["macros"] # Macronutrient requirements
    population_size = 50 # Number of individuals per generation
    generations = 150 # Number of generations
    population = [Individual(categorised_foods) for _ in range(population_size)] # Initialize population
    for gen in range(generations):
        # Evaluate fitness for all individuals (simple version)
        for ind in population:
            evaluate_fitness_simple(ind, calorie_min, calorie_max, macros) # Compute fitness
        # Sort by fitness
        population.sort(key=lambda x: x.fitness, reverse=True) # Sort descending
        # Optimize serving sizes for top 5 individuals only
        for ind in population[:5]:
            evaluate_fitness(ind, calorie_min, calorie_max, macros, food_dict) # Optimize top individuals
        # Re-sort after optimization
        population.sort(key=lambda x: x.fitness, reverse=True) # Re-sort
        next_gen = population[:10]  # Elitism: keep top 10
        while len(next_gen) < population_size:
            parent1 = random.choice(next_gen) # Select parent1
            parent2 = random.choice(next_gen) # Select parent2
            child1, child2 = crossover(parent1, parent2, categorised_foods) # Perform crossover
            next_gen.append(child1) # Add child1
            next_gen.append(child2) # Add child2
        for ind in next_gen[10:]:
            mutate(ind, 0.19, categorised_foods) # Mutate non-elite individuals
        population = next_gen # Update population
        best_ind = population[0] # Best individual
        print(f"Generation {gen + 1}: Best Fitness = {best_ind.fitness:.10f}") # Log best fitness
    # Final optimization for the best individual
    evaluate_fitness(population[0], calorie_min, calorie_max, macros, food_dict) # Optimize best plan
    return population[0].meal_plan # Return best meal plan

# adjust meal plan for meal-type specificity
def adjust_meal_plan_for_categories(meal_plan, categorised_foods, meal_variety, food_dict):
    """
    Post-processes the meal plan to align ingredients with their meal-type categories,
    allowing a percentage of cross-category ingredients, ensuring 3 ingredients per meal.
    
    Args:
        meal_plan: Generated meal plan.
        categorised_foods: Dictionary of categorised foods.
        meal_variety: Percentage of cross-category ingredients to allow.
        food_dict: Dictionary mapping ingredients to nutritional data.
    
    Returns:
        Adjusted meal plan.
    """
    print(f"cross category percentage value: {meal_variety}") # Log cross-category percentage
    adjusted_meal_plan = meal_plan.copy() # Copy meal plan
    
    # Validate meal_variety
    meal_variety = int(meal_variety) # Convert to integer
    meal_variety = max(0, min(100, meal_variety)) # Clamp to 0-100
    cross_category_fraction = meal_variety / 100.0 # Convert to fraction
    
    # Process each day independently
    for day in adjusted_meal_plan:
        # Initialize new meal assignments
        new_breakfast = {}
        new_lunch = {}
        new_dinner = {}
        
        # Collect all ingredients for the day
        day_ingredients = []
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            meal = day[meal_type] # Get meal
            for ingredient in meal:
                day_ingredients.append({
                    "ingredient": ingredient, # Ingredient name
                    "current_meal": meal_type.lower(), # Current meal type
                    "category": food_dict.get(ingredient, {}).get("category", "").lower(), # Intended category
                    "servings": meal[ingredient]["servings"], # Serving size
                    "nutrition": meal[ingredient]["nutrition"] # Nutritional data
                })
        
        # Identify mismatched ingredients
        mismatched_ingredients = [
            item for item in day_ingredients if item["current_meal"] != item["category"]
        ] # Ingredients in wrong meal type
        
        # Determine how many mismatched ingredients to keep
        num_mismatched = len(mismatched_ingredients) # Total mismatches
        num_to_keep = int(round(num_mismatched * cross_category_fraction)) # Number to keep
        num_to_move = num_mismatched - num_to_keep # Number to move
        
        # Randomly select which mismatched ingredients to move
        ingredients_to_move = random.sample(mismatched_ingredients, num_to_move) if num_to_move > 0 else [] # Select ingredients to move
        
        # Assign ingredients to meals based on category or current meal
        for item in day_ingredients:
            ingredient = item["ingredient"] # Get ingredient
            servings = item["servings"] # Get servings
            nutrition = item["nutrition"] # Get nutrition
            # Determine the target meal type
            if item in ingredients_to_move:
                # Move to the correct meal type based on category
                target_meal = item["category"] # Use intended category
            else:
                # Keep in current meal type
                target_meal = item["current_meal"] # Use current meal
            
            # Assign to the appropriate meal
            if target_meal == "breakfast":
                new_breakfast[ingredient] = {"servings": servings, "nutrition": nutrition} # Assign to breakfast
            elif target_meal == "lunch":
                new_lunch[ingredient] = {"servings": servings, "nutrition": nutrition} # Assign to lunch
            elif target_meal == "dinner":
                new_dinner[ingredient] = {"servings": servings, "nutrition": nutrition} # Assign to dinner
            else:
                # Fallback: keep in current meal if category is unknown
                if item["current_meal"] == "breakfast":
                    new_breakfast[ingredient] = {"servings": servings, "nutrition": nutrition} # Fallback to breakfast
                elif item["current_meal"] == "lunch":
                    new_lunch[ingredient] = {"servings": servings, "nutrition": nutrition} # Fallback to lunch
                else:
                    new_dinner[ingredient] = {"servings": servings, "nutrition": nutrition} # Fallback to dinner
        
            meals = {
                "breakfast": new_breakfast,
                "lunch": new_lunch,
                "dinner": new_dinner
            } # Meal assignments
            
        # Ensure exactly three ingredients per meal 
        if meal_variety > 0:
            
            meal_types = ["breakfast", "lunch", "dinner"] # List of meal types
        
            # Count ingredients in each meal
            ingredient_counts = {meal: len(meals[meal]) for meal in meal_types} # Count ingredients
            total_ingredients = sum(ingredient_counts.values()) # Total ingredients
            
            # Check if total ingredients allow for 9 ingredients across 3 meals
            if total_ingredients < 9:
                print(f"Warning: Day {day['Day']} has only {total_ingredients} ingredients, cannot achieve 3 per meal.") # Log warning
                # Proceed with available ingredients, prioritizing correct categories
            elif total_ingredients > 9:
                # Reduce excess ingredients
                while total_ingredients > 9:
                    # Find meal with the most ingredients
                    max_meal = max(ingredient_counts, key=ingredient_counts.get) # Meal with most ingredients
                    # Prefer to remove a cross-category ingredient
                    cross_category_items = [
                        ing for ing in meals[max_meal]
                        if food_dict.get(ing, {}).get("category", "").lower() != max_meal
                    ] # Cross-category ingredients
                    if cross_category_items:
                        ingredient_to_remove = random.choice(cross_category_items) # Remove cross-category
                    else:
                        ingredient_to_remove = random.choice(list(meals[max_meal].keys())) # Remove random
                    # Remove the ingredient
                    removed = meals[max_meal].pop(ingredient_to_remove) # Remove ingredient
                    # Try to place it in a meal needing ingredients
                    for target_meal in meal_types:
                        if ingredient_counts[target_meal] < 3:
                            meals[target_meal][ingredient_to_remove] = removed # Add to target meal
                            ingredient_counts[target_meal] += 1 # Update count
                            ingredient_counts[max_meal] -= 1 # Update count
                            total_ingredients -= 1 # Update total
                            break
                    else:
                        # No meal needs it, discard (rare case)
                        total_ingredients -= 1 # Update total
                        ingredient_counts[max_meal] -= 1 # Update count
            
            # Redistribute ingredients to achieve exactly 3 per meal
            while any(ingredient_counts[meal] != 3 for meal in meal_types):
                # Find a meal with too many ingredients (>3)
                source_meal = next((meal for meal in meal_types if ingredient_counts[meal] > 3), None) # Meal with excess
                if source_meal:
                    # Prefer to move a cross-category ingredient
                    cross_category_items = [
                        ing for ing in meals[source_meal]
                        if food_dict.get(ing, {}).get("category", "").lower() != source_meal
                    ] # Cross-category ingredients
                    if cross_category_items:
                        ingredient_to_move = random.choice(cross_category_items) # Move cross-category
                    else:
                        ingredient_to_move = random.choice(list(meals[source_meal].keys())) # Move random
                    # Find a meal with too few ingredients (<3)
                    target_meal = next((meal for meal in meal_types if ingredient_counts[meal] < 3), None) # Meal needing ingredients
                    if target_meal:
                        # Move the ingredient
                        meals[target_meal][ingredient_to_move] = meals[source_meal].pop(ingredient_to_move) # Move ingredient
                        ingredient_counts[source_meal] -= 1 # Update source count
                        ingredient_counts[target_meal] += 1 # Update target count
                    else:
                        # Should not happen if total_ingredients == 9
                        print(f"Warning: Day {day['Day']} cannot balance ingredients.") # Log warning
                        break
                else:
                    # No meal has >3, but some have <3 (implies total_ingredients < 9)
                    print(f"Warning: Day {day['Day']} has insufficient ingredients.") # Log warning
                    break
        
        # Update the day's meals
        day["Breakfast"] = meals["breakfast"] # Update breakfast
        day["Lunch"] = meals["lunch"] # Update lunch
        day["Dinner"] = meals["dinner"] # Update dinner
        
        # Recalculate totals for each meal
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            meal = day[meal_type] # Get meal
            total_calories = 0
            total_protein = 0
            total_carbs = 0
            total_fats = 0
            for ing in meal:
                serving_size = meal[ing]["servings"] # Get serving size
                total_calories += serving_size * meal[ing]["nutrition"]["calories"] # Sum calories
                total_protein += serving_size * meal[ing]["nutrition"]["protein"] # Sum protein
                total_carbs += serving_size * meal[ing]["nutrition"]["carbs"] # Sum carbs
                total_fats += serving_size * meal[ing]["nutrition"]["fats"] # Sum fats
            dominant_macro = "none" # Default dominant macro
            if total_calories > 0:
                protein_calories = total_protein * 4 # Protein calories
                carb_calories = total_carbs * 4 # Carb calories
                fat_calories = total_fats * 9 # Fat calories
                protein_percentage = (protein_calories / total_calories) * 100 # Protein percentage
                carb_percentage = (carb_calories / total_calories) * 100 # Carb percentage
                fat_percentage = (fat_calories / total_calories) * 100 # Fat percentage
                if protein_percentage > carb_percentage and protein_percentage > fat_percentage:
                    dominant_macro = "protein" # Protein dominant
                elif carb_percentage > protein_percentage and carb_percentage > fat_percentage:
                    dominant_macro = "carbs" # Carbs dominant
                else:
                    dominant_macro = "fats" # Fats dominant
            day["totals"][meal_type] = {
                "calories": round(total_calories, 2), # Rounded calories
                "protein": round(total_protein, 2), # Rounded protein
                "carbs": round(total_carbs, 2), # Rounded carbs
                "fats": round(total_fats, 2), # Rounded fats
                "dominant_macro": dominant_macro # Dominant macronutrient
            }
        
        # Recalculate daily totals
        daily_totals = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0} # Initialize daily totals
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            for macro in daily_totals:
                daily_totals[macro] += day["totals"][meal_type][macro] # Sum meal totals
        day["totals"]["daily"] = daily_totals # Store daily totals
    
    return adjusted_meal_plan # Return adjusted meal plan
    
# Generate a meal plan based on user requirements function
def generate_meal_plan(user_data=None):
    """
    Generates a 7-day meal plan tailored to user requirements.
    
    Args:
        user_data: Dictionary with user details (optional, else uses Flask request).
    
    Returns:
        Tuple of (meal_plan, daily_requirements).
    """
    user_requirements, user_data = get_user_requirements(user_data=user_data) # Get requirements and data
    categorised_foods, food_dict = fetch_food_data(user_data["preferences"], user_data["diet"]) # Fetch food data
    meal_plan = genetic_algorithm(user_requirements, categorised_foods, food_dict) # Generate meal plan
    
    # Get the cross-category percentage from user_data (default to 50 if not provided)
    meal_variety = user_data.get("meal_variety", 50) # Cross-category allowance
    
    # Apply post-processing to adjust for meal-type-specific ingredients
    meal_plan = adjust_meal_plan_for_categories(meal_plan, categorised_foods, meal_variety, food_dict) # Adjust meal plan
    
    # Calculate daily requirements for return value
    daily_requirements = {
        "calories": round((user_requirements["calorie_min"] + user_requirements["calorie_max"]) / 2, 2), # Average calories
        "protein": round((user_requirements["macros"]["protein"]["min"] + user_requirements["macros"]["protein"]["max"]) / 2, 2), # Average protein
        "carbs": round((user_requirements["macros"]["carbs"]["min"] + user_requirements["macros"]["carbs"]["max"]) / 2, 2), # Average carbs
        "fats": round((user_requirements["macros"]["fats"]["min"] + user_requirements["macros"]["fats"]["max"]) / 2, 2) # Average fats
    }
    print("\nFull Generated Meal Plan (Debugging):") # Log meal plan
    for day in meal_plan:
        print(f"Day {day['Day']}:") # Log day
        for meal_type in ["Breakfast", "Lunch", "Dinner"]:
            print(f"  {meal_type}:") # Log meal type
            for ingredient, amount in day[meal_type].items():
                print(f"    {ingredient}: {amount['servings']:.2f} servings") # Log ingredient
    return meal_plan, daily_requirements # Return meal plan and requirements