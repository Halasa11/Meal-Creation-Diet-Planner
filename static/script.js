// Global variable to store the current meal plan
let currentMealPlan = null;

// Flag to determine if the device is mobile (screen width <= 768px)
let isMobile = window.innerWidth <= 768;

// Event listener for when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Setup click handlers for diet buttons to toggle active state
    document.querySelectorAll('.diet-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all diet buttons
            document.querySelectorAll('.diet-btn').forEach(btn => btn.classList.remove('active'));
            // Add active class to the clicked button
            this.classList.add('active');
        });
    });

    // Setup click handlers for goal buttons to toggle active state
    document.querySelectorAll('.goal-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all goal buttons
            document.querySelectorAll('.goal-btn').forEach(btn => btn.classList.remove('active'));
            // Add active class to the clicked button
            this.classList.add('active');
        });
    });

    // Setup activity slider to update displayed activity level
    document.getElementById('activity').addEventListener('input', function() {
        // Array of activity levels corresponding to slider values (1 to 5)
        const levels = ["Very Light", "Light", "Moderate", "Heavy", "Extremely Active"];
        // Update text display with the selected activity level
        document.getElementById('activity-level').innerText = levels[this.value - 1];
    });

    // Setup meal variety slider to update displayed value
    document.getElementById('meal-variety').addEventListener('input', function() {
        // Update display with the current slider value
        const value = parseInt(this.value);
        document.getElementById('meal-variety-value').innerText = `${value}%`;
        if (value === 0) {
            alert("Warning: Setting meal variety to 0% may result in some meal slots being empty due to strict category restrictions.");
        }
    });

    // Setup navigation items to toggle section visibility
    const navItems = document.querySelectorAll(".nav-item");
    const sections = document.querySelectorAll(".section");

    navItems.forEach(item => {
        // Skip navigation items that contain links (e.g., Logout, Login)
        if (!item.querySelector('a')) {
            item.addEventListener("click", function() {
                // Remove active class from all navigation items
                navItems.forEach(nav => nav.classList.remove('active'));
                // Add active class to the clicked item
                this.classList.add('active');

                // Hide all sections
                sections.forEach(section => section.classList.add("hidden"));

                // Show the section corresponding to the clicked navigation item
                const target = this.getAttribute("data-target");
                if (target) {
                    document.getElementById(target).classList.remove("hidden");
                }
                
                // On mobile, close the sidebar after selecting a navigation item
                if (isMobile) {
                    toggleSidebar(false);
                }
            });
        }
    });

    // Initialize mobile sidebar toggle functionality
    setupMobileSidebar();

    // Fetch and display the last saved meal plan (if available)
    fetchLastMealPlan();

    // Setup form submission handler with loading animation
    const calcForm = document.querySelector(".calculator-form");
    if (calcForm) {
        calcForm.addEventListener("submit", handleFormSubmit);
    }

    // Check for stored success message after session data deletion
    const sessionDeletedMessage = sessionStorage.getItem('sessionDeletedMessage');
    if (sessionDeletedMessage) {
        alert(sessionDeletedMessage); // Display the success message
        sessionStorage.removeItem('sessionDeletedMessage'); // Clear the message
    }
});

// Function to setup mobile sidebar toggle button and overlay
function setupMobileSidebar() {
    // Create a button for toggling the sidebar on mobile
    const sidebarToggle = document.createElement('button');
    sidebarToggle.className = 'sidebar-toggle';
    sidebarToggle.addEventListener('click', () => toggleSidebar());
    document.body.appendChild(sidebarToggle);
    
    // Create an overlay to dim the background when the sidebar is open
    const overlay = document.createElement('div');
    overlay.className = 'overlay';
    overlay.addEventListener('click', () => toggleSidebar(false));
    document.body.appendChild(overlay);
    
    // Update sidebar state when window is resized
    window.addEventListener('resize', () => {
        // Update isMobile flag based on current window width
        isMobile = window.innerWidth <= 768;
        // If no longer mobile, ensure sidebar and overlay are closed
        if (!isMobile) {
            document.querySelector('.sidebar').classList.remove('active');
            document.querySelector('.overlay').classList.remove('active');
            document.querySelector('.sidebar-toggle').classList.remove('active');
        }
    });
}

