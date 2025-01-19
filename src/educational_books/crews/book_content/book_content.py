from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import streamlit as st
import os

from educational_books.types import Section

load_dotenv()
if not os.getenv("SERPER_API_KEY"):
  os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]

@CrewBase
class BookContentCrew():
  """BookContent crew"""
  agents_config = 'config/agents.yaml'
  tasks_config = 'config/tasks.yaml'
  api_key = os.getenv("OPENAI_API_KEY") if os.getenv("OPENAI_API_KEY") else st.secrets["OPENAI_API_KEY"]
  llm = LLM(model="gemini/gemini-2.0-flash-exp", api_key=api_key)

  @agent
  def researcher(self) -> Agent:
    return Agent(config=self.agents_config['researcher'], llm=self.llm, tools=[SerperDevTool()])
  
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
      max_rpm=10,
    )