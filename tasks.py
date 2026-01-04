from crewai import Task
from agents import planner_agent, tool_advisor_agent, reviewer_agent

def create_tasks(user_goal: str):

    planning_task = Task(
        description=f"""
Break the goal into clear, ordered steps.
Return ONLY a numbered list. No explanation.

Goal:
{user_goal}
""",
        agent=planner_agent,
        expected_output="Numbered list of steps"
    )

    tool_task = Task(
        description="""
Suggest tools or technologies for each step.

Return ONLY valid JSON.
Do NOT include explanations outside JSON.

Format:
{
  "tools": [
    { "step": 1, "tool": "...", "reason": "..." }
  ]
}
""",
        agent=tool_advisor_agent,
        expected_output="Strict JSON"
    )

    review_task = Task(
        description="""
You MUST return ONLY valid JSON.
DO NOT include markdown, text, or explanations.

STRICT FORMAT (no deviation allowed):

{
  "steps": [
    { "text": "...", "confidence": 0.0 }
  ],
  "tools": [
    { "step": 1, "tool": "...", "reason": "..." }
  ],
  "notes": "...",
  "complexity": "Easy | Medium | Hard"
}

Rules:
- Confidence must be between 0 and 1
- No text before or after JSON
- JSON must be parseable by json.loads()
""",
        agent=reviewer_agent,
        expected_output="Strict JSON only"
    )

    return [planning_task, tool_task, review_task]


def normalize_steps(steps):
    return [
        {
            "step": i + 1,
            "text": s["text"],
            "confidence": s["confidence"]
        }
        for i, s in enumerate(steps)
    ]
