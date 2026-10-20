import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import subprocess
import os
import requests
import mysql.connector
import traceback
from scipy.stats import f_oneway
from uuid import uuid4
from flask import Flask, session
from flask_login import LoginManager, UserMixin, login_user, logout_user
from app.MCDPLogic import generate_meal_plan, get_user_requirements, get_db_connection, save_meal_plan, get_last_meal_plan, fetch_food_data
from app.Calculator import calculate_macronutrients

############################################################# MAPE Test #############################################################

# def generate_sample_users(n_users=50):
#     activity_levels = ["Very Light", "Light", "Moderate", "Heavy", "Extremely active"]
#     goals = ["Maintain Weight", "Maintain Muscle Mass", "Lose Fat", "Build Muscle", "Athlete"]
#     diets = ["Vegan", "Vegetarian", "Pescatarian", "Omnivore"]
#     genders = ["male", "female"]
#     preferences = ["", "nuts", "milk, cheese", "nuts, milk, cheese, olives"]

#     users = []
#     for _ in range(n_users):
#         user = {
#             "weight": random.uniform(50, 100),
#             "height": random.uniform(150, 190),
#             "age": random.randint(18, 60),
#             "gender": random.choice(genders),
#             "activity": random.choice(activity_levels),
#             "goal": random.choice(goals),
#             "diet": random.choice(diets),
#             "preferences": random.choice(preferences),
#             "meal_variety": random.randint(0, 100)  # 0% to 100%
#         }
#         users.append(user)
#     return users

# def calculate_mape(actual, target):
#     if len(actual) != len(target):
#         raise ValueError("Actual and target arrays must have the same length")
#     actual = np.array(actual)
#     target = np.array(target)
#     epsilon = 1e-10
#     mape = np.mean(np.abs((actual - target) / (target + epsilon))) * 100
#     return mape

# def run_mape_test():
#     try:
#         users = generate_sample_users(50)
#         results = []

#         for i, user_data in enumerate(users):
#             try:
#                 user_requirements, _ = get_user_requirements(user_data=user_data)
#                 meal_plan, daily_requirements = generate_meal_plan(user_data=user_data)

#                 # Verify exactly three ingredients per meal
#                 for day in meal_plan:
#                     for meal_type in ["Breakfast", "Lunch", "Dinner"]:
#                         if len(day[meal_type]) != 3:
#                             print(f"Warning: Day {day['Day']} {meal_type} has {len(day[meal_type])} ingredients, expected 3")

#                 target_calories = daily_requirements["calories"]
#                 target_protein = daily_requirements["protein"]
#                 target_carbs = daily_requirements["carbs"]
#                 target_fats = daily_requirements["fats"]

#                 actual_calories = []
#                 actual_protein = []
#                 actual_carbs = []
#                 actual_fats = []

#                 for day in meal_plan:
#                     daily_totals = day["totals"]["daily"]
#                     actual_calories.append(daily_totals["calories"])
#                     actual_protein.append(daily_totals["protein"])
#                     actual_carbs.append(daily_totals["carbs"])
#                     actual_fats.append(daily_totals["fats"])

#                 mape_calories = calculate_mape(actual_calories, [target_calories] * 7)
#                 mape_protein = calculate_mape(actual_protein, [target_protein] * 7)
#                 mape_carbs = calculate_mape(actual_carbs, [target_carbs] * 7)
#                 mape_fats = calculate_mape(actual_fats, [target_fats] * 7)

#                 results.append({
#                     "user_id": i + 1,
#                     "mape_calories": mape_calories,
#                     "mape_protein": mape_protein,
#                     "mape_carbs": mape_carbs,
#                     "mape_fats": mape_fats,
#                     "weight": user_data["weight"],
#                     "height": user_data["height"],
#                     "age": user_data["age"],
#                     "gender": user_data["gender"],
#                     "activity": user_data["activity"],
#                     "goal": user_data["goal"],
#                     "diet": user_data["diet"],
#                     "meal_variety": user_data["meal_variety"]
#                 })

#                 print(f"User {i + 1}: MAPE Calories = {mape_calories:.2f}%, "
#                       f"Protein = {mape_protein:.2f}%, Carbs = {mape_carbs:.2f}%, Fats = {mape_fats:.2f}%")

#             except Exception as e:
#                 print(f"Error processing user {i + 1}: {str(e)}")
#                 traceback.print_exc()

#         results_df = pd.DataFrame(results)

#         mean_mape = {
#             "calories": results_df["mape_calories"].mean(),
#             "protein": results_df["mape_protein"].mean(),
#             "carbs": results_df["mape_carbs"].mean(),
#             "fats": results_df["mape_fats"].mean()
#         }
#         std_mape = {
#             "calories": results_df["mape_calories"].std(),
#             "protein": results_df["mape_protein"].std(),
#             "carbs": results_df["mape_carbs"].std(),
#             "fats": results_df["mape_fats"].std()
#         }

#         print("\nSummary Statistics:")
#         print(f"Mean MAPE: Calories = {mean_mape['calories']:.2f}%, "
#               f"Protein = {mean_mape['protein']:.2f}%, Carbs = {mean_mape['carbs']:.2f}%, "
#               f"Fats = {mean_mape['fats']:.2f}%")
#         print(f"Std MAPE: Calories = {std_mape['calories']:.2f}%, "
#               f"Protein = {std_mape['protein']:.2f}%, Carbs = {std_mape['carbs']:.2f}%, "
#               f"Fats = {std_mape['fats']:.2f}%")

