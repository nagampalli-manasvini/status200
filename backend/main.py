# main.py

from fastapi import FastAPI, UploadFile, File, Form
import uvicorn

# Import the other modules from your project
import planner
import executor
import memory

# -------------------------------------------------------------------------- #
# This is the line the error is about. We are creating an instance of FastAPI
# and assigning it to a variable named "app". This must exist.
# -------------------------------------------------------------------------- #
app = FastAPI(
    title="Fitness Agent API",
    description="The backend for your AI-powered fitness assistant. This agent analyzes your gym setup and creates a personalized plan.",
    version="1.0.0",
)


@app.post("/process-request/")
async def process_request(
    user_goal: str = Form(...),
    image: UploadFile = File(...)
):
    """
    This is the main endpoint that orchestrates the entire agent workflow.
    It takes a user's goal (text) and a gym picture (image) as input.
    """
    # Read the image content from the uploaded file
    image_bytes = await image.read()

    # 1. ORCHESTRATOR -> PLANNER
    sub_tasks = planner.create_plan(user_goal)

    # Context dictionary to hold information passed between tasks
    context = {"goal": user_goal}
    final_response_parts = []

    # 2. ORCHESTRATOR -> EXECUTOR (Loop)
    for task in sub_tasks:
        task_name = task.get("name")
        print(f"Orchestrator: Executing task '{task_name}'...")

        result = executor.execute_task(task_name, context, image_bytes)

        if task_name == "analyze_gym_image":
            context["equipment"] = result

        part_header = f"--- {task['description']} ---\n"
        final_response_parts.append(part_header + result)

    # 3. ASSEMBLE FINAL RESPONSE
    final_response = "\n\n".join(final_response_parts)

    # 4. ORCHESTRATOR -> MEMORY
    memory.add_interaction(user_input=user_goal, agent_response=final_response)

    return {"response": final_response}


@app.get("/history/")
def get_history():
    """A utility endpoint to view the conversation history."""
    return {"history": memory.get_full_history()}


# This block allows you to run the server directly using `python main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)