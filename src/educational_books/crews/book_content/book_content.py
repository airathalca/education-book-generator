from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

from educational_books.types import Section

load_dotenv()

@CrewBase
class BookContentCrew():
  """BookContent crew"""
  agents_config = 'config/agents.yaml'
  tasks_config = 'config/tasks.yaml'
  llm = LLM(model="gemini/gemini-2.0-flash-exp")

  @agent
  def researcher(self) -> Agent:
    return Agent(config=self.agents_config['researcher'], llm=self.llm, tools=[SerperDevTool()], verbose=True)
  
  @agent
  def writer(self) -> Agent:
    return Agent(config=self.agents_config['writer'], llm=self.llm, verbose=True)

  @task
  def research_section(self) -> Task:
    return Task(config=self.tasks_config['research_section'], agent=self.researcher())
  
  @task
  def write_section(self) -> Task:
    return Task(config=self.tasks_config['write_section'], agent=self.writer(), output_pydantic=Section)

  @crew
  def crew(self) -> Crew:
    """Creates the Bookoutline crew"""
    return Crew(
      agents=self.agents,
      tasks=self.tasks,
      process=Process.sequential,
      verbose=True,
      max_rpm=10,
    )