#         results_df.to_csv("mape_test_results.csv", index=False)
#         print("Results saved to mape_test_results.csv")

#         return results_df, mean_mape, std_mape

#     except Exception as e:
#         print(f"Error running MAPE test: {str(e)}")
#         traceback.print_exc()
#         return None, None, None

# def analyze_mape_results(csv_file):
#     try:
#         df = pd.read_csv(csv_file)
#         mape_columns = ["mape_calories", "mape_protein", "mape_carbs", "mape_fats"]
        
#         mean_mape = df[mape_columns].mean()
#         std_mape = df[mape_columns].std()

#         print("Summary Statistics:")
#         print(f"Mean MAPE: Calories = {mean_mape['mape_calories']:.2f}%, "
#               f"Protein = {mean_mape['mape_protein']:.2f}%, "
#               f"Carbs = {mean_mape['mape_carbs']:.2f}%, "
#               f"Fats = {mean_mape['mape_fats']:.2f}%")
#         print(f"Std MAPE: Calories = {std_mape['mape_calories']:.2f}%, "
#               f"Protein = {std_mape['mape_protein']:.2f}%, "
#               f"Carbs = {std_mape['mape_carbs']:.2f}%, "
#               f"Fats = {std_mape['mape_fats']:.2f}%")

#         nutrients = ["Calories", "Protein", "Carbs", "Fats"]
#         mape_values = [mean_mape[col] for col in mape_columns]
        
#         plt.figure(figsize=(8, 6))
#         bars = plt.bar(nutrients, mape_values, color=["#2563eb", "#4f46e5", "#7f9cf5", "#c3dafe"])
#         plt.title("Mean Absolute Percentage Error (MAPE) for Nutritional Targets")
#         plt.xlabel("Nutrient")
#         plt.ylabel("MAPE (%)")
#         plt.ylim(0, max(mape_values) + 5)
        
#         for bar in bars:
#             yval = bar.get_height()
#             plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f"{yval:.2f}%", ha="center", va="bottom")
        
#         plt.savefig("mape_results.png")
#         plt.close()
#         print("Bar chart saved as mape_results.png")

#         return mean_mape, std_mape, df

#     except Exception as e:
#         print(f"Error analyzing MAPE results: {str(e)}")
#         return None, None, None

# def check_mape_thresholds(mean_mape, threshold=5.0):
#     print("\nMAPE Threshold Check (Threshold = 5%):")
#     for nutrient, value in mean_mape.items():
#         status = "Pass" if value < threshold else "Fail"
#         print(f"{nutrient.capitalize()}: {value:.2f}% ({status})")

# if __name__ == "__main__":
#     results_df, mean_mape, std_mape = run_mape_test()
#     if results_df is not None:
#         mean_mape, std_mape, df = analyze_mape_results("mape_test_results.csv")
#         if mean_mape is not None:
#             check_mape_thresholds(mean_mape)

############################################################# Diversity Score Test #############################################################

# def generate_sample_users(n_users_per_rate=50):
#     activity_levels = ["Moderate"]
#     goals = ["Lose Fat"]
#     diets = ["Omnivore"]
#     genders = ["male"]
#     cross_category_percentages = [0, 50, 100]  # Test strict, moderate, and full cross-category allowance

#     users = []
#     for percentage in cross_category_percentages:
#         for _ in range(n_users_per_rate):
#             user = {
#                 "weight": 70.0,
#                 "height": 170.0,
#                 "age": 30,
#                 "gender": random.choice(genders),
#                 "activity": random.choice(activity_levels),
#                 "goal": random.choice(goals),
#                 "diet": random.choice(diets),
#                 "preferences": "",
#                 "meal_variety": percentage
#             }
#             users.append(user)
#     return users

# def calculate_diversity_score(meal_plan):
#     unique_items = set()
#     total_slots = 0

#     for day in meal_plan:
#         for meal_type in ["Breakfast", "Lunch", "Dinner"]:
#             meal = day[meal_type]
#             for ingredient in meal:
#                 unique_items.add(ingredient)
#                 total_slots += 1
    
#     expected_slots = 7 * 3 * 3  # 7 days, 3 meals, 3 ingredients
#     if total_slots != expected_slots:
#         print(f"Warning: Total slots ({total_slots}) does not match expected ({expected_slots})")
    
#     diversity_score = len(unique_items) / expected_slots
#     return diversity_score, len(unique_items)

# def run_diversity_score_test():
#     try:
#         users = generate_sample_users(n_users_per_rate=10)
#         results = []

#         for i, user_data in enumerate(users):
#             try:
#                 meal_plan, _ = generate_meal_plan(user_data=user_data)

#                 # Verify exactly three ingredients per meal
#                 for day in meal_plan:
#                     for meal_type in ["Breakfast", "Lunch", "Dinner"]:
#                         if len(day[meal_type]) != 3:
#                             print(f"Warning: Day {day['Day']} {meal_type} has {len(day[meal_type])} ingredients, expected 3")

#                 diversity_score, unique_item_count = calculate_diversity_score(meal_plan)

