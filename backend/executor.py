# executor.py

import os
import io
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

# --- API KEY CONFIGURATION ---
# Load all the variables from the .env file into the environment
load_dotenv()

# Retrieve the API key from the environment variables
API_KEY = os.getenv("GEMINI_API_KEY")

# Ensure the API key was found
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please create a .env file and add your key.")

# Configure the Google AI SDK with the API key
genai.configure(api_key=API_KEY)

# --- MODEL INITIALIZATION ---
# Initialize the generative models you will be using
vision_model = genai.GenerativeModel('gemini-pro-vision')
text_model = genai.GenerativeModel('gemini-1.5-flash')


# --- TOOL FUNCTIONS ---

def analyze_gym_image(image_bytes: bytes) -> str:
    """
    Uses the Vision model to analyze an image and identify gym equipment.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        prompt = "Analyze the provided image and list all the gym equipment you can identify. Be concise and format it as a simple list."
        # The vision model can take a list of content parts (text, images, etc.)
        response = vision_model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        print(f"ERROR in analyze_gym_image: {e}")
        return f"An error occurred while analyzing the image: {e}"

def generate_workout_plan(goal: str, equipment: str) -> str:
    """
    Uses the Text model to generate a workout plan based on a goal and available equipment.
    """
    try:
        prompt = f"""
        As an expert fitness coach, create a weekly workout plan for a user.

        **User's Goal:** {goal}
        **Available Equipment:** {equipment}

        Structure the response clearly. Provide a day-by-day plan (e.g., Day 1: Chest & Triceps) with specific exercises, including the number of sets and reps for each.
        """
        response = text_model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"ERROR in generate_workout_plan: {e}")
        return f"An error occurred while generating the workout plan: {e}"

def provide_dietary_advice(goal: str) -> str:
    """
    Uses the Text model to generate general dietary advice for a fitness goal.
    """
    try:
        prompt = f"""
        Provide general dietary advice for a user whose fitness goal is '{goal}'.
        Include tips on protein, carbohydrates, fats, and hydration.
        Conclude with a clear disclaimer that this is not medical advice and a doctor should be consulted for personalized plans.
        """
        response = text_model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"ERROR in provide_dietary_advice: {e}")
        return f"An error occurred while generating dietary advice: {e}"

def execute_task(task_name: str, context: dict, image_bytes: bytes = None) -> str:
    """
    A central dispatcher that calls the correct function based on the task name.
    """
    if task_name == "analyze_gym_image":
        if not image_bytes:
            return "Cannot analyze image: No image was provided."
        return analyze_gym_image(image_bytes)
    elif task_name == "generate_workout_plan":
        return generate_workout_plan(goal=context.get("goal"), equipment=context.get("equipment"))
    elif task_name == "provide_dietary_advice":
        return provide_dietary_advice(goal=context.get("goal"))
    else:
        return f"Error: The task '{task_name}' is unknown and cannot be executed."