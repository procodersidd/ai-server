import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_community.chat_models import ChatOpenAI
from cloud_tool import save_to_cloud

# 🔴 HARDCODED KEY (use OpenAI-style for compatibility)
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_KEY"

# ✅ USE COMPATIBLE LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.3
)

search_tool = SerperDevTool()

# --- AGENTS (FIXED) ---
historian = Agent(
    role="Historian",
    goal="Find historical parallels",
    backstory="An expert historian who studies long-term global patterns.",
    tools=[search_tool],
    llm=llm
)

critic = Agent(
    role="Critic",
    goal="Find flaws in reasoning",
    backstory="A sharp analyst who challenges assumptions.",
    llm=llm
)

philosopher = Agent(
    role="Writer",
    goal="Write final report and store it",
    backstory="A thinker who synthesizes insights into deep reports.",
    tools=[save_to_cloud],
    llm=llm
)

# --- MAIN FUNCTION ---
def run_perfected_analysis(topic):
    t1 = Task(
        description=f"Find historical parallels for {topic}",
        agent=historian
    )

    t2 = Task(
        description="Critique the analysis",
        agent=critic,
        context=[t1]
    )

    t3 = Task(
        description=f"Write a report on {topic} and store it",
        agent=philosopher,
        context=[t1, t2]
    )

    crew = Crew(
        agents=[historian, critic, philosopher],
        tasks=[t1, t2, t3],
        process=Process.sequential,
        memory=False
    )

    return crew.kickoff()