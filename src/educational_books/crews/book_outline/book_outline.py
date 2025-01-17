from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebsiteSearchTool
from dotenv import load_dotenv
import os

from educational_books.types import BookOutline

load_dotenv()

@CrewBase
class BookOutlineCrew():
  """Bookoutline crew"""
  agents_config = 'config/agents.yaml'
  tasks_config = 'config/tasks.yaml'
  llm = LLM(api_key=os.getenv("GROQ_API_KEY"), model="groq/llama-3.3-70b-versatile")

  @agent
  def researcher(self) -> Agent:
    return Agent(config=self.agents_config['researcher'], llm=self.llm, tools=[
    SerperDevTool(), 
    # WebsiteSearchTool(
    #   config=dict(
    #     llm=dict(
    #       provider="groq",
    #       config=dict(
    #         model="llama3-8b-8192",
    #         temperature=0.3,
    #         top_p=2,
    #         # stream=true,
    #       ),
    #     ),
    #     embedder=dict(
    #       provider="google", # or openai, ollama, ...
    #       config=dict(
    #           model="models/embedding-001",
    #           task_type="retrieval_document",
    #           # title="Embeddings",
    #       ),
    #     ),
    #   )
    # )
    ], verbose=True)

  @agent
  def planner(self) -> Agent:
    return Agent(config=self.agents_config['planner'], llm=self.llm, verbose=True)

  @task
  def research_topic(self) -> Task:
    return Task(config=self.tasks_config['research_topic'], agent=self.researcher())

  @task
  def generate_outline(self) -> Task:
    return Task(config=self.tasks_config['generate_outline'], agent=self.planner(), output_pydantic=BookOutline)

  @crew
  def crew(self) -> Crew:
    """Creates the Bookoutline crew"""
    return Crew(
      agents=self.agents,
      tasks=self.tasks,
      process=Process.sequential,
      verbose=True,
      max_rpm=1,
    )