import requests
import json
import os

# Placeholder for actual OpenAI API key (or other LLM provider)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_API_URL = "https://api.openai.com/v1/chat/completions" # Example for OpenAI

def generate_robot_plan(natural_language_command):
    """
    Uses an LLM to translate a natural language command into a structured robot action plan.

    Args:
        natural_language_command (str): The user's command (e.g., "pick up the red block").

    Returns:
        list: A list of dictionaries representing robot actions, or None if an error occurred.
              Example: [{"action": "NAVIGATE", "target": "kitchen"}, {"action": "GRASP", "object": "red apple"}]
    """
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return None

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Prompt engineering: Instruct the LLM to output a JSON array of actions
    messages = [
        {
            "role": "system",
            "content": """You are a robotic task planner. Convert user commands into a JSON array of discrete robot actions. 
            Actions include: NAVIGATE(location), IDENTIFY(object), GRASP(object), RELEASE(object), BRING(object, destination). 
            Provide only the JSON array. Ensure the output is valid JSON."""
        },
        {
            "role": "user",
            "content": natural_language_command
        }
    ]

    payload = {
        "model": "gpt-4o", # Or another suitable LLM
        "messages": messages,
        "temperature": 0.2, # Lower temperature for more deterministic output
        "max_tokens": 200
    }

    try:
        response = requests.post(LLM_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        llm_response = response.json()
        
        # Extract the content from the LLM's response
        raw_content = llm_response['choices'][0]['message']['content']
        
        # Attempt to parse the content as JSON
        try:
            robot_plan = json.loads(raw_content)
            if isinstance(robot_plan, list):
                return robot_plan
            else:
                print(f"Error: LLM response content is not a JSON list: {raw_content}")
                return None
        except json.JSONDecodeError:
            print(f"Error: Could not decode LLM response content as JSON: {raw_content}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
        if response is not None:
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")
        return None

if __name__ == "__main__":
    # Example usage:
    command = "Navigate to the kitchen, find the red apple, and pick it up."
    print(f"User command: \"{command}\"")

    plan = generate_robot_plan(command)

    if plan:
        print("\nGenerated Robot Plan:")
        for action in plan:
            print(f"- {action}")
    else:
        print("\nFailed to generate robot plan.")

    command_2 = "Go to the living room and bring me the remote."
    print(f"\nUser command: \"{command_2}\"")
    plan_2 = generate_robot_plan(command_2)
    if plan_2:
        print("\nGenerated Robot Plan:")
        for action in plan_2:
            print(f"- {action}")
    else:
        print("\nFailed to generate robot plan.")