#                 results.append({
#                     "user_id": i + 1,
#                     "meal_variety": user_data["meal_variety"],
#                     "diversity_score": diversity_score,
#                     "unique_items": unique_item_count,
#                     "weight": user_data["weight"],
#                     "height": user_data["height"],
#                     "age": user_data["age"],
#                     "gender": user_data["gender"],
#                     "activity": user_data["activity"],
#                     "goal": user_data["goal"],
#                     "diet": user_data["diet"]
#                 })

#                 print(f"User {i + 1} (Cross-Category %: {user_data["meal_variety"]}): "
#                       f"Diversity Score = {diversity_score:.3f}, Unique Items = {unique_item_count}")

#             except Exception as e:
#                 print(f"Error processing user {i + 1}: {str(e)}")
#                 traceback.print_exc()

#         results_df = pd.DataFrame(results)

#         grouped_stats = results_df.groupby("cross_category_percentage")["diversity_score"].agg(["mean", "std"]).reset_index()
#         print("\nSummary Statistics by Cross-Category Percentage:")
#         for _, row in grouped_stats.iterrows():
#             print(f"Cross-Category {row['cross_category_percentage']}%: "
#                   f"Mean Diversity Score = {row['mean']:.3f}, Std = {row['std']:.3f}")

#         low_scores = results_df[results_df["cross_category_percentage"] == 0]["diversity_score"]
#         moderate_scores = results_df[results_df["cross_category_percentage"] == 50]["diversity_score"]
#         high_scores = results_df[results_df["cross_category_percentage"] == 100]["diversity_score"]
        
#         f_stat, p_val = f_oneway(low_scores, moderate_scores, high_scores)
#         print(f"\nANOVA Test Results: F-value = {f_stat:.2f}, p-value = {p_val:.4f}")

#         plt.figure(figsize=(8, 6))
#         plt.plot(grouped_stats["cross_category_percentage"], grouped_stats["mean"], marker="o", color="#2563eb", label="Mean Diversity Score")
#         plt.fill_between(grouped_stats["cross_category_percentage"],
#                          grouped_stats["mean"] - grouped_stats["std"],
#                          grouped_stats["mean"] + grouped_stats["std"],
#                          color="#2563eb", alpha=0.2, label="±1 Std")
#         plt.title("Diversity Score Across Cross-Category Percentages")
#         plt.xlabel("Cross-Category Percentage (%)")
#         plt.ylabel("Diversity Score")
#         plt.ylim(0, 1)
#         plt.xticks([0, 50, 100])
#         plt.legend()
#         plt.grid(True)
#         plt.savefig("diversity_score_results.png")
#         plt.close()
#         print("Line graph saved as diversity_score_results.png")

#         results_df.to_csv("diversity_score_test_results.csv", index=False)
#         print("Results saved to diversity_score_test_results.csv")

#         return results_df, grouped_stats

#     except Exception as e:
#         print(f"Error running Diversity Score test: {str(e)}")
#         traceback.print_exc()
#         return None, None

# if __name__ == "__main__":
#     results_df, grouped_stats = run_diversity_score_test()

# ############################################################# Response Time Test #############################################################

# def generate_sample_users(n_users=20):
#     activity_levels = ["Very Light", "Light", "Moderate", "Heavy", "Extremely active"]
#     goals = ["Maintain Weight", "Maintain Muscle Mass", "Lose Fat", "Build Muscle", "Athlete"]
#     diets = ["Vegan", "Vegetarian", "Pescatarian", "Omnivore"]
#     genders = ["male", "female"]
#     preferences = ["", "nuts", "milk, cheese", "nuts, milk, cheese, olives"]

#     users = []
#     for _ in range(n_users):
#         user = {
#             "weight": random.uniform(50, 100),
#             "height": random.uniform(150, 190),
#             "age": random.randint(18, 60),
#             "gender": random.choice(genders),
#             "activity": random.choice(activity_levels),
#             "goal": random.choice(goals),
#             "diet": random.choice(diets),
#             "preferences": random.choice(preferences),
#             "meal_variety": random.randint(0, 100)
#         }
#         users.append(user)
#     return users

# def run_response_time_test(n_users=20, runs_per_user=2):
#     try:
#         users = generate_sample_users(n_users)
#         avg_response_times = []

#         for i, user_data in enumerate(users):
#             print(f"\nTesting User {i+1}...")
#             user_times = []
#             for run in range(runs_per_user):
#                 try:
#                     start_time = time.time()
#                     meal_plan, _ = generate_meal_plan(user_data=user_data)
#                     end_time = time.time()
#                     response_time = end_time - start_time
#                     user_times.append(response_time)
#                     print(f"Run {run+1} for User {i+1}: {response_time:.2f} seconds")
                    
#                     # Verify three ingredients per meal
#                     for day in meal_plan:
#                         for meal_type in ["Breakfast", "Lunch", "Dinner"]:
#                             if len(day[meal_type]) != 3:
#                                 print(f"Warning: Day {day['Day']} {meal_type} has {len(day[meal_type])} ingredients, expected 3")
#                 except Exception as e:
#                     print(f"Error during Run {run+1} for User {i+1}: {str(e)}")
#                     traceback.print_exc()
            
#             if user_times:
#                 avg_time = np.mean(user_times)
#                 avg_response_times.append(avg_time)
#                 print(f"Average for User {i+1}: {avg_time:.2f} seconds")

