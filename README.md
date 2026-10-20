# Meal Creation Diet Planner (MCDP)

A Flask web app that works out a user's daily calorie and macronutrient targets and builds a personalised 7-day meal plan (breakfast, lunch and dinner) from a MySQL database of ~400 foods.

- **Targets:** BMR (Mifflin–St Jeor) × activity multiplier = TDEE, then protein/fat/carbs are split according to the user's goal.
- **Meal plan:** a genetic algorithm (population 50, 150 generations) searches for food combinations, and SciPy optimises the serving sizes so each day lands within ±10% of the targets.
- **Filters:** diet (vegan, vegetarian, pescatarian, omnivore), foods to exclude, and a "meal variety" slider that controls how often foods can appear outside their usual meal.
- **Accounts:** works as a guest (plan kept in the session) or with a registered account (plan saved to the database and reloaded on login). Individual days can be regenerated, and users can delete their account or session data.

## Project structure

```
Meal-Creation-Diet-Planner/
├── app.py                 # Flask entry point: routes, login/registration, sessions
├── app/
│   ├── Calculator.py      # BMR, TDEE and macronutrient calculations
│   └── MCDPLogic.py       # Meal plan generation (genetic algorithm) + database read/write
├── templates/
│   ├── Dashboard.html     # Main page: input form and 7-day meal plan
│   ├── login.html         # Login page
│   └── register.html      # Registration page
├── static/
│   ├── script.js          # Front-end logic: sends the form, renders the plan, regenerate/delete buttons
│   └── styles.css         # Styling
├── export.sql             # MySQL dump: table definitions + food data
├── versions.txt           # Python and library versions used
├── testing.py             # Evaluation test suite (all tests commented out by default)
├── *_results.csv          # Saved test results
└── *_results.png          # Charts generated from the test results
```

### What each file does

| File | Purpose |
|---|---|
| `app.py` | Creates the Flask app, sets up Flask-Login, and defines every route (see below). Passwords are hashed with bcrypt. |
| `app/Calculator.py` | `calculate_macronutrients()` takes weight, height, age, gender, activity level and goal and returns daily calories, protein, carbs and fats. |
| `app/MCDPLogic.py` | Fetches foods filtered by diet and exclusions, runs the genetic algorithm (`Individual`, `crossover`, `mutate`, `evaluate_fitness`), adjusts meals to their categories, and saves/loads user details and meal plans. `generate_meal_plan()` is the main entry point. |
| `templates/*.html` | Jinja2 templates for the dashboard, login and registration pages. |
| `static/script.js` | Calls the Flask endpoints with `fetch()` and draws the meal plan, totals and targets on the page. |
| `static/styles.css` | Page styling. |
| `export.sql` | Creates the `User`, `Food`, `Food_High`, `Food_Preference` and `Diet_Plan_Food` tables and fills `Food` (nutrition per serving, meal category, diet type) and `Food_High` (high-carb tags). User tables are empty. |
| `versions.txt` | The exact versions the project was built with. |
| `testing.py` | The evaluation tests used to produce the CSV and PNG results (see [Running the tests](#running-the-tests)). |

### Routes in `app.py`

| Route | Method | What it does |
|---|---|---|
| `/` | GET | Dashboard (pre-fills the form for logged-in users) |
| `/login`, `/register` | GET, POST | Log in / create an account |
| `/logout` | GET | Log out |
| `/calculate` | POST | Generate a new 7-day meal plan from the form data |
| `/regenerate_day` | POST | Regenerate a single day of the current plan |
| `/get_last_meal_plan` | GET | Load the logged-in user's last saved plan |
| `/delete_account` | POST | Delete the user and all their saved data |
| `/delete_session_data` | POST | Clear a guest's session data |

## Requirements

- Python 3.12
- MySQL 8.0
- Python packages: Flask 3.0.3, Werkzeug 3.0.3, Flask-Login 0.6.3, Jinja2 3.1.4, bcrypt 4.3.0, mysql-connector-python 9.0.0, SciPy

## How to run

**1. Clone the repo and install the packages**

```bash
git clone https://github.com/Halasa11/Meal-Creation-Diet-Planner.git
cd Meal-Creation-Diet-Planner

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install Flask==3.0.3 Werkzeug==3.0.3 Flask-Login==0.6.3 Jinja2==3.1.4 bcrypt==4.3.0 mysql-connector-python==9.0.0 scipy
```

**2. Create the database**

The dump doesn't create the database itself, so create `MCDP` first and then import into it:

```bash
mysql -u root -p -e "CREATE DATABASE MCDP;"
mysql -u root -p MCDP < export.sql
```

**3. Set your MySQL credentials**

The connection details are hard-coded in `get_db_connection()` in **two** places: `app.py` and `app/MCDPLogic.py`. Change `user` and `password` in both to match your MySQL setup (host `127.0.0.1`, port `3306`, database `MCDP`).

**4. Make sure `app/` is a package**

`app.py` imports from `app.MCDPLogic`, which only works if the `app/` folder contains an `__init__.py` file. If you see `ModuleNotFoundError: 'app' is not a package`, create an empty one:

```bash
touch app/__init__.py             # Windows: type nul > app\__init__.py
```

**5. Start the app**

Run from the project root:

```bash
python app.py
```

Then open **http://127.0.0.1:5000**. Fill in your details and click calculate to get a plan, or register/log in to have it saved. Generating a plan takes a few seconds while the genetic algorithm runs; progress is printed in the terminal.

## Running the tests

All tests live in `testing.py` and are **commented out**. To run one, uncomment its block (its functions plus its `if __name__ == "__main__":` section) and run:

```bash
pip install pandas numpy matplotlib requests locust
python testing.py
```

The tests use the same database connection as the app, so complete steps 2–4 above first.

| Test | What it measures | Output |
|---|---|---|
| MAPE | How close generated plans are to the calorie/macro targets | `mape_test_results.csv`, `mape_results.png` |
| Diversity score | Food variety across plans at different meal-variety settings | `diversity_score_test_results.csv`, `diversity_score_results.png` |
| Response time | How long plan generation takes | `response_time_results.csv`, `response_time_boxplot.png` |
| Diet compliance | Whether plans respect vegan/vegetarian/pescatarian choices | `diet_compliance_test_results.csv`, `diet_compliance_results.png` |
| Database integrity | Test users and their data are saved and fully deleted | `database_integrity_test_results.csv`, `database_integrity_results.png` |
| Security & privacy | Password hashing, account deletion and session clearing | `security_privacy_test_results.csv`, `security_privacy_results.png` |
| Scalability | Load test with Locust (30 users, 6 minutes). **Start the app with `python app.py` first** | `scalability_test_results.csv`, `scalability_results.png` |
| Nutritional consistency | Repeated runs for the same user stay close to target | `nutritional_consistency_results.csv`, `consistency_plot.png` |
