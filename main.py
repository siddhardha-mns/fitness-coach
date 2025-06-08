import streamlit as st
import google.generativeai as genai
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time

# Configure Streamlit page
st.set_page_config(
    page_title="AI Fitness Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'gemini_api_key': "",
        'user_profile': {},
        'workout_history': [],
        'nutrition_history': [],
        'water_intake': 0,
        'daily_water_goal': 2000,  # ml
        'chat_history': [],
        'sleep_history': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize session state
initialize_session_state()

def configure_gemini():
    """Configure Gemini API"""
    if st.session_state.gemini_api_key:
        try:
            genai.configure(api_key=st.session_state.gemini_api_key)
            return True
        except Exception as e:
            st.error(f"Failed to configure Gemini API: {str(e)}")
            return False
    return False

def get_ai_response(prompt):
    """Get response from Gemini AI"""
    try:
        if not configure_gemini():
            return "Please configure your Gemini API key first."
        
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating AI response: {str(e)}"

# Sidebar Navigation
st.sidebar.title("🏋️ AI Fitness Coach")

# API Key Configuration
with st.sidebar.expander("⚙️ API Configuration"):
    api_key = st.text_input("Enter Gemini API Key", type="password", 
                           value=st.session_state.gemini_api_key)
    if st.button("Save API Key"):
        st.session_state.gemini_api_key = api_key
        if api_key:
            st.success("API Key saved!")
        else:
            st.error("Please enter a valid API key")

# Navigation
page = st.sidebar.selectbox("Navigate", 
                           ["🏠 Dashboard", "💪 Training Plan", "🥗 Nutrition Plan"])

# Quick Stats in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.metric("Water Intake", f"{st.session_state.water_intake}ml", 
                 f"{st.session_state.daily_water_goal - st.session_state.water_intake}ml to go")

# Add water intake buttons
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("💧 +250ml"):
        st.session_state.water_intake += 250
        st.rerun()
with col2:
    if st.button("🚰 +500ml"):
        st.session_state.water_intake += 500
        st.rerun()

if st.sidebar.button("🔄 Reset Water"):
    st.session_state.water_intake = 0
    st.rerun()

# Main Content Area
if page == "🏠 Dashboard":
    st.title("🏠 AI Fitness Dashboard")
    st.markdown("Welcome to your personalized AI fitness companion!")
    
    # Water Intake Progress
    st.subheader("💧 Daily Hydration")
    water_progress = min(st.session_state.water_intake / st.session_state.daily_water_goal, 1.0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Intake", f"{st.session_state.water_intake}ml")
    with col2:
        st.metric("Daily Goal", f"{st.session_state.daily_water_goal}ml")
    with col3:
        st.metric("Progress", f"{water_progress*100:.1f}%")
    
    # Water progress bar
    st.progress(water_progress)
    
    # AI Chat Assistant
    st.subheader("🤖 AI Chat Assistant")
    
    # Display chat history
    for chat in st.session_state.chat_history[-5:]:  # Show last 5 messages
        with st.chat_message(chat['role']):
            st.write(chat['message'])
    
    # Chat input
    user_question = st.chat_input("Ask your AI fitness coach anything...")
    
    if user_question:
        st.session_state.chat_history.append({'role': 'user', 'message': user_question})
        
        with st.chat_message("user"):
            st.write(user_question)
        
        # Generate AI response
        fitness_prompt = f"""
        You are an expert fitness coach and nutritionist. Answer the following question 
        in a helpful, motivating, and professional manner. Keep responses concise but informative.
        
        User question: {user_question}
        
        User profile: {st.session_state.user_profile if st.session_state.user_profile else 'No profile data available'}
        """
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ai_response = get_ai_response(fitness_prompt)
                st.write(ai_response)
                st.session_state.chat_history.append({'role': 'assistant', 'message': ai_response})
    
    # Progress Dashboard
    st.subheader("📈 Progress Dashboard")
    
    if st.session_state.workout_history:
        try:
            # Create workout frequency chart
            workout_dates = [w['date'] for w in st.session_state.workout_history]
            df_workouts = pd.DataFrame({'Date': workout_dates, 'Workouts': [1]*len(workout_dates)})
            df_workouts['Date'] = pd.to_datetime(df_workouts['Date'])
            df_workouts_grouped = df_workouts.groupby(df_workouts['Date'].dt.date).sum().reset_index()
            
            fig = px.line(df_workouts_grouped, x='Date', y='Workouts', 
                         title='Workout Frequency Over Time')
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating workout chart: {str(e)}")
    else:
        st.info("Complete some workouts to see your progress here!")
    
    # Sleep and Recovery Section
    st.subheader("😴 Sleep & Recovery")
    
    col1, col2 = st.columns(2)
    with col1:
        sleep_hours = st.slider("Hours of sleep last night", 0, 12, 8)
        sleep_quality = st.selectbox("Sleep quality", ["Poor", "Fair", "Good", "Excellent"])
    
    with col2:
        stress_level = st.slider("Stress level (1-10)", 1, 10, 5)
        recovery_feeling = st.selectbox("How recovered do you feel?", 
                                      ["Very tired", "Tired", "Okay", "Good", "Excellent"])
    
    if st.button("💾 Save Sleep Data"):
        sleep_data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'hours': sleep_hours,
            'quality': sleep_quality,
            'stress': stress_level,
            'recovery': recovery_feeling
        }
        st.session_state.sleep_history.append(sleep_data)
        st.success("Sleep data saved!")

