def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate (BMR)."""
    if gender.lower() == "male": # If the gender is male then the male calculation for BMR is returned
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == "female": # If the gender is female then the female calculation for BMR is returned
        return 10 * weight + 6.25 * height - 5 * age - 161
    else: # If it is not either then the json send must be corrupted in some way, extra debugging
        raise ValueError("Invalid gender. Please specify 'male' or 'female'.")

def calculate_tdee(bmr, activity_level_multiplier):
    """Calculate Total Daily Energy Expenditure (TDEE)."""
    return bmr * activity_level_multiplier # TDEE is calculated by multiplying the BMR by the activity level multiplier

def calculate_macros(tdee, protein_per_kg, fat_percentage):
    """Calculate daily protein, fat, and carbohydrate intake."""
    # Protein calculation
    protein_grams = protein_per_kg # Protein in grams is calculated by how much per KG of wieght is required, this depends on the goal of the user
    protein_calories = protein_grams * 4 # Each gram of protein is 4 calories

    # Fat calculation
    fat_calories = (fat_percentage / 100) * tdee # Fat percentage is based on the user's goal
    fat_grams = fat_calories / 9 # Each gram of fat is 9 calories

    # Carbohydrates calculation
    carb_calories = tdee - (protein_calories + fat_calories) # Carbohydrates are based on the amount of calories left after caluculating protein and fat
    carb_grams = carb_calories / 4 # Each gram of carbohydrates is 4 calories

    return {
        "calories": round(tdee, 2),
        "protein": round(protein_grams, 2),
        "carbs": round(carb_grams, 2),
        "fats": round(fat_grams, 2)
    }

def calculate_macronutrients(weight, height, age, gender, activity_level, goal):
    """Main function to compute BMR, TDEE, and macronutrient needs."""
    
    # Mapping numeric activity levels to multipliers
    activity_multipliers = {
        "Very Light": 1.20, # Little to no exercise, desk job
        "Light": 1.375, # Light exercise, 1 to 3 days per week
        "Moderate": 1.55, # Moderate exercise, 6 to 7 days per week
        "Heavy": 1.725, # Hard exercise every day, some days 2 times per day
        "Extremely active": 1.9 # Hard exercise twice or more daily every day, or marathon / triathlon training
    }
    
    diet_goals = {
        "Maintain Weight": (1.0, 27.5), # Pass the protein multiplier and the fat multiplier in brackets
        "Maintain Muscle Mass": (1.6, 27.5), # Pass the protein multiplier and the fat multiplier in brackets
        "Lose Fat": (2.0, 22.5), # Pass the protein multiplier and the fat multiplier in brackets
        "Build Muscle": (2.0, 30.0), # Pass the protein multiplier and the fat multiplier in brackets
        "Athlete": (2.0, 30.0) # Pass the protein multiplier and the fat multiplier in brackets
    }

    if goal not in diet_goals:
        raise ValueError("Invalid goal specified.") # Extra debugging, if this was true then something with the json packet must be corrupt

    if activity_level not in activity_multipliers:
        raise ValueError(f"Invalid activity level specified: {activity_level}") # Extra debugging, if this was true then something with the json packet must be corrupt

    activity_multiplier = activity_multipliers[activity_level] # Pass the correct multiplier based on the activity level
    protein_per_kg, fat_percentage = diet_goals[goal] # Pass the protein and fat multipliers based on the goal

    protein_intake = protein_per_kg * weight # Multiply the protein multiplier with the weight of the user
    bmr = calculate_bmr(weight, height, age, gender) # Pass all parameters to the calculate_bmr function
    tdee = calculate_tdee(bmr, activity_multiplier) # Pass all the parameters to the calculate_tdee function

    macros = calculate_macros(tdee, protein_intake, fat_percentage) # Pass all the parameters to calculate_macros function

    return macros