// Function to toggle the sidebar visibility
function toggleSidebar(show) {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    
    // Toggle sidebar state if no explicit show/hide is specified
    if (show === undefined) {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
        sidebarToggle.classList.toggle('active');
    } else if (show) {
        // Show sidebar and overlay
        sidebar.classList.add('active');
        overlay.classList.add('active');
        sidebarToggle.classList.add('active');
    } else {
        // Hide sidebar and overlay
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        sidebarToggle.classList.remove('active');
    }
}

// Function to fetch the last saved meal plan from the server
function fetchLastMealPlan() {
    fetch("/get_last_meal_plan", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        // Check if the response is successful
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(result => {
        // If a meal plan and requirements are returned, display them
        if (result.meal_plan && result.daily_requirements) {
            currentMealPlan = result.meal_plan;
            displayResults(result.meal_plan, result.daily_requirements, true);
        }
    })
    .catch(error => {
        // Log errors but don't alert for guest users (they can generate a new plan)
        console.error("Error fetching last meal plan:", error);
    });
}

// Function to regenerate a specific day's meal plan
async function regenerateDay(day, button) {
    if (!confirm("Regenerating this day's meal plan may change the daily calories and macronutrients. Ensure it aligns with your daily needs. You can regenerate as many times as needed. Proceed?")) {
        return;
    }
    try {
        // Add loading animation to the button
        button.classList.add('loading');
        
        // Send request to regenerate the specified day
        const response = await fetch("/regenerate_day", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ day: day })
        });

        // Check if the response is successful
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
        }
        
        // Parse the response
        const responseText = await response.text();
        const result = JSON.parse(responseText);

        // Check for server-side errors
        if (result.error) {
            throw new Error("Error from server: " + result.error);
        }

        // Validate response data
        if (!result.day || !result.daily_requirements) {
            throw new Error("Response missing expected fields: day or daily_requirements");
        }

        // Update the current meal plan with the regenerated day
        currentMealPlan[day - 1] = result.day;
        
        // Display updated meal plan without scrolling
        displayResults(currentMealPlan, result.daily_requirements, false);
    } catch (error) {
        // Log error and show user-friendly message
        console.error("Error regenerating day:", error);
        alert(error.message === 'No user data available. Please generate a meal plan first.' 
            ? "Please generate a new meal plan before regenerating a day."
            : "Failed to regenerate day: " + error.message);
    } finally {
        // Remove loading animation from button
        if (button) button.classList.remove('loading');
    }
}