elif page == "💪 Training Plan":
    st.title("💪 Personalized Training Plan")
    
    # User Input Form
    st.subheader("📝 Tell us about yourself")
    
    with st.form("training_profile"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=16, max_value=80, value=25)
            weight = st.number_input("Weight (kg)", min_value=40, max_value=200, value=70)
            height = st.number_input("Height (cm)", min_value=140, max_value=220, value=170)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        with col2:
            fitness_level = st.selectbox("Current Fitness Level", 
                                       ["Beginner", "Intermediate", "Advanced", "Expert"])
            primary_goal = st.selectbox("Primary Goal", 
                                      ["Weight Loss", "Muscle Gain", "Strength", "Endurance", 
                                       "General Fitness", "Athletic Performance"])
            workout_days = st.slider("Days per week available for workout", 1, 7, 4)
            session_duration = st.slider("Preferred session duration (minutes)", 15, 120, 60)
        
        # Additional preferences
        st.subheader("🎯 Preferences & Limitations")
        
        col3, col4 = st.columns(2)
        with col3:
            equipment = st.multiselect("Available Equipment", 
                                     ["None (Bodyweight)", "Dumbbells", "Barbells", "Resistance Bands", 
                                      "Pull-up Bar", "Gym Access", "Kettlebells", "Cardio Machines"])
            preferred_exercises = st.multiselect("Preferred Exercise Types",
                                               ["Strength Training", "Cardio", "HIIT", "Yoga", 
                                                "Pilates", "Swimming", "Running", "Cycling"])
        
        with col4:
            injuries = st.text_area("Any injuries or limitations?", 
                                  placeholder="e.g., knee injury, back problems...")
            experience = st.text_area("Previous exercise experience?",
                                    placeholder="e.g., played sports, gym experience...")
        
        submit_training = st.form_submit_button("🚀 Generate Training Plan", use_container_width=True)
    
    if submit_training:
        # Save user profile
        training_profile = {
            'age': age, 'weight': weight, 'height': height, 'gender': gender,
            'fitness_level': fitness_level, 'primary_goal': primary_goal,
            'workout_days': workout_days, 'session_duration': session_duration,
            'equipment': equipment, 'preferred_exercises': preferred_exercises,
            'injuries': injuries, 'experience': experience
        }
        st.session_state.user_profile.update(training_profile)
        
        # Generate AI training plan
        training_prompt = f"""
        Create a detailed, personalized workout plan based on the following information:
        
        User Profile:
        - Age: {age}, Weight: {weight}kg, Height: {height}cm, Gender: {gender}
        - Fitness Level: {fitness_level}
        - Primary Goal: {primary_goal}
        - Available Days: {workout_days} days/week
        - Session Duration: {session_duration} minutes
        - Equipment: {', '.join(equipment) if equipment else 'None'}
        - Preferred Exercises: {', '.join(preferred_exercises) if preferred_exercises else 'None specified'}
        - Injuries/Limitations: {injuries if injuries else 'None'}
        - Experience: {experience if experience else 'Beginner'}
        
        Please provide:
        1. A weekly workout schedule
        2. Specific exercises for each day
        3. Sets, reps, and rest periods
        4. Progression recommendations
        5. Important safety tips
        
        Format the response in a clear, easy-to-follow structure.
        """
        
        with st.spinner("Generating your personalized training plan..."):
            training_plan = get_ai_response(training_prompt)
        
        st.subheader("🎯 Your Personalized Training Plan")
        st.markdown(training_plan)
        
        # Save workout plan
        if st.button("💾 Save This Workout Plan"):
            workout_entry = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'plan': training_plan,
                'profile': training_profile
            }
            st.session_state.workout_history.append(workout_entry)
            st.success("Workout plan saved to your history!")
    
    # Display previous workouts
    if st.session_state.workout_history:
        st.subheader("📚 Previous Workout Plans")
        for i, workout in enumerate(reversed(st.session_state.workout_history[-3:])):  # Show last 3
            with st.expander(f"Workout Plan {len(st.session_state.workout_history)-i} - {workout['date']}"):
                st.markdown(workout['plan'])