#         avg_response_times = np.array(avg_response_times)
#         median_time = np.median(avg_response_times)
#         mean_time = np.mean(avg_response_times)
#         std_time = np.std(avg_response_times)
#         q1 = np.percentile(avg_response_times, 25)
#         q3 = np.percentile(avg_response_times, 75)
#         iqr = q3 - q1

#         print("\nSummary Statistics:")
#         print(f"Median Average Response Time: {median_time:.2f} seconds")
#         print(f"Mean Average Response Time: {mean_time:.2f} seconds")
#         print(f"Std Dev: {std_time:.2f} seconds")
#         print(f"IQR: {q1:.2f}–{q3:.2f} seconds")

#         results_df = pd.DataFrame({
#             "user_id": range(1, len(avg_response_times) + 1),
#             "average_response_time": avg_response_times
#         })
#         results_df.to_csv("response_time_results.csv", index=False)
#         print("Results saved to response_time_results.csv")

#         plt.figure(figsize=(8, 6))
#         plt.boxplot(avg_response_times, labels=["MCDP"])
#         plt.title("Average Response Time per User (MCDP)")
#         plt.ylabel("Average Response Time (seconds)")
#         plt.grid(True, axis="y")
#         plt.scatter(np.ones_like(avg_response_times), avg_response_times, alpha=0.7)
#         plt.savefig("response_time_boxplot.png")
#         plt.close()
#         print("Box plot saved as response_time_boxplot.png")

#         return avg_response_times, median_time, mean_time, std_time, iqr

#     except Exception as e:
#         print(f"Error running response time test: {str(e)}")
#         traceback.print_exc()
#         return None, None, None, None, None

# if __name__ == "__main__":
#     run_response_time_test(n_users=20, runs_per_user=2)

# ############################################################# Diet Compliance Test #############################################################

# def generate_sample_users(n_users=5):
#     activity_levels = ["Very Light", "Light", "Moderate", "Heavy", "Extremely active"]
#     goals = ["Maintain Weight", "Maintain Muscle Mass", "Lose Fat", "Build Muscle", "Athlete"]
#     diets = ["Vegan", "Vegetarian", "Pescatarian", "Omnivore"]
#     genders = ["male", "female"]
#     preferences = ["", "nuts", "milk, cheese", "nuts, milk, cheese, olives"]

#     users = []
#     for _ in range(n_users):
#         user = {
#             "weight": random.uniform(50, 100),
#             "height": random.uniform(150, 190),
#             "age": random.randint(18, 60),
#             "gender": random.choice(genders),
#             "activity": random.choice(activity_levels),
#             "goal": random.choice(goals),
#             "diet": random.choice(diets),
#             "preferences": random.choice(preferences),
#             "meal_variety": random.randint(0, 100)
#         }
#         users.append(user)
#     return users

# def check_diet_compliance(meal_plan, user_diet, conn):
#     cursor = conn.cursor(dictionary=True)
    
#     compliant_meals = 0
#     total_meals = 0
#     non_compliant_details = []

#     allowed_diets = []
#     user_diet = user_diet.lower()
#     if user_diet == "vegan":
#         allowed_diets = ["vegan"]
#     elif user_diet == "vegetarian":
#         allowed_diets = ["vegan", "vegetarian"]
#     elif user_diet == "pescatarian":
#         allowed_diets = ["vegan", "vegetarian", "pescatarian"]
#     elif user_diet == "omnivore":
#         allowed_diets = ["vegan", "vegetarian", "pescatarian", ""]

#     for day in meal_plan:
#         for meal_type in ["Breakfast", "Lunch", "Dinner"]:
#             total_meals += 1
#             meal = day.get(meal_type, {})
#             compliant = True

#             ingredients = list(meal.keys())
#             if ingredients:
#                 placeholders = ",".join(["%s"] * len(ingredients))
#                 query = f"SELECT food_item, diet FROM Food WHERE food_item IN ({placeholders})"
#                 cursor.execute(query, ingredients)
#                 results = cursor.fetchall()

#                 ingredient_diets = {r["food_item"]: r["diet"] if r["diet"] else "" for r in results}

#                 non_compliant_ingredients = []
#                 for ingredient in ingredients:
#                     if ingredient not in ingredient_diets or ingredient_diets[ingredient] not in allowed_diets:
#                         compliant = False
#                         non_compliant_ingredients.append(ingredient)
                        
#                     if not compliant:
#                         non_compliant_details.append({
#                             "day": day_index + 1,
#                             "meal": meal_type,
#                             "ingredients": non_compliant_ingredients
#                     })
#             else:
#                 compliant = False
#                 non_compliant_details.append({
#                     "day": day_index + 1,
#                     "meal": meal_type,
#                     "ingredients": []
#                 })

#             if compliant:
#                 compliant_meals += 1

#     compliance_rate = (compliant_meals / total_meals) * 100 if total_meals > 0 else 0

#     cursor.close()
#     return compliance_rate, compliant_meals, total_meals, non_compliant_details

# def run_diet_compliance_test():
#     conn = get_db_connection()
#     users = generate_sample_users(5)
#     results = []

#     for i, user_data in enumerate(users):
#         meal_plan, _ = generate_meal_plan(user_data=user_data)
#         compliance_rate, compliant_meals, total_meals, non_compliant_details = check_diet_compliance(meal_plan, user_data["diet"], conn)

