#!/usr/bin/env python
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from pydantic import BaseModel
from typing import List
from crewai.flow.flow import Flow, listen, start
from educational_books.crews.book_outline.book_outline import BookOutlineCrew
from educational_books.crews.book_content.book_content import BookContentCrew
from educational_books.types import Section, SectionOutline
import asyncio

class BookState(BaseModel):
  title: str = "Mastering Data Structures and Algorithms"
  book: List[Section] = []
  book_outline: List[SectionOutline] = []
  topic: str = "Sorting Algorithms"
  book_outline_md: str = ""
  book_md: str = ""
  section_finished: int = 0

class BookFlow(Flow[BookState]):
  initial_state = BookState

  def write_to_file(self, filename: str, content: str, mode: str = "a"):
    """Helper method to write content to the file"""
    with open(filename, mode) as f:
      f.write(content)

  @start()
  def initialize(self, topic: str = None):
    if topic:
      self.state.topic = topic

  @listen(initialize)
  def generate_book_outline(self):
    print("Generating book outline")
    crew = BookOutlineCrew()
    outline = crew.crew().kickoff(inputs={"topic": self.state.topic})
    self.state.title = outline["title"]
    for section in outline["sections"]:
      self.state.book_outline_md += f"# {section.title}\n"
      self.state.book_outline_md += f"{section.description}\n\n"
      self.state.book_outline_md += f"## Covered Skills\n"
      for skill in section.covered_skills:
        self.state.book_outline_md += f"- {skill}\n"
      self.state.book_outline_md += "\n"
      self.state.book_outline_md += f"## Learning Objectives\n"
      for objective in section.objectives:
        self.state.book_outline_md += f"- {objective}\n"
      self.state.book_outline_md += "\n"
    self.state.book_outline = outline["sections"]

  @listen(generate_book_outline)
  async def generate_book(self):
    print("Generating book")
    crew = BookContentCrew()
    tasks = []
    book_outline = [(i, section.title, section.description, section.covered_skills) for i, section in enumerate(self.state.book_outline)]

    async def generate_section(section):
      content = crew.crew().kickoff(inputs={
        "topic": self.state.topic,
        "section_title": section.title,
        "section_description": section.description,
        "covered_skills": section.covered_skills,
        "book_outline": book_outline
      })
      title = content["title"]
      content = content["content"]
      section = Section(title=title, content=content)
      section_content = f"# {title}\n\n{content}\n\n"
      self.state.book_md += section_content
      self.state.section_finished += 1
      return section
    for section in self.state.book_outline:
      print(f"Generating content for {section.title}")
      task = asyncio.create_task(generate_section(section))
      tasks.append(task)

    sections = await asyncio.gather(*tasks)
    self.state.book = sections
    print(f"Book generated with {len(self.state.book)} sections")

def kickoff():
  book_name = BookFlow()
  book_name.kickoff()

def plot():
  book_name = BookFlow()
  book_name.plot()


if __name__ == "__main__":
  kickoff()