elif page == "🥗 Nutrition Plan":
    st.title("🥗 Personalized Nutrition Plan")
    
    # Nutrition Input Form
    st.subheader("🍎 Nutrition Profile")
    
    with st.form("nutrition_profile"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Basic info (use saved profile if available)
            current_weight = st.number_input("Current Weight (kg)", 
                                           value=st.session_state.user_profile.get('weight', 70))
            target_weight = st.number_input("Target Weight (kg)", 
                                          value=current_weight)
            activity_level = st.selectbox("Activity Level",
                                        ["Sedentary", "Lightly Active", "Moderately Active", 
                                         "Very Active", "Extremely Active"])
            nutrition_goal = st.selectbox("Nutrition Goal",
                                        ["Weight Loss", "Weight Gain", "Muscle Gain", 
                                         "Maintenance", "Athletic Performance"])
        
        with col2:
            dietary_preference = st.selectbox("Dietary Preference",
                                            ["Omnivore", "Vegetarian", "Vegan", "Pescatarian", 
                                             "Keto", "Paleo", "Mediterranean"])
            meals_per_day = st.slider("Preferred meals per day", 3, 6, 3)
            budget_range = st.selectbox("Budget Range",
                                      ["Low ($5-10/day)", "Moderate ($10-15/day)", 
                                       "High ($15-25/day)", "Premium ($25+/day)"])
            cooking_time = st.selectbox("Available cooking time",
                                      ["Minimal (15 min)", "Short (30 min)", 
                                       "Moderate (45 min)", "Long (1+ hour)"])
        
        # Food preferences and restrictions
        st.subheader("🥘 Food Preferences")
        
        col3, col4 = st.columns(2)
        with col3:
            food_allergies = st.multiselect("Food Allergies/Intolerances",
                                          ["None", "Nuts", "Dairy", "Gluten", "Eggs", "Soy", 
                                           "Shellfish", "Fish", "Other"])
            disliked_foods = st.text_area("Foods you dislike",
                                        placeholder="e.g., broccoli, mushrooms...")
        
        with col4:
            favorite_cuisines = st.multiselect("Favorite Cuisines",
                                             ["Italian", "Asian", "Mexican", "Indian", "Mediterranean", 
                                              "American", "Thai", "Japanese", "Middle Eastern"])
            health_conditions = st.text_area("Health conditions affecting diet",
                                           placeholder="e.g., diabetes, high blood pressure...")
        
        submit_nutrition = st.form_submit_button("🥗 Generate Nutrition Plan", use_container_width=True)
    
    if submit_nutrition:
        # Save nutrition profile
        nutrition_profile = {
            'current_weight': current_weight, 'target_weight': target_weight,
            'activity_level': activity_level, 'nutrition_goal': nutrition_goal,
            'dietary_preference': dietary_preference, 'meals_per_day': meals_per_day,
            'budget_range': budget_range, 'cooking_time': cooking_time,
            'food_allergies': food_allergies, 'disliked_foods': disliked_foods,
            'favorite_cuisines': favorite_cuisines, 'health_conditions': health_conditions
        }
        st.session_state.user_profile.update(nutrition_profile)
        
        # Generate AI nutrition plan
        nutrition_prompt = f"""
        Create a detailed, personalized nutrition and meal plan based on the following information:
        
        User Profile:
        - Current Weight: {current_weight}kg, Target Weight: {target_weight}kg
        - Activity Level: {activity_level}
        - Nutrition Goal: {nutrition_goal}
        - Dietary Preference: {dietary_preference}
        - Meals per Day: {meals_per_day}
        - Budget: {budget_range}
        - Cooking Time Available: {cooking_time}
        - Food Allergies: {', '.join(food_allergies) if food_allergies else 'None'}
        - Disliked Foods: {disliked_foods if disliked_foods else 'None specified'}
        - Favorite Cuisines: {', '.join(favorite_cuisines) if favorite_cuisines else 'None specified'}
        - Health Conditions: {health_conditions if health_conditions else 'None'}
        
        Please provide:
        1. Daily calorie and macro targets
        2. A sample 7-day meal plan
        3. Specific meal ideas for breakfast, lunch, dinner (and snacks if applicable)
        4. Shopping list suggestions
        5. Meal prep tips
        6. Hydration recommendations
        
        Make sure all recommendations align with their dietary preferences and restrictions.
        """
        
        with st.spinner("Creating your personalized nutrition plan..."):
            nutrition_plan = get_ai_response(nutrition_prompt)
        
        st.subheader("🎯 Your Personalized Nutrition Plan")
        st.markdown(nutrition_plan)
        
        # Save nutrition plan
        if st.button("💾 Save This Nutrition Plan"):
            nutrition_entry = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'plan': nutrition_plan,
                'profile': nutrition_profile
            }
            st.session_state.nutrition_history.append(nutrition_entry)
            st.success("Nutrition plan saved to your history!")
    
    # Calorie Calculator
    st.subheader("🔢 Quick Calorie Calculator")
    
    col1, col2 = st.columns(2)
    with col1:
        calc_weight = st.number_input("Weight (kg)", value=70, key="calc_weight")
        calc_height = st.number_input("Height (cm)", value=170, key="calc_height")
        calc_age = st.number_input("Age", value=25, key="calc_age")
        calc_gender = st.selectbox("Gender", ["Male", "Female"], key="calc_gender")
    
    with col2:
        calc_activity = st.selectbox("Activity Level", 
                                   ["Sedentary (1.2)", "Light (1.375)", "Moderate (1.55)", 
                                    "Active (1.725)", "Very Active (1.9)"], key="calc_activity")
        
        if st.button("Calculate BMR & TDEE"):
            # Calculate BMR using Mifflin-St Jeor Equation
            if calc_gender == "Male":
                bmr = 10 * calc_weight + 6.25 * calc_height - 5 * calc_age + 5
            else:
                bmr = 10 * calc_weight + 6.25 * calc_height - 5 * calc_age - 161
            
            # Activity multipliers
            activity_multipliers = {
                "Sedentary (1.2)": 1.2,
                "Light (1.375)": 1.375,
                "Moderate (1.55)": 1.55,
                "Active (1.725)": 1.725,
                "Very Active (1.9)": 1.9
            }
            
            tdee = bmr * activity_multipliers[calc_activity]
            
            st.success(f"**BMR:** {bmr:.0f} calories/day")
            st.success(f"**TDEE:** {tdee:.0f} calories/day")
            st.info(f"For weight loss: {tdee-500:.0f} calories/day")
            st.info(f"For weight gain: {tdee+500:.0f} calories/day")
    
    # Display previous nutrition plans
    if st.session_state.nutrition_history:
        st.subheader("📚 Previous Nutrition Plans")
        for i, plan in enumerate(reversed(st.session_state.nutrition_history[-3:])):  # Show last 3
            with st.expander(f"Nutrition Plan {len(st.session_state.nutrition_history)-i} - {plan['date']}"):
                st.markdown(plan['plan'])

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>💪 AI Fitness Coach - Your Personal Health & Fitness Companion</p>
    <p><small>Powered by Google Gemini AI | Built with Streamlit</small></p>
</div>
""", unsafe_allow_html=True)
