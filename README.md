# 💪 AI Workout Plan Generator

A personalized workout plan generator built using Python, Streamlit, and the Groq API.

## Features

- Generate personalized workout plans using AI.
- Choose a fitness goal: Build Muscle, Lose Fat, General Fitness, or Improve Endurance.
- Select an experience level: Beginner, Intermediate, or Advanced.
- Choose workout frequency from 1 to 7 days per week.
- Select available equipment: No Equipment, Home Dumbbells, or Full Gym.
- Include optional injuries or physical limitations.
- Regenerate workout plans for new variations.
- Swap an individual exercise with an alternative.
- Download workout plans in Markdown (`.md`) or text (`.txt`) format.
- Preserve the current workout plan using Streamlit session state.

## Tech Stack

- Python
- Streamlit
- Groq API
- python-dotenv
- uv

## Setup Instructions

1. Clone the repository.
2. Open the project folder.
3. Install dependencies:

   ```bash
   uv sync
   ```

4. Create a `.env` file in the project root and add your Groq API key:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. Start the application:

   ```bash
   uv run streamlit run app.py
   ```

6. Open the local URL displayed in the terminal, typically `http://localhost:8501`.

## How to Use

1. Select your fitness preferences.
2. Optionally enter any injuries or physical limitations.
3. Click **Generate Plan**.
4. Review your personalized workout plan.
5. Use **Swap Exercise** to replace an individual exercise.
6. Use **Regenerate Plan** to request a new variation.
7. Download the plan as a Markdown or text file.

## AI Model

This project uses the `openai/gpt-oss-20b` model through the Groq API.

## Disclaimer

AI-generated workout plans are for general informational purposes and are not a substitute for professional medical or fitness advice. Consult a qualified professional when dealing with injuries or health concerns.

## Project Information

Created as Assignment 1 for the Codebasics AI Engineering Bootcamp.