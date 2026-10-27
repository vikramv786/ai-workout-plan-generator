
import streamlit as st

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_workout_plan(
    fitness_goal: str,
    experience_level: str,
    days_per_week: int,
    equipment_access: str,
    injuries_or_limitations: str,
    previous_plan: str = ""
) -> str:
    """Generate a personalized workout plan using Groq."""
    prompt = f"""
Create a personalized weekly workout plan using these preferences:

Fitness goal: {fitness_goal}
Experience level: {experience_level}
Workout days per week: {days_per_week}
Available equipment: {equipment_access}
Injuries or physical limitations: {injuries_or_limitations or "None"}

Requirements:
1. Create exactly {days_per_week} workout days.
2. Organize the plan clearly by day (Day 1, Day 2, etc.).
3. Include a warm-up, exercises, and cool-down for each day.
4. Specify sets, repetitions or duration, and rest periods.
5. Match the difficulty to the user's experience level.
6. Recommend only exercises suitable for the available equipment.
7. Respect all stated injuries and physical limitations.
8. Suggest safe alternatives where appropriate.
9. Include rest and recovery guidance.
10. If injuries or limitations are mentioned, include a brief
    disclaimer recommending professional medical guidance.
11. Format the response using clear Markdown headings and bullet points.
"""
    if previous_plan:
        prompt += f"""

This is a REGENERATION request.

Here is the previously generated workout plan:
{previous_plan}

Create a fresh variation of this workout plan.

Important:
- Use different exercises and workout combinations where suitable.
- Avoid repeating the previous plan unnecessarily.
- Keep the same fitness goal, experience level, workout days,
  equipment restrictions, and injury precautions.
- Never sacrifice safety just to make the plan different.
"""
    try:
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a knowledgeable and safety-conscious fitness coach."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        workout_plan = response.choices[0].message.content

        if not workout_plan or not workout_plan.strip():
            return "Error: Groq returned an empty workout plan. Please try again."

        return workout_plan

    except Exception:
        return "Error: Unable to generate your workout plan. Please try again later."

def swap_exercise(
    current_plan: str,
    exercise_to_replace: str
) -> str:
    """Replace one exercise in an existing workout plan."""

    prompt = f"""
You are updating an existing workout plan.

Current workout plan:
{current_plan}

Exercise to replace:
{exercise_to_replace}

Instructions:
1. Find the specified exercise in the workout plan.
2. Replace only one occurrence of that exercise with a suitable alternative.
3. Choose an alternative that trains similar muscles.
4. Respect the original equipment and injury restrictions.
5. Keep all other exercises, workout days, and instructions unchanged.
6. Include appropriate sets, repetitions, and rest periods.
7. Return the COMPLETE updated workout plan in Markdown format.
8. If the exercise cannot be found, return exactly:
   ERROR: Exercise not found in the workout plan.
"""

    try:
        response = groq_client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a careful fitness coach editing an existing workout plan."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        updated_plan = response.choices[0].message.content

        if not updated_plan or not updated_plan.strip():
            return "Error: Groq returned an empty response."

        if updated_plan.strip().startswith("ERROR:"):
            return "Error: Exercise not found in the workout plan."

        return updated_plan

    except Exception:
        return "Error: Unable to swap the exercise. Please try again."

st.set_page_config(
    page_title="AI Workout Plan Generator",
    page_icon="💪",
    layout="centered"
)

if "workout_plan" not in st.session_state:
    st.session_state.workout_plan = None

st.title("💪 AI Workout Plan Generator")

st.write(
    "Welcome! Create a personalized workout plan "
    "based on your fitness goals."
)

st.success("Streamlit is working successfully!")

st.subheader("Your Fitness Preferences")

fitness_goal = st.selectbox(
    "What is your fitness goal?",
    [
        "Build muscle",
        "Lose fat",
        "General fitness",
        "Improve endurance"
    ]
)

experience_level = st.selectbox(
    "What is your experience level?",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

days_per_week = st.slider(
    "How many days per week can you work out?",
    min_value=1,
    max_value=7,
    value=3,
    step=1
)

equipment_access = st.selectbox(
    "What workout equipment do you have access to?",
    [
        "No equipment",
        "Home dumbbells",
        "Full gym"
    ]
)

injuries_or_limitations = st.text_area(
    "Do you have any injuries or physical limitations? (Optional)",
    placeholder="e.g., Knee pain, lower back issues, no overhead pressing",
    height=100
)

if st.button("Generate Plan", type="primary"):
    if injuries_or_limitations.strip() and len(injuries_or_limitations.strip()) < 10:
        st.warning("Please describe your injury or limitation more clearly.")
        st.stop()
    with st.spinner("Generating your personalized workout plan..."):
        workout_plan = generate_workout_plan(
            fitness_goal,
            experience_level,
            days_per_week,
            equipment_access,
            injuries_or_limitations
        )

    if workout_plan.startswith("Error:"):
        st.error(workout_plan)
    else:
        st.session_state.workout_plan = workout_plan

if st.session_state.workout_plan:
    st.subheader("Your Personalized Workout Plan")
    st.markdown(st.session_state.workout_plan)
    st.subheader("🔄 Swap an Exercise")

    exercise_to_replace = st.text_input(
        "Which exercise would you like to replace?",
        placeholder="e.g., Push-ups"
    )

    if st.button("Swap Exercise"):
        if not exercise_to_replace.strip():
            st.warning("Please enter an exercise name.")
        else:
            with st.spinner("Finding an alternative exercise..."):
                updated_plan = swap_exercise(
                    st.session_state.workout_plan,
                    exercise_to_replace.strip()
                )

            if updated_plan.startswith("Error:"):
                st.error(updated_plan)
            else:
                st.session_state.workout_plan = updated_plan
                st.rerun()

    st.download_button(
        label="📥 Download Workout Plan",
        data=st.session_state.workout_plan,
        file_name="my_workout_plan.md",
        mime="text/markdown"
    )
    st.download_button(
        label="📄 Download as TXT",
        data=st.session_state.workout_plan,
        file_name="my_workout_plan.txt",
        mime="text/plain"
    )

    if st.button("🔄 Regenerate Plan"):
        with st.spinner("Regenerating your workout plan..."):
            new_plan = generate_workout_plan(
                fitness_goal,
                experience_level,
                days_per_week,
                equipment_access,
                injuries_or_limitations,
                previous_plan=st.session_state.workout_plan
            )

        if new_plan.startswith("Error:"):
            st.error(new_plan)
        else:
            st.session_state.workout_plan = new_plan
            st.rerun()