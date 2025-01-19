from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, WebsiteSearchTool
from dotenv import load_dotenv
import streamlit as st
import os

from educational_books.types import BookOutline

load_dotenv()

@CrewBase
class BookOutlineCrew():
  """Bookoutline crew"""
  agents_config = 'config/agents.yaml'
  tasks_config = 'config/tasks.yaml'
  api_key = os.getenv("OPENAI_API_KEY") if os.getenv("OPENAI_API_KEY") else st.secrets["OPENAI_API_KEY"]
  llm = LLM(model="gemini/gemini-2.0-flash-exp", api_key=api_key)

  @agent
  def researcher(self) -> Agent:
    return Agent(config=self.agents_config['researcher'], llm=self.llm, tools=[SerperDevTool()])

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
      max_rpm=10,
    )