// Function to display the meal plan and daily requirements
function displayResults(mealPlan, dailyRequirements, shouldScroll = true) {
    const resultDiv = document.getElementById("diet-plan");

    // Handle empty or invalid meal plan
    if (!mealPlan || mealPlan.length === 0) {
        resultDiv.innerHTML = `<h2>Error: No meal plan generated.</h2>`;
        return;
    }

    // Generate HTML for daily nutritional requirements
    let requirementsHTML = `
        <h2>Your Daily Nutritional Requirements</h2>
        <div class="nutrition-requirements">
            <p>Calories: ${Math.round(dailyRequirements.calories)} kcal</p>
            <p>Protein: ${Math.round(dailyRequirements.protein)} g</p>
            <p>Carbs: ${Math.round(dailyRequirements.carbs)} g</p>
            <p>Fats: ${Math.round(dailyRequirements.fats)} g</p>
        </div>
    `;

    // Add a legend for color coding
    let legendHTML = `
        <div class="macro-legend">
            <h3>Meal Color Coding</h3>
            <ul>
                <li class="macro-protein">Protein Dominant</li>
                <li class="macro-carbs">Carbs Dominant</li>
                <li class="macro-fats">Fats Dominant</li>
                <li class="macro-none">No Dominant Macro</li>
            </ul>
        </div>
    `;

    // Generate HTML for the meal plan table
    let tableHTML = `
        <div style="margin-bottom: 10px;">
            <button onclick="window.print()" class="calculate-btn">Print Meal Plan</button>
        </div>
        <h2>Your 7-Day Meal Plan</h2>
        <table border="1" style="width:100%; text-align:left; border-collapse: collapse;">
            <thead>
                <tr>
                    <th style="padding: 10px;">Day</th>
                    <th style="padding: 10px;">Breakfast</th>
                    <th style="padding: 10px;">Lunch</th>
                    <th style="padding: 10px;">Dinner</th>
                </tr>
            </thead>
            <tbody>`;

    // Iterate through each day to populate the table
    mealPlan.forEach(day => {
        tableHTML += `<tr>
            <td style="padding: 10px; font-weight: bold;">
                Day ${day.Day}
                <button onclick="regenerateDay(${day.Day}, this)" class="calculate-btn" style="margin-right: 10px; margin-top: 10px; font-size: 0.8em;">Regenerate</button>
            </td>
            <td style="padding: 10px;" class="macro-${day.totals.Breakfast.dominant_macro}">
                ${formatMeal(day.Breakfast)}
                <p style="font-size: 0.9em; color: #555;">
                    Total: ${Math.round(day.totals.Breakfast.calories)} kcal, 
                    ${Math.round(day.totals.Breakfast.protein)} g protein, 
                    ${Math.round(day.totals.Breakfast.carbs)} g carbs, 
                    ${Math.round(day.totals.Breakfast.fats)} g fats
                </p>
            </td>
            <td style="padding: 10px;" class="macro-${day.totals.Lunch.dominant_macro}">
                ${formatMeal(day.Lunch)}
                <p style="font-size: 0.9em; color: #555;">
                    Total: ${Math.round(day.totals.Lunch.calories)} kcal, 
                    ${Math.round(day.totals.Lunch.protein)} g protein, 
                    ${Math.round(day.totals.Lunch.carbs)} g carbs, 
                    ${Math.round(day.totals.Lunch.fats)} g fats
                </p>
            </td>
            <td style="padding: 10px;" class="macro-${day.totals.Dinner.dominant_macro}">
                ${formatMeal(day.Dinner)}
                <p style="font-size: 0.9em; color: #555;">
                    Total: ${Math.round(day.totals.Dinner.calories)} kcal, 
                    ${Math.round(day.totals.Dinner.protein)} g protein, 
                    ${Math.round(day.totals.Dinner.carbs)} g carbs, 
                    ${Math.round(day.totals.Dinner.fats)} g fats
                </p>
            </td>
        </tr>
        <tr>
            <td colspan="4" style="padding: 10px; background-color: #f9f9f9;">
                <strong>Daily Total:</strong> 
                ${Math.round(day.totals.daily.calories)} kcal, 
                ${Math.round(day.totals.daily.protein)} g protein, 
                ${Math.round(day.totals.daily.carbs)} g carbs, 
                ${Math.round(day.totals.daily.fats)} g fats
            </td>
        </tr>`;
    });

    tableHTML += `</tbody></table>`;
    resultDiv.innerHTML = requirementsHTML + tableHTML + legendHTML;
    
    // Hide all sections and show the diet plan section
    document.querySelectorAll(".section").forEach(section => section.classList.add("hidden"));
    document.getElementById("diet-plan").classList.remove("hidden");
    
    // Update navigation to reflect active state
    document.querySelectorAll(".nav-item").forEach(item => item.classList.remove("active"));
    document.querySelector('.nav-item[data-target="diet-plan"]').classList.add("active");

    // Scroll to the diet plan section if specified
    if (shouldScroll) {
        resultDiv.scrollIntoView({ behavior: "smooth", block: "start" });
    }
}

// Function to format a meal's ingredients into HTML
function formatMeal(meal) {
    // Handle empty or invalid meal
    if (!meal || Object.keys(meal).length === 0) {
        return "<p>No items available for this meal.</p>";
    }

    // Create an unordered list for meal ingredients
    let formattedMeal = "<ul style='margin:0; padding-left:15px;'>";
    for (const ingredient in meal) {
        // Calculate grams (servings * 100)
        const grams = Math.round(meal[ingredient].servings * 100);
        const nutrition = meal[ingredient].nutrition || {};
        // Generate tooltip content with nutritional information
        const tooltipContent = nutrition.calories 
            ? `Calories: ${nutrition.calories} kcal, Protein: ${nutrition.protein} g, Carbs: ${nutrition.carbs} g, Fats: ${nutrition.fats} g (per 100 grams)`
            : "Nutrition data not available";
        formattedMeal += `
            <li class="food-item">
                ${ingredient}: ${grams} g
                <span class="tooltip">${tooltipContent}</span>
            </li>`;
    }
    formattedMeal += "</ul>";
    return formattedMeal;
}