#         results.append({
#             "user_id": i + 1,
#             "diet": user_data["diet"],
#             "compliance_rate": compliance_rate,
#             "compliant_meals": compliant_meals,
#             "total_meals": total_meals,
#             "non_compliant_details": non_compliant_details,
#             "weight": user_data["weight"],
#             "height": user_data["height"],
#             "age": user_data["age"],
#             "gender": user_data["gender"],
#             "activity": user_data["activity"],
#             "goal": user_data["goal"],
#             "meal_variety": user_data["meal_variety"]
#         })

#         print(f"User {i + 1} ({user_data['diet']}): Compliance Rate = {compliance_rate:.2f}%")

#     conn.close()

#     results_df = pd.DataFrame(results)
#     results_df.to_csv("diet_compliance_test_results.csv", index=False)
#     print("\nResults saved to diet_compliance_test_results.csv")

#     compliance_by_diet = results_df.groupby("diet")["compliance_rate"].mean().to_dict()

#     diet_types = list(compliance_by_diet.keys())
#     mean_compliance = [compliance_by_diet[diet] for diet in diet_types]

#     plt.figure(figsize=(8, 6))
#     bars = plt.bar(diet_types, mean_compliance, color=["#2563eb", "#4f46e5", "#7f9cf5", "#c3dafe"])

#     plt.title("Diet Compliance Rate by Diet Type", pad=20)
#     plt.xlabel("Diet Type")
#     plt.ylabel("Compliance Rate (%)")

#     max_compliance = max(mean_compliance)
#     plt.ylim(0, max_compliance + 10)

#     for bar in bars:
#         yval = bar.get_height()
#         plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval:.1f}%", ha="center", va="bottom")

#     plt.tight_layout()
#     plt.savefig("diet_compliance_results.png")
#     plt.close()
#     print("Bar chart saved as diet_compliance_results.png")

# if __name__ == "__main__":
#     run_diet_compliance_test()

# ############################################################# Database Integrity Test #############################################################

# def generate_sample_users(n_users=10):
#     activity_levels = ["Very Light", "Light", "Moderate", "Heavy", "Extremely active"]
#     goals = ["Maintain Weight", "Maintain Muscle Mass", "Lose Fat", "Build Muscle", "Athlete"]
#     diets = ["Vegan", "Vegetarian", "Pescatarian", "Omnivore"]
#     genders = ["male", "female"]
#     preferences = ["", "nuts", "milk, cheese", "nuts, milk, cheese, olives"]

#     users = []
#     for _ in range(n_users):
#         user = {
#             "weight": random.uniform(50, 100),
#             "height": random.uniform(150, 190),
#             "age": random.randint(18, 60),
#             "gender": random.choice(genders),
#             "activity": random.choice(activity_levels),
#             "goal": random.choice(goals),
#             "diet": random.choice(diets),
#             "preferences": random.choice(preferences),
#             "meal_variety": random.randint(0, 100)
#         }
#         users.append(user)
#     return users

# def create_test_user(user_data, conn):
#     cursor = conn.cursor()
#     username = f"test_user_{random.randint(1000, 9999)}"
#     password_hash = "hashed_password"
#     cursor.execute("""
#         INSERT INTO User (username, password_hash, age, weight, height, gender, activity_level, goal, diet)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """, (
#         username,
#         password_hash,
#         user_data["age"],
#         user_data["weight"],
#         user_data["height"],
#         1 if user_data["gender"] == "male" else 0,
#         user_data["activity"],
#         user_data["goal"],
#         user_data["diet"]
#     ))
#     conn.commit()
#     cursor.execute("SELECT LAST_INSERT_ID()")
#     user_id = cursor.fetchone()[0]
#     cursor.close()
#     return user_id

# def delete_test_user(user_id, conn):
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM Diet_Plan_Food WHERE user_id = %s", (user_id,))
#     cursor.execute("DELETE FROM Food_Preference WHERE user_id = %s", (user_id,))
#     cursor.execute("DELETE FROM User WHERE user_id = %s", (user_id,))
#     conn.commit()
#     cursor.close()

# def verify_deletion(user_id, conn):
#     cursor = conn.cursor()
#     cursor.execute("SELECT COUNT(*) FROM User WHERE user_id = %s", (user_id,))
#     user_count = cursor.fetchone()[0]
#     cursor.execute("SELECT COUNT(*) FROM Diet_Plan_Food WHERE user_id = %s", (user_id,))
#     diet_plan_count = cursor.fetchone()[0]
#     cursor.execute("SELECT COUNT(*) FROM Food_Preference WHERE user_id = %s", (user_id,))
#     preference_count = cursor.fetchone()[0]
#     cursor.close()
#     return user_count == 0 and diet_plan_count == 0 and preference_count == 0

# def run_database_integrity_test():
#     conn = get_db_connection()
#     users = generate_sample_users(10)

#     save_success = 0
#     retrieval_success = 0
#     deletion_success = 0

#     for i, user_data in enumerate(users):
#         print(f"Testing User {i+1}...")
#         user_id = create_test_user(user_data, conn)
#         meal_plan, _ = generate_meal_plan(user_data=user_data)
        
