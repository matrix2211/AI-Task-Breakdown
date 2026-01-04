from crewai import Agent, LLM

# ✅ Explicitly define Ollama as provider
llm = LLM(
    model="ollama/llama3.1",
    temperature=0.3
)

planner_agent = Agent(
    role="Task Planner",
    goal="Break a high-level goal into clear, actionable steps",
    backstory="You are an expert project planner who creates logical step-by-step plans.",
    llm=llm,
    verbose=True
)

tool_advisor_agent = Agent(
    role="Tool Advisor",
    goal="Suggest appropriate tools and technologies for each task",
    backstory="You are a senior engineer who recommends the best tech stack.",
    llm=llm,
    verbose=True
)

reviewer_agent = Agent(
    role="Plan Reviewer",
    goal="Review and improve the final plan for clarity and completeness",
    backstory="You are a strict reviewer who improves quality and catches missing steps.",
    llm=llm,
    verbose=True
)
