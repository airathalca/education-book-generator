#!/usr/bin/env python
from pydantic import BaseModel
from typing import List
from crewai.flow.flow import Flow, listen, start
from educational_books.crews.book_outline.book_outline import BookOutlineCrew
from educational_books.crews.book_content.book_content import BookContentCrew
from educational_books.types import Section, SectionOutline
import asyncio

class BookState(BaseModel):
  title: str = "Mastering Competitive Programming"
  book: List[Section] = []
  book_outline: List[SectionOutline] = []
  topic: str = "Data Structures and Algorithms in Competitive Programming"

class BookFlow(Flow[BookState]):
  initial_state = BookState

  def write_to_file(self, filename: str, content: str, mode: str = "a"):
    """Helper method to write content to the file"""
    with open(filename, mode) as f:
      f.write(content)

  @start()
  def generate_book_outline(self):
    print("Generating book outline")
    crew = BookOutlineCrew()
    outline = crew.crew().kickoff(inputs={"topic": self.state.topic})
    self.state.book_outline = outline["sections"]
  
  @listen(generate_book_outline)
  def save_book_outline(self):
    print("Saving book outline")
    content = ""
    for section in self.state.book_outline:
      content += f"# {section.title}\n"
      content += f"{section.description}\n\n"
      content += f"## Covered Skills\n"
      for skill in section.covered_skills:
        content += f"- {skill}\n"
      content += "\n"
      content += f"## Learning Objectives\n"
      for objective in section.objectives:
        content += f"- {objective}\n"
      content += "\n"
    self.write_to_file(f"{self.state.title.replace(' ', '_')}_outline.md", content, "w")

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
      section_content = f"# {title}\n{content}\n\n"
      self.write_to_file(f"{self.state.title.replace(' ', '_')}.md", section_content)
      
      section = Section(title=title, content=content)
      return section
    for section in self.state.book_outline:
      print(f"Generating content for {section.title}")
      task = asyncio.create_task(generate_section(section))
      tasks.append(task)

    sections = await asyncio.gather(*tasks)
    self.state.book = sections
    print(f"Book generated with {len(self.state.book)} sections")

def kickoff():
  poem_flow = BookFlow()
  poem_flow.kickoff()

def plot():
  poem_flow = BookFlow()
  poem_flow.plot()


if __name__ == "__main__":
  kickoff()
