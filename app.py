from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app.MCDPLogic import generate_meal_plan, save_user_details, save_meal_plan, get_user_details, get_last_meal_plan, update_meal_plan_day
import bcrypt
import mysql.connector
import traceback

# Initialize Flask application
app = Flask(__name__)
app.secret_key = "my-secret-key" # Secret key for session management

# Initialize Flask-Login for user authentication
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" # Redirect to login page for unauthorized access

# Function to establish a database connection
def get_db_connection():
    return mysql.connector.connect(
        host="", # Localhost
        port="", # Default MySQL port
        user="", # Database user
        password="", # Database password
        database="" # Database name
    )

# User class for Flask-Login, inheriting from UserMixin
class User(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id # Unique user ID
        self.username = username # User's username

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection() # Get database connection
    cursor = conn.cursor(dictionary=True) # Cursor with dictionary results
    cursor.execute("SELECT user_id, username FROM User WHERE user_id = %s", (user_id,))
    user_data = cursor.fetchone() # Fetch user data
    conn.close() # Close connection
    if user_data:
        return User(user_data['user_id'], user_data['username']) # Return User object
    return None # Return None if user not found

# Route for the homepage (dashboard)
@app.route('/')
def index():
    # Fetch user details if authenticated
    user_details = get_user_details(current_user.id) if current_user.is_authenticated else None
    print("user_details on login:", user_details)
    return render_template("Dashboard.html", user_details=user_details) # Render dashboard template

# Route for login page, handles GET and POST requests
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) # Redirect authenticated users to homepage

    if request.method == 'POST':
        username = request.form['username'] # Get username from form
        password = request.form['password'].encode('utf-8') # Get password and encode

        conn = get_db_connection() # Get database connection
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, username, password_hash FROM User WHERE username = %s", (username,))
        user_data = cursor.fetchone() # Fetch user data
        conn.close()

        # Verify password and log in user
        if user_data and bcrypt.checkpw(password, user_data['password_hash'].encode('utf-8')):
            user = User(user_data['user_id'], user_data['username'])
            login_user(user) # Log in the user
            flash('Logged in successfully!', 'success') # Show success message
            return redirect(url_for('index')) # Redirect to homepage
        else:
            flash('Invalid username or password.', 'error') # Show error message
            return render_template("login.html") # Render login page
    else:
        session.pop('_flashes', None) # Clear flashed messages on GET request to prevent displaying stale messages
        return render_template("login.html") # Render login page for GET request