// Function to handle calculator form submission
async function handleFormSubmit(event) {
    event.preventDefault();

    const calculateBtn = document.querySelector(".calculate-btn");
    // Add loading animation to the submit button
    calculateBtn.classList.add('loading');

    // Collect form input values
    const weight = document.getElementById("weight").value;
    const height = document.getElementById("height").value;
    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;
    const activityValue = parseInt(document.getElementById("activity").value);
    const goalBtn = document.querySelector(".goal-btn.active");
    const dietBtn = document.querySelector(".diet-btn.active");
    
    let hasError = false;

    // Validate the form input values
    if (!weight || weight <= 0) {
        alert("Please enter a valid weight");
        hasError = true;
    } else if (!height || height <= 0) {
        alert("Please enter a valid height");
        hasError = true;
    } else if (!age || age <= 0) {
        alert("Please enter a valid age");
        hasError = true;
    } else if (!gender) {
        alert("Please select a gender");
        hasError = true;
    } else if (!goalBtn) {
        alert("Please select a goal");
        hasError = true;
    } else if (!dietBtn) {
        alert("Please select a diet type");
        hasError = true;
    }
    
    if (hasError) {
        calculateBtn.classList.remove('loading');
        return;
    }
    
    const goal = goalBtn.textContent;
    const diet = dietBtn.textContent;
    const preferences = document.getElementById("preferences").value;
    const meal_variety = document.getElementById("meal-variety").value;

    // Map activity slider values to descriptive labels
    const activityLevels = {
        1: "Very Light",
        2: "Light",
        3: "Moderate",
        4: "Heavy",
        5: "Extremely active"
    };

    const activity = activityLevels[activityValue] || "Unknown";


    // Construct user data object for the API request
    const userData = {
        weight: weight,
        height: height,
        age: age,
        gender: gender,
        activity: activity,
        goal: goal,
        diet: diet,
        preferences: preferences,
        meal_variety: meal_variety
    };

    try {
        // Send user data to the server to generate a meal plan
        const response = await fetch("/calculate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(userData)
        });

        // Check if the response is successful
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
        }

        // Parse the response
        const responseText = await response.text();
        const result = JSON.parse(responseText);

        // Handle server-side errors
        if (result.error) {
            alert("Error: " + result.error);
        } else {
            // Update current meal plan and display results
            currentMealPlan = result.meal_plan;
            displayResults(result.meal_plan, result.daily_requirements, true);
        }
    } catch (error) {
        // Log error and show user-friendly message
        console.error("Error:", error);
        alert("Failed to fetch meal plan: " + error.message);
    } finally {
        // Remove loading animation from button
        calculateBtn.classList.remove('loading');
    }
}

// Event listener to reset currentMealPlan when session data is deleted
document.addEventListener('deleteSessionData', function() {
    // Clear the current meal plan
    currentMealPlan = null;
});

// Function to handle account deletion with confirmation
function confirmDeleteAccount() {
    // Prompt user to confirm account deletion
    if (confirm("Are you sure you want to delete your account? This action cannot be undone, and all your data will be permanently deleted.")) {
        // Send request to delete account
        fetch('/delete_account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            // Handle server response
            if (!response.ok) {
                // Handle non-redirect error responses
                return response.json().then(data => {
                    throw new Error(data.error || 'Failed to delete account');
                });
            }
                // Redirect to homepage after successful deletion
                window.location.href = '/';
        })
        .catch(error => {
            // Log error and show user-friendly message
            console.error('Error deleting account:', error);
            alert('Failed to delete account.');
        });
    }
}

// Function to handle session data deletion with confirmation
function deleteSessionData() {
    // Prompt user to confirm session data deletion
    if (confirm("Are you sure you want to delete your session data? This will clear your current meal plan and user data from this session.")) {
        // Send request to delete session data
        fetch('/delete_session_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Handle server response
            if (data.error) {
                alert('Failed to delete session data: ' + data.error);
            } else {
                // Store success message in sessionStorage
                sessionStorage.setItem('sessionDeletedMessage', 'Session data deleted successfully.');
                // Reset the diet plan section
                document.getElementById('diet-plan').innerHTML = '<h2>Diet Plan</h2><p>Your personalized diet plan will appear here.</p>';
                document.getElementById('diet-plan').classList.add('hidden');
                // Dispatch custom event to notify other parts of the app
                document.dispatchEvent(new CustomEvent('deleteSessionData'));
                // Refresh the page to clear form inputs
                window.location.reload();
            }
        })
        .catch(error => {
            // Log error and show user-friendly message
            console.error('Error deleting session data:', error);
            alert('Failed to delete session data.');
        });
    }
}