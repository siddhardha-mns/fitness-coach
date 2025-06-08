import streamlit as st
import datetime
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="AI Fitness Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gemini Client Class
class GeminiClient:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_content(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"Error generating content: {str(e)}")
            return None

# Initialize Gemini client with Streamlit secrets
@st.cache_resource
def init_gemini_client():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        return GeminiClient(api_key)
    except KeyError:
        st.error("⚠️ Gemini API key not found in secrets. Please configure GEMINI_API_KEY in Streamlit secrets.")
        return None
    except Exception as e:
        st.error(f"⚠️ Error initializing Gemini client: {str(e)}")
        return None

# Prompt creation functions
def create_nutrition_prompt(data):
    return f"""
Create a comprehensive, personalized nutrition plan based on the following information:

PERSONAL DETAILS:
- Age: {data['age']} years
- Gender: {data['gender']}
- Height: {data['height']} cm
- Current Weight: {data['weight']} kg
- Target Weight: {data['target_weight']} kg
- Activity Level: {data['activity_level']}
- Health Conditions: {data.get('health_conditions', 'None')}

NUTRITION GOALS:
- Primary Goal: {data['primary_goal']}
- Timeline: {data['timeline']}

DIETARY PREFERENCES:
- Diet Type: {data['diet_type']}
- Food Allergies/Intolerances: {', '.join(data.get('food_allergies', []))}
- Foods Disliked: {', '.join(data.get('dislikes', []))}
- Food Preferences: {', '.join(data.get('preferences', []))}

LIFESTYLE FACTORS:
- Meals per Day: {data['meals_per_day']}
- Cooking Skill: {data['cooking_skill']}
- Available Cooking Time: {data['cooking_time']}
- Weekly Budget: {data['budget']}
- Meal Prep Preference: {data['meal_prep']}
- Eating Schedule: {data.get('eating_schedule', 'Flexible')}
- Kitchen Equipment: {', '.join(data.get('kitchen_equipment', []))}
- Shopping Frequency: {data['shopping_frequency']}
- Current Supplements: {data.get('supplements', 'None')}

SPECIAL NOTES: {data.get('special_notes', 'None')}

Please provide:
1. Daily calorie target and macronutrient breakdown
2. Sample meal plan for one day
3. Weekly meal prep suggestions
4. Hydration recommendations
5. Specific tips based on their goals and preferences
6. Progress tracking suggestions

Format the response in clear sections with headers and bullet points for easy reading.
"""

def create_training_prompt(data):
    return f"""
Create a comprehensive, personalized training plan based on the following information:

PERSONAL DETAILS:
- Age: {data['age']} years
- Gender: {data['gender']}
- Height: {data['height']} cm
- Weight: {data['weight']} kg
- Current Fitness Level: {data['fitness_level']}
- Activity Level: {data['activity_level']}
- Medical Conditions/Injuries: {data.get('medical_conditions', 'None')}

FITNESS GOALS:
- Primary Goal: {data['primary_goal']}
- Secondary Goals: {', '.join(data.get('secondary_goals', []))}
- Target Timeline: {data['timeline']}

WORKOUT PREFERENCES:
- Workout Days per Week: {data['workout_days']}
- Time per Session: {data['time_per_session']} minutes
- Workout Location: {data['workout_location']}
- Available Equipment: {', '.join(data.get('equipment', []))}
- Preferred Workout Types: {', '.join(data.get('workout_types', []))}
- Exercise Experience: {', '.join(data.get('exercise_experience', []))}

SCHEDULE & PREFERENCES:
- Preferred Workout Time: {data.get('workout_time', 'Flexible')}
- Rest Day Preferences: {data.get('rest_days', 'Flexible')}

SPECIAL NOTES: {data.get('special_notes', 'None')}

Please provide:
1. Weekly training schedule with specific days
2. Detailed workout routines for each training day
3. Warm-up and cool-down recommendations
4. Exercise descriptions and proper form tips
5. Progressive overload suggestions
6. Recovery and rest recommendations
7. Progress tracking methods

Format the response in clear sections with headers and detailed exercise instructions.
"""