# Route for registration page, handles GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index')) # Redirect authenticated users to homepage

    if request.method == 'POST':
        username = request.form['username'] # Get username from form
        password = request.form['password'].encode('utf-8') # Get password and encode
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8') # Hash password

        conn = get_db_connection() # Get database connection
        cursor = conn.cursor()
        try:
            # Insert new user into database
            cursor.execute(
                "INSERT INTO User (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )
            conn.commit() # Commit transaction
            flash('Registration successful! Please log in.', 'success') # Show success message
            return redirect(url_for('login')) # Redirect to login page
        except mysql.connector.Error as e:
            conn.rollback() # Rollback on error
            flash(f'Registration failed: {str(e)}', 'error') # Show error message
        finally:
            conn.close() # Close connection
    else:
        session.pop('_flashes', None) # Clear flashed messages on GET request to prevent displaying stale messages
        return render_template("register.html") # Render register page for GET request

# Route for logging out
@app.route('/logout')
@login_required
def logout():
    logout_user() # Log out the user
    flash('You have been logged out.', 'success') # Show success message
    return redirect(url_for('index')) # Redirect to homepage

# Route to calculate and generate a meal plan
@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        user_data = request.json # Get user data from JSON request
        # Generate meal plan based on user data
        meal_plan, daily_requirements = generate_meal_plan(user_data=user_data)

        # Save user details and meal plan if authenticated
        if current_user.is_authenticated:
            save_user_details(current_user.id, user_data)
            save_meal_plan(current_user.id, meal_plan)

        # Store user data and meal plan in session for guest users
        session['user_data'] = user_data
        session['current_meal_plan'] = meal_plan

        # Return meal plan and requirements as JSON
        response = {
            "meal_plan": meal_plan,
            "daily_requirements": daily_requirements
        }
        return jsonify(response)
    except Exception as e:
        print("Error in /calculate endpoint:")
        print(traceback.format_exc()) # Log error details
        return jsonify({'error': str(e)}), 500 # Return error response

# Route to regenerate a specific day in the meal plan
@app.route('/regenerate_day', methods=['POST'])
def regenerate_day():
    try:
        # Check if user data exists in session
        if 'user_data' not in session:
            return jsonify({'error': 'No user data available. Please generate a meal plan first.'}), 400

        user_data = session['user_data'] # Get user data from session
        print("User data in /regenerate_day:", user_data)

        data = request.json # Get request data
        day_to_regenerate = data['day'] # Day to regenerate

        # Generate a new meal plan
        meal_plan, daily_requirements = generate_meal_plan(user_data=user_data)
        regenerated_day = meal_plan[day_to_regenerate - 1] # Get specific day

        # Transform meal data to match expected format
        transformed_day = {
            "Day": regenerated_day["Day"],
            "Breakfast": transform_meal(regenerated_day["Breakfast"]),
            "Lunch": transform_meal(regenerated_day["Lunch"]),
            "Dinner": transform_meal(regenerated_day["Dinner"]),
            "totals": regenerated_day["totals"]
        }

        # Update current meal plan in session
        if 'current_meal_plan' not in session:
            return jsonify({'error': 'No current meal plan available. Please generate a meal plan first.'}), 400

        current_meal_plan = session['current_meal_plan']
        current_meal_plan[day_to_regenerate - 1] = transformed_day
        session['current_meal_plan'] = current_meal_plan

        # Update meal plan in database if authenticated
        if current_user.is_authenticated:
            print("Updating meal plan in database for user:", current_user.id)
            update_meal_plan_day(current_user.id, day_to_regenerate, transformed_day)

        # Return regenerated day and requirements
        return jsonify({
            "day": transformed_day,
            "daily_requirements": daily_requirements
        })
    except Exception as e:
        print("Error in /regenerate_day endpoint:")
        print(traceback.format_exc()) # Log error details
        return jsonify({'error': str(e)}), 500 # Return error response

# Route to fetch the last meal plan for the user
@app.route('/get_last_meal_plan', methods=['GET'])
def get_last_meal_plan_endpoint():
    try:
        # Return empty response for unauthenticated users
        if not current_user.is_authenticated:
            return jsonify({'meal_plan': None, 'daily_requirements': None})

        # Fetch last meal plan and requirements
        meal_plan, daily_requirements = get_last_meal_plan(current_user.id)
        if meal_plan:
            # Update session with last meal plan and user data
            session['current_meal_plan'] = meal_plan
            session['user_data'] = get_user_details(current_user.id)
        return jsonify({
            "meal_plan": meal_plan,
            "daily_requirements": daily_requirements
        })
    except Exception as e:
        print("Error in /get_last_meal_plan endpoint:")
        print(traceback.format_exc()) # Log error details
        return jsonify({'error': str(e)}), 500 # Return error response

# Route to delete user account
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    try:
        user_id = current_user.id # Get current user ID
        conn = get_db_connection() # Get database connection
        cursor = conn.cursor()

        # Delete associated meal plan data
        cursor.execute("DELETE FROM Diet_Plan_Food WHERE user_id = %s", (user_id,))

        # Delete associated food preferences
        cursor.execute("DELETE FROM Food_Preference WHERE user_id = %s", (user_id,))

        # Delete user account
        cursor.execute("DELETE FROM User WHERE user_id = %s", (user_id,))

        conn.commit() # Commit transaction
        conn.close()

        # Clear session data
        session.pop('user_data', None)
        session.pop('current_meal_plan', None)

        # Log out the user
        logout_user()
        flash('Your account and all associated data have been deleted.', 'success') # Show success message
        return redirect(url_for('index')) # Redirect to homepage
    except Exception as e:
        print("Error in /delete_account endpoint:")
        print(traceback.format_exc()) # Log error details
        conn.close() # Ensure connection is closed on error
        flash(f'Failed to delete account: {str(e)}', 'error') # Return error response
        return redirect(url_for('index'))

# Route to delete session data for guest users
@app.route('/delete_session_data', methods=['POST'])
def delete_session_data():
    try:
        # Clear session data
        session.pop('user_data', None)
        session.pop('current_meal_plan', None)
        return jsonify({'message': 'Session data deleted successfully.'}), 200 # Return success response
    except Exception as e:
        print("Error in /delete_session_data endpoint:")
        print(traceback.format_exc()) # Log error details
        return jsonify({'error': str(e)}), 500 # Return error response

# Function to transform meal data into expected format
def transform_meal(meal):
    transformed = {}
    for ingredient, data in meal.items():
        if isinstance(data, dict) and "servings" in data:
            transformed[ingredient] = data # Keep existing structure
        else:
            transformed[ingredient] = {
                "servings": data,
                "nutrition": {} # Empty nutrition if not provided
            }
    return transformed

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)