#         # Verify three ingredients per meal
#         for day in meal_plan:
#             for meal_type in ["Breakfast", "Lunch", "Dinner"]:
#                 if len(day[meal_type]) != 3:
#                     print(f"Warning: Day {day['Day']} {meal_type} has {len(day[meal_type])} ingredients, expected 3")
        
#         save_meal_plan(user_id, meal_plan)
#         save_success += 1
#         retrieved_plan, _ = get_last_meal_plan(user_id)
#         if retrieved_plan and len(retrieved_plan) == len(meal_plan):
#             retrieval_success += 1
#         delete_test_user(user_id, conn)
#         if verify_deletion(user_id, conn):
#             deletion_success += 1

#     conn.close()

#     total_users = len(users)
#     save_accuracy = (save_success / total_users) * 100
#     retrieval_accuracy = (retrieval_success / total_users) * 100
#     deletion_accuracy = (deletion_success / total_users) * 100

#     print("\nSummary Statistics:")
#     print(f"Save Accuracy: {save_accuracy:.2f}%")
#     print(f"Retrieval Accuracy: {retrieval_accuracy:.2f}%")
#     print(f"Deletion Compliance: {deletion_accuracy:.2f}%")

#     results_df = pd.DataFrame({
#         "metric": ["Save Accuracy", "Retrieval Accuracy", "Deletion Compliance"],
#         "success_rate": [save_accuracy, retrieval_accuracy, deletion_accuracy]
#     })
#     results_df.to_csv("database_integrity_test_results.csv", index=False)
#     print("Results saved to database_integrity_test_results.csv")

#     plt.figure(figsize=(8, 6))
#     bars = plt.bar(results_df["metric"], results_df["success_rate"], color=["#2563eb", "#4f46e5", "#7f9cf5"])
#     plt.title("Database Integrity Success Rates", pad=20)
#     plt.xlabel("Operation")
#     plt.ylabel("Success Rate (%)")
#     plt.ylim(0, 110)
#     for bar in bars:
#         yval = bar.get_height()
#         plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval:.1f}%", ha="center", va="bottom")
#     plt.tight_layout()
#     plt.savefig("database_integrity_results.png")
#     plt.close()
#     print("Bar chart saved as database_integrity_results.png")

# if __name__ == "__main__":
#     run_database_integrity_test()

# ############################################################# Security and Privacy Test #############################################################

# app = Flask(__name__)
# app.secret_key = "test_secret_key_for_security_privacy_test"
# login_manager = LoginManager()
# login_manager.init_app(app)

# class TestUser(UserMixin):
#     def __init__(self, user_id):
#         self.id = user_id

# @login_manager.user_loader
# def load_user(user_id):
#     return TestUser(user_id)

# def hash_password(password):
#     return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# def verify_password(password, hashed_password):
#     return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# def create_test_user(conn):
#     cursor = conn.cursor()
#     username = f"test_user_{random.randint(1000, 9999)}"
#     password = f"password_{random.randint(1000, 9999)}"
#     hashed_password = hash_password(password)

#     cursor.execute("""
#         INSERT INTO User (username, password_hash, age, weight, height, gender, activity_level, goal, diet)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """, (
#         username,
#         hashed_password.decode('utf-8'),
#         random.randint(18, 60),
#         random.uniform(50, 100),
#         random.uniform(150, 190),
#         random.choice([0, 1]),
#         random.choice(["Very Light", "Light", "Moderate", "Heavy", "Extremely active"]),
#         random.choice(["Maintain Weight", "Maintain Muscle Mass", "Lose Fat", "Build Muscle", "Athlete"]),
#         random.choice(["Vegan", "Vegetarian", "Pescatarian", "Omnivore"])
#     ))
#     conn.commit()
#     cursor.execute("SELECT LAST_INSERT_ID()")
#     user_id = cursor.fetchone()[0]
#     cursor.close()
#     return user_id, username, password, hashed_password.decode('utf-8')

# def delete_test_user(user_id, conn):
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM Diet_Plan_Food WHERE user_id = %s", (user_id,))
#     cursor.execute("DELETE FROM Food_Preference WHERE user_id = %s", (user_id,))
#     cursor.execute("DELETE FROM User WHERE user_id = %s", (user_id,))
#     conn.commit()
#     cursor.close()

# def verify_deletion(user_id, conn):
#     cursor = conn.cursor()
#     cursor.execute("SELECT COUNT(*) FROM User WHERE user_id = %s", (user_id,))
#     user_count = cursor.fetchone()[0]
#     cursor.execute("SELECT COUNT(*) FROM Diet_Plan_Food WHERE user_id = %s", (user_id,))
#     diet_plan_count = cursor.fetchone()[0]
#     cursor.execute("SELECT COUNT(*) FROM Food_Preference WHERE user_id = %s", (user_id,))
#     preference_count = cursor.fetchone()[0]
#     cursor.close()
#     return user_count == 0 and diet_plan_count == 0 and preference_count == 0

# def delete_session_data(session):
#     session.clear()
#     return True

# def run_security_privacy_test():
#     conn = get_db_connection()
    
#     total_users = 10
#     total_sessions = 10

#     password_success = 0
#     session_success = 0
#     deletion_success = 0

#     users = []

#     print("Testing Password Hashing...")
#     for _ in range(total_users):
#         user_id, username, password, hashed_password = create_test_user(conn)
#         if verify_password(password, hashed_password.encode('utf-8')):
#             password_success += 1
#         users.append((user_id, username))