def main():
    # Initialize session state
    if 'gemini_client' not in st.session_state:
        st.session_state.gemini_client = init_gemini_client()
    
    # Sidebar navigation
    st.sidebar.title("🏋️ AI Fitness Coach")
    st.sidebar.markdown("---")
    
    # Navigation menu
    page = st.sidebar.radio(
        "Navigate to:",
        ["🏠 Home", "💪 Training Plan", "🥗 Nutrition Plan"],
        index=0
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This AI-powered fitness app uses Google's Gemini API to create "
        "personalized training and nutrition plans tailored to your goals."
    )
    
    # Add API status indicator
    if st.session_state.gemini_client:
        st.sidebar.success("✅ AI Service Connected")
    else:
        st.sidebar.error("❌ AI Service Unavailable")
    
    # Main content area
    if page == "🏠 Home":
        show_home_page()
    elif page == "💪 Training Plan":
        show_training_page()
    elif page == "🥗 Nutrition Plan":
        show_nutrition_page()

def show_home_page():
    # Hero section
    st.title("🏋️ AI Fitness Coach")
    st.markdown("### Your Personal AI-Powered Fitness and Nutrition Companion")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Welcome to your personalized fitness journey! Our AI-powered coach uses advanced 
        machine learning to create customized training and nutrition plans that adapt to 
        your unique needs, goals, and lifestyle.
        
        **🎯 What We Offer:**
        - **Personalized Training Plans**: Custom workout routines based on your fitness level, 
          goals, and available equipment
        - **Smart Nutrition Planning**: Meal plans tailored to your dietary preferences, 
          restrictions, and health objectives
        - **AI-Powered Recommendations**: Intelligent suggestions that evolve with your progress
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Quick Start
        1. Choose a service from the sidebar
        2. Fill in your personal details
        3. Get your AI-generated plan
        4. Start your fitness journey!
        """)
    
    # Features section
    st.markdown("---")
    st.markdown("## ✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 💪 Training Plans
        - Beginner to advanced levels
        - Home and gym workouts
        - Equipment-based customization
        - Time-flexible routines
        - Progress tracking guidance
        """)
    
    with col2:
        st.markdown("""
        ### 🥗 Nutrition Plans
        - Dietary restriction support
        - Calorie and macro planning
        - Meal prep suggestions
        - Budget-conscious options
        - Cooking time considerations
        """)
    
    with col3:
        st.markdown("""
        ### 🤖 AI Intelligence
        - Powered by Google Gemini
        - Personalized recommendations
        - Evidence-based advice
        - Continuous adaptation
        - Expert-level guidance
        """)
    
    # Getting started section
    st.markdown("---")
    st.markdown("## 🎯 Ready to Start?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💪 Create Training Plan", use_container_width=True):
            st.session_state.current_page = "💪 Training Plan"
            st.rerun()
    
    with col2:
        if st.button("🥗 Create Nutrition Plan", use_container_width=True):
            st.session_state.current_page = "🥗 Nutrition Plan"
            st.rerun()

