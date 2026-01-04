from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from crewai import Crew
from tasks import create_tasks
import json
import re

app = FastAPI(title="AI Task Breakdown Agent")

# -------------------------
# Serve static files
# -------------------------
app.mount("/static", StaticFiles(directory="static"), name="static")


# -------------------------
# Serve frontend
# -------------------------
@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")


# -------------------------
# Utility: Extract JSON safely
# -------------------------
def extract_json(raw):
    """
    Safely extract JSON from CrewAI output (string or object).
    """
    # Normalize to string
    if not isinstance(raw, str):
        raw = str(raw)

    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return None
    return match.group(0)



# -------------------------
# Request schema
# -------------------------
class GoalRequest(BaseModel):
    goal: str


# -------------------------
# API endpoint
# -------------------------
@app.post("/plan")
def generate_plan(request: GoalRequest):
    tasks = create_tasks(request.goal)

    crew = Crew(
        agents=[task.agent for task in tasks],
        tasks=tasks,
        verbose=True
    )

    raw_result = crew.kickoff()

    json_text = extract_json(raw_result)

    if not json_text:
        raise HTTPException(
            status_code=500,
            detail="Agent returned invalid JSON. Please retry."
        )

    try:
        parsed_result = json.loads(json_text)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Agent returned invalid JSON. Please retry."
        )

    return {
        "goal": request.goal,
        "result": parsed_result
    }