#     print("\nTesting Session Security...")
#     with app.test_request_context():
#         for i in range(total_sessions):
#             user = TestUser(i + 1)
#             login_user(user)
#             if session.get('_user_id') == str(i + 1):
#                 session_success += 1
#             logout_user()

#     print("\nTesting Data Deletion...")
#     for user_id, username in users:
#         delete_test_user(user_id, conn)
#         if verify_deletion(user_id, conn):
#             deletion_success += 1

#     with app.test_request_context():
#         session['test_data'] = "guest_data"
#         if delete_session_data(session):
#             deletion_success += 1

#     conn.close()

#     password_security_rate = (password_success / total_users) * 100
#     session_security_rate = (session_success / total_sessions) * 100
#     deletion_rate = (deletion_success / (total_users + 1)) * 100

#     print("\nSummary Statistics:")
#     print(f"Password Security: {password_security_rate:.2f}%")
#     print(f"Session Security: {session_security_rate:.2f}%")
#     print(f"Data Deletion: {deletion_rate:.2f}%")

#     results_df = pd.DataFrame({
#         "metric": ["Password Security", "Session Security", "Data Deletion"],
#         "success_rate": [password_security_rate, session_security_rate, deletion_rate]
#     })
#     results_df.to_csv("security_privacy_test_results.csv", index=False)
#     print("Results saved to security_privacy_test_results.csv")

#     plt.figure(figsize=(8, 6))
#     bars = plt.bar(results_df["metric"], results_df["success_rate"], color=["#2563eb", "#4f46e5", "#7f9cf5"])
#     plt.title("Security and Privacy Success Rates", pad=20)
#     plt.xlabel("Operation")
#     plt.ylabel("Success Rate (%)")
#     plt.ylim(0, 110)
#     for bar in bars:
#         yval = bar.get_height()
#         plt.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval:.1f}%", ha="center", va="bottom")
#     plt.tight_layout()
#     plt.savefig("security_privacy_results.png")
#     plt.close()
#     print("Bar chart saved as security_privacy_results.png")

# if __name__ == "__main__":
#     run_security_privacy_test()

# ############################################################# Scalability Test #############################################################

# def check_flask_app(host="http://127.0.0.1:5000"):
#     try:
#         response = requests.get(host)
#         return response.status_code == 200
#     except requests.ConnectionError:
#         return False

# def generate_locust_script():
#     locust_script = """
# from locust import HttpUser, task, between
# import random

# class MCDPUser(HttpUser):
#     wait_time = between(1, 5)

#     @task
#     def generate_meal_plan(self):
#         user_data = {
#             "weight": random.uniform(50, 100),
#             "height": random.uniform(150, 190),
#             "age": random.randint(18, 60),
#             "gender": random.choice(["male", "female"]),
#             "activity": random.choice(["Very Light", "Light", "Moderate", "Heavy", "Extremely active"]),
#             "goal": random.choice(["Maintain Weight", "Maintain Muscle Mass", "Lose Fat", "Build Muscle", "Athlete"]),
#             "diet": random.choice(["Vegan", "Vegetarian", "Pescatarian", "Omnivore"]),
#             "preferences": random.choice(["", "nuts", "milk, cheese", "nuts, milk, cheese, olives"]),
#             "meal_variety": random.randint(0, 100)
#         }
#         with self.client.post("/calculate", json=user_data, catch_response=True) as response:
#             if response.status_code != 200:
#                 response.failure(f"Status {response.status_code}: {response.text}")
# """
#     with open("locustfile.py", "w") as f:
#         f.write(locust_script)

# def run_locust_test():
#     host = "http://127.0.0.1:5000"
    
#     if not check_flask_app(host):
#         print("Flask app is not running at http://127.0.0.1:5000. Please start it and try again.")
#         return None, None

#     generate_locust_script()

#     cmd = [
#         "locust",
#         "--headless",
#         "--users", "30",
#         "--spawn-rate", "3",
#         "--run-time", "6m",
#         "--host", host,
#         "--csv", "locust_results",
#         "--csv-full-history"
#     ]

#     print("Starting Locust test...")
#     subprocess.run(cmd, check=True)

#     stats_file = "locust_results_stats.csv"
#     if not os.path.exists(stats_file):
#         print("Error: locust_results_stats.csv not found.")
#         return None, None

#     stats_df = pd.read_csv(stats_file)
#     aggregated = stats_df[stats_df["Name"] == "Aggregated"]

#     if aggregated.empty:
#         print("Error: Aggregated results not found in Locust output.")
#         return None, None

#     median_response_time = aggregated["Median Response Time"].iloc[0] / 1000
#     total_requests = aggregated.get("Total Request Count", aggregated.get("Request Count")).iloc[0]
#     failed_requests = aggregated.get("Total Failure Count", aggregated.get("Failure Count")).iloc[0]
#     error_rate = (failed_requests / total_requests) * 100 if total_requests > 0 else 0

#     results_df = pd.DataFrame({
#         "metric": ["Median Response Time", "Total Requests", "Error Rate"],
#         "value": [median_response_time, total_requests, error_rate]
#     })
#     results_df.to_csv("scalability_test_results.csv", index=False)
#     print("Results saved to scalability_test_results.csv")

