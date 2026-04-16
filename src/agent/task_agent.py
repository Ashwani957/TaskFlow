import os
import json
import re
from google import genai
from src.tasks import controller as task_controller
from sqlalchemy.orm import Session
from datetime import datetime

# Initialize client
# Connection Object to our google ai 
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# client.models.list()
# -------- TOOL FUNCTIONS -------- #

def create_task_tool(data: dict, db: Session, user):
    from src.tasks.dtos import TaskSchema
    
    task = TaskSchema(
        title=data.get("title"),
        description=data.get("description"),
        priority=data.get("priority", "medium"),
        due_date=datetime.strptime(data["due_date"], "%Y-%m-%d") if data.get("due_date") else None
    )
    
    task_controller.create_task(task, db, user)
    return "Task created successfully"


def delete_task_tool(task_id: int, db: Session, user):
    task_controller.delete_task(task_id, db, user)
    return f"Task {task_id} deleted successfully"



def delete_task_byTitle(title:str, db:Session , user):
    task_controller.delete_task_by_title(title, db, user)
    return f"Task {title} deleted successfully"


def update_task_tool(task_id: int, data: dict, db: Session, user):
    from src.tasks.dtos import TaskSchema
    
    task = TaskSchema(
        title=data.get("title"),
        description=data.get("description"),
        priority=data.get("priority", "medium"),
        is_completed=data.get("is_completed", False),
        due_date=datetime.strptime(data["due_date"], "%Y-%m-%d") if data.get("due_date") else None
    )
    
    task_controller.update_tasks(task, task_id, db, user)
    return f"Task {task_id} updated successfully"


def update_task_byTitle(title:str, data: dict, db: Session, user):
    from src.tasks.dtos import TaskSchema
    
    task = TaskSchema(
        title=data.get("title"),
        description=data.get("description"),
        priority=data.get("priority", "medium"),
        is_completed=data.get("is_completed", False),
        due_date=datetime.strptime(data["due_date"], "%Y-%m-%d") if data.get("due_date") else None
    )
    
    task_controller.update_tasks_by_title(task, title, db, user)
    return f"Task {title} updated successfully"



# -------- JSON HELPER -------- #

def extract_json(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None


# -------- MAIN AGENT -------- #

# def run_agent(prompt: str, db: Session, user):
    
#     # from Here we should send the requesst to the gemini model 
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents=f"""
# You are a task manager agent.

# STRICT RULES:
# - Return ONLY valid JSON
# - Do NOT write explanation
# - Do NOT add text before or after JSON

# Format:

# {{
#   "action": "create | update | delete",
#   "task_id": number (required for update ),
#   "title": string (required for delete),
#   "data": {{
#     "title": string (optional),
#     "description": string (optional),
#     "priority": "low | medium | high" (optional),
#     "due_date": "YYYY-MM-DD" (optional),
#     "is_completed": true/false (optional)
#   }}
# }}

# User request: {prompt}
# """
#     )

#     # Debug (optional)
#     print("MODEL RESPONSE:", response.text)

#     result = extract_json(response.text)

#     if not result:
#         return f"Could not parse response: {response.text}"

#     action = result.get("action")

#     if action == "create":
#         return create_task_tool(result.get("data", {}), db, user)

#     elif action == "delete":
#         if result.get("task_id"):
#             return delete_task_tool(result.get("task_id"), db, user)
#         else:
#             return delete_task_byTitle(result.get("title"), db, user)

#     elif action == "update":
        
#         return update_task_tool(result.get("task_id"), result.get("data", {}), db, user)

#     return "Invalid action"





def run_agent(prompt: str, db: Session, user):
    
    # from Here we should send the requesst to the gemini model 
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
You are a task manager assistant.

You must decide whether the user is asking about task management or just having a normal conversation.

------------------------
BEHAVIOR RULES:

1. If the user request is related to tasks (create, update, delete, complete, modify tasks):
   - Return ONLY valid JSON
   - Do NOT include any explanation or extra text
   - Follow the exact JSON format below

2. If the user request is NOT related to tasks (e.g., greetings, casual chat, questions like "hello", "how are you"):
   - Respond like a normal helpful assistant
   - DO NOT return JSON
   - DO NOT mention tools or task format

------------------------
JSON FORMAT (ONLY for task-related requests):

{{
  "action": "create | update | delete",
  "task_id": number (required for update/delete),
  "title": string (required for delete if task_id not provided),
  "data": {{
    "title": string (optional),
    "description": string (optional),
    "priority": "low | medium | high" (optional),
    "due_date": "YYYY-MM-DD" (optional),
    "is_completed": true/false (optional)
  }}
}}

------------------------
IMPORTANT:
- NEVER return JSON for non-task queries
- NEVER return text for task queries
- Decide intent carefully before responding

------------------------
User request:
{prompt}
"""
    )
    # Debug (optional)
    print("MODEL RESPONSE:", response.text)

    result = extract_json(response.text)

    if not result:
        return response.text

    action = result.get("action")

    if action == "create":
        return create_task_tool(result.get("data", {}), db, user)

    elif action == "delete":
        if result.get("task_id"):
            return delete_task_tool(result.get("task_id"), db, user)
        else:
            return delete_task_byTitle(result.get("title"), db, user)

    elif action == "update":
        if result.get("task_id"):
            return update_task_tool(result.get("task_id"), result.get("data", {}), db, user)
        else :
            return update_task_byTitle(result.get("title"), result.get("data", {}), db, user)
             

        
        

    return "Invalid action"