def show_training_page():
    st.title("💪 Personalized Training Plan Generator")
    st.markdown("Tell us about yourself and your fitness goals to get a customized workout plan!")
    
    # Check if Gemini client is available
    if not st.session_state.get('gemini_client'):
        st.error("⚠️ AI service is not available. Please check your API configuration.")
        return
    
    with st.form("training_form"):
        st.markdown("### 📊 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=16, max_value=80, value=25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            height = st.number_input("Height (cm)", min_value=120, max_value=220, value=170)
            weight = st.number_input("Weight (kg)", min_value=40, max_value=200, value=70)
        
        with col2:
            fitness_level = st.selectbox(
                "Current Fitness Level",
                ["Beginner", "Intermediate", "Advanced", "Expert"]
            )
            activity_level = st.selectbox(
                "Current Activity Level",
                ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
            )
            medical_conditions = st.text_area(
                "Medical Conditions or Injuries (if any)",
                placeholder="e.g., lower back pain, knee issues, etc."
            )
        
        st.markdown("### 🎯 Fitness Goals")
        
        primary_goal = st.selectbox(
            "Primary Fitness Goal",
            [
                "Weight Loss",
                "Muscle Building",
                "Strength Training",
                "Endurance/Cardio",
                "General Fitness",
                "Athletic Performance",
                "Rehabilitation",
                "Flexibility/Mobility"
            ]
        )
        
        secondary_goals = st.multiselect(
            "Secondary Goals (optional)",
            [
                "Improve Posture",
                "Increase Energy",
                "Better Sleep",
                "Stress Relief",
                "Core Strength",
                "Balance & Coordination",
                "Functional Movement"
            ]
        )
        
        timeline = st.selectbox(
            "Goal Timeline",
            ["1-2 months", "3-6 months", "6-12 months", "Long-term lifestyle change"]
        )
        
        st.markdown("### 🏋️ Workout Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            workout_days = st.slider("Workout Days per Week", 2, 7, 4)
            time_per_session = st.selectbox(
                "Time per Session (minutes)",
                ["15-30", "30-45", "45-60", "60-90", "90+"]
            )
            workout_location = st.selectbox(
                "Workout Location",
                ["Home", "Gym", "Outdoor", "Mixed (Home + Gym)"]
            )
        
        with col2:
            equipment = st.multiselect(
                "Available Equipment",
                [
                    "No Equipment (Bodyweight)",
                    "Dumbbells",
                    "Resistance Bands",
                    "Pull-up Bar",
                    "Kettlebells",
                    "Barbell",
                    "Cable Machine",
                    "Cardio Equipment",
                    "Full Gym Access"
                ]
            )
            
            workout_types = st.multiselect(
                "Preferred Workout Types",
                [
                    "Strength Training",
                    "Cardio/HIIT",
                    "Yoga/Pilates",
                    "Functional Training",
                    "Bodyweight Exercises",
                    "Olympic Lifting",
                    "Circuit Training",
                    "Sports-Specific"
                ]
            )
        
        st.markdown("### ⏰ Schedule Preferences")
        
        workout_time = st.selectbox(
            "Preferred Workout Time",
            ["Early Morning", "Morning", "Afternoon", "Evening", "Night", "Flexible"]
        )
        
        rest_days = st.text_input(
            "Preferred Rest Days",
            placeholder="e.g., Wednesday, Sunday or Flexible"
        )
        
        exercise_experience = st.multiselect(
            "Previous Exercise Experience",
            [
                "Weight Training",
                "Running/Cardio",
                "Sports",
                "Yoga/Pilates",
                "Martial Arts",
                "Dancing",
                "Swimming",
                "Cycling"
            ]
        )
        
        st.markdown("### 💡 Additional Information")
        
        special_notes = st.text_area(
            "Special Requests or Notes",
            placeholder="Any specific requirements, preferences, or additional information..."
        )
        
        # Form submission
        submitted = st.form_submit_button("🚀 Generate My Training Plan", use_container_width=True)
        
        if submitted:
            # Store form data in session state
            st.session_state.training_data = {
                'age': age,
                'gender': gender,
                'height': height,
                'weight': weight,
                'fitness_level': fitness_level,
                'activity_level': activity_level,
                'medical_conditions': medical_conditions,
                'primary_goal': primary_goal,
                'secondary_goals': secondary_goals,
                'timeline': timeline,
                'workout_days': workout_days,
                'time_per_session': time_per_session,
                'workout_location': workout_location,
                'equipment': equipment,
                'workout_types': workout_types,
                'workout_time': workout_time,
                'rest_days': rest_days,
                'exercise_experience': exercise_experience,
                'special_notes': special_notes
            }
            
            # Generate training plan
            generate_training_plan()

def generate_training_plan():
    """Generate and display the training plan using Gemini API"""
    
    if 'training_data' not in st.session_state:
        st.error("No training data found. Please fill out the form first.")
        return
    
    st.markdown("---")
    st.markdown("## 💪 Your Personalized Training Plan")
    
    with st.spinner("🤖 AI is creating your personalized training plan..."):
        try:
            # Create prompt for Gemini
            prompt = create_training_prompt(st.session_state.training_data)
            
            # Get response from Gemini
            response = st.session_state.gemini_client.generate_content(prompt)
            
            if response:
                st.markdown("### 📋 Generated Training Plan")
                st.markdown(response)
                
                # Store the generated plan
                st.session_state.generated_training_plan = response
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🔄 Generate New Plan"):
                        st.rerun()
                
                with col2:
                    if st.button("📱 Save Plan"):
                        st.success("Plan saved to your session!")
                
                with col3:
                    # Create downloadable text file
                    plan_text = f"""
PERSONALIZED TRAINING PLAN
Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{response}

---
Generated by AI Fitness Coach
                    """.strip()
                    
                    st.download_button(
                        label="📥 Download Plan",
                        data=plan_text,
                        file_name=f"training_plan_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                
                # Training tips section
                st.markdown("---")
                st.markdown("### 💡 Training Success Tips")
                st.info("""
                - **Start Slowly**: Begin with lighter weights and gradually increase
                - **Focus on Form**: Proper technique prevents injury and maximizes results
                - **Stay Consistent**: Regular workouts are more effective than sporadic intense sessions
                - **Listen to Your Body**: Rest when you need it, push when you can
                - **Track Progress**: Keep a workout log to monitor improvements
                - **Warm Up & Cool Down**: Always include proper warm-up and stretching
                - **Stay Hydrated**: Drink water before, during, and after workouts
                - **Get Adequate Rest**: Muscles grow during rest, not just during workouts
                """)
                
            else:
                st.error("Failed to generate training plan. Please try again.")
                
        except Exception as e:
            st.error(f"An error occurred while generating your training plan: {str(e)}")

def show_nutrition_page():
    st.title("🥗 Personalized Nutrition Plan Generator")
    st.markdown("Let's create a customized meal plan that fits your lifestyle and goals!")
    
    # Check if Gemini client is available
    if not st.session_state.get('gemini_client'):
        st.error("⚠️ AI service is not available. Please check your API configuration.")
        return
    
    with st.form("nutrition_form"):
        st.markdown("### 👤 Personal Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=16, max_value=80, value=25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            height = st.number_input("Height (cm)", min_value=120, max_value=220, value=170)
            weight = st.number_input("Current Weight (kg)", min_value=40, max_value=200, value=70)
        
        with col2:
            target_weight = st.number_input(
                "Target Weight (kg)", 
                min_value=40, 
                max_value=200, 
                value=weight,
                help="Leave same as current weight if maintaining"
            )
            activity_level = st.selectbox(
                "Activity Level",
                ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"]
            )
            health_conditions = st.text_area(
                "Health Conditions (if any)",
                placeholder="e.g., diabetes, high cholesterol, food allergies, etc."
            )
        
        st.markdown("### 🎯 Nutrition Goals")
        
        primary_goal = st.selectbox(
            "Primary Nutrition Goal",
            [
                "Weight Loss",
                "Weight Gain",
                "Muscle Building",
                "Weight Maintenance",
                "Improved Health",
                "Better Energy",
                "Athletic Performance",
                "Medical Dietary Needs"
            ]
        )
        
        timeline = st.selectbox(
            "Goal Timeline",
            ["1-2 months", "3-6 months", "6-12 months", "Long-term lifestyle change"]
        )
        
        st.markdown("### 🍽️ Dietary Preferences & Restrictions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            diet_type = st.selectbox(
                "Diet Type",
                [
                    "No Specific Diet",
                    "Vegetarian",
                    "Vegan",
                    "Pescatarian",
                    "Keto",
                    "Paleo",
                    "Mediterranean",
                    "Low-Carb",
                    "Low-Fat",
                    "DASH",
                    "Intermittent Fasting"
                ]
            )
            
            food_allergies = st.multiselect(
                "Food Allergies/Intolerances",
                [
                    "None",
                    "Nuts",
                    "Dairy/Lactose",
                    "Gluten",
                    "Shellfish",
                    "Eggs",
                    "Soy",
                    "Fish",
                    "Sesame"
                ]
            )
        
        with col2:
            dislikes = st.multiselect(
                "Foods You Dislike",
                [
                    "Seafood",
                    "Spicy Food",
                    "Mushrooms",
                    "Onions",
                    "Garlic",
                    "Cilantro",
                    "Olives",
                    "Tomatoes",
                    "Beans/Legumes",
                    "Leafy Greens"
                ]
            )
            
            preferences = st.multiselect(
                "Food Preferences",
                [
                    "Organic Foods",
                    "Locally Sourced",
                    "Minimal Processing",
                    "High Protein",
                    "High Fiber",
                    "Low Sodium",
                    "Low Sugar",
                    "Fermented Foods"
                ]
            )
        
        st.markdown("### 🕐 Lifestyle & Practical Considerations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            meals_per_day = st.slider("Preferred Meals per Day", 2, 6, 3)
            
            cooking_skill = st.selectbox(
                "Cooking Skill Level",
                ["Beginner", "Intermediate", "Advanced", "Professional"]
            )
            
            cooking_time = st.selectbox(
                "Available Cooking Time",
                ["15 minutes or less", "15-30 minutes", "30-60 minutes", "60+ minutes", "Meal prep sessions"]
            )
        
        with col2:
            budget = st.selectbox(
                "Weekly Food Budget",
                ["Under $50", "$50-100", "$100-150", "$150-200", "$200+", "No specific budget"]
            )
            
            meal_prep = st.selectbox(
                "Meal Prep Preference",
                ["No meal prep", "Some meal prep", "Extensive meal prep", "Batch cooking"]
            )
            
            eating_schedule = st.text_input(
                "Eating Schedule Preferences",
                placeholder="e.g., breakfast at 7am, lunch at 12pm, dinner at 7pm"
            )
        
        st.markdown("### 🛒 Shopping & Kitchen Setup")
        
        kitchen_equipment = st.multiselect(
            "Available Kitchen Equipment",
            [
                "Basic stove/oven",
                "Microwave",
                "Blender",
                "Food processor",
                "Slow cooker",
                "Air fryer",
                "Grill",
                "Steamer",
                "Pressure cooker",
                "Well-stocked pantry"
            ]
        )
        
        shopping_frequency = st.selectbox(
            "Grocery Shopping Frequency",
            ["Daily", "Every 2-3 days", "Weekly", "Bi-weekly", "Monthly"]
        )
        
        st.markdown("### 💡 Additional Information")
        
        supplements = st.text_area(
            "Current Supplements (if any)",
            placeholder="e.g., multivitamin, protein powder, omega-3, etc."
        )
        
        special_notes = st.text_area(
            "Special Requests or Notes",
            placeholder="Any specific requirements, cultural preferences, or additional information..."
        )
        
        # Form submission
        submitted = st.form_submit_button("🚀 Generate My Nutrition Plan", use_container_width=True)
        
        if submitted:
            # Validate required fields
            if not kitchen_equipment:
                st.error("Please select at least one kitchen equipment option.")
                return
            
            # Store form data in session state
            st.session_state.nutrition_data = {
                'age': age,
                'gender': gender,
                'height': height,
                'weight': weight,
                'target_weight': target_weight,
                'activity_level': activity_level,
                'health_conditions': health_conditions,
                'primary_goal': primary_goal,
                'timeline': timeline,
                'diet_type': diet_type,
                'food_allergies': food_allergies,
                'dislikes': dislikes,
                'preferences': preferences,
                'meals_per_day': meals_per_day,
                'cooking_skill': cooking_skill,
                'cooking_time': cooking_time,
                'budget': budget,
                'meal_prep': meal_prep,
                'eating_schedule': eating_schedule,
                'kitchen_equipment': kitchen_equipment,
                'shopping_frequency': shopping_frequency,
                'supplements': supplements,
                'special_notes': special_notes
            }
            
            # Generate nutrition plan
            generate_nutrition_plan()

def generate_nutrition_plan():
    """Generate and display the nutrition plan using Gemini API"""
    
    if 'nutrition_data' not in st.session_state:
        st.error("No nutrition data found. Please fill out the form first.")
        return
    
    st.markdown("---")
    st.markdown("## 🍽️ Your Personalized Nutrition Plan")
    
    with st.spinner("🤖 AI is creating your personalized nutrition plan..."):
        try:
            # Create prompt for Gemini
            prompt = create_nutrition_prompt(st.session_state.nutrition_data)
            
            # Get response from Gemini
            response = st.session_state.gemini_client.generate_content(prompt)
            
            if response:
                st.markdown("### 📋 Generated Nutrition Plan")
                st.markdown(response)
                
                # Store the generated plan
                st.session_state.generated_nutrition_plan = response
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("🔄 Generate New Plan"):
                        st.rerun()
                
                with col2:
                    if st.button("📱 Save Plan"):
                        st.success("Plan saved to your session!")
                
                with col3:
                    # Create downloadable text file
                    plan_text = f"""
PERSONALIZED NUTRITION PLAN
Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{response}

---
Generated by AI Fitness Coach
                    """.strip()
                    
                    st.download_button(
                        label="📥 Download Plan",
                        data=plan_text,
                        file_name=f"nutrition_plan_{datetime.datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
                
                # Nutrition tips section
                st.markdown("---")
                st.markdown("### 💡 Nutrition Success Tips")
                st.info("""
                - **Gradual Changes**: Make small, sustainable changes rather than drastic overhauls
                - **Stay Hydrated**: Aim for 8-10 glasses of water daily
                - **Portion Control**: Use smaller plates and listen to hunger cues
                - **Meal Timing**: Eat regular meals to maintain stable energy levels
                - **Read Labels**: Understand nutritional information on packaged foods
                - **Cook at Home**: Prepare meals when possible for better control
                - **Track Progress**: Keep a food diary or use nutrition apps
                - **Be Patient**: Lasting changes take time - focus on consistency over perfection
                """)
                
            else:
                st.error("Failed to generate nutrition plan. Please try again.")
                
        except Exception as e:
            st.error(f"An error occurred while generating your nutrition plan: {str(e)}")

if __name__ == "__main__":
    main()