#     plt.figure(figsize=(8, 6))
#     plt.bar(["Median Response Time"], [median_response_time], color="#2563eb")
#     plt.title("Scalability Test: Median Response Time")
#     plt.ylabel("Time (seconds)")
#     plt.text(0, median_response_time + 0.1, f"{median_response_time:.2f}s", ha="center", va="bottom")
#     plt.ylim(0, median_response_time + 1)
#     plt.savefig("scalability_results.png")
#     plt.close()
#     print("Bar chart saved as scalability_results.png")

#     return results_df, error_rate

# if __name__ == "__main__":
#     run_locust_test()

# ############################################################# Consistency Test #############################################################

# USER_PROFILE = {
#     "weight": 80.0,
#     "height": 170.0,
#     "age": 30,
#     "gender": "male",
#     "activity": "Moderate",
#     "goal": "Lose Fat",
#     "diet": "Omnivore",
#     "preferences": "",
#     "meal_variety": 50
# }

# TOLERANCE = 0.175  # 17.5% tolerance

# def run_test(num_runs=50):
#     results = []
    
#     for run in range(num_runs):
#         print(f"Running iteration {run + 1}/{num_runs}")
#         meal_plan, daily_requirements = generate_meal_plan(user_data=USER_PROFILE)
        
#         # Verify three ingredients per meal
#         for day in meal_plan:
#             for meal_type in ["Breakfast", "Lunch", "Dinner"]:
#                 if len(day[meal_type]) != 3:
#                     print(f"Warning: Day {day['Day']} {meal_type} has {len(day[meal_type])} ingredients, expected 3")
        
#         run_result = {
#             "run": run + 1,
#             "calories_within_range": False,
#             "protein_within_range": False,
#             "carbs_within_range": False,
#             "fats_within_range": False,
#             "calories_mape": 0.0,
#             "protein_mape": 0.0,
#             "carbs_mape": 0.0,
#             "fats_mape": 0.0
#         }
        
#         target = {
#             "calories": daily_requirements["calories"],
#             "protein": daily_requirements["protein"],
#             "carbs": daily_requirements["carbs"],
#             "fats": daily_requirements["fats"]
#         }
        
#         daily_errors = {
#             "calories": [],
#             "protein": [],
#             "carbs": [],
#             "fats": []
#         }
        
#         for day in meal_plan:
#             daily_totals = day["totals"]["daily"]
#             for nutrient in target:
#                 actual = daily_totals[nutrient]
#                 target_value = target[nutrient]
#                 lower_bound = target_value * (1 - TOLERANCE)
#                 upper_bound = target_value * (1 + TOLERANCE)
#                 run_result[f"{nutrient}_within_range"] = lower_bound <= actual <= upper_bound
#                 ape = abs(actual - target_value) / target_value * 100
#                 daily_errors[nutrient].append(ape)
        
#         for nutrient in daily_errors:
#             run_result[f"{nutrient}_mape"] = np.mean(daily_errors[nutrient])
        
#         results.append(run_result)
    
#     return results, target

# def analyze_results(results, target):
#     consistency = {
#         "Calories": np.mean([r["calories_within_range"] for r in results]) * 100,
#         "Protein": np.mean([r["protein_within_range"] for r in results]) * 100,
#         "Carbs": np.mean([r["carbs_within_range"] for r in results]) * 100,
#         "Fats": np.mean([r["fats_within_range"] for r in results]) * 100
#     }
    
#     average_mape = {
#         "Calories": np.mean([r["calories_mape"] for r in results]),
#         "Protein": np.mean([r["protein_mape"] for r in results]),
#         "Carbs": np.mean([ported_mape for r in results]),
#         "Fats": np.mean([r["fats_mape"] for r in results])
#     }
    
#     return consistency, average_mape

# def save_results_to_csv(results, filename="nutritional_consistency_results.csv"):
#     df = pd.DataFrame(results)
#     df.to_csv(filename, index=False)
#     print(f"Results saved to {filename}")

# def plot_consistency(consistency, filename="consistency_plot.png"):
#     nutrients = list(consistency.keys())
#     percentages = list(consistency.values())
    
#     plt.figure(figsize=(10, 6))
#     bars = plt.bar(nutrients, percentages, color=['#4CAF50', '#2196F3', '#FF9800', '#F44336'])
    
#     for bar in bars:
#         height = bar.get_height()
#         plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.1f}%', 
#                 ha='center', va='bottom')
    
#     plt.title('Nutritional Consistency Across 50 Runs (±17.5% Tolerance)')
#     plt.xlabel('Nutrient')
#     plt.ylabel('Percentage of Runs Within Target Range (%)')
#     plt.ylim(0, 100)
#     plt.grid(axis='y', linestyle='--', alpha=0.7)
    
#     plt.savefig(filename)
#     plt.close()
#     print(f"Plot saved to {filename}")

# def main():
#     results, target = run_test(num_runs=50)
#     consistency, average_mape = analyze_results(results, target)
    
#     print("\nConsistency Percentages (±17.5% tolerance):")
#     for nutrient, percentage in consistency.items():
#         print(f"{nutrient}: {percentage:.2f}%")
    
#     print("\nAverage MAPE:")
#     for nutrient, mape in average_mape.items():
#         print(f"{nutrient}: {mape:.2f}%")
    
#     save_results_to_csv(results)
#     plot_consistency(consistency)

# if __name__ == "__main__":
#     main()